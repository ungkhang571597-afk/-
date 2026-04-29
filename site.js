(function () {
  var header = document.querySelector(".site-header");
  var menuToggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[href^='#']"));
  var sections = navLinks
    .map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    })
    .filter(Boolean);
  var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal-on-scroll"));
  var backToTop = document.getElementById("back-to-top");
  var toast = document.getElementById("toast");
  var ticking = false;

  function updateHeaderState() {
    var currentY = window.scrollY || window.pageYOffset || 0;

    if (header) {
      header.classList.toggle("is-scrolled", currentY > 24);
    }

    if (backToTop) {
      backToTop.classList.toggle("show", currentY > 560);
    }
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
      link.classList.toggle("is-current", !!isActive);

      if (isActive) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  function syncScrollUi() {
    updateHeaderState();
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
        threshold: 0.14,
        rootMargin: "0px 0px -7% 0px"
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

    clearTimeout(button._tid);
    button.textContent = isSuccess ? "已复制" : "失败";
    button.classList.toggle("is-copied", isSuccess);
    button.classList.toggle("is-failed", !isSuccess);

    button._tid = window.setTimeout(function () {
      button.textContent = "复制";
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
        copied ? onSuccess() : onFail();
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

  function closeMenu() {
    document.body.classList.remove("nav-open");
    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", "false");
    }
  }

  function onScroll() {
    if (ticking) {
      return;
    }

    ticking = true;
    window.requestAnimationFrame(syncScrollUi);
  }

  if (menuToggle && nav) {
    menuToggle.addEventListener("click", function () {
      var shouldOpen = !document.body.classList.contains("nav-open");
      document.body.classList.toggle("nav-open", shouldOpen);
      menuToggle.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
    });
  }

  document.addEventListener("click", function (event) {
    var backButton = event.target.closest("#back-to-top");
    if (backButton) {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
      closeMenu();
      return;
    }

    var copyButton = event.target.closest("[data-copy]");
    if (copyButton) {
      event.preventDefault();
      copyTextFromSelector(copyButton.getAttribute("data-copy"), copyButton);
      return;
    }

    if (event.target.closest(".site-nav a")) {
      closeMenu();
    }
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", syncScrollUi);

  setupReveal();
  syncScrollUi();
})();
