/**
 * Lizzys – MBI Courses / EC Self-Assessment Wizard
 * Guided step-by-step assessment → competency profile → course recommendations
 */

// ===== EC DOMAINS =====
const EC_DOMAINS = [
  {id:"Opportunity",label:"Opportunity Recognition",evidence:"SEHR STARK",mbiScore:1.5,courses:3,warn:true,desc:"Geschäftsmöglichkeiten erkennen und bewerten",question:"Kannst du Marktlücken und Gründungschancen systematisch identifizieren?"},
  {id:"Strategic",label:"Strategic Thinking",evidence:"SEHR STARK",mbiScore:4,courses:25,warn:false,desc:"Strategisch denken, planen und Geschäftsmodelle entwickeln",question:"Kannst du eine Geschäftsstrategie entwickeln und ein Business Model Canvas erstellen?"},
  {id:"Commitment",label:"Commitment & Drive",evidence:"SEHR STARK",mbiScore:4,courses:25,warn:false,desc:"Durchhaltevermögen, Einsatz und Zielorientierung",question:"Bleibst du auch bei Rückschlägen motiviert und arbeitest konsequent auf Ziele hin?"},
  {id:"Analytical",label:"Analytical Competence",evidence:"SEHR STARK",mbiScore:5,courses:37,warn:false,desc:"Daten analysieren, Entscheidungen fundiert treffen",question:"Kannst du Daten auswerten und daraus fundierte Geschäftsentscheidungen ableiten?"},
  {id:"Innovative",label:"Creativity & Innovation",evidence:"STARK",mbiScore:4,courses:22,warn:false,desc:"Kreativ und innovativ Lösungen entwickeln",question:"Entwickelst du regelmässig neue Ideen und kreative Lösungsansätze?"},
  {id:"Human",label:"Leading & Managing",evidence:"STARK",mbiScore:4,courses:23,warn:false,desc:"Teams führen, motivieren und organisieren",question:"Hast du Erfahrung in der Führung von Teams oder Projekten?"},
  {id:"Operational",label:"Operational Management",evidence:"STARK",mbiScore:5,courses:50,warn:false,desc:"Prozesse und Ressourcen effizient managen",question:"Kannst du Prozesse optimieren und Ressourcen effizient einsetzen?"},
  {id:"Relationship",label:"Networking & Relationships",evidence:"SEHR STARK",mbiScore:5,courses:47,warn:false,desc:"Netzwerke aufbauen, pflegen und nutzen",question:"Baust du aktiv Netzwerke auf und pflegst professionelle Beziehungen?"},
  {id:"Learning",label:"Learning Agility",evidence:"STARK",mbiScore:5,courses:54,warn:false,desc:"Kontinuierlich lernen und sich anpassen",question:"Lernst du schnell aus Fehlern und passt dich neuen Situationen an?"},
  {id:"PersonalStrength",label:"Pitching & Personal Strength",evidence:"MODERAT",mbiScore:1,courses:12,warn:true,desc:"Überzeugend pitchen, Resilienz zeigen",question:"Kannst du eine Geschäftsidee überzeugend vor Investoren präsentieren?"},
  {id:"Technical",label:"Technical Competence",evidence:"MODERAT",mbiScore:4.5,courses:43,warn:false,desc:"Technisches Verständnis und digitale Skills",question:"Hast du technisches Verständnis (z.B. Programmierung, Datenbanken, Cloud)?"},
  {id:"Ethical",label:"Ethical & Sustainable Thinking",evidence:"MODERAT",mbiScore:3.5,courses:12,warn:false,desc:"Ethisch und nachhaltig handeln und entscheiden",question:"Berücksichtigst du ethische und nachhaltige Aspekte bei Geschäftsentscheidungen?"}
];

// State
let currentStep = 0;
const ecState = {};
const STORAGE_KEY = 'lizzys_ec_assessment';

// Load from localStorage
function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved && typeof saved === 'object') {
      Object.assign(ecState, saved);
      return Object.keys(saved).length === EC_DOMAINS.length && EC_DOMAINS.every(d => saved[d.id]);
    }
  } catch(e) {}
  EC_DOMAINS.forEach(d => ecState[d.id] = null);
  return false;
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(ecState));
}

// ===== EC COURSES =====
const EC_COURSES = {
  Opportunity:[
    {name:"Technology Entrepreneurship",ects:3,lang:"EN",score:1,ecs:["Opportunity"]},
    {name:"Business Innovation I: Geschäftsmodelle entwickeln",ects:4,lang:"DE",score:1,ecs:["Opportunity","Strategic","Innovative","Human","Learning"]},
    {name:"IC: Aktuelle Managementfragestellungen im Schweizer Startup-Ökosystem",ects:4,lang:"DE",score:1,ecs:["Opportunity","Strategic","Commitment","Analytical","Innovative","Human","Operational","Relationship","PersonalStrength"]}
  ],
  Strategic:[
    {name:"Grundlagen Business Innovation",ects:4,lang:"DE",score:3,ecs:["Strategic","Operational","Relationship","Learning","Technical"]},
    {name:"Business Innovation I: Geschäftsmodelle entwickeln",ects:4,lang:"DE",score:3,ecs:["Opportunity","Strategic","Innovative","Human","Learning"]},
    {name:"RPV: Digital Business and IT Innovations",ects:4,lang:"EN",score:3,ecs:["Strategic","Operational","Learning","Technical"]},
    {name:"IT Management: Strategische Positionierung der IT",ects:3,lang:"DE",score:3,ecs:["Strategic","Commitment","Learning"]},
    {name:"Platform Economy",ects:6,lang:"EN",score:2,ecs:["Strategic","Analytical","Innovative","Learning"]},
    {name:"Methods: Lean Venturing",ects:3,lang:"EN",score:2,ecs:["Strategic","Analytical","Human","Learning"]}
  ],
  Commitment:[
    {name:"Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle",ects:3,lang:"DE",score:3,ecs:["Commitment","Innovative","Analytical","Relationship"]},
    {name:"Digitale Kommunikation und Content Management",ects:3,lang:"DE",score:3,ecs:["Commitment","Relationship","Learning"]},
    {name:"Digital Platforms: Foundations, Management, Governance",ects:6,lang:"EN",score:2,ecs:["Commitment","PersonalStrength","Technical","Ethical"]},
    {name:"Effective Data Communication - How to Talk about Data",ects:3,lang:"EN",score:2,ecs:["Commitment","Relationship","PersonalStrength"]}
  ],
  Analytical:[
    {name:"FPV: Digitale und Datengetriebene Organisationen",ects:4,lang:"DE",score:3,ecs:["Analytical","Learning","Technical"]},
    {name:"RPV: Social Media Mining with NoSQL-Databases",ects:4,lang:"EN",score:3,ecs:["Analytical","Technical"]},
    {name:"Methoden: Data Science und AI for Business",ects:6,lang:"DE",score:3,ecs:["Analytical","Operational","Relationship","Learning"]},
    {name:"Evaluating Innovation in Companies and at System Level",ects:3,lang:"EN",score:3,ecs:["Analytical","Operational","Relationship","Learning","Technical"]},
    {name:"Behavioral Science & Technology",ects:4,lang:"EN",score:3,ecs:["Analytical","Commitment","PersonalStrength","Technical"]},
    {name:"User-Centred Design",ects:6,lang:"EN",score:3,ecs:["Analytical","Operational","Learning"]}
  ],
  Innovative:[
    {name:"FPV: Design Thinking für Digital Innovation",ects:4,lang:"DE",score:3,ecs:["Innovative","Human","Learning"]},
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Innovative","Operational","Technical","Ethical"]},
    {name:"Business Innovation I: Geschäftsmodelle entwickeln",ects:4,lang:"DE",score:3,ecs:["Innovative","Opportunity","Strategic","Human","Learning"]},
    {name:"FPV: Design Thinking mit KI",ects:4,lang:"DE",score:3,ecs:["Innovative","Human","Learning","Technical"]},
    {name:"Sustainable Innovation through Human-centered Design",ects:3,lang:"EN",score:2,ecs:["Innovative","Analytical"]}
  ],
  Human:[
    {name:"FPV: Design Thinking für Digital Innovation",ects:4,lang:"DE",score:3,ecs:["Human","Innovative","Learning"]},
    {name:"Chancen und Gefahren des Unternehmenswachstums",ects:3,lang:"DE",score:3,ecs:["Human","Operational","Relationship","Learning"]},
    {name:"High-Growth Entrepreneurship: An International Applied Perspective",ects:4,lang:"EN",score:3,ecs:["Human","Operational","Learning","Technical"]},
    {name:"Project Leadership für Business Innovation",ects:3,lang:"DE",score:3,ecs:["Human","Strategic","Analytical","Operational","Relationship","Learning","Ethical"]},
    {name:"Change und Project Management",ects:3,lang:"DE",score:2,ecs:["Human","Commitment","Operational","Relationship","Technical"]}
  ],
  Operational:[
    {name:"Technology Entrepreneurship",ects:3,lang:"EN",score:3,ecs:["Operational","Opportunity"]},
    {name:"Change und Project Management",ects:3,lang:"DE",score:3,ecs:["Operational","Human","Commitment","Relationship","Technical"]},
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Operational","Innovative","Technical","Ethical"]},
    {name:"Methods: Integrated Business Planning with Certificate",ects:3,lang:"EN",score:3,ecs:["Operational","Strategic","Relationship"]},
    {name:"Introduction to Business Process Management",ects:3,lang:"EN",score:3,ecs:["Operational","Learning","Technical"]}
  ],
  Relationship:[
    {name:"FPV: Digitale Kommunikation und Geschäftsmodelle",ects:4,lang:"DE",score:3,ecs:["Relationship","Strategic","Commitment","Human"]},
    {name:"Digitale Kommunikation und Content Management",ects:3,lang:"DE",score:3,ecs:["Relationship","Commitment","Learning"]},
    {name:"Methods: Social Network Analysis",ects:3,lang:"EN",score:3,ecs:["Relationship","Learning"]},
    {name:"Selling Technology Solutions",ects:3,lang:"EN",score:3,ecs:["Relationship","Strategic","Commitment","Operational","Technical","Ethical"]},
    {name:"Effective Data Communication - How to Talk about Data",ects:3,lang:"EN",score:3,ecs:["Relationship","Commitment","PersonalStrength"]}
  ],
  Learning:[
    {name:"Methoden: Data Science und AI for Business",ects:6,lang:"DE",score:3,ecs:["Learning","Analytical","Operational","Relationship"]},
    {name:"Leveraging AI for Healthcare",ects:6,lang:"EN",score:3,ecs:["Learning","Operational","Relationship","Technical"]},
    {name:"FPV: Design Thinking für Digital Innovation",ects:4,lang:"DE",score:3,ecs:["Learning","Innovative","Human"]},
    {name:"Entrepreneurial Finance",ects:3,lang:"EN",score:3,ecs:["Learning","Analytical","Relationship"]},
    {name:"User-Centred Design",ects:6,lang:"EN",score:3,ecs:["Learning","Analytical","Operational"]}
  ],
  PersonalStrength:[
    {name:"Technology Entrepreneurship",ects:3,lang:"EN",score:2,ecs:["PersonalStrength","Opportunity","Operational"]},
    {name:"FPV: Data Science und AI for Business",ects:4,lang:"DE",score:2,ecs:["PersonalStrength","Innovative","Strategic","Commitment","Analytical","Operational","Relationship","Learning"]},
    {name:"IC: Gesellschaftliche Aspekte der Digitalisierung",ects:4,lang:"DE",score:2,ecs:["PersonalStrength","Analytical","Operational","Learning"]},
    {name:"RPV: Prompt Engineering: Innovation through generative AI",ects:4,lang:"EN",score:2,ecs:["PersonalStrength","Analytical","Operational","Relationship","Learning","Technical"]},
    {name:"Effective Data Communication - How to Talk about Data",ects:3,lang:"EN",score:2,ecs:["PersonalStrength","Commitment","Relationship"]}
  ],
  Technical:[
    {name:"Technology Entrepreneurship",ects:3,lang:"EN",score:3,ecs:["Technical","Opportunity","Operational"]},
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Technical","Innovative","Operational","Ethical"]},
    {name:"Business Process Mining and Engineering",ects:6,lang:"EN",score:3,ecs:["Technical","Analytical","Human","Operational","Ethical"]},
    {name:"RPV: Prompt Engineering: Innovation through generative AI",ects:4,lang:"EN",score:3,ecs:["Technical","Analytical","Operational","Relationship","Learning","PersonalStrength"]},
    {name:"Cloud Computing für datengetriebene Geschäftsmodelle",ects:6,lang:"DE",score:3,ecs:["Technical","Commitment","Analytical"]},
    {name:"Methods: Scalable Tech Stacks for Business Ideas",ects:3,lang:"EN",score:3,ecs:["Technical","Innovative","Operational"]},
    {name:"Introduction to Software Engineering",ects:6,lang:"EN",score:3,ecs:["Technical","Learning"]}
  ],
  Ethical:[
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Ethical","Innovative","Operational","Technical"]},
    {name:"Digital Platforms: Foundations, Management, Governance",ects:6,lang:"EN",score:3,ecs:["Ethical","Commitment","PersonalStrength","Relationship","Technical"]},
    {name:"Managing IT Security and Privacy in Organisations",ects:3,lang:"EN",score:3,ecs:["Ethical","Commitment","Human","Operational"]},
    {name:"IC: Responsible Innovation Lab",ects:4,lang:"EN",score:3,ecs:["Ethical","Innovative","Operational","Relationship","Technical"]}
  ]
};

// ===== SECTOR COURSES =====
const SECTOR_COURSES = {
  GenAI:[
    {name:"FPV: Digitale Kommunikation und Geschäftsmodelle",ects:4,lang:"DE",score:3,ecs:["Strategic","Commitment","Human","Relationship"],doppelt:true},
    {name:"Methoden: Data Science und AI for Business",ects:6,lang:"DE",score:3,ecs:["Analytical","Operational","Relationship","Learning"],doppelt:true},
    {name:"IC: From Data2Dollar - Dein Technologiekoffer",ects:4,lang:"DE",score:3,ecs:["Analytical","Operational","Learning","PersonalStrength","Technical"],doppelt:true},
    {name:"RPV: Prompt Engineering: Innovation through generative AI",ects:4,lang:"EN",score:3,ecs:["Analytical","Operational","Relationship","Learning","PersonalStrength","Technical"],doppelt:true},
    {name:"FPV: Gestaltung Digitaler Produkte und Lösungen mit AI",ects:4,lang:"DE",score:2,ecs:["Strategic","Innovative","Human","Learning"],doppelt:true},
    {name:"Selling Technology Solutions",ects:3,lang:"EN",score:2,ecs:["Strategic","Commitment","Operational","Relationship","Technical","Ethical"],doppelt:true},
    {name:"Business Process Mining and Engineering",ects:6,lang:"EN",score:2,ecs:["Analytical","Human","Operational","Technical","Ethical"],doppelt:true},
    {name:"Cloud Computing für datengetriebene Geschäftsmodelle",ects:6,lang:"DE",score:1,ecs:["Commitment","Analytical","Technical"],doppelt:true}
  ],
  HealthTech:[
    {name:"Leveraging AI for Healthcare",ects:6,lang:"EN",score:3,ecs:["Operational","Relationship","Learning","Technical"],doppelt:true},
    {name:"Evaluating Innovation in Companies and at System Level",ects:3,lang:"EN",score:3,ecs:["Analytical","Operational","Relationship","Learning","Technical"],doppelt:true},
    {name:"IC: Aktuelle Managementfragestellungen im Schweizer Startup-Ökosystem",ects:4,lang:"DE",score:2,ecs:["Opportunity","Strategic","Commitment","Analytical","Innovative","Human","Operational","Relationship","PersonalStrength"],doppelt:true},
    {name:"Mobile Sensing and Behavioral Metrics",ects:6,lang:"EN",score:2,ecs:["Analytical","Innovative","Relationship"],doppelt:true}
  ],
  MedTech:[
    {name:"Business Process Mining and Engineering",ects:6,lang:"EN",score:2,ecs:["Analytical","Human","Operational","Technical","Ethical"],doppelt:true}
  ],
  BioTech:[
    {name:"RPV: Aviation and Space Industry",ects:4,lang:"EN",score:3,ecs:["Relationship","Technical"],doppelt:true}
  ],
  Robotics:[
    {name:"KI- und Technologie-Anwendungen im Supply Chain",ects:3,lang:"DE",score:3,ecs:["Commitment","Operational","Learning","Ethical"],doppelt:true},
    {name:"Evaluating Innovation in Companies and at System Level",ects:3,lang:"EN",score:2,ecs:["Analytical","Operational","Relationship","Learning","Technical"],doppelt:true},
    {name:"Methoden: Data Science und AI for Business",ects:6,lang:"DE",score:1,ecs:["Analytical","Operational","Relationship","Learning"],doppelt:true}
  ]
};

const SECTOR_HINTS = {
  MedTech:"MedTech kaum im MBI-Curriculum abgedeckt. Externe Ressourcen empfohlen: Swiss Medtech Cluster, EPFL, FDA/CE-Mark Grundlagen.",
  BioTech:"BioTech nicht im MBI-Curriculum. Externe Ressourcen: Swiss Biotech Association, ETH Life Sciences, Basel Biovalley.",
  Robotics:"Robotics kaum im MBI-Curriculum. Externe Ressourcen: ETH Robotics, Swiss Innovation Park, NCCR Robotics."
};

// ===== WIZARD RENDERING =====
function renderWizard() {
  renderProgress();
  renderWizardCard();
  renderCounter();
}

function renderProgress() {
  const el = document.getElementById('wizardProgress');
  el.innerHTML = EC_DOMAINS.map((d,i) => {
    let cls = '';
    if (i < currentStep) cls = 'done';
    else if (i === currentStep) cls = 'active';
    return `<div class="wizard-dot ${cls}" title="${d.label}"></div>`;
  }).join('');
}

function renderWizardCard() {
  const d = EC_DOMAINS[currentStep];
  const state = ecState[d.id];
  const card = document.getElementById('wizardCard');
  card.innerHTML = `
    <div class="wizard-domain">${d.label}</div>
    <div class="wizard-desc">${d.desc}</div>
    <div class="wizard-evidence">Evidenz: ${d.evidence} · ${d.courses} MBI-Kurse${d.warn?' · ⚠️ Kritische Lücke im MBI':''}</div>
    <div class="wizard-question">${d.question}</div>
    <div class="wizard-btns">
      <button class="wizard-btn ${state==='stark'?'selected-stark':''}" onclick="selectAnswer('${d.id}','stark')">💪 Stark</button>
      <button class="wizard-btn ${state==='okay'?'selected-okay':''}" onclick="selectAnswer('${d.id}','okay')">👍 Okay</button>
      <button class="wizard-btn ${state==='luecke'?'selected-luecke':''}" onclick="selectAnswer('${d.id}','luecke')">⚠️ Lücke</button>
    </div>
    <div class="wizard-nav">
      <button class="wizard-nav-btn" onclick="prevStep()" ${currentStep===0?'disabled style="opacity:0.3"':''}>← Zurück</button>
      ${currentStep < EC_DOMAINS.length - 1 
        ? `<button class="wizard-nav-btn primary" onclick="nextStep()" ${!state?'disabled style="opacity:0.5"':''}>Weiter →</button>`
        : `<button class="wizard-nav-btn primary" onclick="finishAssessment()" ${!state?'disabled style="opacity:0.5"':''}>✓ Auswertung anzeigen</button>`
      }
    </div>
  `;
}

function renderCounter() {
  document.getElementById('wizardCounter').textContent = `${currentStep + 1} von ${EC_DOMAINS.length}`;
}

window.selectAnswer = function(id, value) {
  ecState[id] = value;
  saveState();
  renderWizardCard();
};

window.nextStep = function() {
  if (currentStep < EC_DOMAINS.length - 1 && ecState[EC_DOMAINS[currentStep].id]) {
    currentStep++;
    renderWizard();
  }
};

window.prevStep = function() {
  if (currentStep > 0) {
    currentStep--;
    renderWizard();
  }
};

window.finishAssessment = function() {
  if (!ecState[EC_DOMAINS[currentStep].id]) return;
  saveState();
  showResults();
};

window.restartAssessment = function() {
  EC_DOMAINS.forEach(d => ecState[d.id] = null);
  currentStep = 0;
  localStorage.removeItem(STORAGE_KEY);
  document.getElementById('wizardView').style.display = 'block';
  document.getElementById('resultsView').style.display = 'none';
  renderWizard();
};

// ===== RESULTS =====
function showResults() {
  document.getElementById('wizardView').style.display = 'none';
  document.getElementById('resultsView').style.display = 'block';
  renderGapSummary();
  renderRadarChart();
  renderGapCourses();
  renderOkayCourses();
}

function renderGapSummary() {
  const el = document.getElementById('gapSummary');
  el.innerHTML = EC_DOMAINS.map(d => {
    const s = ecState[d.id] || 'unrated';
    return `<span class="gap-badge ${s}">${s==='luecke'?'⚠️':s==='stark'?'✅':'➖'} ${d.label}</span>`;
  }).join('');
}

function renderRadarChart() {
  const labels = EC_DOMAINS.map(d => d.label);
  const mbiScores = EC_DOMAINS.map(d => d.mbiScore);
  const userScores = EC_DOMAINS.map(d => {
    const s = ecState[d.id];
    return s === 'stark' ? 5 : s === 'okay' ? 3 : 1;
  });

  const trace1 = {
    type:'scatterpolar', r:[...mbiScores, mbiScores[0]], theta:[...labels, labels[0]],
    fill:'toself', name:'MBI-Abdeckung',
    fillcolor:'rgba(0,229,160,0.1)', line:{color:'#00E5A0',width:2},
    marker:{size:4}
  };
  const trace2 = {
    type:'scatterpolar', r:[...userScores, userScores[0]], theta:[...labels, labels[0]],
    fill:'toself', name:'Deine Stärke',
    fillcolor:'rgba(74,158,255,0.1)', line:{color:'#4A9EFF',width:2},
    marker:{size:4}
  };

  Plotly.newPlot('radarChart',[trace1,trace2],{
    polar:{
      bgcolor:'rgba(0,0,0,0)',
      radialaxis:{visible:true,range:[0,5.5],tickfont:{size:9,color:'#6b7280'},gridcolor:'rgba(255,255,255,0.08)'},
      angularaxis:{tickfont:{size:10,color:'#E6EDF3'},gridcolor:'rgba(255,255,255,0.08)'}
    },
    plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)',
    font:{family:'DM Sans, sans-serif',color:'#8B949E'},
    legend:{orientation:'h',x:0.2,y:-0.15,font:{size:12,color:'#8B949E'}},
    margin:{l:60,r:60,t:40,b:60}
  },{responsive:true,displayModeBar:false});
}

function renderGapCourses() {
  const gaps = EC_DOMAINS.filter(d => ecState[d.id] === 'luecke');
  const el = document.getElementById('gapCoursesSection');

  if (!gaps.length) {
    el.innerHTML = '<div class="no-gaps-msg">🎉 Keine Lücken identifiziert! Schau dir trotzdem die Sektor-Kurse unten an.</div>';
    return;
  }

  const courseMap = new Map();
  gaps.forEach(g => {
    (EC_COURSES[g.id] || []).forEach(c => {
      if (!courseMap.has(c.name)) {
        courseMap.set(c.name, {...c, gapDomains: [g.label], gapCount: 1});
      } else {
        const existing = courseMap.get(c.name);
        existing.gapDomains.push(g.label);
        existing.gapCount++;
      }
    });
  });

  const sorted = [...courseMap.values()].sort((a,b) => {
    if (b.gapCount !== a.gapCount) return b.gapCount - a.gapCount;
    return b.score - a.score;
  });

  el.innerHTML = `
    <h3 style="color:var(--text);margin-bottom:0.5rem;">🚨 Kurse für deine ${gaps.length} Lücke${gaps.length>1?'n':''}</h3>
    <p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:1rem;">Sortiert nach Relevanz: Kurse die mehrere Lücken abdecken stehen oben.</p>
    ${sorted.map((c,i) => renderCourseItem(c, c.gapDomains, i+1)).join('')}
  `;
}

function renderOkayCourses() {
  const okays = EC_DOMAINS.filter(d => ecState[d.id] === 'okay');
  const el = document.getElementById('okayCoursesSection');

  if (!okays.length) { el.innerHTML = ''; return; }

  const courseMap = new Map();
  okays.forEach(g => {
    (EC_COURSES[g.id] || []).slice(0, 3).forEach(c => {
      if (!courseMap.has(c.name)) {
        courseMap.set(c.name, {...c, okayDomains: [g.label]});
      } else {
        courseMap.get(c.name).okayDomains.push(g.label);
      }
    });
  });

  const sorted = [...courseMap.values()].sort((a,b) => b.score - a.score);

  el.innerHTML = `
    <h3 style="color:var(--text);margin-top:2rem;margin-bottom:0.5rem;">📈 Kurse zum Vertiefen (für deine «Okay»-Bereiche)</h3>
    <p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:1rem;">Diese Kompetenzen hast du, aber es gibt Potenzial zum Ausbauen.</p>
    ${sorted.slice(0,8).map(c => renderCourseItem(c, c.okayDomains || c.ecs)).join('')}
  `;
}

function renderCourseItem(c, highlightEcs, rank) {
  const dots = [1,2,3].map(i => `<div class="score-dot ${i<=c.score?'filled':''}"></div>`).join('');
  const ecLabels = (highlightEcs||c.ecs||[]).map(e => `<span style="color:#00E5A0">${e}</span>`).join(' · ');
  const rankBadge = rank ? `<span class="badge-rank">#${rank}</span>` : '';
  return `<div class="course-item">
    <div>
      <div class="course-name">${rankBadge}${c.name}${c.doppelt?'<span class="badge-doppelt">Doppelt wertvoll</span>':''}</div>
      <div class="course-meta">${c.ects} ECTS · ${c.lang}</div>
      <div class="course-ecs">${ecLabels}</div>
    </div>
    <div class="course-score">${dots}</div>
  </div>`;
}

// ===== SECTOR TABS =====
function renderSektorContent(sektor) {
  const courses = SECTOR_COURSES[sektor] || [];
  const hint = SECTOR_HINTS[sektor];
  const el = document.getElementById('sektorContent');
  const sorted = [...courses].sort((a,b) => b.score - a.score);
  el.innerHTML = sorted.map((c,i) => renderCourseItem(c, c.ecs, i+1)).join('') +
    (hint ? `<div class="sector-hint">⚠️ ${hint}</div>` : '');
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  const isComplete = loadState();

  if (isComplete) {
    showResults();
  } else {
    // Find first unanswered step
    const firstUnanswered = EC_DOMAINS.findIndex(d => !ecState[d.id]);
    currentStep = firstUnanswered >= 0 ? firstUnanswered : 0;
    renderWizard();
  }

  // Sektor tabs
  const tabs = document.querySelectorAll('#sektorTabs .sector-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderSektorContent(tab.dataset.sektor);
    });
  });
  renderSektorContent('GenAI');
});
