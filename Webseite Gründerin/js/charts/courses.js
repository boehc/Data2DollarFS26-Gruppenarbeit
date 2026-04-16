/**
 * data2dollar – MBI Courses / EC Self-Assessment
 * Mai & Thai (2025) · 12 EC Domains · Sektor-Kurse
 */

// ===== EC DOMAINS =====
const EC_DOMAINS = [
  {id:"Opportunity",label:"Opportunity",evidence:"SEHR STARK",courses:3,warn:true,desc:"Geschäftsmöglichkeiten erkennen"},
  {id:"Strategic",label:"Strategic",evidence:"SEHR STARK",courses:25,warn:false,desc:"Strategisch denken & planen"},
  {id:"Commitment",label:"Commitment",evidence:"SEHR STARK",courses:25,warn:false,desc:"Durchhaltevermögen & Einsatz"},
  {id:"Analytical",label:"Analytical",evidence:"SEHR STARK",courses:37,warn:false,desc:"Daten analysieren & entscheiden"},
  {id:"Innovative",label:"Innovative",evidence:"STARK",courses:22,warn:false,desc:"Kreativ & innovativ gestalten"},
  {id:"Human",label:"Human",evidence:"STARK",courses:23,warn:false,desc:"Teams führen & motivieren"},
  {id:"Operational",label:"Operational",evidence:"STARK",courses:50,warn:false,desc:"Prozesse & Ressourcen managen"},
  {id:"Relationship",label:"Relationship",evidence:"SEHR STARK",courses:47,warn:false,desc:"Netzwerke aufbauen & pflegen"},
  {id:"Learning",label:"Learning",evidence:"STARK",courses:54,warn:false,desc:"Kontinuierlich lernen & anpassen"},
  {id:"PersonalStrength",label:"Personal Strength",evidence:"MODERAT",courses:12,warn:true,desc:"Pitchen, überzeugen, Resilienz"},
  {id:"Technical",label:"Technical",evidence:"MODERAT",courses:43,warn:false,desc:"Technisches Verständnis"},
  {id:"Ethical",label:"Ethical",evidence:"MODERAT",courses:12,warn:false,desc:"Ethisch & nachhaltig handeln"}
];

// State
const ecState = {};
EC_DOMAINS.forEach(d => ecState[d.id] = null); // null=unrated, 'stark', 'okay', 'luecke'

// ===== EC COURSES (top courses per domain, score >= 2) =====
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
    {name:"FPV: Gestaltung Digitaler Produkte und Lösungen mit AI",ects:4,lang:"DE",score:2,ecs:["Strategic","Innovative","Human","Learning"]},
    {name:"Business Innovation II: Unternehmen gestalten und digital transformieren",ects:4,lang:"DE",score:2,ecs:["Strategic","Innovative","Technical"]},
    {name:"Quality Management for Superior Performance and Innovation",ects:3,lang:"EN",score:2,ecs:["Strategic","Operational","Relationship","Learning"]},
    {name:"Methods: Lean Venturing",ects:3,lang:"EN",score:2,ecs:["Strategic","Analytical","Human","Learning"]},
    {name:"Project Leadership für Business Innovation",ects:3,lang:"DE",score:2,ecs:["Strategic","Analytical","Human","Operational","Relationship","Learning","Ethical"]}
  ],
  Commitment:[
    {name:"Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle",ects:3,lang:"DE",score:3,ecs:["Commitment","Innovative","Analytical","Relationship"]},
    {name:"Digitale Kommunikation und Content Management",ects:3,lang:"DE",score:3,ecs:["Commitment","Relationship","Learning"]},
    {name:"Digital Platforms: Foundations, Management, Governance",ects:6,lang:"EN",score:2,ecs:["Commitment","PersonalStrength","Technical","Ethical"]},
    {name:"Effective Data Communication - How to Talk about Data",ects:3,lang:"EN",score:2,ecs:["Commitment","Relationship","PersonalStrength"]},
    {name:"Behavioral Science & Technology",ects:4,lang:"EN",score:2,ecs:["Commitment","Analytical","PersonalStrength","Technical"]}
  ],
  Analytical:[
    {name:"FPV: Digitale und Datengetriebene Organisationen",ects:4,lang:"DE",score:3,ecs:["Analytical","Learning","Technical"]},
    {name:"RPV: Social Media Mining with NoSQL-Databases",ects:4,lang:"EN",score:3,ecs:["Analytical","Technical"]},
    {name:"Methoden: Data Science und AI for Business",ects:6,lang:"DE",score:3,ecs:["Analytical","Operational","Relationship","Learning"]},
    {name:"IC: Gesellschaftliche Aspekte der Digitalisierung",ects:4,lang:"DE",score:3,ecs:["Analytical","Operational","Learning","PersonalStrength"]},
    {name:"Evaluating Innovation in Companies and at System Level",ects:3,lang:"EN",score:3,ecs:["Analytical","Operational","Relationship","Learning","Technical"]},
    {name:"Methods: Supply Chain and Operations Management",ects:3,lang:"EN",score:3,ecs:["Analytical","Operational","Relationship","Learning"]},
    {name:"Behavioral Science & Technology",ects:4,lang:"EN",score:3,ecs:["Analytical","Commitment","PersonalStrength","Technical"]},
    {name:"User-Centred Design",ects:6,lang:"EN",score:3,ecs:["Analytical","Operational","Learning"]},
    {name:"IC: Lean Product and Outsourcing Management",ects:4,lang:"EN",score:3,ecs:["Analytical","Innovative","Operational","Learning"]},
    {name:"Forschungsmethoden für Geschäftsinnovation",ects:3,lang:"DE",score:2,ecs:["Analytical","Innovative"]},
    {name:"Sustainable Innovation through Human-centered Design",ects:3,lang:"EN",score:2,ecs:["Analytical","Innovative"]},
    {name:"Entrepreneurial Finance",ects:3,lang:"EN",score:2,ecs:["Analytical","Relationship","Learning"]},
    {name:"Business Process Mining and Engineering",ects:6,lang:"EN",score:2,ecs:["Analytical","Human","Operational","Technical","Ethical"]},
    {name:"RPV: Prompt Engineering: Innovation through generative AI",ects:4,lang:"EN",score:2,ecs:["Analytical","Operational","Relationship","Learning","PersonalStrength","Technical"]}
  ],
  Innovative:[
    {name:"Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle",ects:3,lang:"DE",score:3,ecs:["Innovative","Commitment","Analytical","Relationship"]},
    {name:"FPV: Design Thinking für Digital Innovation",ects:4,lang:"DE",score:3,ecs:["Innovative","Human","Learning"]},
    {name:"FPV: Data Science und AI for Business",ects:4,lang:"DE",score:3,ecs:["Innovative","Strategic","Commitment","Analytical","Operational","Relationship","Learning","PersonalStrength"]},
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Innovative","Operational","Technical","Ethical"]},
    {name:"Business Innovation I: Geschäftsmodelle entwickeln",ects:4,lang:"DE",score:3,ecs:["Innovative","Opportunity","Strategic","Human","Learning"]},
    {name:"Business Innovation II: Unternehmen gestalten und digital transformieren",ects:4,lang:"DE",score:3,ecs:["Innovative","Strategic","Technical"]},
    {name:"FPV: Design Thinking mit KI",ects:4,lang:"DE",score:3,ecs:["Innovative","Human","Learning","Technical"]},
    {name:"RPV: Venturing in Emerging Trends",ects:4,lang:"EN",score:2,ecs:["Innovative","Commitment","Human","Relationship","Learning","PersonalStrength"]},
    {name:"Sustainable Innovation through Human-centered Design",ects:3,lang:"EN",score:2,ecs:["Innovative","Analytical"]},
    {name:"IC: Lean Product and Outsourcing Management",ects:4,lang:"EN",score:2,ecs:["Innovative","Analytical","Operational","Learning"]}
  ],
  Human:[
    {name:"FPV: Design Thinking für Digital Innovation",ects:4,lang:"DE",score:3,ecs:["Human","Innovative","Learning"]},
    {name:"Chancen und Gefahren des Unternehmenswachstums",ects:3,lang:"DE",score:3,ecs:["Human","Operational","Relationship","Learning"]},
    {name:"High-Growth Entrepreneurship: An International Applied Perspective",ects:4,lang:"EN",score:3,ecs:["Human","Operational","Learning","Technical"]},
    {name:"IC: Strategic Management of New Technologies in Companies",ects:4,lang:"EN",score:3,ecs:["Human","Operational","Relationship","PersonalStrength"]},
    {name:"Project Leadership für Business Innovation",ects:3,lang:"DE",score:3,ecs:["Human","Strategic","Analytical","Operational","Relationship","Learning","Ethical"]},
    {name:"Change und Project Management",ects:3,lang:"DE",score:2,ecs:["Human","Commitment","Operational","Relationship","Technical"]},
    {name:"Corporate Transformation - An Integrative Perspective",ects:3,lang:"EN",score:2,ecs:["Human","Operational","Relationship","Learning","Technical"]},
    {name:"FPV: Psychologie der Innovationsprozesse",ects:4,lang:"DE",score:2,ecs:["Human","Commitment","Operational","Relationship","Learning"]}
  ],
  Operational:[
    {name:"Technology Entrepreneurship",ects:3,lang:"EN",score:3,ecs:["Operational","Opportunity"]},
    {name:"FPV: Supply Chain Innovation",ects:4,lang:"DE",score:3,ecs:["Operational","Commitment","Relationship","Learning","Ethical"]},
    {name:"Change und Project Management",ects:3,lang:"DE",score:3,ecs:["Operational","Human","Commitment","Relationship","Technical"]},
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Operational","Innovative","Technical","Ethical"]},
    {name:"Methods: Integrated Business Planning with Certificate",ects:3,lang:"EN",score:3,ecs:["Operational","Strategic","Relationship"]},
    {name:"Introduction to Business Process Management",ects:3,lang:"EN",score:3,ecs:["Operational","Learning","Technical"]},
    {name:"IC: Agile Transformation und Arbeitsprinzipien",ects:4,lang:"DE",score:3,ecs:["Operational","Innovative","Learning","Technical","Relationship"]},
    {name:"Supply Chain Management I",ects:3,lang:"DE",score:3,ecs:["Operational","Commitment","Learning","Ethical"]}
  ],
  Relationship:[
    {name:"FPV: Digitale Kommunikation und Geschäftsmodelle",ects:4,lang:"DE",score:3,ecs:["Relationship","Strategic","Commitment","Human"]},
    {name:"FPV: Data Science und AI for Business",ects:4,lang:"DE",score:3,ecs:["Relationship","Innovative","Strategic","Commitment","Analytical","Operational","Learning","PersonalStrength"]},
    {name:"Digitale Kommunikation und Content Management",ects:3,lang:"DE",score:3,ecs:["Relationship","Commitment","Learning"]},
    {name:"Methods: Social Network Analysis",ects:3,lang:"EN",score:3,ecs:["Relationship","Learning"]},
    {name:"Selling Technology Solutions",ects:3,lang:"EN",score:3,ecs:["Relationship","Strategic","Commitment","Operational","Technical","Ethical"]},
    {name:"Digital Platforms: Foundations, Management, Governance",ects:6,lang:"EN",score:3,ecs:["Relationship","Commitment","PersonalStrength","Technical","Ethical"]},
    {name:"RPV: Prompt Engineering: Innovation through generative AI",ects:4,lang:"EN",score:3,ecs:["Relationship","Analytical","Operational","Learning","PersonalStrength","Technical"]},
    {name:"Project Leadership für Business Innovation",ects:3,lang:"DE",score:3,ecs:["Relationship","Strategic","Human","Analytical","Operational","Learning","Ethical"]},
    {name:"Effective Data Communication - How to Talk about Data",ects:3,lang:"EN",score:3,ecs:["Relationship","Commitment","PersonalStrength"]},
    {name:"Community Management",ecs:3,lang:"DE",score:3,ecs:["Relationship","Strategic","Innovative","Human","Technical"]}
  ],
  Learning:[
    {name:"IC: Innovationen in Entwicklungsländern",ects:4,lang:"DE",score:3,ecs:["Learning","Commitment"]},
    {name:"FPV: Supply Chain Innovation",ects:4,lang:"DE",score:3,ecs:["Learning","Operational","Commitment","Relationship","Ethical"]},
    {name:"Methoden: Data Science und AI for Business",ects:6,lang:"DE",score:3,ecs:["Learning","Analytical","Operational","Relationship"]},
    {name:"Leveraging AI for Healthcare",ects:6,lang:"EN",score:3,ecs:["Learning","Operational","Relationship","Technical"]},
    {name:"FPV: Design Thinking für Digital Innovation",ects:4,lang:"DE",score:3,ecs:["Learning","Innovative","Human"]},
    {name:"Entrepreneurial Finance",ects:3,lang:"EN",score:3,ecs:["Learning","Analytical","Relationship"]},
    {name:"RPV: Low Code Development Platforms",ects:4,lang:"EN",score:3,ecs:["Learning","Operational","Human","Technical"]},
    {name:"User-Centred Design",ects:6,lang:"EN",score:3,ecs:["Learning","Analytical","Operational"]},
    {name:"Software Assessment: From Planning to Experimentation",ects:6,lang:"EN",score:3,ecs:["Learning","Analytical","Operational","Technical"]},
    {name:"Ubiquitous Computing",ects:3,lang:"EN",score:3,ecs:["Learning","Relationship","Technical"]}
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
    {name:"Change und Project Management",ects:3,lang:"DE",score:3,ecs:["Technical","Human","Commitment","Operational","Relationship"]},
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Technical","Innovative","Operational","Ethical"]},
    {name:"Business Process Mining and Engineering",ects:6,lang:"EN",score:3,ecs:["Technical","Analytical","Human","Operational","Ethical"]},
    {name:"Digital Platforms: Foundations, Management, Governance",ects:6,lang:"EN",score:3,ecs:["Technical","Commitment","PersonalStrength","Relationship","Ethical"]},
    {name:"RPV: Prompt Engineering: Innovation through generative AI",ects:4,lang:"EN",score:3,ecs:["Technical","Analytical","Operational","Relationship","Learning","PersonalStrength"]},
    {name:"Cloud Computing für datengetriebene Geschäftsmodelle",ects:6,lang:"DE",score:3,ecs:["Technical","Commitment","Analytical"]},
    {name:"Methods: Scalable Tech Stacks for Business Ideas",ects:3,lang:"EN",score:3,ecs:["Technical","Innovative","Operational"]},
    {name:"Introduction to Blockchain, DLT & Crypto",ects:3,lang:"EN",score:3,ecs:["Technical","Strategic","Learning","Ethical"]},
    {name:"Introduction to Software Engineering",ects:6,lang:"EN",score:3,ecs:["Technical","Learning"]}
  ],
  Ethical:[
    {name:"Agentic AI Design, Governance and Management",ects:6,lang:"EN",score:3,ecs:["Ethical","Innovative","Operational","Technical"]},
    {name:"KI- und Technologie-Anwendungen im Supply Chain",ects:3,lang:"DE",score:3,ecs:["Ethical","Commitment","Operational","Learning"]},
    {name:"Digital Platforms: Foundations, Management, Governance",ects:6,lang:"EN",score:3,ecs:["Ethical","Commitment","PersonalStrength","Relationship","Technical"]},
    {name:"Managing IT Security and Privacy in Organisations",ects:3,lang:"EN",score:3,ecs:["Ethical","Commitment","Human","Operational"]},
    {name:"IC: Responsible Innovation Lab",ects:4,lang:"EN",score:3,ecs:["Ethical","Innovative","Operational","Relationship","Technical"]},
    {name:"Operative Excellence (OPEX)",ects:3,lang:"EN",score:2,ecs:["Ethical","Operational","Learning","Technical"]},
    {name:"Supply Chain Management I",ects:3,lang:"DE",score:2,ecs:["Ethical","Operational","Commitment","Learning"]},
    {name:"Project Leadership für Business Innovation",ects:3,lang:"DE",score:2,ecs:["Ethical","Strategic","Human","Analytical","Operational","Relationship","Learning"]},
    {name:"Introduction to Blockchain, DLT & Crypto",ects:3,lang:"EN",score:2,ecs:["Ethical","Technical","Strategic","Learning"]}
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
    {name:"FPV: Data Science und AI for Business",ects:4,lang:"DE",score:2,ecs:["Strategic","Commitment","Analytical","Innovative","Operational","Relationship","Learning","PersonalStrength"],doppelt:true},
    {name:"Selling Technology Solutions",ects:3,lang:"EN",score:2,ecs:["Strategic","Commitment","Operational","Relationship","Technical","Ethical"],doppelt:true},
    {name:"Business Process Mining and Engineering",ects:6,lang:"EN",score:2,ecs:["Analytical","Human","Operational","Technical","Ethical"],doppelt:true},
    {name:"FPV: Gestaltung und Entwicklung von User Interfaces",ects:4,lang:"DE",score:1,ecs:["Innovative","Operational","Technical"],doppelt:true},
    {name:"Methods: Social Network Analysis",ects:3,lang:"EN",score:1,ecs:["Relationship","Learning"],doppelt:true},
    {name:"IC: Gesellschaftliche Aspekte der Digitalisierung",ects:4,lang:"DE",score:1,ecs:["Analytical","Operational","Learning","PersonalStrength"],doppelt:true},
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

// ===== RENDER EC GRID =====
function renderECGrid() {
  const grid = document.getElementById('ecGrid');
  grid.innerHTML = EC_DOMAINS.map(d => {
    const state = ecState[d.id];
    const cls = state || '';
    return `<div class="ec-card ${cls}" id="ec-${d.id}">
      ${d.warn?'<span class="ec-card-warn">⚠️</span>':''}
      <div class="ec-card-name">${d.label}</div>
      <div class="ec-card-meta">${d.courses} Kurse · ${d.desc}</div>
      <div class="ec-card-evidence">Evidenz: ${d.evidence}</div>
      <div class="ec-state-btns">
        <button class="ec-state-btn ${state==='stark'?'active-stark':''}" onclick="setEC('${d.id}','stark')">✅ stark</button>
        <button class="ec-state-btn ${state==='okay'?'active-okay':''}" onclick="setEC('${d.id}','okay')">➖ okay</button>
        <button class="ec-state-btn ${state==='luecke'?'active-luecke':''}" onclick="setEC('${d.id}','luecke')">⚠️ Lücke</button>
      </div>
    </div>`;
  }).join('');
}

window.setEC = function(id, state) {
  ecState[id] = ecState[id] === state ? null : state;
  renderECGrid();
  renderECResult();
};

function renderECResult() {
  const gaps = EC_DOMAINS.filter(d => ecState[d.id] === 'luecke');
  const el = document.getElementById('ecResult');
  if (!gaps.length) {
    el.innerHTML = '<div class="ec-result-empty">Markiere Domains als «Lücke», um passende Kurse zu sehen.</div>';
    return;
  }

  // Collect courses for gap domains, deduplicate, sort by score
  const courseMap = new Map();
  gaps.forEach(g => {
    const courses = EC_COURSES[g.id] || [];
    courses.forEach(c => {
      const key = c.name;
      if (!courseMap.has(key)) {
        courseMap.set(key, {...c, gapDomains: [g.label]});
      } else {
        courseMap.get(key).gapDomains.push(g.label);
      }
    });
  });

  const sorted = [...courseMap.values()].sort((a,b) => {
    // Sort by number of gap domains covered desc, then score desc
    if (b.gapDomains.length !== a.gapDomains.length) return b.gapDomains.length - a.gapDomains.length;
    return b.score - a.score;
  });

  el.innerHTML = `<h4 style="color:var(--text);margin-bottom:0.75rem;">📋 ${sorted.length} Kurse für deine ${gaps.length} Lücke${gaps.length>1?'n':''}</h4>` +
    sorted.map(c => renderCourseItem(c, c.gapDomains)).join('');
}

function renderCourseItem(c, highlightEcs) {
  const dots = [1,2,3].map(i => `<div class="score-dot ${i<=c.score?'filled':''}"></div>`).join('');
  const ecLabels = (highlightEcs||c.ecs||[]).map(e => `<span style="color:#00E5A0">${e}</span>`).join(' · ');
  return `<div class="course-item">
    <div>
      <div class="course-name">${c.name}${c.doppelt?'<span class="badge-doppelt">Doppelt wertvoll</span>':''}</div>
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
  el.innerHTML = courses.map(c => renderCourseItem(c, c.ecs)).join('') +
    (hint ? `<div class="sector-hint">⚠️ ${hint}</div>` : '');
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  renderECGrid();

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
