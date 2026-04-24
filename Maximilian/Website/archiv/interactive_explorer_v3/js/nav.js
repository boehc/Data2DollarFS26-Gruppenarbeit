// MBI Explorer – Navigation
(function () {
  const nav = document.querySelector('.nav');
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');

  // Scroll effect
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 8) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile toggle
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });
    links.querySelectorAll('.nav-link').forEach((l) => {
      l.addEventListener('click', () => links.classList.remove('open'));
    });
  }

  // Active link based on current path
  const path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('.nav-link').forEach((l) => {
    const href = (l.getAttribute('href') || '').toLowerCase();
    if (!href) return;
    if (href === path || (path === '' && href === 'index.html')) {
      l.classList.add('active');
    }
  });
})();
