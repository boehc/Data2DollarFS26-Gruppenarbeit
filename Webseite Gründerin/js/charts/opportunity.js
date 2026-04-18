/**
 * Lizzys – Opportunity Analysis
 * Plotly.js · News × VC · Tech × Industry
 */

const QUARTERS = ["2023-Q1","2023-Q2","2023-Q3","2023-Q4","2024-Q1","2024-Q2","2024-Q3","2024-Q4","2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1"];

const MATRIX_A = [
  {kw:"BioTech",n25:3.0,d25:33.9,dg:-2.1,td:413},
  {kw:"FinTech",n25:17.5,d25:39.6,dg:4.4,td:465},
  {kw:"ClimateTech",n25:3.8,d25:10.8,dg:-1.9,td:169},
  {kw:"HealthTech",n25:5.8,d25:4.5,dg:1.9,td:48},
  {kw:"MedTech",n25:0.2,d25:5.5,dg:-1.4,td:65},
  {kw:"PropTech",n25:0.2,d25:1.8,dg:1.0,td:15},
  {kw:"Enterprise",n25:0.5,d25:0.8,dg:-2.1,td:28},
  {kw:"SpaceTech",n25:2.2,d25:0.0,dg:-0.3,td:4},
  {kw:"Ecommerce",n25:2.2,d25:1.8,dg:0.7,td:19},
  {kw:"AgriTech",n25:0.2,d25:1.3,dg:-0.3,td:14}
];

const HEATMAP_RAW = [
  {t:"GenAI",i:"BioTech",n:15},{t:"GenAI",i:"FinTech",n:24},{t:"GenAI",i:"HealthTech",n:18},{t:"GenAI",i:"ClimateTech",n:8},{t:"GenAI",i:"DefenseTech",n:16},{t:"GenAI",i:"Ecommerce",n:6},{t:"GenAI",i:"EdTech",n:1},{t:"GenAI",i:"MedTech",n:0},
  {t:"LLM",i:"BioTech",n:6},{t:"LLM",i:"FinTech",n:8},{t:"LLM",i:"HealthTech",n:11},{t:"LLM",i:"ClimateTech",n:7},{t:"LLM",i:"DefenseTech",n:4},{t:"LLM",i:"Ecommerce",n:3},{t:"LLM",i:"EdTech",n:0},{t:"LLM",i:"MedTech",n:1},
  {t:"AgentAI",i:"BioTech",n:0},{t:"AgentAI",i:"FinTech",n:11},{t:"AgentAI",i:"HealthTech",n:5},{t:"AgentAI",i:"ClimateTech",n:0},{t:"AgentAI",i:"DefenseTech",n:4},{t:"AgentAI",i:"Ecommerce",n:3},{t:"AgentAI",i:"EdTech",n:0},{t:"AgentAI",i:"MedTech",n:0},
  {t:"Robotics",i:"BioTech",n:4},{t:"Robotics",i:"FinTech",n:10},{t:"Robotics",i:"HealthTech",n:11},{t:"Robotics",i:"ClimateTech",n:10},{t:"Robotics",i:"DefenseTech",n:11},{t:"Robotics",i:"Ecommerce",n:1},{t:"Robotics",i:"EdTech",n:0},{t:"Robotics",i:"MedTech",n:1}
];

const TECH_DIVE = [
  {q:"2023-Q1",nG:99,nL:41,nA:0,nR:17,vG:2,vR:1},{q:"2023-Q2",nG:138,nL:74,nA:2,nR:18,vG:3,vR:1},
  {q:"2023-Q3",nG:142,nL:66,nA:2,nR:24,vG:1,vR:0},{q:"2023-Q4",nG:144,nL:55,nA:3,nR:27,vG:1,vR:2},
  {q:"2024-Q1",nG:134,nL:61,nA:5,nR:29,vG:1,vR:1},{q:"2024-Q2",nG:131,nL:57,nA:9,nR:23,vG:4,vR:3},
  {q:"2024-Q3",nG:127,nL:30,nA:10,nR:17,vG:3,vR:2},{q:"2024-Q4",nG:115,nL:43,nA:19,nR:29,vG:5,vR:1},
  {q:"2025-Q1",nG:91,nL:41,nA:23,nR:25,vG:3,vR:5},{q:"2025-Q2",nG:93,nL:16,nA:33,nR:17,vG:1,vR:3},
  {q:"2025-Q3",nG:91,nL:30,nA:53,nR:30,vG:5,vR:4},{q:"2025-Q4",nG:78,nL:30,nA:50,nR:32,vG:8,vR:5},
  {q:"2026-Q1",nG:43,nL:15,nA:35,nR:20,vG:5,vR:0}
];

const C = {
  BioTech:'#0d9488',FinTech:'#f97316',ClimateTech:'#8b5cf6',HealthTech:'#ec4899',
  GenAI:'#84cc16',MedTech:'#eab308',Robotics:'#a16207',Enterprise:'#3b82f6',
  Ecommerce:'#22d3ee',PropTech:'#fb923c',AgriTech:'#a78bfa',SpaceTech:'#14b8a6',
  DefenseTech:'#dc2626',EdTech:'#f43f5e'
};

const BASE = {
  plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)',
  font:{family:'DM Sans, sans-serif',color:'#8B949E'},
  margin:{l:55,r:20,t:30,b:70},
  xaxis:{tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(255,255,255,0.06)',linecolor:'rgba(255,255,255,0.1)'},
  yaxis:{tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(255,255,255,0.06)',zeroline:false},
  hovermode:'closest',
  legend:{orientation:'h',x:0,y:-0.22,font:{size:11,color:'#8B949E'},bgcolor:'rgba(0,0,0,0)'}
};
const CFG = {responsive:true,displayModeBar:true,modeBarButtonsToRemove:['lasso2d','select2d'],displaylogo:false};
function ml(o){return JSON.parse(JSON.stringify({...BASE,...o,xaxis:{...BASE.xaxis,...(o.xaxis||{})},yaxis:{...BASE.yaxis,...(o.yaxis||{})}}));}

// ===== TAB SWITCHING =====
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('#oppTabs .sector-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      document.querySelectorAll('.opp-tab-content').forEach(c => c.style.display = 'none');
      document.getElementById('tab-' + tab.dataset.tab).style.display = 'block';
      setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
    });
  });
  renderRanking();
  renderHeatmap();
  renderTechDive();
  renderRobotics();
});

// ===== MATRIX =====
function renderMatrix() {
  const d = MATRIX_A;
  const trace = {
    x: d.map(r=>r.n25), y: d.map(r=>r.d25), text: d.map(r=>r.kw),
    mode:'markers+text', type:'scatter',
    textposition:'top center', textfont:{size:11,color:'#E6EDF3'},
    marker:{
      size: d.map(r=>Math.max(14,Math.sqrt(r.td)*1.8)),
      color: d.map(r=>C[r.kw]||'#6b7280'), opacity:0.85,
      line:{width:1,color:'rgba(255,255,255,0.2)'}
    },
    customdata: d.map(r=>[r.td,r.dg]),
    hovertemplate:'<b>%{text}</b><br>News 2025: %{x:.1f}%<br>Deals 2025: %{y:.1f}%<br>Total Deals: %{customdata[0]}<br>Trend: %{customdata[1]:+.1f}%/a<extra></extra>'
  };
  const shapes = [
    {type:'line',x0:4,x1:4,y0:0,y1:40,line:{color:'rgba(255,255,255,0.1)',dash:'dot',width:1}},
    {type:'line',x0:0,x1:20,y0:8,y1:8,line:{color:'rgba(255,255,255,0.1)',dash:'dot',width:1}}
  ];
  const annotations = [
    {x:1,y:38,text:'Stille Stärke<br>(viel VC, wenig Hype)',showarrow:false,font:{size:10,color:'#6b7280'}},
    {x:15,y:38,text:'Goldzone<br>(viel VC + Hype)',showarrow:false,font:{size:10,color:'#00E5A0'}},
    {x:1,y:1,text:'Nische',showarrow:false,font:{size:10,color:'#6b7280'}},
    {x:15,y:1,text:'Hype ohne Deals',showarrow:false,font:{size:10,color:'#FF7A45'}}
  ];
  Plotly.newPlot('matrixChart',[trace],ml({
    xaxis:{title:{text:'News-Anteil 2025 (%)'}},
    yaxis:{title:{text:'Deal-Anteil 2025 (%)'}},
    shapes, annotations
  }),CFG);
}

// ===== RANKING TABLE =====
const RANKING_EXPLAIN = {
  BioTech: 'Dominanter Marktführer mit 34% aller Schweizer VC-Deals und über 19 Mrd. CHF Funding. Leichter Rückgang (–2.1pp), aber absolute Dominanz. Grosses Potenzial in GenAI-Anwendungen.',
  FinTech: 'Grösster Deal-Anteil (40%), aber langfristig sinkende Dynamik. Quartalszahlen schwanken stark. Differenzierung nötig (z.B. GenAI-Layer, Nischenfokus).',
  ClimateTech: '10.8% Deal-Anteil, leicht rückläufig (–1.9pp). Gesellschaftlich relevant, aber Funding-Umfeld aktuell schwieriger. Regulatorisches Know-how essentiell.',
  HealthTech: 'Wachsender Deal-Anteil (+1.9pp) auf 4.5%. Absolut +70% mehr Deals 2025 vs 2024. Starkes Schweizer Gesundheitssystem als Fundament, GenAI als Hebel.',
  MedTech: '5.5% Deal-Anteil, leicht rückläufig (–1.4pp). Regulatorisches Know-how ist Key – starker Standortvorteil Schweiz (Medtech-Cluster).',
  PropTech: 'Kleiner Markt (1.8%), aber wachsend (+1.0pp). Wenig Konkurrenz – interessant für fokussierte Gründer.',
  Enterprise: 'Sehr kleiner Deal-Anteil (0.8%) mit starkem Rückgang (–2.1pp). –73% weniger Deals 2025 vs 2024. Schwieriger Markt.',
  SpaceTech: 'Keine Deals mehr in 2025. Sehr kapitalintensiv und spezialisiert – nur mit starkem technischem Background und Forschungsnähe.',
  Ecommerce: 'Kleiner Markt (1.8%), aber wachsend (+0.7pp). +75% mehr Deals 2025 vs 2024. Chancen eher in Nischen oder Tech-Enablement.',
  AgriTech: 'Kleiner, stabiler Markt (1.3%, –0.3pp). Schweizer Stärken in Präzisionstechnologie und Nachhaltigkeit als Vorteil.'
};

function renderRanking() {
  const signalOrder = {'Attraktiv':0,'Wachsend':1,'Stabil':2,'Stagnierend':3,'Rückläufig':4};

  const enriched = MATRIX_A.map(r => {
    let signal, cls, signalKey;
    if (r.kw === 'FinTech') {
      signal='🟡 Stagnierend'; cls='color:#fbbf24'; signalKey='Stagnierend';
    } else if (r.d25>20) {
      signal='🟢 Attraktiv'; cls='color:#00E5A0'; signalKey='Attraktiv';
    } else if (r.d25>3 && r.dg>=0) {
      signal='🟢 Attraktiv'; cls='color:#00E5A0'; signalKey='Attraktiv';
    } else if (r.dg>0) {
      signal='🟡 Wachsend'; cls='color:#fbbf24'; signalKey='Wachsend';
    } else if (r.dg>-2 && r.d25>0.5) {
      signal='🟡 Stabil'; cls='color:#fbbf24'; signalKey='Stabil';
    } else {
      signal='🔴 Rückläufig'; cls='color:#ef4444'; signalKey='Rückläufig';
    }
    return {...r, signal, cls, signalKey};
  });

  enriched.sort((a,b) => (signalOrder[a.signalKey]??99) - (signalOrder[b.signalKey]??99) || b.d25 - a.d25);

  const tbody = document.querySelector('#rankingTable tbody');
  tbody.innerHTML = enriched.map((r,i) => {
    const explain = RANKING_EXPLAIN[r.kw] || '';
    return `<tr class="ranking-row" style="cursor:pointer" onclick="this.nextElementSibling.classList.toggle('ranking-detail--open')">
      <td>${i+1}</td>
      <td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${C[r.kw]||'#6b7280'};margin-right:6px;vertical-align:middle;"></span>${r.kw}</td>
      <td>${r.d25.toFixed(1)}%</td><td>${r.n25.toFixed(1)}%</td>
      <td>${r.dg>0?'+':''}${r.dg.toFixed(1)}%</td>
      <td style="${r.cls};font-weight:600">${r.signal}</td>
    </tr>
    <tr class="ranking-detail"><td colspan="6"><div class="ranking-detail-inner">💡 ${explain}</div></td></tr>`;
  }).join('');
}

// ===== HEATMAP =====
function renderHeatmap() {
  const techs = ["GenAI","LLM","AgentAI","Robotics"];
  const industries = ["FinTech","HealthTech","BioTech","DefenseTech","ClimateTech","Ecommerce","EdTech","MedTech"];
  const z = techs.map(t => industries.map(i => {
    const found = HEATMAP_RAW.find(h=>h.t===t&&h.i===i);
    return found?found.n:0;
  }));
  const trace = {
    z, x:industries, y:techs, type:'heatmap',
    colorscale:[[0,'#0D1117'],[0.3,'#1a3a2a'],[0.6,'#00E5A0'],[1,'#fbbf24']],
    hovertemplate:'<b>%{y} × %{x}</b><br>Co-Occurrences: %{z}<extra></extra>'
  };
  Plotly.newPlot('heatmapChart',[trace],ml({
    margin:{l:90,r:20,t:20,b:80},
    xaxis:{tickangle:-45},yaxis:{}
  }),CFG);
}

// ===== TECH DIVE =====
function renderTechDive() {
  const qs = TECH_DIVE.map(d=>d.q);
  const traces = [
    {x:qs,y:TECH_DIVE.map(d=>d.nG),type:'scatter',mode:'lines',name:'GenAI News',line:{color:'#84cc16',width:2.5},yaxis:'y'},
    {x:qs,y:TECH_DIVE.map(d=>d.nA),type:'scatter',mode:'lines',name:'AgentAI News',line:{color:'#f97316',width:2.5,dash:'dash'},yaxis:'y'},
    {x:qs,y:TECH_DIVE.map(d=>d.vG),type:'bar',name:'GenAI CH-Deals',marker:{color:'#84cc16',opacity:0.5},yaxis:'y2'},
  ];
  Plotly.newPlot('techDiveChart',traces,ml({
    yaxis:{title:{text:'News-Artikel'},side:'left'},
    yaxis2:{title:{text:'CH VC-Deals'},overlaying:'y',side:'right',tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(0,0,0,0)'},
    xaxis:{tickangle:-45},legend:{y:-0.3}
  }),CFG);
}

// ===== ROBOTICS =====
function renderRobotics() {
  const qs = TECH_DIVE.map(d=>d.q);
  const traces = [
    {x:qs,y:TECH_DIVE.map(d=>d.nR),type:'scatter',mode:'lines',name:'Robotics News',line:{color:'#a16207',width:2.5},yaxis:'y'},
    {x:qs,y:TECH_DIVE.map(d=>d.vR),type:'bar',name:'Robotics CH-Deals',marker:{color:'#a16207',opacity:0.5},yaxis:'y2'},
  ];
  Plotly.newPlot('roboticsChart',traces,ml({
    yaxis:{title:{text:'News-Artikel'},side:'left'},
    yaxis2:{title:{text:'CH VC-Deals'},overlaying:'y',side:'right',tickfont:{size:11,color:'#8B949E'},gridcolor:'rgba(0,0,0,0)'},
    xaxis:{tickangle:-45},legend:{y:-0.3}
  }),CFG);
}


