# Copilot Prompt — MBI Skills Widget für data2dollar Präsentation

## Kontext
HSG MBI Gruppenarbeit "Too HSG to Handle" — data2dollar (IC: From Data2Dollar).
Charakter: Lizzy, ETH CS Gründerin, analysiert ob das MBI sie auf ihre Gründung vorbereitet.
Wissenschaftliche Basis: Mai & Thai (2025), Journal of International Entrepreneurship —
Systematischer Review von 174 Papers zu Entrepreneurial Competencies (ECs).

---

## Aufgabe
Erstelle ein einzelnes interaktives HTML-Widget (kein React, kein Framework,
plain HTML + CSS + vanilla JS, alles in einer Datei).

Das Widget hat zwei Bereiche:

---

## BEREICH A — EC Self-Assessment

### Was es zeigt
12 EC-Domains aus Mai & Thai (2025) als klickbare Karten.
Lizzy bewertet sich selbst pro Domain: stark / okay / Lücke.
Basierend auf ihren Lücken erscheint darunter eine priorisierte Kursliste.

### Die 12 EC-Domains mit Anzahl MBI-Kurse (bilinguales DE+EN Matching)

| Domain | MBI-Kurse |
|--------|-----------|
| Opportunity | 3 |
| Strategic | 25 |
| Commitment | 25 |
| Analytical | 37 |
| Innovative | 22 |
| Human | 23 |
| Operational | 50 |
| Relationship | 47 |
| Learning | 54 |
| Personal Strength | 12 |
| Technical | 43 |
| Ethical | 12 |

### Kurse pro EC-Domain (bilingual DE+EN, sortiert nach Score)

EC: Opportunity
- Technology Entrepreneurship (3 ECTS | EN) — score: 1
- Business Innovation I: Geschäftsmodelle entwickeln (4 ECTS | DE) — score: 1
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 1

EC: Strategic
- Grundlagen Business Innovation (4 ECTS | DE) — score: 3
- Business Innovation I: Geschäftsmodelle entwickeln (4 ECTS | DE) — score: 3
- RPV: Digital Business and IT Innovations (4 ECTS | EN) — score: 3
- IT Management: Strategische Positionierung der IT in der (3 ECTS | DE) — score: 3
- Management von Verkehrsunternehmen (3 ECTS | DE) — score: 3
- Platform Economy (6 ECTS | EN) — score: 2
- FPV: Gestaltung Digitaler Produkte und Lösungen mit AI (4 ECTS | DE) — score: 2
- IT Management: Business/IT-Integration durch Enterprise (3 ECTS | DE) — score: 2
- Business Innovation II: Unternehmen gestalten und digital (4 ECTS | DE) — score: 2
- Quality Management for Superior Performance and Innovation (3 ECTS | EN) — score: 2
- Methods: Lean Venturing (3 ECTS | EN) — score: 2
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 2
- Introduction to Blockchain, DLT & Crypto (3 ECTS | EN) — score: 2
- FPV: Digitale Kommunikation und Geschäftsmodelle (4 ECTS | DE) — score: 1
- IC: Innovationen in Entwicklungsländern (4 ECTS | DE) — score: 1
- Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle (3 ECTS | DE) — score: 1
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 1
- Chancen und Gefahren des Unternehmenswachstums (3 ECTS | DE) — score: 1
- Methods: Integrated Business Planning with Certificate (3 ECTS | EN) — score: 1
- Selling Technology Solutions (3 ECTS | EN) — score: 1
- Corporate Venturing (3 ECTS | EN) — score: 1
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 1
- Digitalisierung in der Industrie: Smart Production und Services (3 ECTS | DE) — score: 1
- Corporate Venture Capital (3 ECTS | EN) — score: 1
- Community Management (3 ECTS | DE) — score: 1

EC: Commitment
- Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle (3 ECTS | DE) — score: 3
- Digitale Kommunikation und Content Management (3 ECTS | DE) — score: 3
- Digital Platforms: Foundations, Management, Governance (6 ECTS | EN) — score: 2
- Effective Data Communication - How to Talk about Data (3 ECTS | EN) — score: 2
- Behavioral Science & Technology (4 ECTS | EN) — score: 2
- Technology Entrepreneurship (3 ECTS | EN) — score: 1
- RPV: Venturing in Emerging Trends - Entrepreneurship and (4 ECTS | EN) — score: 1
- FPV: Digitale Kommunikation und Geschäftsmodelle (4 ECTS | DE) — score: 1
- IC: Innovationen in Entwicklungsländern (4 ECTS | DE) — score: 1
- FPV: Supply Chain Innovation (4 ECTS | DE) — score: 1
- RPV: Social Media Mining with NoSQL-Databases (4 ECTS | EN) — score: 1
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 1
- Sustainable Corporate Strategies and Solutions (3 ECTS | EN) — score: 1
- Change und Project Management (3 ECTS | DE) — score: 1
- Methoden: Agile und traditionelle Lösungsgestaltung für Business (3 ECTS | DE) — score: 1
- Selling Technology Solutions (3 ECTS | EN) — score: 1
- KI- und Technologie-Anwendungen im Supply Chain (3 ECTS | DE) — score: 1
- FPV: Psychologie der Innovationsprozesse (4 ECTS | DE) — score: 1
- Managing IT Security and Privacy in Organisations (3 ECTS | EN) — score: 1
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 1
- Cloud Computing für datengetriebene Geschäftsmodelle: (6 ECTS | DE) — score: 1
- Supply Chain Management I (3 ECTS | DE) — score: 1
- IT Management: Strategische Positionierung der IT in der (3 ECTS | DE) — score: 1
- Gestaltung und Management von Digital Channels und (3 ECTS | DE) — score: 1
- IC: Lean Product and Outsourcing Management (4 ECTS | EN) — score: 1

EC: Analytical
- FPV: Digitale und Datengetriebene Organisationen (4 ECTS | DE) — score: 3
- RPV: Social Media Mining with NoSQL-Databases (4 ECTS | EN) — score: 3
- Methoden: Data Science und AI for Business (6 ECTS | DE) — score: 3
- IC: Gesellschaftliche Aspekte der Digitalisierung (4 ECTS | DE) — score: 3
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) — score: 3
- Methods: Supply Chain and Operations Management (3 ECTS | EN) — score: 3
- Behavioral Science & Technology (4 ECTS | EN) — score: 3
- User-Centred Design (6 ECTS | EN) — score: 3
- IC: Lean Product and Outsourcing Management (4 ECTS | EN) — score: 3
- Forschungsmethoden für Geschäftsinnovation (3 ECTS | DE) — score: 2
- Platform Economy (6 ECTS | EN) — score: 2
- Sustainable Innovation through Human-centered Design (3 ECTS | EN) — score: 2
- Managing Behavioral Visibility (3 ECTS | EN) — score: 2
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 2
- Entrepreneurial Finance (3 ECTS | EN) — score: 2
- Business Process Mining and Engineering (6 ECTS | EN) — score: 2
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) — score: 2
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 2
- Cloud Computing für datengetriebene Geschäftsmodelle: (6 ECTS | DE) — score: 2
- Mobile Sensing and Behavioral Metrics (6 ECTS | EN) — score: 2
- Turning Geographic Information into Business Insights (6 ECTS | EN) — score: 2
- Software Assessment: From Planning to Experimentation (6 ECTS | EN) — score: 2
- FPV: Supply Chain Innovation (4 ECTS | DE) — score: 1
- Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle (3 ECTS | DE) — score: 1
- Corporate Venturing (3 ECTS | EN) — score: 1
- IT Management: Business/IT-Integration durch Enterprise (3 ECTS | DE) — score: 1
- IC: From Data2Dollar - Dein Technologiekoffer von der (4 ECTS | DE) — score: 1
- Managing IT Security and Privacy in Organisations (3 ECTS | EN) — score: 1
- Tech Investing  (3 ECTS | EN) — score: 1
- Methods: Scalable Tech Stacks for Business Ideas (3 ECTS | EN) — score: 1
- Supply Chain Management I (3 ECTS | DE) — score: 1
- Methods: Lean Venturing (3 ECTS | EN) — score: 1
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 1
- Effective Data Communication - How to Talk about Data (3 ECTS | EN) — score: 1
- Gestaltung und Management von Digital Channels und (3 ECTS | DE) — score: 1
- Corporate Venture Capital (3 ECTS | EN) — score: 1
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 1

EC: Innovative
- Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle (3 ECTS | DE) — score: 3
- FPV: Design Thinking für Digital Innovation (4 ECTS | DE) — score: 3
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 3
- Agentic AI Design, Governance and Management (6 ECTS | EN) — score: 3
- Business Innovation I: Geschäftsmodelle entwickeln (4 ECTS | DE) — score: 3
- Business Innovation II: Unternehmen gestalten und digital (4 ECTS | DE) — score: 3
- FPV: Design Thinking mit KI (4 ECTS | DE) — score: 3
- RPV: Venturing in Emerging Trends - Entrepreneurship and (4 ECTS | EN) — score: 2
- Sustainable Innovation through Human-centered Design (3 ECTS | EN) — score: 2
- IC: Lean Product and Outsourcing Management (4 ECTS | EN) — score: 2
- Community Management (3 ECTS | DE) — score: 2
- Forschungsmethoden für Geschäftsinnovation (3 ECTS | DE) — score: 1
- Platform Economy (6 ECTS | EN) — score: 1
- FPV: Gestaltung Digitaler Produkte und Lösungen mit AI (4 ECTS | DE) — score: 1
- FPV: Gestaltung und Entwicklung von User Interfaces (4 ECTS | DE) — score: 1
- Methods: Business Knowledge Visualisation (3 ECTS | EN) — score: 1
- IC: Agile Transformation und Arbeitsprinzipien (4 ECTS | DE) — score: 1
- Grundlagen Business Innovation (4 ECTS | DE) — score: 1
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 1
- Methods: Scalable Tech Stacks for Business Ideas (3 ECTS | EN) — score: 1
- Mobile Sensing and Behavioral Metrics (6 ECTS | EN) — score: 1
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 1

EC: Human
- FPV: Design Thinking für Digital Innovation (4 ECTS | DE) — score: 3
- Chancen und Gefahren des Unternehmenswachstums (3 ECTS | DE) — score: 3
- High-Growth Entrepreneurship: An International Applied Perspective (4 ECTS | EN) — score: 3
- IC: Strategic Management of New Technologies in Companies (4 ECTS | EN) — score: 3
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 3
- FPV: Digitale Kommunikation und Geschäftsmodelle (4 ECTS | DE) — score: 2
- Change und Project Management (3 ECTS | DE) — score: 2
- Corporate Transformation - An Integrative Perspective (3 ECTS | EN) — score: 2
- Business Innovation I: Geschäftsmodelle entwickeln (4 ECTS | DE) — score: 2
- FPV: Psychologie der Innovationsprozesse (4 ECTS | DE) — score: 2
- Managing IT Security and Privacy in Organisations (3 ECTS | EN) — score: 2
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 2
- Tech Investing  (3 ECTS | EN) — score: 2
- Methods: Lean Venturing (3 ECTS | EN) — score: 2
- Community Management (3 ECTS | DE) — score: 2
- Technology Entrepreneurship (3 ECTS | EN) — score: 1
- RPV: Venturing in Emerging Trends - Entrepreneurship and (4 ECTS | EN) — score: 1
- FPV: Gestaltung Digitaler Produkte und Lösungen mit AI (4 ECTS | DE) — score: 1
- Business Process Mining and Engineering (6 ECTS | EN) — score: 1
- RPV: Low Code Development Platforms (4 ECTS | EN) — score: 1
- Gestaltung und Management von Digital Channels und (3 ECTS | DE) — score: 1
- FPV: Design Thinking mit KI (4 ECTS | DE) — score: 1
- FPV: Circular Economy - Optimierung im Supply Chain (4 ECTS | DE) — score: 1

EC: Operational
- Technology Entrepreneurship (3 ECTS | EN) — score: 3
- FPV: Digitale und Datengetriebene Organisationen (4 ECTS | DE) — score: 3
- FPV: Supply Chain Innovation (4 ECTS | DE) — score: 3
- Change und Project Management (3 ECTS | DE) — score: 3
- Corporate Transformation - An Integrative Perspective (3 ECTS | EN) — score: 3
- Chancen und Gefahren des Unternehmenswachstums (3 ECTS | DE) — score: 3
- Methods: Integrated Business Planning with Certificate (3 ECTS | EN) — score: 3
- Agentic AI Design, Governance and Management (6 ECTS | EN) — score: 3
- Methoden: Agile und traditionelle Lösungsgestaltung für Business (3 ECTS | DE) — score: 3
- KI- und Technologie-Anwendungen im Supply Chain (3 ECTS | DE) — score: 3
- Business Process Mining and Engineering (6 ECTS | EN) — score: 3
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) — score: 3
- IC: Agile Transformation und Arbeitsprinzipien (4 ECTS | DE) — score: 3
- Grundlagen Business Innovation (4 ECTS | DE) — score: 3
- RPV: Low Code Development Platforms (4 ECTS | EN) — score: 3
- IC: Strategic Management of New Technologies in Companies (4 ECTS | EN) — score: 3
- Introduction to Business Process Management (3 ECTS | EN) — score: 3
- RPV: Digital Business and IT Innovations (4 ECTS | EN) — score: 3
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 3
- Supply Chain Management I (3 ECTS | DE) — score: 3
- Methods: Supply Chain and Operations Management (3 ECTS | EN) — score: 3
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 3
- Management von Verkehrsunternehmen (3 ECTS | DE) — score: 3
- Software Assessment: From Planning to Experimentation (6 ECTS | EN) — score: 3
- IC: Lean Product and Outsourcing Management (4 ECTS | EN) — score: 3
- Leveraging AI for Healthcare (6 ECTS | EN) — score: 2
- Corporate Venturing (3 ECTS | EN) — score: 2
- High-Growth Entrepreneurship: An International Applied Perspective (4 ECTS | EN) — score: 2
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) — score: 2
- FPV: Psychologie der Innovationsprozesse (4 ECTS | DE) — score: 2
- Methods: Scalable Tech Stacks for Business Ideas (3 ECTS | EN) — score: 2
- Quality Management for Superior Performance and Innovation (3 ECTS | EN) — score: 2
- Corporate Venture Capital (3 ECTS | EN) — score: 2
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 2
- User-Centred Design (6 ECTS | EN) — score: 2
- Methoden: Data Science und AI for Business (6 ECTS | DE) — score: 1
- FPV: Gestaltung und Entwicklung von User Interfaces (4 ECTS | DE) — score: 1
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 1
- Entrepreneurial Finance (3 ECTS | EN) — score: 1
- Selling Technology Solutions (3 ECTS | EN) — score: 1
- IC: Gesellschaftliche Aspekte der Digitalisierung (4 ECTS | DE) — score: 1
- IC: From Data2Dollar - Dein Technologiekoffer von der (4 ECTS | DE) — score: 1
- Business Innovation I: Geschäftsmodelle entwickeln (4 ECTS | DE) — score: 1
- R & D Management (3 ECTS | EN) — score: 1
- Managing IT Security and Privacy in Organisations (3 ECTS | EN) — score: 1
- Operative Excellence (OPEX) (3 ECTS | EN) — score: 1
- Methods: Lean Venturing (3 ECTS | EN) — score: 1
- Turning Geographic Information into Business Insights (6 ECTS | EN) — score: 1
- FPV: Circular Economy - Optimierung im Supply Chain (4 ECTS | DE) — score: 1
- Community Management (3 ECTS | DE) — score: 1

EC: Relationship
- FPV: Digitale Kommunikation und Geschäftsmodelle (4 ECTS | DE) — score: 3
- FPV: Supply Chain Innovation (4 ECTS | DE) — score: 3
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 3
- Digitale Kommunikation und Content Management (3 ECTS | DE) — score: 3
- Change und Project Management (3 ECTS | DE) — score: 3
- Methods: Social Network Analysis - a Systematic and Quantifying (3 ECTS | EN) — score: 3
- Selling Technology Solutions (3 ECTS | EN) — score: 3
- Corporate Venturing (3 ECTS | EN) — score: 3
- Digital Platforms: Foundations, Management, Governance (6 ECTS | EN) — score: 3
- Grundlagen Business Innovation (4 ECTS | DE) — score: 3
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) — score: 3
- IC: Strategic Management of New Technologies in Companies (4 ECTS | EN) — score: 3
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 3
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 3
- Effective Data Communication - How to Talk about Data (3 ECTS | EN) — score: 3
- Gestaltung und Management von Digital Channels und (3 ECTS | DE) — score: 3
- Corporate Venture Capital (3 ECTS | EN) — score: 3
- Community Management (3 ECTS | DE) — score: 3
- Technology Entrepreneurship (3 ECTS | EN) — score: 2
- Leveraging AI for Healthcare (6 ECTS | EN) — score: 2
- Methods: Business Knowledge Visualisation (3 ECTS | EN) — score: 2
- Chancen und Gefahren des Unternehmenswachstums (3 ECTS | DE) — score: 2
- Methoden: Web, Social und Mobile Analytics (3 ECTS | DE) — score: 2
- Methods: Supply Chain and Operations Management (3 ECTS | EN) — score: 2
- Mobile Sensing and Behavioral Metrics (6 ECTS | EN) — score: 2
- RPV: Venturing in Emerging Trends - Entrepreneurship and (4 ECTS | EN) — score: 1
- Methoden: Data Science und AI for Business (6 ECTS | DE) — score: 1
- Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle (3 ECTS | DE) — score: 1
- Managing Behavioral Visibility (3 ECTS | EN) — score: 1
- Corporate Transformation - An Integrative Perspective (3 ECTS | EN) — score: 1
- Methods: Integrated Business Planning with Certificate (3 ECTS | EN) — score: 1
- Entrepreneurial Finance (3 ECTS | EN) — score: 1
- Agentic AI Design, Governance and Management (6 ECTS | EN) — score: 1
- Methoden: Agile und traditionelle Lösungsgestaltung für Business (3 ECTS | DE) — score: 1
- IT Management: Business/IT-Integration durch Enterprise (3 ECTS | DE) — score: 1
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) — score: 1
- IC: Agile Transformation und Arbeitsprinzipien (4 ECTS | DE) — score: 1
- FPV: Psychologie der Innovationsprozesse (4 ECTS | DE) — score: 1
- R & D Management (3 ECTS | EN) — score: 1
- RPV: Digital Business and IT Innovations (4 ECTS | EN) — score: 1
- Quality Management for Superior Performance and Innovation (3 ECTS | EN) — score: 1
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 1
- Ubiquitous Computing (3 ECTS | EN) — score: 1
- FPV: Design Thinking mit KI (4 ECTS | DE) — score: 1
- RPV: Aviation and Space Industry (4 ECTS | EN) — score: 1
- IC: Lean Product and Outsourcing Management (4 ECTS | EN) — score: 1
- FPV: Circular Economy - Optimierung im Supply Chain (4 ECTS | DE) — score: 1

EC: Learning
- IC: Innovationen in Entwicklungsländern (4 ECTS | DE) — score: 3
- FPV: Supply Chain Innovation (4 ECTS | DE) — score: 3
- Methoden: Data Science und AI for Business (6 ECTS | DE) — score: 3
- Leveraging AI for Healthcare (6 ECTS | EN) — score: 3
- FPV: Design Thinking für Digital Innovation (4 ECTS | DE) — score: 3
- Digitale Kommunikation und Content Management (3 ECTS | DE) — score: 3
- Entrepreneurial Finance (3 ECTS | EN) — score: 3
- FPV: Psychologie der Innovationsprozesse (4 ECTS | DE) — score: 3
- RPV: Low Code Development Platforms (4 ECTS | EN) — score: 3
- Introduction to Business Process Management (3 ECTS | EN) — score: 3
- Operative Excellence (OPEX) (3 ECTS | EN) — score: 3
- Digitalisierung in der Industrie: Smart Production und Services (3 ECTS | DE) — score: 3
- Methods: Supply Chain and Operations Management (3 ECTS | EN) — score: 3
- User-Centred Design (6 ECTS | EN) — score: 3
- Software Assessment: From Planning to Experimentation (6 ECTS | EN) — score: 3
- Ubiquitous Computing (3 ECTS | EN) — score: 3
- IC: Lean Product and Outsourcing Management (4 ECTS | EN) — score: 3
- Chancen und Gefahren des Unternehmenswachstums (3 ECTS | DE) — score: 2
- Methods: Social Network Analysis - a Systematic and Quantifying (3 ECTS | EN) — score: 2
- KI- und Technologie-Anwendungen im Supply Chain (3 ECTS | DE) — score: 2
- Digital Platforms: Foundations, Management, Governance (6 ECTS | EN) — score: 2
- Business Innovation I: Geschäftsmodelle entwickeln (4 ECTS | DE) — score: 2
- RPV: Digital Business and IT Innovations (4 ECTS | EN) — score: 2
- FPV: Design Thinking mit KI (4 ECTS | DE) — score: 2
- Introduction to Blockchain, DLT & Crypto (3 ECTS | EN) — score: 2
- Platform Economy (6 ECTS | EN) — score: 1
- RPV: Venturing in Emerging Trends - Entrepreneurship and (4 ECTS | EN) — score: 1
- FPV: Digitale und Datengetriebene Organisationen (4 ECTS | DE) — score: 1
- FPV: Gestaltung Digitaler Produkte und Lösungen mit AI (4 ECTS | DE) — score: 1
- Methoden: Prototyping von Produkten, Dienstleistungen und Geschäftsmodelle (3 ECTS | DE) — score: 1
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 1
- Methods: Business Knowledge Visualisation (3 ECTS | EN) — score: 1
- Sustainable Corporate Strategies and Solutions (3 ECTS | EN) — score: 1
- Corporate Transformation - An Integrative Perspective (3 ECTS | EN) — score: 1
- Corporate Venturing (3 ECTS | EN) — score: 1
- IC: Gesellschaftliche Aspekte der Digitalisierung (4 ECTS | DE) — score: 1
- IC: From Data2Dollar - Dein Technologiekoffer von der (4 ECTS | DE) — score: 1
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) — score: 1
- High-Growth Entrepreneurship: An International Applied Perspective (4 ECTS | EN) — score: 1
- IC: Agile Transformation und Arbeitsprinzipien (4 ECTS | DE) — score: 1
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) — score: 1
- IC: Strategic Management of New Technologies in Companies (4 ECTS | EN) — score: 1
- Managing IT Security and Privacy in Organisations (3 ECTS | EN) — score: 1
- Tech Investing  (3 ECTS | EN) — score: 1
- Methods: Scalable Tech Stacks for Business Ideas (3 ECTS | EN) — score: 1
- Supply Chain Management I (3 ECTS | DE) — score: 1
- IT Management: Strategische Positionierung der IT in der (3 ECTS | DE) — score: 1
- Quality Management for Superior Performance and Innovation (3 ECTS | EN) — score: 1
- Methods: Lean Venturing (3 ECTS | EN) — score: 1
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 1
- Corporate Venture Capital (3 ECTS | EN) — score: 1
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 1
- FPV: Circular Economy - Optimierung im Supply Chain (4 ECTS | DE) — score: 1
- Introduction to Software Engineering (6 ECTS | EN) — score: 1

EC: Personal Strength
- Technology Entrepreneurship (3 ECTS | EN) — score: 2
- FPV: Data Science und AI for Business (4 ECTS | DE) — score: 2
- IC: Gesellschaftliche Aspekte der Digitalisierung (4 ECTS | DE) — score: 2
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) — score: 2
- Effective Data Communication - How to Talk about Data (3 ECTS | EN) — score: 2
- RPV: Venturing in Emerging Trends - Entrepreneurship and (4 ECTS | EN) — score: 1
- IC: From Data2Dollar - Dein Technologiekoffer von der (4 ECTS | DE) — score: 1
- Digital Platforms: Foundations, Management, Governance (6 ECTS | EN) — score: 1
- IC: Strategic Management of New Technologies in Companies (4 ECTS | EN) — score: 1
- R & D Management (3 ECTS | EN) — score: 1
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) — score: 1
- Behavioral Science & Technology (4 ECTS | EN) — score: 1

EC: Technical
- Technology Entrepreneurship (3 ECTS | EN) — score: 3
- Change und Project Management (3 ECTS | DE) — score: 3
- Agentic AI Design, Governance and Management (6 ECTS | EN) — score: 3
- Methoden: Agile und traditionelle Lösungsgestaltung für Business (3 ECTS | DE) — score: 3
- Selling Technology Solutions (3 ECTS | EN) — score: 3
- IT Management: Business/IT-Integration durch Enterprise (3 ECTS | DE) — score: 3
- Business Process Mining and Engineering (6 ECTS | EN) — score: 3
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) — score: 3
- Digital Platforms: Foundations, Management, Governance (6 ECTS | EN) — score: 3
- High-Growth Entrepreneurship: An International Applied Perspective (4 ECTS | EN) — score: 3
- Grundlagen Business Innovation (4 ECTS | DE) — score: 3
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) — score: 3
- Cloud Computing für datengetriebene Geschäftsmodelle: (6 ECTS | DE) — score: 3
- Methods: Scalable Tech Stacks for Business Ideas (3 ECTS | EN) — score: 3
- Asia Compact: Fintech Innovation in Singapore and Southeast (3 ECTS | EN) — score: 3
- Turning Geographic Information into Business Insights (6 ECTS | EN) — score: 3
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 3
- Behavioral Science & Technology (4 ECTS | EN) — score: 3
- Software Assessment: From Planning to Experimentation (6 ECTS | EN) — score: 3
- Ubiquitous Computing (3 ECTS | EN) — score: 3
- RPV: Aviation and Space Industry (4 ECTS | EN) — score: 3
- Introduction to Blockchain, DLT & Crypto (3 ECTS | EN) — score: 3
- Introduction to Software Engineering (6 ECTS | EN) — score: 3
- RPV: Social Media Mining with NoSQL-Databases (4 ECTS | EN) — score: 2
- Leveraging AI for Healthcare (6 ECTS | EN) — score: 2
- FPV: Gestaltung und Entwicklung von User Interfaces (4 ECTS | DE) — score: 2
- IC: From Data2Dollar - Dein Technologiekoffer von der (4 ECTS | DE) — score: 2
- Tech Investing  (3 ECTS | EN) — score: 2
- Methoden: Web, Social und Mobile Analytics (3 ECTS | DE) — score: 2
- Community Management (3 ECTS | DE) — score: 2
- FPV: Digitale und Datengetriebene Organisationen (4 ECTS | DE) — score: 1
- Corporate Transformation - An Integrative Perspective (3 ECTS | EN) — score: 1
- Corporate Venturing (3 ECTS | EN) — score: 1
- IC: Agile Transformation und Arbeitsprinzipien (4 ECTS | DE) — score: 1
- Business Innovation II: Unternehmen gestalten und digital (4 ECTS | DE) — score: 1
- IC: Strategic Management of New Technologies in Companies (4 ECTS | EN) — score: 1
- Introduction to Business Process Management (3 ECTS | EN) — score: 1
- RPV: Digital Business and IT Innovations (4 ECTS | EN) — score: 1
- Operative Excellence (OPEX) (3 ECTS | EN) — score: 1
- Gestaltung und Management von Digital Channels und (3 ECTS | DE) — score: 1
- Corporate Venture Capital (3 ECTS | EN) — score: 1
- User-Centred Design (6 ECTS | EN) — score: 1
- FPV: Design Thinking mit KI (4 ECTS | DE) — score: 1

EC: Ethical
- Agentic AI Design, Governance and Management (6 ECTS | EN) — score: 3
- KI- und Technologie-Anwendungen im Supply Chain (3 ECTS | DE) — score: 3
- Digital Platforms: Foundations, Management, Governance (6 ECTS | EN) — score: 3
- Managing IT Security and Privacy in Organisations (3 ECTS | EN) — score: 3
- IC: Responsible Innovation Lab (4 ECTS | EN) — score: 3
- Operative Excellence (OPEX) (3 ECTS | EN) — score: 2
- Supply Chain Management I (3 ECTS | DE) — score: 2
- Project Leadership für Business Innovation (3 ECTS | DE) — score: 2
- Introduction to Blockchain, DLT & Crypto (3 ECTS | EN) — score: 2
- FPV: Supply Chain Innovation (4 ECTS | DE) — score: 1
- Selling Technology Solutions (3 ECTS | EN) — score: 1
- Business Process Mining and Engineering (6 ECTS | EN) — score: 1

---

## BEREICH B — Sektor-Kurse

### Was es zeigt
Lizzy wählt ihren Zielsektor. Es erscheinen die relevanten Kurse
für diesen Sektor, mit Hinweis ob der Kurs auch EC-Kompetenzen trainiert
(Label: "Doppelt wertvoll").

### Kurse pro Sektor (bilingual DE+EN)

Sektor: GenAI (12 Kurse)
- FPV: Digitale Kommunikation und Geschäftsmodelle (4 ECTS | DE) | EC: Strategic, Commitment, Human, Relationship | score: 3 | DOPPELT WERTVOLL
- Methoden: Data Science und AI for Business (6 ECTS | DE) | EC: Analytical, Operational, Relationship, Learning | score: 3 | DOPPELT WERTVOLL
- IC: From Data2Dollar - Dein Technologiekoffer von der (4 ECTS | DE) | EC: Analytical, Operational, Learning, Personal Strength, Technical | score: 3 | DOPPELT WERTVOLL
- RPV: Prompt Engineering: Innovation through generative AI (4 ECTS | EN) | EC: Analytical, Operational, Relationship, Learning, Personal Strength, Technical | score: 3 | DOPPELT WERTVOLL
- FPV: Gestaltung Digitaler Produkte und Lösungen mit AI (4 ECTS | DE) | EC: Strategic, Innovative, Human, Learning | score: 2 | DOPPELT WERTVOLL
- FPV: Data Science und AI for Business (4 ECTS | DE) | EC: Strategic, Commitment, Analytical, Innovative, Operational, Relationship, Learning, Personal Strength | score: 2 | DOPPELT WERTVOLL
- Selling Technology Solutions (3 ECTS | EN) | EC: Strategic, Commitment, Operational, Relationship, Technical, Ethical | score: 2 | DOPPELT WERTVOLL
- Business Process Mining and Engineering (6 ECTS | EN) | EC: Analytical, Human, Operational, Technical, Ethical | score: 2 | DOPPELT WERTVOLL
- FPV: Gestaltung und Entwicklung von User Interfaces (4 ECTS | DE) | EC: Innovative, Operational, Technical | score: 1 | DOPPELT WERTVOLL
- Methods: Social Network Analysis - a Systematic and Quantifying (3 ECTS | EN) | EC: Relationship, Learning | score: 1 | DOPPELT WERTVOLL
- IC: Gesellschaftliche Aspekte der Digitalisierung (4 ECTS | DE) | EC: Analytical, Operational, Learning, Personal Strength | score: 1 | DOPPELT WERTVOLL
- Cloud Computing für datengetriebene Geschäftsmodelle: (6 ECTS | DE) | EC: Commitment, Analytical, Technical | score: 1 | DOPPELT WERTVOLL

Sektor: HealthTech (4 Kurse)
- Leveraging AI for Healthcare (6 ECTS | EN) | EC: Operational, Relationship, Learning, Technical | score: 3 | DOPPELT WERTVOLL
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) | EC: Analytical, Operational, Relationship, Learning, Technical | score: 3 | DOPPELT WERTVOLL
- IC: Aktuelle Managementfragestellungen im Schweizer (4 ECTS | DE) | EC: Opportunity, Strategic, Commitment, Analytical, Innovative, Human, Operational, Relationship, Personal Strength | score: 2 | DOPPELT WERTVOLL
- Mobile Sensing and Behavioral Metrics (6 ECTS | EN) | EC: Analytical, Innovative, Relationship | score: 2 | DOPPELT WERTVOLL

Sektor: MedTech (1 Kurse)
- Business Process Mining and Engineering (6 ECTS | EN) | EC: Analytical, Human, Operational, Technical, Ethical | score: 2 | DOPPELT WERTVOLL
- HINWEIS: MedTech kaum im MBI-Curriculum abgedeckt. Externe Ressourcen nötig: Swiss Medtech Cluster, EPFL, FDA/CE-Mark Grundlagen.

Sektor: BioTech (1 Kurse)
- RPV: Aviation and Space Industry (4 ECTS | EN) | EC: Relationship, Technical | score: 3 | DOPPELT WERTVOLL
- HINWEIS: BioTech nicht im MBI-Curriculum. Externe Ressourcen: Swiss Biotech Association, ETH Life Sciences, Basel Biovalley.

Sektor: Robotics (3 Kurse)
- KI- und Technologie-Anwendungen im Supply Chain (3 ECTS | DE) | EC: Commitment, Operational, Learning, Ethical | score: 3 | DOPPELT WERTVOLL
- Evaluating Innovation in Companies and at System Level (3 ECTS | EN) | EC: Analytical, Operational, Relationship, Learning, Technical | score: 2 | DOPPELT WERTVOLL
- Methoden: Data Science und AI for Business (6 ECTS | DE) | EC: Analytical, Operational, Relationship, Learning | score: 1 | DOPPELT WERTVOLL
- HINWEIS: Robotics kaum im MBI-Curriculum. Externe Ressourcen: ETH Robotics, Swiss Innovation Park.

---

## UI-Anforderungen

### Layout
- Einzelne HTML-Datei, kein externes Framework
- Zwei Sektionen klar getrennt: "EC Self-Assessment" oben, "Sektor-Kurse" unten
- Responsiv, funktioniert auf Laptop-Bildschirm für Präsentation

### BEREICH A — EC Self-Assessment
- 12 klickbare Karten, je eine pro EC-Domain
- Jede Karte zeigt: Domain-Name und Anzahl MBI-Kurse
- 3 Zustände pro Karte: neutral (noch nicht bewertet) / stark (grün) / Lücke (orange)
- Alle 12 Karten optisch gleich — keine Hervorhebungen
- Darunter: dynamische Kursliste — zeigt nur Kurse für Domains die als "Lücke" markiert
- Kursliste sortiert nach score DESC, zeigt Kursname + ECTS + Sprache + betroffene EC-Domains

### BEREICH B — Sektor-Kurse
- 5 Tabs: GenAI / HealthTech / MedTech / BioTech / Robotics
- Pro Sektor: Kursliste mit Kursname, ECTS, Sprache, EC-Domains, "Doppelt wertvoll"-Badge
- Für MedTech/BioTech/Robotics: Hinweis-Box "Lücke im Curriculum"

### Styling
- Farben: akademisch, ruhig — kein buntes Pop-Color-Schema
- Lücke-Zustand: orange/amber
- Stark-Zustand: grün/teal
- "Doppelt wertvoll" Badge: blau
- Schrift: System-Font, gut lesbar bei Präsentation auf Beamer

---

## Datengrundlage
Alle Scores basieren auf bilingualen DE+EN Keyword-Matching (Scoring 0–3, gekappt bei 3).
Quelle: mbi_ec_sector_matrix_bilingual.csv (84 Kurse x 24 Spalten)

---

## Wichtige Botschaft die visuell klar werden muss
"Das MBI deckt viele Gründer-Kompetenzen gut ab — aber Opportunity Recognition
und Personal Strength (Pitching) sind kritische Lücken. Genau diese zwei Domains
sind laut Mai & Thai (2025) am wichtigsten für Startup-Erfolg."

Quelle: Mai & Thai (2025), Journal of International Entrepreneurship, Vol. 23(1), S. 54–130
DOI: 10.1007/s10843-024-00356-7