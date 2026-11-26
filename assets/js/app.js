/* ==========================================================================
   NOVA — app.js
   این فایل فقط تعاملات ظاهری و رابط کاربری را پیاده‌سازی می‌کند.
   طبق قوانین پروژه، هیچ منطق سبد خرید، محصولات یا مقالاتی اینجا وجود ندارد:
   - افزودن/حذف از سبد و علاقه‌مندی‌ها: فقط با فرم‌های HTML (متد POST)
   - افزایش/کاهش تعداد: فقط با فرم‌های HTML
   - صفحه‌بندی محصولات و مقالات: فقط با input radio و CSS
   ========================================================================== */

(function () {
  "use strict";

  var d = document;

  function $(sel, ctx) { return (ctx || d).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || d).querySelectorAll(sel)); }

  /* ------------------------------------------------------------------
     ۱) منوی موبایل هدر: باز و بسته کردن کشوی ناوبری
  ------------------------------------------------------------------ */
  var header = $(".site-header");
  var navToggle = $("#nav-toggle");
  var mainNav = $("#main-nav");
  var navOverlay = $("#nav-overlay");

  function closeNav() {
    d.body.classList.remove("nav-open");
    if (navToggle) navToggle.setAttribute("aria-expanded", "false");
  }

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      var isOpen = d.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  if (navOverlay) navOverlay.addEventListener("click", closeNav);

  if (mainNav) {
    $$("a", mainNav).forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
  }

  /* ------------------------------------------------------------------
     ۲) سایه هدر هنگام اسکرول + نمایش دکمه بازگشت به بالا
  ------------------------------------------------------------------ */
  var backTop = $("#back-top");

  function onScroll() {
    if (header) {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    }
    if (backTop) {
      backTop.classList.toggle("is-visible", window.scrollY > 480);
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });

  if (backTop) {
    backTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ------------------------------------------------------------------
     ۳) سایدبار پنل کاربری و پنل مدیریت در موبایل
  ------------------------------------------------------------------ */
  var panelToggle = $("#panel-toggle");
  var adminToggle = $("#admin-toggle");
  var panelOverlay = $("#panel-overlay");

  function closeSidePanels() {
    d.body.classList.remove("panel-open", "admin-open");
    if (panelToggle) panelToggle.setAttribute("aria-expanded", "false");
    if (adminToggle) adminToggle.setAttribute("aria-expanded", "false");
  }

  if (panelToggle) {
    panelToggle.addEventListener("click", function () {
      var isOpen = d.body.classList.toggle("panel-open");
      panelToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  if (adminToggle) {
    adminToggle.addEventListener("click", function () {
      var isOpen = d.body.classList.toggle("admin-open");
      adminToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  if (panelOverlay) panelOverlay.addEventListener("click", closeSidePanels);

  $$(".panel-menu a, .admin-menu a, .admin-menu summary").forEach(function (el) {
    el.addEventListener("click", function () {
      /* برای لینک‌ها منو بسته شود؛ برای summary (بازکردن زیرمنو) باز بماند */
      if (el.tagName === "A") closeSidePanels();
    });
  });

  /* ------------------------------------------------------------------
     ۴) آکاردئون منوی مدیریت: هر بار فقط یک گروه details باز بماند
  ------------------------------------------------------------------ */
  var adminGroups = $$(".admin-menu details");

  adminGroups.forEach(function (group) {
    group.addEventListener("toggle", function () {
      if (!group.open) return;
      adminGroups.forEach(function (other) {
        if (other !== group) other.open = false;
      });
    });
  });

  /* ------------------------------------------------------------------
     ۵) نمایش / پنهان‌سازی رمز عبور در فرم‌ها
  ------------------------------------------------------------------ */
  $$(".pass-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var field = btn.closest(".pass-field");
      var input = field ? field.querySelector("input") : null;
      if (!input) return;

      var show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.classList.toggle("is-active", show);
      btn.setAttribute("aria-label", show ? "پنهان کردن رمز عبور" : "نمایش رمز عبور");
    });
  });

  /* ------------------------------------------------------------------
     ۶) بستن منوها با کلید Esc
  ------------------------------------------------------------------ */
  d.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      closeNav();
      closeSidePanels();
    }
  });
  var resizeTimer;

  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (window.innerWidth > 1024) {
        closeNav();
        closeSidePanels();
      }
    }, 160);
  });

  /* راه‌اندازی اولیه */
  onScroll();
})();



const qun = document.getElementById('pd-qty');

qun.addEventListener('input', () => {
    if (Number(qun.value) < 1) {
        qun.value = 1;
    }
});














