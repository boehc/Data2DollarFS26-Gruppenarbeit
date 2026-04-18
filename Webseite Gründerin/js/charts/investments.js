/**
 * Lizzys – Investments
 * Plotly.js · alle Daten embedded
 */

const QUARTERS = ["2023-Q1","2023-Q2","2023-Q3","2023-Q4","2024-Q1","2024-Q2","2024-Q3","2024-Q4","2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1"];

const TOTALS = [
  {q:"2023-Q1",deals:119,funding:2322.6},{q:"2023-Q2",deals:90,funding:2539.0},{q:"2023-Q3",deals:82,funding:3512.5},{q:"2023-Q4",deals:106,funding:2016.7},
  {q:"2024-Q1",deals:96,funding:3067.6},{q:"2024-Q2",deals:102,funding:3094.7},{q:"2024-Q3",deals:105,funding:1582.2},{q:"2024-Q4",deals:98,funding:2188.7},
  {q:"2025-Q1",deals:110,funding:4867.1},{q:"2025-Q2",deals:69,funding:2050.4},{q:"2025-Q3",deals:122,funding:3415.4},{q:"2025-Q4",deals:117,funding:4328.7},
  {q:"2026-Q1",deals:106,funding:3494.3}
];

const ALL_SECTORS = ["BioTech","FinTech","ClimateTech","HealthTech","GenAI","MedTech","Robotics","Enterprise","Ecommerce","EdTech","PropTech","Cybersecurity","AgriTech","SpaceTech"];

const F1_SM = {
  AgriTech:[1,1,1,0,2,1,2,1,1,1,0,3,0],BioTech:[32,25,22,31,43,31,32,30,36,24,34,35,38],
  ClimateTech:[16,20,13,18,7,13,11,17,15,4,12,10,13],Cybersecurity:[0,0,1,2,0,0,1,0,0,0,0,2,0],
  Ecommerce:[0,2,1,2,1,1,2,0,1,3,3,0,3],EdTech:[0,0,2,1,2,0,0,0,0,0,1,0,0],
  Enterprise:[5,1,3,1,3,2,3,3,1,0,1,1,4],FinTech:[46,29,33,38,23,40,37,33,39,20,51,41,35],
  GenAI:[2,3,1,1,1,4,3,5,3,1,5,8,5],HealthTech:[6,3,2,6,3,2,2,3,6,5,1,5,4],
  MedTech:[6,3,3,2,9,3,9,5,3,7,8,3,4],PropTech:[2,2,0,1,1,1,1,0,0,1,2,4,0],
  Robotics:[1,1,0,2,1,3,2,1,5,3,4,5,0],SpaceTech:[2,0,0,1,0,1,0,0,0,0,0,0,0]
};

const FV_SM = {
  AgriTech:[0,0,0,0,6,0,5,2,10,10,0,13,0],BioTech:[1621,865,1841,1079,2697,832,786,1131,2961,1158,1620,2801,2537],
  ClimateTech:[402,76,925,529,49,140,6,82,121,32,229,114,118],Cybersecurity:[0,0,0,1,0,0,1,0,0,0,0,2,0],
  Ecommerce:[0,0,0,0,0,3,101,0,0,2,0,0,180],EdTech:[0,0,1,1,0,0,0,0,0,0,9,0,0],
  Enterprise:[7,0,58,1,0,0,0,23,0,0,0,0,79],FinTech:[263,1439,667,379,213,2065,440,897,874,811,907,701,353],
  GenAI:[4,5,1,0,14,7,2,14,2,0,56,296,59],HealthTech:[1,9,0,7,30,0,44,15,885,20,1,19,11],
  MedTech:[23,140,18,5,54,11,198,24,3,10,26,164,157],PropTech:[0,2,0,0,1,0,0,0,0,6,0,208,0],
  Robotics:[0,4,0,9,3,35,0,0,12,1,567,9,0],SpaceTech:[0,0,0,6,0,2,0,0,0,0,0,0,0]
};

const STAGE_KEYS = ["Pre-Seed","Seed","Series A","Series B","Series C+","Strategic","Grant"];
const STAGES = [
  {q:"2023-Q1","Pre-Seed":16,Seed:42,"Series A":24,"Series B":14,"Series C+":7,Strategic:5,Grant:5},
  {q:"2023-Q2","Pre-Seed":17,Seed:31,"Series A":8,"Series B":3,"Series C+":6,Strategic:7,Grant:4},
  {q:"2023-Q3","Pre-Seed":16,Seed:35,"Series A":18,"Series B":3,"Series C+":4,Strategic:0,Grant:4},
  {q:"2023-Q4","Pre-Seed":7,Seed:51,"Series A":22,"Series B":3,"Series C+":6,Strategic:1,Grant:1},
  {q:"2024-Q1","Pre-Seed":17,Seed:28,"Series A":30,"Series B":14,"Series C+":3,Strategic:5,Grant:2},
  {q:"2024-Q2","Pre-Seed":15,Seed:52,"Series A":16,"Series B":4,"Series C+":12,Strategic:3,Grant:0},
  {q:"2024-Q3","Pre-Seed":18,Seed:29,"Series A":13,"Series B":14,"Series C+":2,Strategic:7,Grant:3},
  {q:"2024-Q4","Pre-Seed":12,Seed:38,"Series A":23,"Series B":10,"Series C+":5,Strategic:4,Grant:1},
  {q:"2025-Q1","Pre-Seed":16,Seed:37,"Series A":23,"Series B":3,"Series C+":2,Strategic:4,Grant:5},
  {q:"2025-Q2","Pre-Seed":8,Seed:23,"Series A":19,"Series B":6,"Series C+":0,Strategic:3,Grant:3},
  {q:"2025-Q3","Pre-Seed":21,Seed:37,"Series A":21,"Series B":3,"Series C+":4,Strategic:10,Grant:5},
  {q:"2025-Q4","Pre-Seed":16,Seed:29,"Series A":14,"Series B":6,"Series C+":3,Strategic:12,Grant:8},
  {q:"2026-Q1","Pre-Seed":22,Seed:47,"Series A":17,"Series B":7,"Series C+":6,Strategic:10,Grant:2}
];

const C = {
  BioTech:'#0d9488',FinTech:'#f97316',ClimateTech:'#8b5cf6',HealthTech:'#ec4899',
  GenAI:'#84cc16',MedTech:'#eab308',Robotics:'#a16207',Cybersecurity:'#6b7280',
  Enterprise:'#3b82f6',Ecommerce:'#22d3ee',EdTech:'#f43f5e',PropTech:'#fb923c',
  AgriTech:'#a78bfa',SpaceTech:'#14b8a6',
  "Pre-Seed":'#a7f3d0',Seed:'#6ee7b7',"Series A":'#fbbf24',"Series B":'#f97316',
  "Series C+":'#ef4444',Strategic:'#8b5cf6',Grant:'#38bdf8'
};

const BASE_LAYOUT = {
  plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)',
  font:{family:'DM Sans, sans-serif',color:'#8B949E'},
  margin:{l:55,r:55,t:30,b:70},
  xaxis:{tickangle:-45,tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(255,255,255,0.06)',linecolor:'rgba(255,255,255,0.1)'},
  yaxis:{tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(255,255,255,0.06)',zeroline:false},
  hovermode:'x unified',
  legend:{orientation:'h',x:0,y:-0.22,font:{size:11,color:'#8B949E'},bgcolor:'rgba(0,0,0,0)'}
};
const CFG = {responsive:true,displayModeBar:true,modeBarButtonsToRemove:['lasso2d','select2d'],displaylogo:false};
function ml(o){return JSON.parse(JSON.stringify({...BASE_LAYOUT,...o,xaxis:{...BASE_LAYOUT.xaxis,...(o.xaxis||{})},yaxis:{...BASE_LAYOUT.yaxis,...(o.yaxis||{})}}));}

// ===== TAB SWITCHING =====
document.addEventListener('DOMContentLoaded', () => {
  // Main tabs
  const tabs = document.querySelectorAll('#investTabs .sector-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      document.querySelectorAll('.invest-tab-content').forEach(c => c.style.display = 'none');
      const target = document.getElementById('tab-' + tab.dataset.tab);
      if (target) target.style.display = 'block';
      setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
    });
  });

  // Sub-tabs (Deal & Funding)
  document.querySelectorAll('.sector-subtabs').forEach(container => {
    container.querySelectorAll('.sector-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        container.querySelectorAll('.sector-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const prefix = btn.dataset.subtab.split('-')[0]; // 'deal' or 'funding'
        document.getElementById('subtab-' + prefix + '-top7').style.display = btn.dataset.subtab.endsWith('top7') ? 'block' : 'none';
        document.getElementById('subtab-' + prefix + '-custom').style.display = btn.dataset.subtab.endsWith('custom') ? 'block' : 'none';
        if (prefix === 'deal') renderDealShare(); // update share chart
        setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
      });
    });
  });

  buildBranchSelectors();
  renderAll();
});

// ===== CUSTOM BRANCH SELECTORS =====
function buildBranchSelectors() {
  ['deal', 'funding'].forEach(type => {
    const container = document.getElementById(type === 'deal' ? 'dealBranchSelector' : 'fundingBranchSelector');
    if (!container) return;
    container.innerHTML = ALL_SECTORS.map(s =>
      `<label class="branch-chip"><input type="checkbox" value="${s}" data-type="${type}"><span class="branch-chip-dot" style="background:${C[s]}"></span>${s}</label>`
    ).join('');
    container.querySelectorAll('input').forEach(cb => {
      cb.addEventListener('change', () => {
        const checked = container.querySelectorAll('input:checked');
        if (checked.length > 7) { cb.checked = false; return; }
        // Disable unchecked when 7 reached
        const atMax = checked.length >= 7;
        container.querySelectorAll('input').forEach(c => {
          c.closest('.branch-chip').classList.toggle('disabled', atMax && !c.checked);
        });
        if (type === 'deal') renderDealCustom();
        else renderFundingCustom();
      });
    });
  });
}

function getSelectedSectors(type) {
  const container = document.getElementById(type === 'deal' ? 'dealBranchSelector' : 'fundingBranchSelector');
  return Array.from(container.querySelectorAll('input:checked')).map(c => c.value);
}

function renderDealCustom() {
  const sectors = getSelectedSectors('deal');
  const el = document.getElementById('dealCustomChart');
  if (!sectors.length) {
    Plotly.purge('dealCustomChart');
    el.innerHTML = '<div class="custom-empty-hint">👆 Wähle oben bis zu 7 Branchen aus, um den Chart zu sehen</div>';
    el.style.minHeight = '120px';
    renderDealShare();
    return;
  }
  el.style.minHeight = '';
  const traces = sectors.map(k => ({
    x:QUARTERS,y:F1_SM[k],type:'scatter',mode:'lines+markers',name:k,
    line:{color:C[k],width:2},marker:{size:4,color:C[k]},
    hovertemplate:`${k}: %{y}<extra></extra>`
  }));
  Plotly.newPlot('dealCustomChart',traces,ml({yaxis:{title:{text:'Deals'}}}),CFG);
  renderDealShare(); // sync share chart
}

function renderFundingCustom() {
  const sectors = getSelectedSectors('funding');
  const el = document.getElementById('fundingCustomChart');
  if (!sectors.length) {
    Plotly.purge('fundingCustomChart');
    el.innerHTML = '<div class="custom-empty-hint">👆 Wähle oben bis zu 7 Branchen aus, um den Chart zu sehen</div>';
    el.style.minHeight = '120px';
    return;
  }
  el.style.minHeight = '';
  const traces = sectors.map(k => ({
    x:QUARTERS,y:FV_SM[k],type:'scatter',mode:'lines+markers',name:k,
    line:{color:C[k],width:2},marker:{size:4},
    hovertemplate:`${k}: CHF %{y:,.0f} Mio.<extra></extra>`
  }));
  Plotly.newPlot('fundingCustomChart',traces,ml({yaxis:{title:{text:'Mio. CHF'}}}),CFG);
}

function renderAll() {
  renderComboChart();
  renderStages();
  renderDealSizeTable();
  renderDealLines();
  renderDealShare();
  renderFundingLines();
}

// ===== COMBO CHART: Deals (bars) + Funding (line) =====
function renderComboChart() {
  const dealBars = {
    x: TOTALS.map(t=>t.q), y: TOTALS.map(t=>t.deals),
    type:'bar', name:'Deals', marker:{color:'#00E5A0',opacity:0.75},
    hovertemplate:'%{y} Deals<extra></extra>', yaxis:'y'
  };
  const fundingLine = {
    x: TOTALS.map(t=>t.q), y: TOTALS.map(t=>t.funding),
    type:'scatter', mode:'lines+markers', name:'Funding (Mio. CHF)',
    line:{color:'#C77DFF',width:2.5}, marker:{size:5,color:'#C77DFF'},
    hovertemplate:'CHF %{y:,.0f} Mio.<extra></extra>', yaxis:'y2'
  };
  Plotly.newPlot('comboChart',[dealBars,fundingLine],ml({
    yaxis:{title:{text:'Anzahl Deals'},side:'left'},
    yaxis2:{title:{text:'Mio. CHF'},overlaying:'y',side:'right',tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(0,0,0,0)',zeroline:false},
    legend:{y:-0.28}
  }),CFG);
}

// ===== STAGES =====
function renderStages() {
  const traces = STAGE_KEYS.map(k => ({
    x:STAGES.map(s=>s.q),y:STAGES.map(s=>s[k]),
    type:'bar',name:k,marker:{color:C[k]},
    hovertemplate:`${k}: %{y}<extra></extra>`
  }));
  Plotly.newPlot('stagesChart',traces,ml({barmode:'stack',yaxis:{title:{text:'Deals'}},legend:{y:-0.28}}),CFG);
}

// ===== TABLE =====
let tableSortCol = 'deals';
let tableSortDir = -1; // -1 = desc, 1 = asc

function getQuarterIndices(yearFilter) {
  if (yearFilter === 'all') return QUARTERS.map((_,i) => i);
  return QUARTERS.map((q,i) => q.startsWith(yearFilter) ? i : -1).filter(i => i >= 0);
}

function renderDealSizeTable() {
  const yearFilter = document.getElementById('yearFilter')?.value || 'all';
  const indices = getQuarterIndices(yearFilter);
  const hint = document.getElementById('tableHint');
  if (hint) hint.textContent = yearFilter === 'all' ? 'Kumuliert 2023–2026' : `Kumuliert ${yearFilter}`;

  const agg = {};
  ALL_SECTORS.forEach(s => {
    const deals = indices.reduce((a,i) => a + (F1_SM[s][i]||0), 0);
    // Only sum funding for quarters where there are deals
    const funding = indices.reduce((a,i) => {
      return a + (F1_SM[s][i] > 0 ? (FV_SM[s][i]||0) : 0);
    }, 0);
    agg[s] = {deals, funding, avg: deals > 0 ? funding / deals : 0, name: s};
  });

  let sorted = Object.entries(agg);
  if (tableSortCol === 'name') {
    sorted.sort((a,b) => tableSortDir * a[0].localeCompare(b[0]));
  } else {
    sorted.sort((a,b) => tableSortDir * (a[1][tableSortCol] - b[1][tableSortCol]));
  }

  const tbody = document.querySelector('#dealSizeTable tbody');
  tbody.innerHTML = sorted.map(([s,v]) =>
    `<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${C[s]||'#6b7280'};margin-right:6px;vertical-align:middle;"></span>${s}</td>
     <td>${v.deals}</td><td>${(v.funding/1000).toFixed(1)}</td><td>${Math.round(v.avg)}</td></tr>`
  ).join('');

  // Update sort icons
  document.querySelectorAll('#dealSizeTable th.sortable').forEach(th => {
    const col = th.dataset.sort;
    const icon = th.querySelector('.sort-icon');
    th.classList.remove('sorted-asc','sorted-desc');
    if (col === tableSortCol) {
      th.classList.add(tableSortDir === 1 ? 'sorted-asc' : 'sorted-desc');
      icon.textContent = tableSortDir === 1 ? '↑' : '↓';
    } else {
      icon.textContent = '⇅';
    }
  });
}

// Table sort click handler
document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#dealSizeTable thead')?.addEventListener('click', e => {
    const th = e.target.closest('th.sortable');
    if (!th) return;
    const col = th.dataset.sort;
    if (col === tableSortCol) { tableSortDir *= -1; }
    else { tableSortCol = col; tableSortDir = col === 'name' ? 1 : -1; }
    renderDealSizeTable();
  });
  document.getElementById('yearFilter')?.addEventListener('change', () => renderDealSizeTable());
});

// ===== DEAL LINES =====
function renderDealLines() {
  const top7 = ["BioTech","FinTech","ClimateTech","HealthTech","GenAI","MedTech","Robotics"];
  const traces = top7.map(k => ({
    x:QUARTERS,y:F1_SM[k],
    type:'scatter',mode:'lines+markers',name:k,
    line:{color:C[k],width:2},marker:{size:4,color:C[k]},
    hovertemplate:`${k}: %{y}<extra></extra>`
  }));
  Plotly.newPlot('dealLinesChart',traces,ml({yaxis:{title:{text:'Deals'}}}),CFG);
}

// ===== DEAL SHARE =====
function isCustomDealActive() {
  const el = document.getElementById('subtab-deal-custom');
  return el && el.style.display !== 'none';
}

function renderDealShare() {
  const customActive = isCustomDealActive();
  const customSectors = customActive ? getSelectedSectors('deal') : [];
  const top = customActive && customSectors.length ? customSectors : ["BioTech","FinTech","ClimateTech","HealthTech","GenAI","MedTech"];
  const hint = document.getElementById('shareChartHint');
  if (hint) hint.textContent = customActive && customSectors.length ? 'Eigene Auswahl · Quartalsweise' : 'Top-Branchen · Quartalsweise';
  const traces = top.map(k => {
    const shares = F1_SM[k].map((v,i) => {
      const total = TOTALS[i].deals;
      return total>0? +(v/total*100).toFixed(1) : 0;
    });
    return {
      x:QUARTERS,y:shares,type:'scatter',mode:'lines+markers',name:k,
      line:{color:C[k],width:2},marker:{size:4},
      hovertemplate:`${k}: %{y:.1f}%<extra></extra>`
    };
  });
  Plotly.newPlot('shareChart',traces,ml({yaxis:{title:{text:'Marktanteil (%)'},ticksuffix:'%'}}),CFG);
}

// ===== FUNDING LINES =====
function renderFundingLines() {
  const top7 = ["BioTech","FinTech","HealthTech","ClimateTech","Robotics","EdTech","GenAI"];
  const traces = top7.map(k => ({
    x:QUARTERS,y:FV_SM[k],
    type:'scatter',mode:'lines+markers',name:k,
    line:{color:C[k],width:2},marker:{size:4},
    hovertemplate:`${k}: CHF %{y:,.0f} Mio.<extra></extra>`
  }));
  Plotly.newPlot('fundingLinesChart',traces,ml({yaxis:{title:{text:'Mio. CHF'}}}),CFG);
}
