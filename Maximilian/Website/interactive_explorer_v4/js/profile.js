/* ─────────────────────────────────────────────────────────────
   Profile page interactions
   - Detail panel (slide-in from right)
   - Live search, filter chips, sort dropdown
   - Pagination: 50 per page + "Weitere anzeigen"
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var PAGE_SIZE = 50;

  function $(id) { return document.getElementById(id); }
  function num(text) {
    var m = String(text || '').match(/\d+/);
    return m ? parseInt(m[0], 10) : 0;
  }

  /* ── Hoist panel+overlay to <body> to avoid ancestor containing blocks ── */
  function hoistPanel() {
    ['overlay', 'detailPanel'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el && el.parentElement !== document.body) document.body.appendChild(el);
    });
  }

  /* ── Enrich each card with numeric data attributes for filter/sort ── */
  function enrichCards() {
    document.querySelectorAll('.job-card').forEach(function (card, i) {
      var badges = card.querySelectorAll('.badge');
      var skills = badges[0] ? num(badges[0].textContent) : 0;
      var gaps   = badges[2] ? num(badges[2].textContent) : 0;
      card.dataset.skills = skills;
      card.dataset.gaps   = gaps;
      card.dataset.index  = i;
    });
  }

  /* ── Detail panel open/close ── */
  function openPanel(card) {
    var panel = $('detailPanel'), overlay = $('overlay');
    var body = $('panelBody'), title = $('panelTitle');
    if (!panel || !overlay || !body) return;
    if (title) title.textContent = card.dataset.title || '';
    body.innerHTML = card.dataset.panel || '<p>Keine Details.</p>';
    body.scrollTop = 0;
    panel.classList.add('visible');
    overlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
    document.querySelectorAll('.job-card.active').forEach(function (c) {
      c.classList.remove('active');
    });
    card.classList.add('active');
  }
  function closePanel() {
    var panel = $('detailPanel'), overlay = $('overlay');
    if (panel)   panel.classList.remove('visible');
    if (overlay) overlay.classList.remove('visible');
    document.body.style.overflow = '';
    document.querySelectorAll('.job-card.active').forEach(function (c) {
      c.classList.remove('active');
    });
  }

  /* ── Global click handler (event delegation) ── */
  document.addEventListener('click', function (ev) {
    if (ev.target.closest('.panel-close, #closeBtn')) { closePanel(); return; }
    if (ev.target.closest('#overlay'))                 { closePanel(); return; }
    if (ev.target.closest('#loadMoreBtn'))             { showMore();   return; }
    var chip = ev.target.closest('.filter-chip');
    if (chip) { setFilter(chip.dataset.filter, chip); return; }
    var card = ev.target.closest('.job-card');
    if (card) { openPanel(card); return; }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closePanel();
  });

  /* ── Filter / Sort / Search / Pagination state ── */
  var state = { filter: 'all', sort: 'default', query: '', visibleCount: PAGE_SIZE };

  function matchesFilter(card) {
    var s = parseInt(card.dataset.skills || 0, 10);
    var g = parseInt(card.dataset.gaps   || 0, 10);
    switch (state.filter) {
      case 'perfect':     return g === 0;
      case 'good':        return g <= 1;
      case 'many-skills': return s >= 15;
      default:            return true;
    }
  }
  function matchesQuery(card) {
    if (!state.query) return true;
    var t = (card.dataset.title || card.textContent || '').toLowerCase();
    return t.indexOf(state.query) !== -1;
  }

  function applyAll() {
    var list = $('jobList');
    if (!list) return;
    var cards = Array.prototype.slice.call(list.querySelectorAll('.job-card'));

    // 1. Sort
    var sorted = cards.slice();
    if (state.sort === 'skills-desc') {
      sorted.sort(function (a, b) { return b.dataset.skills - a.dataset.skills; });
    } else if (state.sort === 'gaps-asc') {
      sorted.sort(function (a, b) { return a.dataset.gaps - b.dataset.gaps; });
    } else if (state.sort === 'alpha') {
      sorted.sort(function (a, b) {
        return (a.dataset.title || '').localeCompare(b.dataset.title || '', 'de');
      });
    } else {
      sorted.sort(function (a, b) { return a.dataset.index - b.dataset.index; });
    }
    sorted.forEach(function (c) { list.appendChild(c); });

    // 2. Filter + Search
    var pool = sorted.filter(function (c) {
      return matchesFilter(c) && matchesQuery(c);
    });

    // 3. Pagination
    var shown = 0;
    sorted.forEach(function (c) {
      var inPool = pool.indexOf(c) !== -1;
      if (inPool && shown < state.visibleCount) {
        c.style.display = '';
        shown++;
      } else {
        c.style.display = 'none';
      }
    });

    // 4. Counters + Load-More button
    var count = $('resultsCount');
    if (count) {
      var tail = (pool.length > shown)
        ? ' · <span style="color:var(--text-muted);">zeige ' + shown + '</span>'
        : '';
      count.innerHTML = '<strong>' + pool.length + '</strong> von ' +
                        cards.length + ' Stellen' + tail;
    }
    var btn = $('loadMoreBtn');
    if (btn) {
      var remaining = pool.length - shown;
      if (remaining > 0) {
        btn.style.display = '';
        btn.textContent = 'Weitere ' + Math.min(PAGE_SIZE, remaining) +
                          ' anzeigen (' + remaining + ' verbleibend)';
      } else {
        btn.style.display = 'none';
      }
    }
  }

  function setFilter(f, chipEl) {
    state.filter = f;
    state.visibleCount = PAGE_SIZE;
    document.querySelectorAll('.filter-chip').forEach(function (c) {
      c.classList.toggle('is-active', c === chipEl);
    });
    applyAll();
  }
  function showMore() {
    state.visibleCount += PAGE_SIZE;
    applyAll();
  }

  /* ── Initial wire-up ── */
  function init() {
    hoistPanel();
    enrichCards();

    var search = $('searchInput');
    if (search) {
      search.addEventListener('input', function () {
        state.query = (this.value || '').toLowerCase().trim();
        state.visibleCount = PAGE_SIZE;
        applyAll();
      });
    }
    var sel = $('sortSelect');
    if (sel) {
      sel.addEventListener('change', function () {
        state.sort = this.value;
        state.visibleCount = PAGE_SIZE;
        applyAll();
      });
    }

    // Inject Load-More button if missing
    var list = $('jobList');
    if (list && !$('loadMoreBtn')) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.id = 'loadMoreBtn';
      btn.className = 'btn-load-more';
      btn.textContent = 'Weitere anzeigen';
      list.parentNode.insertBefore(btn, list.nextSibling);
    }

    applyAll();
    console.log('[profile.js] ready — ' + document.querySelectorAll('.job-card').length + ' cards');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
