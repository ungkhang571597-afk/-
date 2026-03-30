(function () {
  var header = document.querySelector(".site-header");
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav a[href^='#']"));
  var sections = navLinks
    .map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    })
    .filter(Boolean);
  var backToTop = document.getElementById("back-to-top");
  var toast = document.getElementById("toast");
  var ticking = false;

  function updateHeaderState() {
    if (!header) {
      return;
    }

    var currentY = window.scrollY || window.pageYOffset || 0;
    header.classList.toggle("is-scrolled", currentY > 18);

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
    updateActiveNav();
    ticking = false;
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

  syncScrollUi();
})();
