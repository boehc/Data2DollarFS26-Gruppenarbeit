/*
  Trend-Visualisierung - Script (VERBESSERT)
  Automatisch generiert von prepare_trend_data.py
  Quartalweise Keyword-Trends mit normalisierte Werten (keyword_pct)
*/

// Eingebettete Trenddaten
const trendData = {
  "metadata": {
    "generated": "2026-04-14T19:25:39.860369",
    "total_keywords": 28,
    "quarters_count": 13,
    "metric": "keyword_pct (normalisiert, %)",
    "date_range": {
      "from": "2023-Q1",
      "to": "2026-Q1"
    }
  },
  "data": [
    {
      "keyword": "AgentAI",
      "quarter": "2023-Q1",
      "keyword_pct": 6.9,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Web3",
      "quarter": "2023-Q1",
      "keyword_pct": 6.58,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2023-Q1",
      "keyword_pct": 1.85,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2023-Q1",
      "keyword_pct": 2.77,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Robotics",
      "quarter": "2023-Q1",
      "keyword_pct": 3.44,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2023-Q1",
      "keyword_pct": 0.9,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "PropTech",
      "quarter": "2023-Q1",
      "keyword_pct": 0.5,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2023-Q1",
      "keyword_pct": 0.7,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "MedTech",
      "quarter": "2023-Q1",
      "keyword_pct": 0.6,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "LLM",
      "quarter": "2023-Q1",
      "keyword_pct": 6.3,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2023-Q1",
      "keyword_pct": 3.08,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "HealthTech",
      "quarter": "2023-Q1",
      "keyword_pct": 1.87,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2023-Q1",
      "keyword_pct": 0.45,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "GameTech",
      "quarter": "2023-Q1",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "GenAI",
      "quarter": "2023-Q1",
      "keyword_pct": 11.02,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2023-Q1",
      "keyword_pct": 1.13,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "ComputerVision",
      "quarter": "2023-Q1",
      "keyword_pct": 0.65,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2023-Q1",
      "keyword_pct": 0.5,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2023-Q1",
      "keyword_pct": 5.08,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "BioTech",
      "quarter": "2023-Q1",
      "keyword_pct": 0.45,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2023-Q1",
      "keyword_pct": 0.57,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2023-Q1",
      "keyword_pct": 1.27,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "Enterprise",
      "quarter": "2023-Q1",
      "keyword_pct": 0.8,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "FinTech",
      "quarter": "2023-Q1",
      "keyword_pct": 5.63,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2023-Q1",
      "keyword_pct": 1.4,
      "year": 2023,
      "quarter_num": 1
    },
    {
      "keyword": "HealthTech",
      "quarter": "2023-Q2",
      "keyword_pct": 1.97,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "Web3",
      "quarter": "2023-Q2",
      "keyword_pct": 5.26,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2023-Q2",
      "keyword_pct": 4.13,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "Robotics",
      "quarter": "2023-Q2",
      "keyword_pct": 3.0,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.85,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "MedTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "LLM",
      "quarter": "2023-Q2",
      "keyword_pct": 9.18,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2023-Q2",
      "keyword_pct": 1.87,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "GenAI",
      "quarter": "2023-Q2",
      "keyword_pct": 15.12,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "PropTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "EdTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "AgriTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "BioTech",
      "quarter": "2023-Q2",
      "keyword_pct": 0.57,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2023-Q2",
      "keyword_pct": 1.73,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "ComputerVision",
      "quarter": "2023-Q2",
      "keyword_pct": 0.85,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "AgentAI",
      "quarter": "2023-Q2",
      "keyword_pct": 1.67,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "FinTech",
      "quarter": "2023-Q2",
      "keyword_pct": 3.83,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2023-Q2",
      "keyword_pct": 6.03,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2023-Q2",
      "keyword_pct": 1.0,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2023-Q2",
      "keyword_pct": 1.3,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2023-Q2",
      "keyword_pct": 1.3,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2023-Q2",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 2
    },
    {
      "keyword": "HealthTech",
      "quarter": "2023-Q3",
      "keyword_pct": 2.25,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2023-Q3",
      "keyword_pct": 1.73,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "LLM",
      "quarter": "2023-Q3",
      "keyword_pct": 8.27,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2023-Q3",
      "keyword_pct": 1.1,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Web3",
      "quarter": "2023-Q3",
      "keyword_pct": 6.1,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.9,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2023-Q3",
      "keyword_pct": 3.9,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "HRTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "PropTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Robotics",
      "quarter": "2023-Q3",
      "keyword_pct": 3.47,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "GenAI",
      "quarter": "2023-Q3",
      "keyword_pct": 13.3,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "FinTech",
      "quarter": "2023-Q3",
      "keyword_pct": 4.47,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "GameTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "AgentAI",
      "quarter": "2023-Q3",
      "keyword_pct": 1.3,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "AgriTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "BioTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.65,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2023-Q3",
      "keyword_pct": 1.68,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2023-Q3",
      "keyword_pct": 1.0,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2023-Q3",
      "keyword_pct": 0.65,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "EdTech",
      "quarter": "2023-Q3",
      "keyword_pct": 0.9,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Enterprise",
      "quarter": "2023-Q3",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2023-Q3",
      "keyword_pct": 7.1,
      "year": 2023,
      "quarter_num": 3
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.75,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2023-Q4",
      "keyword_pct": 1.1,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "LLM",
      "quarter": "2023-Q4",
      "keyword_pct": 7.68,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "MedTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.45,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2023-Q4",
      "keyword_pct": 1.17,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "HealthTech",
      "quarter": "2023-Q4",
      "keyword_pct": 2.67,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.63,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Robotics",
      "quarter": "2023-Q4",
      "keyword_pct": 3.77,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2023-Q4",
      "keyword_pct": 4.57,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.5,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Web3",
      "quarter": "2023-Q4",
      "keyword_pct": 4.16,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "PropTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "GenAI",
      "quarter": "2023-Q4",
      "keyword_pct": 16.87,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "BioTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.9,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "FinTech",
      "quarter": "2023-Q4",
      "keyword_pct": 3.23,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "GameTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "AgriTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.5,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2023-Q4",
      "keyword_pct": 2.7,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "ComputerVision",
      "quarter": "2023-Q4",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2023-Q4",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "AgentAI",
      "quarter": "2023-Q4",
      "keyword_pct": 0.7,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2023-Q4",
      "keyword_pct": 2.17,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2023-Q4",
      "keyword_pct": 0.5,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2023-Q4",
      "keyword_pct": 1.1,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "EdTech",
      "quarter": "2023-Q4",
      "keyword_pct": 0.4,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2023-Q4",
      "keyword_pct": 7.4,
      "year": 2023,
      "quarter_num": 4
    },
    {
      "keyword": "Web3",
      "quarter": "2024-Q1",
      "keyword_pct": 4.93,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "HealthTech",
      "quarter": "2024-Q1",
      "keyword_pct": 1.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2024-Q1",
      "keyword_pct": 2.4,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "Robotics",
      "quarter": "2024-Q1",
      "keyword_pct": 5.17,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2024-Q1",
      "keyword_pct": 1.35,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "PropTech",
      "quarter": "2024-Q1",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2024-Q1",
      "keyword_pct": 0.5,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "MedTech",
      "quarter": "2024-Q1",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "LLM",
      "quarter": "2024-Q1",
      "keyword_pct": 7.92,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2024-Q1",
      "keyword_pct": 1.27,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "GenAI",
      "quarter": "2024-Q1",
      "keyword_pct": 16.8,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2024-Q1",
      "keyword_pct": 4.16,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "FinTech",
      "quarter": "2024-Q1",
      "keyword_pct": 3.9,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "BioTech",
      "quarter": "2024-Q1",
      "keyword_pct": 1.07,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2024-Q1",
      "keyword_pct": 1.1,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "ComputerVision",
      "quarter": "2024-Q1",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2024-Q1",
      "keyword_pct": 1.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "AgentAI",
      "quarter": "2024-Q1",
      "keyword_pct": 1.4,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2024-Q1",
      "keyword_pct": 1.0,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2024-Q1",
      "keyword_pct": 0.55,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "EdTech",
      "quarter": "2024-Q1",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "Enterprise",
      "quarter": "2024-Q1",
      "keyword_pct": 0.55,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2024-Q1",
      "keyword_pct": 2.67,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "GameTech",
      "quarter": "2024-Q1",
      "keyword_pct": 1.6,
      "year": 2024,
      "quarter_num": 1
    },
    {
      "keyword": "HealthTech",
      "quarter": "2024-Q2",
      "keyword_pct": 2.42,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "Web3",
      "quarter": "2024-Q2",
      "keyword_pct": 2.62,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2024-Q2",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2024-Q2",
      "keyword_pct": 5.75,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "Robotics",
      "quarter": "2024-Q2",
      "keyword_pct": 4.22,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2024-Q2",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2024-Q2",
      "keyword_pct": 1.8,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2024-Q2",
      "keyword_pct": 1.2,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "LLM",
      "quarter": "2024-Q2",
      "keyword_pct": 12.62,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2024-Q2",
      "keyword_pct": 2.32,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "GenAI",
      "quarter": "2024-Q2",
      "keyword_pct": 21.18,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "GameTech",
      "quarter": "2024-Q2",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "FinTech",
      "quarter": "2024-Q2",
      "keyword_pct": 3.43,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "EdTech",
      "quarter": "2024-Q2",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2024-Q2",
      "keyword_pct": 0.8,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2024-Q2",
      "keyword_pct": 2.23,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2024-Q2",
      "keyword_pct": 2.1,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2024-Q2",
      "keyword_pct": 2.45,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "BioTech",
      "quarter": "2024-Q2",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "AgentAI",
      "quarter": "2024-Q2",
      "keyword_pct": 3.07,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "HRTech",
      "quarter": "2024-Q2",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 2
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2024-Q3",
      "keyword_pct": 2.35,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "LLM",
      "quarter": "2024-Q3",
      "keyword_pct": 6.77,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2024-Q3",
      "keyword_pct": 0.85,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "PropTech",
      "quarter": "2024-Q3",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "HealthTech",
      "quarter": "2024-Q3",
      "keyword_pct": 1.9,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2024-Q3",
      "keyword_pct": 5.74,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2024-Q3",
      "keyword_pct": 0.5,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "Web3",
      "quarter": "2024-Q3",
      "keyword_pct": 2.75,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "Robotics",
      "quarter": "2024-Q3",
      "keyword_pct": 3.62,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "GenAI",
      "quarter": "2024-Q3",
      "keyword_pct": 17.04,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "BioTech",
      "quarter": "2024-Q3",
      "keyword_pct": 1.65,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "FinTech",
      "quarter": "2024-Q3",
      "keyword_pct": 3.4,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2024-Q3",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2024-Q3",
      "keyword_pct": 0.85,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2024-Q3",
      "keyword_pct": 2.23,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2024-Q3",
      "keyword_pct": 1.1,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2024-Q3",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "ComputerVision",
      "quarter": "2024-Q3",
      "keyword_pct": 0.55,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2024-Q3",
      "keyword_pct": 1.7,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "GameTech",
      "quarter": "2024-Q3",
      "keyword_pct": 0.5,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "AgentAI",
      "quarter": "2024-Q3",
      "keyword_pct": 1.97,
      "year": 2024,
      "quarter_num": 3
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2024-Q4",
      "keyword_pct": 2.6,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "LLM",
      "quarter": "2024-Q4",
      "keyword_pct": 10.06,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2024-Q4",
      "keyword_pct": 1.97,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2024-Q4",
      "keyword_pct": 1.33,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "Web3",
      "quarter": "2024-Q4",
      "keyword_pct": 2.53,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2024-Q4",
      "keyword_pct": 0.7,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "Robotics",
      "quarter": "2024-Q4",
      "keyword_pct": 4.88,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2024-Q4",
      "keyword_pct": 5.43,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "HealthTech",
      "quarter": "2024-Q4",
      "keyword_pct": 1.6,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "PropTech",
      "quarter": "2024-Q4",
      "keyword_pct": 0.4,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "HRTech",
      "quarter": "2024-Q4",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2024-Q4",
      "keyword_pct": 0.5,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "GameTech",
      "quarter": "2024-Q4",
      "keyword_pct": 0.4,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "AgriTech",
      "quarter": "2024-Q4",
      "keyword_pct": 0.6,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "BioTech",
      "quarter": "2024-Q4",
      "keyword_pct": 1.67,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2024-Q4",
      "keyword_pct": 2.32,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2024-Q4",
      "keyword_pct": 0.4,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "AgentAI",
      "quarter": "2024-Q4",
      "keyword_pct": 3.17,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2024-Q4",
      "keyword_pct": 1.87,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2024-Q4",
      "keyword_pct": 1.1,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "FinTech",
      "quarter": "2024-Q4",
      "keyword_pct": 3.03,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2024-Q4",
      "keyword_pct": 2.13,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "GenAI",
      "quarter": "2024-Q4",
      "keyword_pct": 14.43,
      "year": 2024,
      "quarter_num": 4
    },
    {
      "keyword": "Web3",
      "quarter": "2025-Q1",
      "keyword_pct": 3.14,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "HealthTech",
      "quarter": "2025-Q1",
      "keyword_pct": 1.65,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2025-Q1",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2025-Q1",
      "keyword_pct": 7.92,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "Robotics",
      "quarter": "2025-Q1",
      "keyword_pct": 4.63,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2025-Q1",
      "keyword_pct": 0.93,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2025-Q1",
      "keyword_pct": 1.4,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2025-Q1",
      "keyword_pct": 1.1,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "LLM",
      "quarter": "2025-Q1",
      "keyword_pct": 6.2,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2025-Q1",
      "keyword_pct": 2.07,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "GameTech",
      "quarter": "2025-Q1",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "FinTech",
      "quarter": "2025-Q1",
      "keyword_pct": 4.17,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "EdTech",
      "quarter": "2025-Q1",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2025-Q1",
      "keyword_pct": 0.85,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2025-Q1",
      "keyword_pct": 0.55,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2025-Q1",
      "keyword_pct": 2.58,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2025-Q1",
      "keyword_pct": 1.38,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2025-Q1",
      "keyword_pct": 1.4,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "BioTech",
      "quarter": "2025-Q1",
      "keyword_pct": 1.67,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "AgentAI",
      "quarter": "2025-Q1",
      "keyword_pct": 4.56,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "GenAI",
      "quarter": "2025-Q1",
      "keyword_pct": 11.95,
      "year": 2025,
      "quarter_num": 1
    },
    {
      "keyword": "LLM",
      "quarter": "2025-Q2",
      "keyword_pct": 3.84,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "Web3",
      "quarter": "2025-Q2",
      "keyword_pct": 2.13,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2025-Q2",
      "keyword_pct": 1.53,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "PropTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2025-Q2",
      "keyword_pct": 2.3,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "Robotics",
      "quarter": "2025-Q2",
      "keyword_pct": 3.3,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2025-Q2",
      "keyword_pct": 4.08,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "HealthTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.97,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2025-Q2",
      "keyword_pct": 1.43,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "GenAI",
      "quarter": "2025-Q2",
      "keyword_pct": 16.4,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "HRTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2025-Q2",
      "keyword_pct": 3.05,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "AgentAI",
      "quarter": "2025-Q2",
      "keyword_pct": 6.35,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "FinTech",
      "quarter": "2025-Q2",
      "keyword_pct": 3.47,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "GameTech",
      "quarter": "2025-Q2",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2025-Q2",
      "keyword_pct": 1.17,
      "year": 2025,
      "quarter_num": 2
    },
    {
      "keyword": "LLM",
      "quarter": "2025-Q3",
      "keyword_pct": 6.27,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "Web3",
      "quarter": "2025-Q3",
      "keyword_pct": 2.02,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2025-Q3",
      "keyword_pct": 0.7,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2025-Q3",
      "keyword_pct": 6.46,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "Robotics",
      "quarter": "2025-Q3",
      "keyword_pct": 4.7,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2025-Q3",
      "keyword_pct": 0.9,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2025-Q3",
      "keyword_pct": 1.8,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2025-Q3",
      "keyword_pct": 0.9,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2025-Q3",
      "keyword_pct": 1.43,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "HealthTech",
      "quarter": "2025-Q3",
      "keyword_pct": 0.9,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "GenAI",
      "quarter": "2025-Q3",
      "keyword_pct": 12.6,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "GameTech",
      "quarter": "2025-Q3",
      "keyword_pct": 0.6,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "FinTech",
      "quarter": "2025-Q3",
      "keyword_pct": 2.42,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2025-Q3",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2025-Q3",
      "keyword_pct": 2.42,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2025-Q3",
      "keyword_pct": 1.9,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2025-Q3",
      "keyword_pct": 1.6,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "BioTech",
      "quarter": "2025-Q3",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "AgentAI",
      "quarter": "2025-Q3",
      "keyword_pct": 7.86,
      "year": 2025,
      "quarter_num": 3
    },
    {
      "keyword": "LLM",
      "quarter": "2025-Q4",
      "keyword_pct": 5.0,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "MedTech",
      "quarter": "2025-Q4",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Web3",
      "quarter": "2025-Q4",
      "keyword_pct": 2.77,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2025-Q4",
      "keyword_pct": 0.9,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2025-Q4",
      "keyword_pct": 1.93,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2025-Q4",
      "keyword_pct": 1.27,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Robotics",
      "quarter": "2025-Q4",
      "keyword_pct": 5.87,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2025-Q4",
      "keyword_pct": 9.63,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2025-Q4",
      "keyword_pct": 3.3,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2025-Q4",
      "keyword_pct": 1.8,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "HealthTech",
      "quarter": "2025-Q4",
      "keyword_pct": 1.27,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2025-Q4",
      "keyword_pct": 0.7,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "GameTech",
      "quarter": "2025-Q4",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "FinTech",
      "quarter": "2025-Q4",
      "keyword_pct": 3.03,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Enterprise",
      "quarter": "2025-Q4",
      "keyword_pct": 1.2,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2025-Q4",
      "keyword_pct": 1.1,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "Cybersecurity",
      "quarter": "2025-Q4",
      "keyword_pct": 1.73,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2025-Q4",
      "keyword_pct": 2.33,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "BioTech",
      "quarter": "2025-Q4",
      "keyword_pct": 1.1,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "AgriTech",
      "quarter": "2025-Q4",
      "keyword_pct": 0.5,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "AgentAI",
      "quarter": "2025-Q4",
      "keyword_pct": 9.17,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "GenAI",
      "quarter": "2025-Q4",
      "keyword_pct": 9.7,
      "year": 2025,
      "quarter_num": 4
    },
    {
      "keyword": "LLM",
      "quarter": "2026-Q1",
      "keyword_pct": 6.85,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "MedTech",
      "quarter": "2026-Q1",
      "keyword_pct": 1.1,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "MobilityTech",
      "quarter": "2026-Q1",
      "keyword_pct": 1.7,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "Semiconductors",
      "quarter": "2026-Q1",
      "keyword_pct": 7.55,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "QuantumTech",
      "quarter": "2026-Q1",
      "keyword_pct": 1.6,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "Robotics",
      "quarter": "2026-Q1",
      "keyword_pct": 6.22,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "Infrastructure",
      "quarter": "2026-Q1",
      "keyword_pct": 0.95,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "PhysicalAI",
      "quarter": "2026-Q1",
      "keyword_pct": 1.55,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "HealthTech",
      "quarter": "2026-Q1",
      "keyword_pct": 3.0,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "DigitalHealth",
      "quarter": "2026-Q1",
      "keyword_pct": 0.6,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "FinTech",
      "quarter": "2026-Q1",
      "keyword_pct": 1.45,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "Enterprise",
      "quarter": "2026-Q1",
      "keyword_pct": 0.6,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "Ecommerce",
      "quarter": "2026-Q1",
      "keyword_pct": 2.1,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "DefenseTech",
      "quarter": "2026-Q1",
      "keyword_pct": 3.97,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "CreatorEconomy",
      "quarter": "2026-Q1",
      "keyword_pct": 0.6,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "ClimateTech",
      "quarter": "2026-Q1",
      "keyword_pct": 0.8,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "BioTech",
      "quarter": "2026-Q1",
      "keyword_pct": 0.6,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "AgentAI",
      "quarter": "2026-Q1",
      "keyword_pct": 8.53,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "SpaceTech",
      "quarter": "2026-Q1",
      "keyword_pct": 1.7,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "GenAI",
      "quarter": "2026-Q1",
      "keyword_pct": 13.9,
      "year": 2026,
      "quarter_num": 1
    },
    {
      "keyword": "Web3",
      "quarter": "2026-Q1",
      "keyword_pct": 4.85,
      "year": 2026,
      "quarter_num": 1
    }
  ]
};

// ===== KONFIGURATION =====
let selectedKeywords = [];
const maxKeywords = 5;  // FIX 4: Enforce max 5 keywords cap

// DOM-Elemente
const keywordsList = document.getElementById('keywordsList');
const selectAllButton = document.getElementById('selectAllButton');
const resetButton = document.getElementById('resetButton');
const chart = document.getElementById('chart');
const chartWrapper = document.getElementById('chartWrapper');
const warningMessage = document.getElementById('warningMessage');
const emptyStateMessage = document.getElementById('emptyStateMessage');

// ===== HILFSFUNKTIONEN =====

/**
 * Extrahiert alle Keywords
 */
function getAllKeywords() {
    const keywords = new Set();
    trendData.data.forEach(item => keywords.add(item.keyword));
    return Array.from(keywords).sort();
}

/**
 * Extrahiert alle Quartale in chronologischer Reihenfolge
 */
function getAllQuarters() {
    const quarters = new Set();
    trendData.data.forEach(item => quarters.add(item.quarter));
    return Array.from(quarters).sort((a, b) => {
        const [yearA, qA] = a.split('-Q').map(x => parseInt(x));
        const [yearB, qB] = b.split('-Q').map(x => parseInt(x));
        if (yearA !== yearB) return yearA - yearB;
        return qA - qB;
    });
}

/**
 * Holt Daten für ein Keyword
 */
function getDataForKeyword(keyword) {
    return trendData.data
        .filter(item => item.keyword === keyword)
        .sort((a, b) => {
            const [yearA, qA] = a.quarter.split('-Q').map(x => parseInt(x));
            const [yearB, qB] = b.quarter.split('-Q').map(x => parseInt(x));
            if (yearA !== yearB) return yearA - yearB;
            return qA - qB;
        });
}


/**
 * Maps a trend label to the corresponding CSS class
 * BUG 1: Helper function for label-to-CSS mapping
 */
function getLabelClass(trendLabel) {
    if (!trendLabel) return 'trend-badge--stable';
    const labelStr = String(trendLabel).toLowerCase();
    if (labelStr.includes('emerging')) return 'trend-badge--emerging';
    if (labelStr.includes('rising'))   return 'trend-badge--rising';
    if (labelStr.includes('hot'))      return 'trend-badge--hot';
    if (labelStr.includes('mature'))   return 'trend-badge--mature';
    if (labelStr.includes('declining')) return 'trend-badge--declining';
    if (labelStr.includes('stable'))   return 'trend-badge--stable';
    return 'trend-badge--stable';
}

/**
 * Erstellt Checkboxen für Keyword-Auswahl, sortiert nach Trend-Attraktivität
 * FIX: Simplified to always show badge for every keyword
 */
function populateKeywordsList() {
    const keywords = getAllKeywords();
    keywordsList.innerHTML = '';
    
    if (keywords.length === 0) {
        keywordsList.classList.add('empty');
        keywordsList.innerHTML = '<div class="loading">Keine Keywords gefunden</div>';
        return;
    }
    
    // Build array with trends for each keyword
    const keywordsWithTrends = keywords.map(keyword => {
        const keywordData = getDataForKeyword(keyword);
        
        // Default to Stable
        let trend = { label: 'Stable', emoji: '😴', momentum: 0 };
        let displayLabel = '😴 Stable';
        
        // Try to classify if we have enough data
        if (keywordData && keywordData.length >= 2) {
            const values = keywordData.map(item => item.keyword_pct);
            try {
                const result = classifyTrend(values);
                if (result && result.label && result.emoji) {
                    trend = result;
                    displayLabel = `${result.emoji} ${result.label}`;
                }
            } catch(e) {
                console.error(`Error classifying ${keyword}:`, e);
            }
        }
        
        return { keyword, trend, displayLabel };
    });
    
    // Sort by attractiveness
    const attractivenessOrder = {
        'Emerging': 0,
        'Rising': 1,
        'Hot': 2,
        'Mature': 3,
        'Stable': 4,
        'Declining': 5
    };
    
    keywordsWithTrends.sort((a, b) => {
        const orderA = attractivenessOrder[a.trend.label] ?? 6;
        const orderB = attractivenessOrder[b.trend.label] ?? 6;
        return orderA !== orderB ? orderA - orderB : a.keyword.localeCompare(b.keyword);
    });
    
    // Create checkbox HTML for each keyword
    keywordsWithTrends.forEach(({ keyword, trend, displayLabel }) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'keyword-checkbox-wrapper';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `kw-${keyword}`;
        checkbox.value = keyword;
        checkbox.addEventListener('change', handleKeywordChange);
        
        const label = document.createElement('label');
        label.htmlFor = `kw-${keyword}`;
        label.innerHTML = `${keyword} <span class="trend-badge ${getLabelClass(trend.label)}">${displayLabel}</span>`;
        
        wrapper.appendChild(checkbox);
        wrapper.appendChild(label);
        keywordsList.appendChild(wrapper);
        
        console.log(`Added: ${keyword} with label: ${displayLabel}`);
    });
    
    // Select first keyword by default
    if (keywordsWithTrends.length > 0) {
        const firstCheckbox = document.getElementById(`kw-${keywordsWithTrends[0].keyword}`);
        if (firstCheckbox) {
            firstCheckbox.checked = true;
            selectedKeywords = [keywordsWithTrends[0].keyword];
        }
    }
}

/**
 * Updates checkbox disabled states based on selection count
 * BUG 2: Visual feedback when at max keywords
 */
function updateCheckboxStates() {
    const checkedBoxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    const isAtMax = checkedBoxes.length >= maxKeywords;
    
    allCheckboxes.forEach(checkbox => {
        const wrapper = checkbox.closest('.keyword-checkbox-wrapper');
        if (isAtMax && !checkbox.checked) {
            checkbox.disabled = true;
            if (wrapper) wrapper.style.opacity = '0.4';
        } else {
            checkbox.disabled = false;
            if (wrapper) wrapper.style.opacity = '1';
        }
    });
}

/**
 * Behandelt Änderungen in der Checkbox-Auswahl
 * BUG 2: Fixed warning logic and checkbox state management
 */
function handleKeywordChange(event) {
    // BUG 2: Check BEFORE processing if this is a new check that would exceed the limit
    const isCheckingNewBox = event.target.checked === true;
    const currentlyChecked = document.querySelectorAll('input[type="checkbox"]:checked').length;
    
    // BUG 2: If checking a NEW box and already at or above maxKeywords, prevent it
    if (isCheckingNewBox && currentlyChecked > maxKeywords) {
        event.target.checked = false;
        showWarning('⚠️ Maximal ' + maxKeywords + ' Trends gleichzeitig auswählbar. Bitte zuerst einen Trend abwählen.');
        return;
    }
    
    // BUG 2: Otherwise, allow the change
    const checkedBoxes = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'));
    const selected = checkedBoxes.map(box => box.value);
    
    selectedKeywords = selected;
    hideWarning();
    
    // BUG 2: Update visual state of all checkboxes
    updateCheckboxStates();
    
    updateChart();
}

/**
 * Zeigt Warnung an
 */
function showWarning(message) {
    warningMessage.textContent = message;
    warningMessage.style.display = 'block';
}

/**
 * Versteckt Warnung
 */
function hideWarning() {
    warningMessage.style.display = 'none';
}

/**
 * Setzt Auswahl zurück
 * BUG 2: Re-enable all checkboxes and update visual state
 */
function resetSelection() {
    const keywords = getAllKeywords();
    if (keywords.length > 0) {
        // Alle Checkboxen deselektieren und re-enablen
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
            cb.disabled = false;
        });
        
        // Erstes Keyword auswählen
        const firstCheckbox = document.getElementById(`kw-${keywords[0]}`);
        if (firstCheckbox) {
            firstCheckbox.checked = true;
            selectedKeywords = [keywords[0]];
        }
        hideWarning();
        updateCheckboxStates();  // BUG 2: Update visual state
        updateChart();
    }
}

/**
 * Wählt bis zu maxKeywords Keywords aus
 * BUG 2: Updates visual state after selection
 */
function selectAllKeywords() {
    const keywords = getAllKeywords();
    
    // Begrenze auf maxKeywords
    const toSelect = keywords.slice(0, maxKeywords);
    
    // Alle Checkboxen deselektieren
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
    
    // Erste maxKeywords-Checkboxen auswählen
    toSelect.forEach(keyword => {
        const checkbox = document.getElementById(`kw-${keyword}`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    
    selectedKeywords = toSelect;
    
    hideWarning();
    updateCheckboxStates();  // BUG 2: Update visual state
    updateChart();
}

/**
 * Berechnet den Median eines Arrays
 */
function calculateMedian(arr) {
    if (!arr || arr.length === 0) return NaN;
    const sorted = [...arr].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    if (sorted.length % 2 === 0) {
        return (sorted[mid - 1] + sorted[mid]) / 2;
    }
    return sorted[mid];
}

/**
 * Berechnet das X-Perzentil eines Arrays
 */
function calculatePercentile(arr, percentile) {
    if (!arr || arr.length === 0) return NaN;
    const sorted = [...arr].sort((a, b) => a - b);
    const index = (percentile / 100) * (sorted.length - 1);
    const lower = Math.floor(index);
    const upper = Math.ceil(index);
    const weight = index - lower;
    
    if (lower === upper) {
        return sorted[lower];
    }
    
    return sorted[lower] * (1 - weight) + sorted[upper] * weight;
}

/**
 * Berechnet alle letzten Werte aller Keywords für Perzentilvergleiche
 */
function computeAllLastValues() {
    const allKeywords = getAllKeywords();
    const lastValues = [];
    
    allKeywords.forEach(keyword => {
        const keywordData = getDataForKeyword(keyword);
        if (keywordData.length > 0) {
            lastValues.push(keywordData[keywordData.length - 1].keyword_pct);
        }
    });
    
    return lastValues;
}

/**
 * Klassifiziert den Trend basierend auf Level und Momentum
 * @param {number[]} values - Array mit keyword_pct Werten chronologisch sortiert
 * @returns {Object} { label, emoji, momentum } - z.B. { label: 'Emerging', emoji: '🚀', momentum: 0.15 }
 * BUG 1: Added guard for insufficient data
 */
function classifyTrend(values) {
    // BUG 1: Guard for insufficient data
    if (!values || values.length < 2) {
        console.warn('classifyTrend: Insufficient data', values?.length);
        return { label: 'Stable', emoji: '😴', momentum: 0 };
    }
    
    if (values.length === 0) {
        return { label: 'Stable', emoji: '😴', momentum: 0 };
    }
    
    // lastValue = letzter Element
    const lastValue = values[values.length - 1];
    
    // recentValues = letzte 4 Werte
    const recentValues = values.slice(-4);
    
    // momentum = durchschnittliche Quarter-over-Quarter Änderung in recentValues
    let momentum = 0;
    if (recentValues.length >= 2) {
        let totalChange = 0;
        for (let i = 1; i < recentValues.length; i++) {
            totalChange += (recentValues[i] - recentValues[i - 1]);
        }
        momentum = totalChange / (recentValues.length - 1);
    }
    
    // shortMomentum = Veränderung zwischen letzten 2 Werten
    let shortMomentum = 0;
    if (values.length >= 2) {
        shortMomentum = values[values.length - 1] - values[values.length - 2];
    }
    
    // allLastValues und Perzentile berechnen
    const allLastValues = computeAllLastValues();
    
    // Guard: Wenn keine anderen Keywords vorhanden, als Stable klassifizieren
    if (!allLastValues || allLastValues.length === 0) {
        console.warn(`classifyTrend: No allLastValues data for percentile comparison, defaulting to Stable`);
        // Nutze momentan für einfache Rising/Stable Klassifikation
        if (momentum > 0.15) {
            return { label: 'Rising', emoji: '✨', momentum: momentum };
        }
        return { label: 'Stable', emoji: '😴', momentum: momentum };
    }
    
    const level75 = calculatePercentile(allLastValues, 75);
    const levelMedian = calculateMedian(allLastValues);
    
    // Guard: Überprüfe NaN resultate
    if (isNaN(level75) || isNaN(levelMedian)) {
        console.warn(`classifyTrend: Invalid percentile calculations, defaulting to Stable`);
        if (momentum > 0.15) {
            return { label: 'Rising', emoji: '✨', momentum: momentum };
        }
        return { label: 'Stable', emoji: '😴', momentum: momentum };
    }
    
    // Klassifikation nach Regeln (in dieser Reihenfolge)
    if (momentum < -0.3) {
        return { label: 'Declining', emoji: '📉', momentum: momentum };
    } else if (lastValue > level75 && momentum > 0.3) {
        return { label: 'Hot', emoji: '🔥', momentum: momentum };
    } else if (lastValue > level75 && momentum >= -0.3 && momentum <= 0.3) {
        return { label: 'Mature', emoji: '⚖️', momentum: momentum };
    } else if (lastValue < levelMedian && momentum > 0.3) {
        return { label: 'Emerging', emoji: '🚀', momentum: momentum };
    } else if (momentum > 0.15) {
        return { label: 'Rising', emoji: '✨', momentum: momentum };
    } else {
        return { label: 'Stable', emoji: '😴', momentum: momentum };
    }
}

/**
 * Generiert dynamischen Chart-Titel
 */
function getChartTitle() {
    if (selectedKeywords.length === 0) {
        return 'Keine Keywords ausgewählt';
    } else if (selectedKeywords.length === 1) {
        return `Trendentwicklung: ${selectedKeywords[0]}`;
    } else {
        return `Keyword Trend Comparison (Quarterly)`;
    }
}

/**
 * Aktualisiert das Chart
 * FIX 3: Generate unique per-keyword colors using HSL spacing
 */
function updateChart() {
    // Empty State prüfen
    if (selectedKeywords.length === 0) {
        emptyStateMessage.style.display = 'block';
        chartWrapper.style.display = 'none';
        return;
    }
    
    emptyStateMessage.style.display = 'none';
    chartWrapper.style.display = 'block';
    
    const quarters = getAllQuarters();
    const traces = [];
    
    // BUG 2: Generate unique HSL colors for all keywords using golden angle distribution
    const allKeywords = getAllKeywords();
    const keywordColors = {};
    const GOLDEN = 137.508;  // Golden angle in degrees for maximally distinct colors
    allKeywords.forEach((kw, i) => {
        const hue = Math.round((i * GOLDEN) % 360);
        keywordColors[kw] = `hsl(${hue}, 70%, 42%)`;
        console.log(`Color for ${kw}: hsl(${hue}, 70%, 42%)`);
    });
    
    // Trace pro ausgewähltem Keyword
    selectedKeywords.forEach((keyword) => {
        const keywordData = getDataForKeyword(keyword);
        
        // Mapping Quartale -> Werte
        const valuesByQuarter = {};
        keywordData.forEach(item => {
            valuesByQuarter[item.quarter] = item.keyword_pct;
        });
        
        // Arrays erstellen
        const yValues = quarters.map(q => valuesByQuarter[q] || 0);
        
        // Trend klassifizieren
        const trend = classifyTrend(yValues);
        const trendKey = trend.label.toLowerCase();
        
        // BUG 2: Use unique per-keyword color with golden angle distribution
        const traceColor = keywordColors[keyword] || '#90A4AE';
        
        traces.push({
            x: quarters,
            y: yValues,
            mode: 'lines+markers',
            name: `${keyword} ${trend.emoji} ${trend.label}`,
            type: 'scatter',
            line: {
                color: traceColor,
                width: 2.5
            },
            marker: {
                size: 5
            },
            hovertemplate: '<b>' + keyword + ' ' + trend.emoji + '</b><br>' +
                          'Q: %{x}<br>' +
                          'Attention Share: %{y:.2f}%<br>' +
                          'Momentum: ' + (trend.momentum >= 0 ? '+' : '') + trend.momentum.toFixed(2) + '%/Q<br>' +
                          '<extra></extra>'
        });
    });
    
    const layout = {
        title: {
            text: getChartTitle(),
            font: { size: 18 },
        },
        xaxis: {
            title: 'Quartal',
            tickangle: -45
        },
        yaxis: {
            title: 'Attention Share (%)',
            zeroline: false
        },
        hovermode: 'closest',
        margin: { l: 70, r: 30, t: 100, b: 100 },
        plot_bgcolor: '#f9f9f9',
        paper_bgcolor: '#ffffff',
        legend: {
            orientation: 'v',
            x: 1.02,
            y: 1
        },
        responsive: true
    };
    
    Plotly.newPlot(chart, traces, layout, { responsive: true });
}

// ===== HILFSFUNKTIONEN FÜR DATENEXTRAKTION =====

/**
 * Gibt alle einzigartigen Keywords zurück
 */
function getAllKeywords() {
    const keywords = new Set();
    trendData.data.forEach(item => {
        keywords.add(item.keyword);
    });
    return Array.from(keywords).sort();
}

/**
 * Gibt alle Datenpunkte für ein spezifisches Keyword zurück, sortiert nach Quarter
 */
function getDataForKeyword(keyword) {
    return trendData.data
        .filter(item => item.keyword === keyword)
        .sort((a, b) => {
            // Sortiere nach Jahr, dann nach Quarter
            if (a.year !== b.year) return a.year - b.year;
            return a.quarter_num - b.quarter_num;
        });
}

/**
 * Gibt alle einzigartigen Quartale zurück
 */
function getAllQuarters() {
    const quarters = new Set();
    trendData.data.forEach(item => {
        quarters.add(item.quarter);
    });
    return Array.from(quarters).sort();
}

// ===== EVENT LISTENER =====
resetButton.addEventListener('click', resetSelection);
selectAllButton.addEventListener('click', selectAllKeywords);

// ===== INITIALISIERUNG =====
window.addEventListener('DOMContentLoaded', function() {
    populateKeywordsList();
    updateChart();
    console.log('✓ Visualisierung initialisiert');
    console.log(`  Keywords: ${getAllKeywords().length}`);
    console.log(`  Quartale: ${getAllQuarters().length}`);
    console.log(`  Metrik: ${trendData.metadata.metric}`);
});
