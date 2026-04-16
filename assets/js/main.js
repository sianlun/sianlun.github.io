// ================================================================
// MAIN.JS — Interactions for Prof. Lau Sian Lun's Website
// ================================================================

// ===== Theme Toggle =====
(function () {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const moonIcon = document.getElementById('theme-icon-moon');
  const sunIcon = document.getElementById('theme-icon-sun');

  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = saved || (prefersDark ? 'dark' : 'light');
  setTheme(initial);

  if (toggle) {
    toggle.addEventListener('click', function () {
      const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  function setTheme(mode) {
    if (mode === 'dark') {
      root.setAttribute('data-theme', 'dark');
      if (moonIcon) moonIcon.style.display = 'none';
      if (sunIcon) sunIcon.style.display = 'inline';
    } else {
      root.removeAttribute('data-theme');
      if (moonIcon) moonIcon.style.display = 'inline';
      if (sunIcon) sunIcon.style.display = 'none';
    }
  }
})();

// ===== Scroll Progress Bar =====
(function () {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  window.addEventListener('scroll', function () {
    const h = document.documentElement;
    const scrolled = h.scrollTop / (h.scrollHeight - h.clientHeight);
    bar.style.width = Math.min(scrolled * 100, 100) + '%';
  }, { passive: true });
})();

// ===== Navbar Scroll Effect =====
(function () {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;
  window.addEventListener('scroll', function () {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, { passive: true });
})();

// ===== Mobile Menu =====
(function () {
  const btn = document.getElementById('hamburger');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', function () {
    menu.classList.toggle('active');
  });
  menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      menu.classList.remove('active');
    });
  });
  // Close on outside click
  document.addEventListener('click', function (e) {
    if (!menu.contains(e.target) && !btn.contains(e.target)) {
      menu.classList.remove('active');
    }
  });
})();

// ===== Active Nav Section on Scroll =====
(function () {
  const links = document.querySelectorAll('.navbar-nav a[href^="#"]');
  if (!links.length) return;
  const sections = Array.from(links).map(function (l) {
    var id = l.getAttribute('href').slice(1);
    return { link: l, el: document.getElementById(id) };
  }).filter(function (s) { return s.el; });

  function onScroll() {
    var y = window.scrollY + 150;
    var active = sections[0];
    sections.forEach(function (s) {
      if (s.el.offsetTop <= y) active = s;
    });
    links.forEach(function (l) { l.classList.remove('active'); });
    if (active) active.link.classList.add('active');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// ===== Scroll Animations (Intersection Observer) =====
(function () {
  var animElements = document.querySelectorAll('[data-animate]');
  if (!animElements.length) return;

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    animElements.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 0.08 + 's';
      observer.observe(el);
    });
  } else {
    // Fallback: show everything
    animElements.forEach(function (el) { el.classList.add('visible'); });
  }
})();

// ===== Animated Counter =====
(function () {
  var counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  function animateCount(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var duration = 2000;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      // Ease out cubic
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.floor(eased * target);
      el.textContent = current.toLocaleString();
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target.toLocaleString();
      }
    }
    requestAnimationFrame(step);
  }

  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    counters.forEach(function (c) { obs.observe(c); });
  } else {
    counters.forEach(function (c) {
      c.textContent = parseInt(c.getAttribute('data-count'), 10).toLocaleString();
    });
  }
})();

// ===== Smooth scroll for anchor links =====
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var offset = 80;
        var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });
})();
