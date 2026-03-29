(function () {
  var header = document.querySelector(".site-header");
  var scrollProgressBar = document.querySelector(".scroll-progress-bar");
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav a[href^='#']"));
  var sections = navLinks
    .map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    })
    .filter(Boolean);
  var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal-on-scroll"));
  var backToTop = document.getElementById("back-to-top");
  var toast = document.getElementById("toast");
  var lastScrollY = window.scrollY || 0;
  var ticking = false;

  function updateHeaderState() {
    if (!header) {
      return;
    }

    var currentY = window.scrollY || window.pageYOffset || 0;
    var isTop = currentY < 36;

    header.classList.toggle("is-top", isTop);
    header.classList.toggle("is-scrolled", !isTop);

    if (isTop) {
      header.classList.remove("is-hidden");
    } else if (currentY > lastScrollY + 12) {
      header.classList.add("is-hidden");
    } else if (currentY < lastScrollY - 12) {
      header.classList.remove("is-hidden");
    }

    if (backToTop) {
      backToTop.classList.toggle("show", currentY > 560);
    }

    lastScrollY = currentY;
  }

  function updateScrollProgress() {
    if (!scrollProgressBar) {
      return;
    }

    var doc = document.documentElement;
    var scrollable = doc.scrollHeight - window.innerHeight;
    var progress = scrollable > 0 ? Math.min(Math.max(window.scrollY / scrollable, 0), 1) : 0;
    scrollProgressBar.style.transform = "scaleX(" + progress + ")";
  }

  function updateActiveNav() {
    if (!navLinks.length || !sections.length) {
      return;
    }

    var offset = (header ? header.offsetHeight : 0) + 120;
    var currentId = "";

    sections.forEach(function (section) {
      if (window.scrollY + offset >= section.offsetTop) {
        currentId = section.id;
      }
    });

    navLinks.forEach(function (link) {
      var isActive = currentId && link.getAttribute("href") === "#" + currentId;
      link.classList.toggle("is-active", !!isActive);

      if (isActive) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  function syncScrollUi() {
    updateHeaderState();
    updateScrollProgress();
    updateActiveNav();
    ticking = false;
  }

  function setupReveal() {
    if (!revealItems.length) {
      return;
    }

    if (!("IntersectionObserver" in window)) {
      revealItems.forEach(function (item) {
        item.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }

          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.16,
        rootMargin: "0px 0px -8% 0px"
      }
    );

    revealItems.forEach(function (item) {
      item.classList.add("reveal-pending");
      observer.observe(item);
    });
  }

  function showToast(text) {
    if (!toast) {
      return;
    }

    toast.textContent = text;
    toast.classList.add("show");
    clearTimeout(toast._tid);
    toast._tid = window.setTimeout(function () {
      toast.classList.remove("show");
    }, 1600);
  }

  function setCopiedState(button, isSuccess) {
    if (!button) {
      return;
    }

    var label = button.querySelector("span:last-child");
    if (!label) {
      return;
    }

    clearTimeout(button._tid);
    label.textContent = isSuccess ? "已复制" : "失败";
    button.classList.toggle("is-copied", isSuccess);
    button.classList.toggle("is-failed", !isSuccess);

    button._tid = window.setTimeout(function () {
      label.textContent = "复制";
      button.classList.remove("is-copied");
      button.classList.remove("is-failed");
    }, 1600);
  }

  function copyTextFromSelector(selector, button) {
    var el = document.querySelector(selector);
    if (!el) {
      return;
    }

    var text = el.tagName === "A" ? el.textContent.trim() : (el.value || el.textContent || "").trim();

    function onSuccess() {
      showToast("已复制");
      setCopiedState(button, true);
    }

    function onFail() {
      showToast("复制失败");
      setCopiedState(button, false);
    }

    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();

      try {
        var copied = document.execCommand("copy");
        if (copied) {
          onSuccess();
        } else {
          onFail();
        }
      } catch (error) {
        onFail();
      }

      document.body.removeChild(ta);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(onSuccess).catch(fallback);
    } else {
      fallback();
    }
  }

  function onScroll() {
    if (ticking) {
      return;
    }

    ticking = true;
    window.requestAnimationFrame(syncScrollUi);
  }

  document.addEventListener("click", function (event) {
    var backButton = event.target.closest("#back-to-top");
    if (backButton) {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    var button = event.target.closest(".copy-btn");
    if (!button) {
      return;
    }

    event.preventDefault();
    copyTextFromSelector(button.getAttribute("data-copy"), button);
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", syncScrollUi);

  setupReveal();
  syncScrollUi();
})();
