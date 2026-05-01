(function () {
  var header = document.querySelector(".site-header");
  var menuToggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  var menuLinks = nav ? Array.prototype.slice.call(nav.querySelectorAll("a")) : [];
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[href^='#']"));
  var sections = navLinks
    .map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    })
    .filter(Boolean);
  var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal-on-scroll"));
  var backToTop = document.getElementById("back-to-top");
  var toast = document.getElementById("toast");
  var mobileQuery = window.matchMedia ? window.matchMedia("(max-width: 860px)") : null;
  var ticking = false;

  function isMobileNav() {
    return mobileQuery ? mobileQuery.matches : window.innerWidth <= 860;
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

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

    if (!("IntersectionObserver" in window) || prefersReducedMotion()) {
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
        threshold: 0.01,
        rootMargin: "0px 0px 20% 0px"
      }
    );

    revealItems.forEach(function (item, index) {
      item.style.setProperty("--reveal-delay", Math.min(index * 55, 180) + "ms");
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

  function copyLabelFor(selector) {
    if (selector === "#email-text") {
      return "邮箱";
    }

    if (selector === "#phone-text") {
      return "手机号";
    }

    return "内容";
  }

  function setCopiedState(button, isSuccess, label) {
    if (!button) {
      return;
    }

    clearTimeout(button._tid);
    button.textContent = isSuccess ? "已复制" : "失败";
    button.setAttribute("aria-label", isSuccess ? label + "已复制" : label + "复制失败");
    button.classList.toggle("is-copied", isSuccess);
    button.classList.toggle("is-failed", !isSuccess);

    button._tid = window.setTimeout(function () {
      button.textContent = "复制";
      button.setAttribute("aria-label", "复制" + label);
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
    var label = copyLabelFor(selector);

    function onSuccess() {
      showToast(label + "已复制");
      setCopiedState(button, true, label);
    }

    function onFail() {
      showToast(label + "复制失败");
      setCopiedState(button, false, label);
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

  function syncMenuAccessibility() {
    if (!nav || !menuToggle) {
      return;
    }

    var isOpen = document.body.classList.contains("nav-open");
    var isMobile = isMobileNav();
    var label = menuToggle.querySelector(".sr-only");

    if (!isMobile && isOpen) {
      document.body.classList.remove("nav-open");
      isOpen = false;
    }

    menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");

    if (label) {
      label.textContent = isOpen ? "关闭导航" : "打开导航";
    }

    if (isMobile) {
      nav.setAttribute("aria-hidden", isOpen ? "false" : "true");
      menuLinks.forEach(function (link) {
        link.tabIndex = isOpen ? 0 : -1;
      });
    } else {
      nav.removeAttribute("aria-hidden");
      menuLinks.forEach(function (link) {
        link.removeAttribute("tabindex");
      });
    }
  }

  function closeMenu() {
    document.body.classList.remove("nav-open");
    syncMenuAccessibility();
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
      syncMenuAccessibility();
    });
  }

  document.addEventListener("click", function (event) {
    if (event.target.closest(".menu-toggle")) {
      return;
    }

    if (document.body.classList.contains("nav-open") && !event.target.closest("#site-nav")) {
      closeMenu();
      return;
    }

    var backButton = event.target.closest("#back-to-top");
    if (backButton) {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? "auto" : "smooth" });

      if (window.history && window.location.hash) {
        window.history.replaceState(null, "", window.location.pathname + window.location.search);
      }

      var focusTarget = document.getElementById("home") || document.getElementById("main-content");
      if (focusTarget) {
        focusTarget.setAttribute("tabindex", "-1");
        focusTarget.focus({ preventScroll: true });
      }

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

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && document.body.classList.contains("nav-open")) {
      closeMenu();
      if (menuToggle) {
        menuToggle.focus();
      }
      return;
    }

    if (event.key !== "Tab" || !document.body.classList.contains("nav-open") || !isMobileNav()) {
      return;
    }

    var focusables = [menuToggle].concat(menuLinks).filter(Boolean);
    var first = focusables[0];
    var last = focusables[focusables.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () {
    syncMenuAccessibility();
    syncScrollUi();
  });

  if (mobileQuery && mobileQuery.addEventListener) {
    mobileQuery.addEventListener("change", syncMenuAccessibility);
  }

  setupReveal();
  syncMenuAccessibility();
  syncScrollUi();
})();
