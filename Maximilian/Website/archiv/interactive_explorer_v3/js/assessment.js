/* ─────────────────────────────────────────────────────────────
   Self-Assessment v3 — weighted matching
   ──────────────────────────────────────────────────────────────
   Core scoring formula (per job j, given user skill set U):

       covered(j) = j.skills ∩ U
       num   = Σ w(s) · focus(s) · intensity(j,s)   for s ∈ covered(j)
       denom = Σ w(s) · focus(s) · intensity(j,s)   for s ∈ j.skills
       score = num / denom                    ∈ [0, 1]

       w(s)      = idf(s) × group_weight(s)   (from skills.json)
       focus(s)  = user-chosen slider, tilts Tech vs Soft
       intensity = 1 + small bonus if the job's group score is high

   Additional signals:
     • Keyword-channel:  fuzzy overlap of course keywords ↔ job title
     • Profile affinity: user-preferred profile gets a soft boost
     • Seniority & experience: filters, not score components
     • Duplicates pre-merged in the preprocessor
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  const PROFILES = [
    { key: 'bd',    name: 'Business Development',    color: '#059669' },
    { key: 'dc',    name: 'Digital Channel & CRM',   color: '#DB2777' },
    { key: 'su',    name: 'Startup & Scale-up',      color: '#F59E0B' },
    { key: 'sc',    name: 'Supply Chain & Ops',      color: '#2563EB' },
    { key: 'ts',    name: 'Technology Architecture', color: '#7C3AED' },
    { key: 'tm',    name: 'Digital Transformation',  color: '#0891B2' },
    { key: 'other', name: 'Weitere / unzugeordnet',  color: '#64748B' },
  ];
  const PROFILE_BY_KEY = Object.fromEntries(PROFILES.map(p => [p.key, p]));

  const TECH_GROUPS = new Set(['FD', 'FK']);   // „Tech-Fit"
  const SOFT_GROUPS = new Set(['SK', 'MK', 'PK']); // „Profil-Fit"

  const state = {
    courses: [],
    jobs: [],
    skills: {},
    skillToCourses: new Map(),   // skill-code → [courseId,…]  (reverse index)
    selected: new Set(),
    profileFilter: new Set(PROFILES.map(p => p.key)),
    affinity: null,              // profile key the user leans towards
    sort: 'match-desc',
    searchCourse: '',
    visible: 30,
    // Controls
    focus: 0.55,                 // 0 = all-soft, 1 = all-tech (default slight tech-lean)
    maxYears: null,              // null = no filter, else integer (user's experience cap)
    seniority: new Set(['junior', 'mid', 'senior', 'lead']),
    includeOther: false,
    includeSparse: false,
  };

  /* ── Load ──────────────────────────────────────────────── */
  async function loadAll() {
    // When opened as file:// fetch() is blocked by the browser.
    // The HTML pre-loads data/*_data.js which expose window.__COURSES__ etc.
    // Fall back to fetch() when served via HTTP (e.g. a local dev server).
    async function loadData(windowKey, path) {
      if (window[windowKey] !== undefined) return window[windowKey];
      return fetch(path).then(r => r.json());
    }
    const [courses, jobs, skills] = await Promise.all([
      loadData('__COURSES__', 'data/courses.json'),
      loadData('__JOBS__',    'data/jobs.json'),
      loadData('__SKILLS__',  'data/skills.json'),
    ]);
    state.courses = courses
      .filter(c => c.title)
      .sort((a, b) => a.title.localeCompare(b.title, 'de'));
    state.jobs = jobs;
    state.skills = skills;

    // Build reverse index skill→[courseIds]
    const m = new Map();
    for (const c of state.courses) {
      for (const sk of c.skills) {
        if (!m.has(sk)) m.set(sk, []);
        m.get(sk).push(c.id);
      }
    }
    state.skillToCourses = m;

    // Pre-compute a "typical" job denominator so we can dampen thin/noisy jobs
    // (a job of only 4 generic soft-skills shouldn't hit 100 % just because
    // the user's courses happen to cover Teamwork + Motivation).
    const sampleDens = [];
    for (const j of state.jobs) {
      let d = 0;
      for (const s of j.skills) {
        const meta = state.skills[s];
        if (meta) d += meta.weight;  // neutral focus for this estimate
      }
      sampleDens.push(d);
    }
    sampleDens.sort((a, b) => a - b);
    state.medianDen = sampleDens[Math.floor(sampleDens.length / 2)] || 20;

    // Reflect default profile filter in state (exclude "other" by default)
    if (!state.includeOther) state.profileFilter.delete('other');
  }

  /* ── Scoring helpers ───────────────────────────────────── */
  function focusMultiplier(group) {
    // focus slider: 0 → soft only, 1 → tech only. 0.5 is neutral.
    const t = state.focus;
    if (TECH_GROUPS.has(group)) return 0.3 + 1.4 * t;       // 0.3 … 1.7
    if (SOFT_GROUPS.has(group)) return 0.3 + 1.4 * (1 - t); // 0.3 … 1.7
    return 1.0;
  }

  function intensityForJob(job, group) {
    // use the numeric scores as a mild boost (+0…+40 %)
    const s = job.scores || {};
    const lookup = { FK: s.fk, FD: s.fd, SK: s.sk, MK: s.mk, PK: s.pk }[group] || 0;
    // scores live roughly in 0..8. normalize 0..1, amplitude 0.4
    return 1 + Math.min(lookup / 8, 1) * 0.4;
  }

  function userSkillSet() {
    const s = new Set();
    for (const id of state.selected) {
      const c = state.courses.find(x => x.id === id);
      if (!c) continue;
      for (const sk of c.skills) s.add(sk);
    }
    return s;
  }

  function userKeywordSet() {
    const s = new Set();
    for (const id of state.selected) {
      const c = state.courses.find(x => x.id === id);
      if (!c || !c.keywords) continue;
      for (const k of c.keywords) s.add(k);
    }
    return s;
  }

  function keywordTitleBonus(job, kws) {
    if (!kws.size) return 0;
    const title = job.title.toLowerCase();
    let hits = 0;
    for (const k of kws) {
      if (k.length < 4) continue;
      if (title.includes(k)) hits++;
      if (hits >= 3) break;
    }
    // max +0.05 to final score — it's a nudge, not a rewrite
    return Math.min(hits, 3) * 0.02;
  }

  function scoreJob(job, userSkills, userKws) {
    const req = job.skills;
    if (!req.length) return null;

    let num = 0, den = 0;
    const hit = [], gaps = [];
    let techNum = 0, techDen = 0, softNum = 0, softDen = 0;

    for (const s of req) {
      const meta = state.skills[s];
      if (!meta) continue;
      const w = meta.weight * focusMultiplier(meta.group) * intensityForJob(job, meta.group);
      den += w;
      const isTech = TECH_GROUPS.has(meta.group);
      if (isTech) techDen += w; else softDen += w;
      if (userSkills.has(s)) {
        num += w;
        hit.push(s);
        if (isTech) techNum += w; else softNum += w;
      } else {
        gaps.push(s);
      }
    }

    let ratio = den > 0 ? num / den : 0;

    // Confidence dampening: jobs whose total requirement-mass is far below the
    // median (= few or only generic skills) shouldn't be able to reach 100 %.
    // Use sqrt to make the curve soft.
    const confidence = Math.min(1, Math.sqrt(den / (state.medianDen || 20)));
    ratio *= confidence;

    // Keyword nudge
    ratio += keywordTitleBonus(job, userKws);

    // Profile affinity (soft boost)
    if (state.affinity && job.profile === state.affinity) ratio *= 1.08;
    ratio = Math.min(ratio, 1);

    return {
      job,
      ratio,
      covered: hit.length,
      total:   req.length,
      hit, gaps,
      techFit: techDen > 0 ? techNum / techDen : 0,
      softFit: softDen > 0 ? softNum / softDen : 0,
    };
  }

  /* ── Next-best-course suggestion for a job ─────────────── */
  function suggestNextCourse(job, userSkills) {
    if (state.selected.size >= state.courses.length) return null;
    let best = null, bestGain = 0;
    for (const c of state.courses) {
      if (state.selected.has(c.id)) continue;
      let gain = 0, gained = [];
      for (const s of c.skills) {
        if (job.skills.includes(s) && !userSkills.has(s)) {
          const meta = state.skills[s];
          if (meta) { gain += meta.weight; gained.push(s); }
        }
      }
      if (gain > bestGain) { bestGain = gain; best = { course: c, gain, skills: gained }; }
    }
    return best && best.skills.length ? best : null;
  }

  /* ── Rendering: course picker ──────────────────────────── */
  function renderCourses() {
    const wrap = document.getElementById('courseList');
    const q = state.searchCourse.trim().toLowerCase();
    const rows = state.courses.filter(c => !q || c.title.toLowerCase().includes(q));
    wrap.innerHTML = rows.map(c => {
      const checked = state.selected.has(c.id) ? 'checked' : '';
      const pills = c.profiles.map(pk => {
        const p = PROFILE_BY_KEY[pk];
        return p ? `<span class="a-course-pill" style="--pc:${p.color}" title="${p.name}">${p.name.split(' ')[0]}</span>` : '';
      }).join('');
      const ects = c.ects ? `${c.ects} ECTS` : '';
      const meta = [ects, `${c.skills.length} Skills`].filter(Boolean).join(' · ');
      return `
        <label class="a-course-row ${checked ? 'is-active' : ''}" data-id="${escapeAttr(c.id)}">
          <input type="checkbox" ${checked} data-id="${escapeAttr(c.id)}">
          <div class="a-course-body">
            <div class="a-course-title">${escapeHtml(c.title)}</div>
            <div class="a-course-meta">${meta}</div>
            ${pills ? `<div class="a-course-pills">${pills}</div>` : ''}
          </div>
        </label>`;
    }).join('') || `<div class="a-empty-mini">Keine Kurse gefunden.</div>`;
    document.getElementById('courseStats').textContent =
      `${state.selected.size} / ${state.courses.length} ausgewählt`;
  }

  /* ── Rendering: profile chips + affinity marker ───────── */
  function renderProfileChips() {
    const el = document.getElementById('profileFilterChips');
    el.innerHTML = PROFILES.map(p => {
      const on  = state.profileFilter.has(p.key);
      const aff = state.affinity === p.key;
      const count = state.jobs.filter(j => j.profile === p.key).length;
      if (!count) return '';
      return `
        <button type="button" class="chip ${on ? 'chip-on' : ''} ${aff ? 'chip-aff' : ''}"
                data-profile="${p.key}" style="--pc:${p.color}"
                title="${aff ? 'Favorit (soft boost)' : 'Klick: ein/aus · Doppelklick: als Favorit'}">
          <span class="chip-dot"></span>${p.name} <em>${count}</em>
          ${aff ? '<span class="chip-star">★</span>' : ''}
        </button>`;
    }).join('');
  }

  /* ── Rendering: main results ───────────────────────────── */
  function renderResults() {
    const main  = document.getElementById('assessmentResults');
    const empty = document.getElementById('assessmentEmpty');
    const count = document.getElementById('assessmentCount');

    document.getElementById('sumCourses').textContent = String(state.selected.size);

    if (state.selected.size === 0) {
      main.innerHTML = '';
      empty.style.display = '';
      count.innerHTML = `<strong>${state.jobs.length}</strong> Stellen wartend`;
      setSummary('–', '–', '–', '–');
      return;
    }
    empty.style.display = 'none';

    const userSkills = userSkillSet();
    const userKws    = userKeywordSet();

    let pool = state.jobs
      .filter(j => state.profileFilter.has(j.profile))
      .filter(j => state.seniority.has(j.seniority))
      .filter(j => state.includeSparse || !j.sparse);
    if (state.maxYears != null) pool = pool.filter(j => j.years_exp <= state.maxYears);

    const scored = pool
      .map(j => scoreJob(j, userSkills, userKws))
      .filter(r => r && r.total > 0);

    // Summary
    const topRatio = scored.reduce((m, r) => Math.max(m, r.ratio), 0);
    const avg = scored.length ? scored.reduce((s, r) => s + r.ratio, 0) / scored.length : 0;
    const avgTech = scored.length ? scored.reduce((s, r) => s + r.techFit, 0) / scored.length : 0;
    const avgSoft = scored.length ? scored.reduce((s, r) => s + r.softFit, 0) / scored.length : 0;

    const byProfile = new Map();
    for (const r of scored) {
      const p = r.job.profile;
      if (!byProfile.has(p)) byProfile.set(p, { sum: 0, n: 0 });
      const e = byProfile.get(p); e.sum += r.ratio; e.n += 1;
    }
    let best = null, bestAvg = -1;
    for (const [p, e] of byProfile) {
      if (e.n < 5) continue; // need a minimum sample
      const a = e.sum / e.n;
      if (a > bestAvg) { bestAvg = a; best = p; }
    }

    setSummary(
      scored.length ? pct(topRatio) : '–',
      pct(avgTech),
      pct(avgSoft),
      best ? (PROFILE_BY_KEY[best]?.name || best) : '–'
    );

    // Sort
    scored.sort((a, b) => {
      switch (state.sort) {
        case 'covered-desc': return b.covered - a.covered || b.ratio - a.ratio;
        case 'gaps-asc':     return a.gaps.length - b.gaps.length || b.ratio - a.ratio;
        case 'tech-desc':    return b.techFit - a.techFit || b.ratio - a.ratio;
        case 'match-desc':
        default:             return b.ratio - a.ratio || b.covered - a.covered;
      }
    });

    count.innerHTML = `<strong>${scored.length}</strong> Stellen analysiert · Top ${Math.min(state.visible, scored.length)} angezeigt`;

    const slice = scored.slice(0, state.visible);
    main.innerHTML = slice.map(r => renderJobCard(r, userSkills)).join('');

    if (scored.length > state.visible) {
      main.insertAdjacentHTML('beforeend',
        `<div class="a-more"><button type="button" class="btn btn-ghost" id="aMoreBtn">Weitere Stellen laden (${Math.min(50, scored.length - state.visible)})</button></div>`);
    }
  }

  function setSummary(top, tech, soft, profile) {
    const el = id => document.getElementById(id);
    if (el('sumTop'))     el('sumTop').textContent     = top;
    if (el('sumTech'))    el('sumTech').textContent    = tech;
    if (el('sumSoft'))    el('sumSoft').textContent    = soft;
    if (el('sumProfile')) el('sumProfile').textContent = profile;
  }
  function pct(r) { return Math.round(r * 100) + '%'; }

  /* ── Single job card ───────────────────────────────────── */
  function renderJobCard(r, userSkills) {
    const p = PROFILE_BY_KEY[r.job.profile] || PROFILE_BY_KEY.other;
    const score = Math.round(r.ratio * 100);
    const techPct = Math.round(r.techFit * 100);
    const softPct = Math.round(r.softFit * 100);

    // Sort gaps by weight (most important missing first)
    const hit  = [...r.hit ].sort((a, b) => (state.skills[b]?.weight || 0) - (state.skills[a]?.weight || 0));
    const gaps = [...r.gaps].sort((a, b) => (state.skills[b]?.weight || 0) - (state.skills[a]?.weight || 0));

    const hitChips = hit.slice(0, 8).map(sk => skillChip(sk, 'hit')).join('');
    const gapChips = gaps.slice(0, 6).map(sk => skillChip(sk, 'gap')).join('');
    const hitMore = hit.length > 8  ? `<span class="a-chip a-chip-more">+${hit.length - 8}</span>` : '';
    const gapMore = gaps.length > 6 ? `<span class="a-chip a-chip-more">+${gaps.length - 6}</span>` : '';

    const company = r.job.company ? `<span class="a-job-company">${escapeHtml(r.job.company)}</span>` : '';
    const loc     = r.job.location ? `<span class="a-job-loc">${escapeHtml(r.job.location)}</span>` : '';
    const badges = [];
    if (r.job.count > 1) badges.push(`<span class="a-badge">${r.job.count}× ausgeschrieben</span>`);
    if (r.job.seniority !== 'mid') badges.push(`<span class="a-badge a-badge-${r.job.seniority}">${seniorityLabel(r.job.seniority)}</span>`);
    if (r.job.years_exp > 0) badges.push(`<span class="a-badge">${r.job.years_exp}+ Jahre</span>`);

    const suggestion = suggestNextCourse(r.job, userSkills);
    const suggHtml = suggestion
      ? `<div class="a-suggest">
           <span class="a-suggest-icon">💡</span>
           Mit <strong>${escapeHtml(suggestion.course.title)}</strong> würdest du
           ${suggestion.skills.length} weitere Skill${suggestion.skills.length === 1 ? '' : 's'} abdecken.
           <button type="button" class="a-suggest-add" data-add="${escapeAttr(suggestion.course.id)}">Hinzufügen</button>
         </div>`
      : '';

    return `
      <article class="a-job-card" style="--pc:${p.color}">
        <header class="a-job-head">
          <div class="a-job-title">
            <h4>${escapeHtml(r.job.title)}</h4>
            <div class="a-job-sub">${company}${company && loc ? ' · ' : ''}${loc}</div>
            <div class="a-job-meta-row">
              <span class="a-job-profile"><span class="chip-dot"></span>${p.name}</span>
              ${badges.join('')}
            </div>
          </div>
          <div class="a-job-score">
            <div class="a-job-score-ring" style="--pct:${score}">
              <span>${score}<em>%</em></span>
            </div>
            <div class="a-job-score-split">
              <span title="Tech-Fit (FD/FK-Skills)">🔧 ${techPct}%</span>
              <span title="Profil-Fit (SK/MK/PK)">🤝 ${softPct}%</span>
            </div>
          </div>
        </header>
        ${hit.length ? `
        <div class="a-job-block">
          <div class="a-job-block-lbl">Deine Kurse decken ab (${r.covered}/${r.total})</div>
          <div class="a-chips">${hitChips}${hitMore}</div>
        </div>` : ''}
        ${gaps.length ? `
        <div class="a-job-block">
          <div class="a-job-block-lbl">Lücken — geordnet nach Bedeutung</div>
          <div class="a-chips">${gapChips}${gapMore}</div>
        </div>` : ''}
        ${suggHtml}
      </article>`;
  }

  function skillChip(sk, kind) {
    const meta = state.skills[sk] || { label: sk, group: '', job_pct: 0 };
    const courses = state.skillToCourses.get(sk) || [];
    const selected = courses.filter(id => state.selected.has(id));
    const picked = selected.map(id => state.courses.find(c => c.id === id)?.title).filter(Boolean);
    const tip = kind === 'hit'
      ? `${meta.group_label || ''}: ${meta.label}\nGelernt in:\n  • ${picked.join('\n  • ')}`
      : `${meta.group_label || ''}: ${meta.label}\n${meta.job_pct}% aller Jobs verlangen das.`;
    return `<span class="a-chip a-chip-${kind}" title="${escapeAttr(tip)}">${escapeHtml(meta.label)}</span>`;
  }

  function seniorityLabel(s) {
    return { junior: 'Junior', senior: 'Senior', lead: 'Lead / Head', mid: 'Mid' }[s] || s;
  }

  /* ── Utilities ─────────────────────────────────────────── */
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function escapeAttr(s) { return escapeHtml(s); }

  /* ── Events ────────────────────────────────────────────── */
  function bind() {
    document.getElementById('courseList').addEventListener('change', e => {
      const cb = e.target.closest('input[type="checkbox"]');
      if (!cb) return;
      toggleCourse(cb.dataset.id, cb.checked);
    });
    document.getElementById('courseSearch').addEventListener('input', e => {
      state.searchCourse = e.target.value;
      renderCourses();
    });
    document.getElementById('selectAllBtn').addEventListener('click', () => {
      for (const c of state.courses) state.selected.add(c.id);
      renderCourses(); renderResults();
    });
    document.getElementById('clearAllBtn').addEventListener('click', () => {
      state.selected.clear();
      renderCourses(); renderResults();
    });

    // Profile chips: click = toggle, dblclick = set affinity
    const chips = document.getElementById('profileFilterChips');
    let lastClick = 0, lastKey = null;
    chips.addEventListener('click', e => {
      const btn = e.target.closest('[data-profile]');
      if (!btn) return;
      const k = btn.dataset.profile;
      const now = Date.now();
      if (k === lastKey && now - lastClick < 350) {
        state.affinity = state.affinity === k ? null : k;
      } else {
        if (state.profileFilter.has(k)) state.profileFilter.delete(k);
        else state.profileFilter.add(k);
      }
      lastClick = now; lastKey = k;
      state.visible = 30;
      renderProfileChips(); renderResults();
    });

    document.getElementById('assessmentSort').addEventListener('change', e => {
      state.sort = e.target.value; renderResults();
    });

    // New controls
    const focus = document.getElementById('focusSlider');
    if (focus) focus.addEventListener('input', e => {
      state.focus = parseFloat(e.target.value);
      document.getElementById('focusValue').textContent = focusLabel(state.focus);
      renderResults();
    });
    const yrs = document.getElementById('yearsSelect');
    if (yrs) yrs.addEventListener('change', e => {
      const v = e.target.value;
      state.maxYears = v === '' ? null : parseInt(v, 10);
      renderResults();
    });
    document.querySelectorAll('[data-seniority]').forEach(el => {
      el.addEventListener('change', e => {
        const k = e.target.dataset.seniority;
        if (e.target.checked) state.seniority.add(k); else state.seniority.delete(k);
        renderResults();
      });
    });
    const otherToggle = document.getElementById('otherToggle');
    if (otherToggle) otherToggle.addEventListener('change', e => {
      state.includeOther = e.target.checked;
      if (state.includeOther) state.profileFilter.add('other');
      else state.profileFilter.delete('other');
      renderProfileChips(); renderResults();
    });
    const sparseToggle = document.getElementById('sparseToggle');
    if (sparseToggle) sparseToggle.addEventListener('change', e => {
      state.includeSparse = e.target.checked;
      renderResults();
    });

    // Results clicks: load more + "add course" suggestion
    document.getElementById('assessmentResults').addEventListener('click', e => {
      if (e.target.id === 'aMoreBtn') {
        state.visible += 50; renderResults();
      } else if (e.target.matches('[data-add]')) {
        toggleCourse(e.target.dataset.add, true);
      }
    });
  }

  function toggleCourse(id, on) {
    if (on) state.selected.add(id); else state.selected.delete(id);
    state.visible = 30;
    renderCourses(); renderResults();
  }

  function focusLabel(f) {
    if (f <= 0.25) return 'Soft-Skills';
    if (f <= 0.45) return 'Ausgewogen (soft-lastig)';
    if (f <= 0.55) return 'Ausgewogen';
    if (f <= 0.75) return 'Ausgewogen (tech-lastig)';
    return 'Tech-Skills';
  }

  /* ── Init ──────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', async () => {
    try {
      await loadAll();
      document.getElementById('assessmentLoading').style.display = 'none';
      document.getElementById('assessmentApp').style.display = '';
      renderCourses();
      renderProfileChips();
      const fl = document.getElementById('focusValue');
      if (fl) fl.textContent = focusLabel(state.focus);
      renderResults();
      bind();
    } catch (err) {
      console.error(err);
      const el = document.getElementById('assessmentLoading');
      if (el) el.innerHTML = `<div style="color:#b91c1c">Fehler beim Laden der Daten: ${escapeHtml(err.message || String(err))}</div>`;
    }
  });
})();
