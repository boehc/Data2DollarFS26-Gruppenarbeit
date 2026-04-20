/**
 * data2dollar – Trend-Visualisierung
 * Datenquelle: index_standalone.html (Lizzy/Trends)
 * 28 Keywords · 13 Quartale · Plotly.js
 */

// ===== EMBEDDED TREND DATA =====
const trendData = {
  metadata: {
    generated: "2026-04-14T19:25:39.860369",
    total_keywords: 28,
    quarters_count: 13,
    metric: "keyword_pct (normalisiert, %)",
    date_range: { from: "2023-Q1", to: "2026-Q1" }
  },
  data: [
    // 2023-Q1
    {"keyword":"AgentAI","quarter":"2023-Q1","keyword_pct":6.9},
    {"keyword":"Web3","quarter":"2023-Q1","keyword_pct":6.58},
    {"keyword":"SpaceTech","quarter":"2023-Q1","keyword_pct":1.85},
    {"keyword":"Semiconductors","quarter":"2023-Q1","keyword_pct":2.77},
    {"keyword":"Robotics","quarter":"2023-Q1","keyword_pct":3.44},
    {"keyword":"QuantumTech","quarter":"2023-Q1","keyword_pct":0.9},
    {"keyword":"PropTech","quarter":"2023-Q1","keyword_pct":0.5},
    {"keyword":"PhysicalAI","quarter":"2023-Q1","keyword_pct":0.7},
    {"keyword":"MedTech","quarter":"2023-Q1","keyword_pct":0.6},
    {"keyword":"LLM","quarter":"2023-Q1","keyword_pct":6.3},
    {"keyword":"Infrastructure","quarter":"2023-Q1","keyword_pct":3.08},
    {"keyword":"HealthTech","quarter":"2023-Q1","keyword_pct":1.87},
    {"keyword":"MobilityTech","quarter":"2023-Q1","keyword_pct":0.45},
    {"keyword":"GameTech","quarter":"2023-Q1","keyword_pct":0.4},
    {"keyword":"GenAI","quarter":"2023-Q1","keyword_pct":11.02},
    {"keyword":"ClimateTech","quarter":"2023-Q1","keyword_pct":1.13},
    {"keyword":"ComputerVision","quarter":"2023-Q1","keyword_pct":0.65},
    {"keyword":"CreatorEconomy","quarter":"2023-Q1","keyword_pct":0.5},
    {"keyword":"Cybersecurity","quarter":"2023-Q1","keyword_pct":5.08},
    {"keyword":"BioTech","quarter":"2023-Q1","keyword_pct":0.45},
    {"keyword":"DigitalHealth","quarter":"2023-Q1","keyword_pct":0.57},
    {"keyword":"Ecommerce","quarter":"2023-Q1","keyword_pct":1.27},
    {"keyword":"Enterprise","quarter":"2023-Q1","keyword_pct":0.8},
    {"keyword":"FinTech","quarter":"2023-Q1","keyword_pct":5.63},
    {"keyword":"DefenseTech","quarter":"2023-Q1","keyword_pct":1.4},
    // 2023-Q2
    {"keyword":"HealthTech","quarter":"2023-Q2","keyword_pct":1.97},
    {"keyword":"Web3","quarter":"2023-Q2","keyword_pct":5.26},
    {"keyword":"SpaceTech","quarter":"2023-Q2","keyword_pct":0.4},
    {"keyword":"Semiconductors","quarter":"2023-Q2","keyword_pct":4.13},
    {"keyword":"Robotics","quarter":"2023-Q2","keyword_pct":3.0},
    {"keyword":"QuantumTech","quarter":"2023-Q2","keyword_pct":0.85},
    {"keyword":"PhysicalAI","quarter":"2023-Q2","keyword_pct":0.4},
    {"keyword":"MedTech","quarter":"2023-Q2","keyword_pct":0.4},
    {"keyword":"LLM","quarter":"2023-Q2","keyword_pct":9.18},
    {"keyword":"Infrastructure","quarter":"2023-Q2","keyword_pct":1.87},
    {"keyword":"GenAI","quarter":"2023-Q2","keyword_pct":15.12},
    {"keyword":"PropTech","quarter":"2023-Q2","keyword_pct":0.4},
    {"keyword":"EdTech","quarter":"2023-Q2","keyword_pct":0.4},
    {"keyword":"AgriTech","quarter":"2023-Q2","keyword_pct":0.4},
    {"keyword":"BioTech","quarter":"2023-Q2","keyword_pct":0.57},
    {"keyword":"ClimateTech","quarter":"2023-Q2","keyword_pct":1.73},
    {"keyword":"ComputerVision","quarter":"2023-Q2","keyword_pct":0.85},
    {"keyword":"AgentAI","quarter":"2023-Q2","keyword_pct":1.67},
    {"keyword":"FinTech","quarter":"2023-Q2","keyword_pct":3.83},
    {"keyword":"Cybersecurity","quarter":"2023-Q2","keyword_pct":6.03},
    {"keyword":"DefenseTech","quarter":"2023-Q2","keyword_pct":1.0},
    {"keyword":"DigitalHealth","quarter":"2023-Q2","keyword_pct":1.3},
    {"keyword":"Ecommerce","quarter":"2023-Q2","keyword_pct":1.3},
    {"keyword":"CreatorEconomy","quarter":"2023-Q2","keyword_pct":0.4},
    // 2023-Q3
    {"keyword":"HealthTech","quarter":"2023-Q3","keyword_pct":2.25},
    {"keyword":"Infrastructure","quarter":"2023-Q3","keyword_pct":1.73},
    {"keyword":"LLM","quarter":"2023-Q3","keyword_pct":8.27},
    {"keyword":"MobilityTech","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"PhysicalAI","quarter":"2023-Q3","keyword_pct":1.1},
    {"keyword":"Web3","quarter":"2023-Q3","keyword_pct":6.1},
    {"keyword":"QuantumTech","quarter":"2023-Q3","keyword_pct":0.9},
    {"keyword":"Semiconductors","quarter":"2023-Q3","keyword_pct":3.9},
    {"keyword":"SpaceTech","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"HRTech","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"PropTech","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"Robotics","quarter":"2023-Q3","keyword_pct":3.47},
    {"keyword":"GenAI","quarter":"2023-Q3","keyword_pct":13.3},
    {"keyword":"FinTech","quarter":"2023-Q3","keyword_pct":4.47},
    {"keyword":"GameTech","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"AgentAI","quarter":"2023-Q3","keyword_pct":1.3},
    {"keyword":"AgriTech","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"BioTech","quarter":"2023-Q3","keyword_pct":0.65},
    {"keyword":"CreatorEconomy","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"ClimateTech","quarter":"2023-Q3","keyword_pct":1.68},
    {"keyword":"DefenseTech","quarter":"2023-Q3","keyword_pct":1.0},
    {"keyword":"DigitalHealth","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"Ecommerce","quarter":"2023-Q3","keyword_pct":0.65},
    {"keyword":"EdTech","quarter":"2023-Q3","keyword_pct":0.9},
    {"keyword":"Enterprise","quarter":"2023-Q3","keyword_pct":0.4},
    {"keyword":"Cybersecurity","quarter":"2023-Q3","keyword_pct":7.1},
    // 2023-Q4
    {"keyword":"MobilityTech","quarter":"2023-Q4","keyword_pct":0.75},
    {"keyword":"Infrastructure","quarter":"2023-Q4","keyword_pct":1.1},
    {"keyword":"LLM","quarter":"2023-Q4","keyword_pct":7.68},
    {"keyword":"MedTech","quarter":"2023-Q4","keyword_pct":0.45},
    {"keyword":"PhysicalAI","quarter":"2023-Q4","keyword_pct":1.17},
    {"keyword":"HealthTech","quarter":"2023-Q4","keyword_pct":2.67},
    {"keyword":"QuantumTech","quarter":"2023-Q4","keyword_pct":0.63},
    {"keyword":"Robotics","quarter":"2023-Q4","keyword_pct":3.77},
    {"keyword":"Semiconductors","quarter":"2023-Q4","keyword_pct":4.57},
    {"keyword":"SpaceTech","quarter":"2023-Q4","keyword_pct":0.5},
    {"keyword":"Web3","quarter":"2023-Q4","keyword_pct":4.16},
    {"keyword":"PropTech","quarter":"2023-Q4","keyword_pct":0.4},
    {"keyword":"GenAI","quarter":"2023-Q4","keyword_pct":16.87},
    {"keyword":"BioTech","quarter":"2023-Q4","keyword_pct":0.9},
    {"keyword":"FinTech","quarter":"2023-Q4","keyword_pct":3.23},
    {"keyword":"GameTech","quarter":"2023-Q4","keyword_pct":0.4},
    {"keyword":"AgriTech","quarter":"2023-Q4","keyword_pct":0.5},
    {"keyword":"ClimateTech","quarter":"2023-Q4","keyword_pct":2.7},
    {"keyword":"ComputerVision","quarter":"2023-Q4","keyword_pct":0.4},
    {"keyword":"CreatorEconomy","quarter":"2023-Q4","keyword_pct":0.4},
    {"keyword":"AgentAI","quarter":"2023-Q4","keyword_pct":0.7},
    {"keyword":"DefenseTech","quarter":"2023-Q4","keyword_pct":2.17},
    {"keyword":"DigitalHealth","quarter":"2023-Q4","keyword_pct":0.5},
    {"keyword":"Ecommerce","quarter":"2023-Q4","keyword_pct":1.1},
    {"keyword":"EdTech","quarter":"2023-Q4","keyword_pct":0.4},
    {"keyword":"Cybersecurity","quarter":"2023-Q4","keyword_pct":7.4},
    // 2024-Q1
    {"keyword":"Web3","quarter":"2024-Q1","keyword_pct":4.93},
    {"keyword":"HealthTech","quarter":"2024-Q1","keyword_pct":1.6},
    {"keyword":"SpaceTech","quarter":"2024-Q1","keyword_pct":2.4},
    {"keyword":"Robotics","quarter":"2024-Q1","keyword_pct":5.17},
    {"keyword":"QuantumTech","quarter":"2024-Q1","keyword_pct":1.35},
    {"keyword":"PropTech","quarter":"2024-Q1","keyword_pct":0.6},
    {"keyword":"MobilityTech","quarter":"2024-Q1","keyword_pct":0.5},
    {"keyword":"MedTech","quarter":"2024-Q1","keyword_pct":0.6},
    {"keyword":"LLM","quarter":"2024-Q1","keyword_pct":7.92},
    {"keyword":"Infrastructure","quarter":"2024-Q1","keyword_pct":1.27},
    {"keyword":"GenAI","quarter":"2024-Q1","keyword_pct":16.8},
    {"keyword":"Semiconductors","quarter":"2024-Q1","keyword_pct":4.16},
    {"keyword":"FinTech","quarter":"2024-Q1","keyword_pct":3.9},
    {"keyword":"BioTech","quarter":"2024-Q1","keyword_pct":1.07},
    {"keyword":"ClimateTech","quarter":"2024-Q1","keyword_pct":1.1},
    {"keyword":"ComputerVision","quarter":"2024-Q1","keyword_pct":0.6},
    {"keyword":"Cybersecurity","quarter":"2024-Q1","keyword_pct":1.6},
    {"keyword":"AgentAI","quarter":"2024-Q1","keyword_pct":1.4},
    {"keyword":"DigitalHealth","quarter":"2024-Q1","keyword_pct":1.0},
    {"keyword":"Ecommerce","quarter":"2024-Q1","keyword_pct":0.55},
    {"keyword":"EdTech","quarter":"2024-Q1","keyword_pct":0.6},
    {"keyword":"Enterprise","quarter":"2024-Q1","keyword_pct":0.55},
    {"keyword":"DefenseTech","quarter":"2024-Q1","keyword_pct":2.67},
    {"keyword":"GameTech","quarter":"2024-Q1","keyword_pct":1.6},
    // 2024-Q2
    {"keyword":"HealthTech","quarter":"2024-Q2","keyword_pct":2.42},
    {"keyword":"Web3","quarter":"2024-Q2","keyword_pct":2.62},
    {"keyword":"SpaceTech","quarter":"2024-Q2","keyword_pct":0.6},
    {"keyword":"Semiconductors","quarter":"2024-Q2","keyword_pct":5.75},
    {"keyword":"Robotics","quarter":"2024-Q2","keyword_pct":4.22},
    {"keyword":"QuantumTech","quarter":"2024-Q2","keyword_pct":0.6},
    {"keyword":"PhysicalAI","quarter":"2024-Q2","keyword_pct":1.8},
    {"keyword":"MobilityTech","quarter":"2024-Q2","keyword_pct":1.2},
    {"keyword":"LLM","quarter":"2024-Q2","keyword_pct":12.62},
    {"keyword":"Infrastructure","quarter":"2024-Q2","keyword_pct":2.32},
    {"keyword":"GenAI","quarter":"2024-Q2","keyword_pct":21.18},
    {"keyword":"GameTech","quarter":"2024-Q2","keyword_pct":0.6},
    {"keyword":"FinTech","quarter":"2024-Q2","keyword_pct":3.43},
    {"keyword":"EdTech","quarter":"2024-Q2","keyword_pct":0.6},
    {"keyword":"DigitalHealth","quarter":"2024-Q2","keyword_pct":0.8},
    {"keyword":"DefenseTech","quarter":"2024-Q2","keyword_pct":2.23},
    {"keyword":"Cybersecurity","quarter":"2024-Q2","keyword_pct":2.1},
    {"keyword":"ClimateTech","quarter":"2024-Q2","keyword_pct":2.45},
    {"keyword":"BioTech","quarter":"2024-Q2","keyword_pct":0.6},
    {"keyword":"AgentAI","quarter":"2024-Q2","keyword_pct":3.07},
    {"keyword":"HRTech","quarter":"2024-Q2","keyword_pct":0.6},
    // 2024-Q3
    {"keyword":"Infrastructure","quarter":"2024-Q3","keyword_pct":2.35},
    {"keyword":"LLM","quarter":"2024-Q3","keyword_pct":6.77},
    {"keyword":"PhysicalAI","quarter":"2024-Q3","keyword_pct":0.85},
    {"keyword":"PropTech","quarter":"2024-Q3","keyword_pct":0.6},
    {"keyword":"HealthTech","quarter":"2024-Q3","keyword_pct":1.9},
    {"keyword":"Semiconductors","quarter":"2024-Q3","keyword_pct":5.74},
    {"keyword":"SpaceTech","quarter":"2024-Q3","keyword_pct":0.5},
    {"keyword":"Web3","quarter":"2024-Q3","keyword_pct":2.75},
    {"keyword":"Robotics","quarter":"2024-Q3","keyword_pct":3.62},
    {"keyword":"GenAI","quarter":"2024-Q3","keyword_pct":17.04},
    {"keyword":"BioTech","quarter":"2024-Q3","keyword_pct":1.65},
    {"keyword":"FinTech","quarter":"2024-Q3","keyword_pct":3.4},
    {"keyword":"Ecommerce","quarter":"2024-Q3","keyword_pct":0.6},
    {"keyword":"DigitalHealth","quarter":"2024-Q3","keyword_pct":0.85},
    {"keyword":"DefenseTech","quarter":"2024-Q3","keyword_pct":2.23},
    {"keyword":"Cybersecurity","quarter":"2024-Q3","keyword_pct":1.1},
    {"keyword":"CreatorEconomy","quarter":"2024-Q3","keyword_pct":0.6},
    {"keyword":"ComputerVision","quarter":"2024-Q3","keyword_pct":0.55},
    {"keyword":"ClimateTech","quarter":"2024-Q3","keyword_pct":1.7},
    {"keyword":"GameTech","quarter":"2024-Q3","keyword_pct":0.5},
    {"keyword":"AgentAI","quarter":"2024-Q3","keyword_pct":1.97},
    // 2024-Q4
    {"keyword":"Infrastructure","quarter":"2024-Q4","keyword_pct":2.6},
    {"keyword":"LLM","quarter":"2024-Q4","keyword_pct":10.06},
    {"keyword":"MobilityTech","quarter":"2024-Q4","keyword_pct":1.97},
    {"keyword":"PhysicalAI","quarter":"2024-Q4","keyword_pct":1.33},
    {"keyword":"Web3","quarter":"2024-Q4","keyword_pct":2.53},
    {"keyword":"QuantumTech","quarter":"2024-Q4","keyword_pct":0.7},
    {"keyword":"Robotics","quarter":"2024-Q4","keyword_pct":4.88},
    {"keyword":"Semiconductors","quarter":"2024-Q4","keyword_pct":5.43},
    {"keyword":"HealthTech","quarter":"2024-Q4","keyword_pct":1.6},
    {"keyword":"PropTech","quarter":"2024-Q4","keyword_pct":0.4},
    {"keyword":"HRTech","quarter":"2024-Q4","keyword_pct":0.6},
    {"keyword":"SpaceTech","quarter":"2024-Q4","keyword_pct":0.5},
    {"keyword":"GameTech","quarter":"2024-Q4","keyword_pct":0.4},
    {"keyword":"AgriTech","quarter":"2024-Q4","keyword_pct":0.6},
    {"keyword":"BioTech","quarter":"2024-Q4","keyword_pct":1.67},
    {"keyword":"ClimateTech","quarter":"2024-Q4","keyword_pct":2.32},
    {"keyword":"CreatorEconomy","quarter":"2024-Q4","keyword_pct":0.4},
    {"keyword":"AgentAI","quarter":"2024-Q4","keyword_pct":3.17},
    {"keyword":"DefenseTech","quarter":"2024-Q4","keyword_pct":1.87},
    {"keyword":"Ecommerce","quarter":"2024-Q4","keyword_pct":1.1},
    {"keyword":"FinTech","quarter":"2024-Q4","keyword_pct":3.03},
    {"keyword":"Cybersecurity","quarter":"2024-Q4","keyword_pct":2.13},
    {"keyword":"GenAI","quarter":"2024-Q4","keyword_pct":14.43},
    // 2025-Q1
    {"keyword":"Web3","quarter":"2025-Q1","keyword_pct":3.14},
    {"keyword":"HealthTech","quarter":"2025-Q1","keyword_pct":1.65},
    {"keyword":"SpaceTech","quarter":"2025-Q1","keyword_pct":0.6},
    {"keyword":"Semiconductors","quarter":"2025-Q1","keyword_pct":7.92},
    {"keyword":"Robotics","quarter":"2025-Q1","keyword_pct":4.63},
    {"keyword":"QuantumTech","quarter":"2025-Q1","keyword_pct":0.93},
    {"keyword":"PhysicalAI","quarter":"2025-Q1","keyword_pct":1.4},
    {"keyword":"MobilityTech","quarter":"2025-Q1","keyword_pct":1.1},
    {"keyword":"LLM","quarter":"2025-Q1","keyword_pct":6.2},
    {"keyword":"Infrastructure","quarter":"2025-Q1","keyword_pct":2.07},
    {"keyword":"GameTech","quarter":"2025-Q1","keyword_pct":0.5},
    {"keyword":"FinTech","quarter":"2025-Q1","keyword_pct":4.17},
    {"keyword":"EdTech","quarter":"2025-Q1","keyword_pct":0.6},
    {"keyword":"Ecommerce","quarter":"2025-Q1","keyword_pct":0.85},
    {"keyword":"DigitalHealth","quarter":"2025-Q1","keyword_pct":0.55},
    {"keyword":"DefenseTech","quarter":"2025-Q1","keyword_pct":2.58},
    {"keyword":"Cybersecurity","quarter":"2025-Q1","keyword_pct":1.38},
    {"keyword":"ClimateTech","quarter":"2025-Q1","keyword_pct":1.4},
    {"keyword":"BioTech","quarter":"2025-Q1","keyword_pct":1.67},
    {"keyword":"AgentAI","quarter":"2025-Q1","keyword_pct":4.56},
    {"keyword":"GenAI","quarter":"2025-Q1","keyword_pct":11.95},
    // 2025-Q2
    {"keyword":"LLM","quarter":"2025-Q2","keyword_pct":3.84},
    {"keyword":"Web3","quarter":"2025-Q2","keyword_pct":2.13},
    {"keyword":"PhysicalAI","quarter":"2025-Q2","keyword_pct":1.53},
    {"keyword":"PropTech","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"Infrastructure","quarter":"2025-Q2","keyword_pct":2.3},
    {"keyword":"Robotics","quarter":"2025-Q2","keyword_pct":3.3},
    {"keyword":"Semiconductors","quarter":"2025-Q2","keyword_pct":4.08},
    {"keyword":"SpaceTech","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"QuantumTech","quarter":"2025-Q2","keyword_pct":0.5},
    {"keyword":"HealthTech","quarter":"2025-Q2","keyword_pct":0.97},
    {"keyword":"MobilityTech","quarter":"2025-Q2","keyword_pct":1.43},
    {"keyword":"GenAI","quarter":"2025-Q2","keyword_pct":16.4},
    {"keyword":"HRTech","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"ClimateTech","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"CreatorEconomy","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"Cybersecurity","quarter":"2025-Q2","keyword_pct":3.05},
    {"keyword":"AgentAI","quarter":"2025-Q2","keyword_pct":6.35},
    {"keyword":"DigitalHealth","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"Ecommerce","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"FinTech","quarter":"2025-Q2","keyword_pct":3.47},
    {"keyword":"GameTech","quarter":"2025-Q2","keyword_pct":0.6},
    {"keyword":"DefenseTech","quarter":"2025-Q2","keyword_pct":1.17},
    // 2025-Q3
    {"keyword":"LLM","quarter":"2025-Q3","keyword_pct":6.27},
    {"keyword":"Web3","quarter":"2025-Q3","keyword_pct":2.02},
    {"keyword":"SpaceTech","quarter":"2025-Q3","keyword_pct":0.7},
    {"keyword":"Semiconductors","quarter":"2025-Q3","keyword_pct":6.46},
    {"keyword":"Robotics","quarter":"2025-Q3","keyword_pct":4.7},
    {"keyword":"QuantumTech","quarter":"2025-Q3","keyword_pct":0.9},
    {"keyword":"PhysicalAI","quarter":"2025-Q3","keyword_pct":1.8},
    {"keyword":"MobilityTech","quarter":"2025-Q3","keyword_pct":0.9},
    {"keyword":"Infrastructure","quarter":"2025-Q3","keyword_pct":1.43},
    {"keyword":"HealthTech","quarter":"2025-Q3","keyword_pct":0.9},
    {"keyword":"GenAI","quarter":"2025-Q3","keyword_pct":12.6},
    {"keyword":"GameTech","quarter":"2025-Q3","keyword_pct":0.6},
    {"keyword":"FinTech","quarter":"2025-Q3","keyword_pct":2.42},
    {"keyword":"Ecommerce","quarter":"2025-Q3","keyword_pct":0.5},
    {"keyword":"DefenseTech","quarter":"2025-Q3","keyword_pct":2.42},
    {"keyword":"Cybersecurity","quarter":"2025-Q3","keyword_pct":1.9},
    {"keyword":"ClimateTech","quarter":"2025-Q3","keyword_pct":1.6},
    {"keyword":"BioTech","quarter":"2025-Q3","keyword_pct":0.5},
    {"keyword":"AgentAI","quarter":"2025-Q3","keyword_pct":7.86},
    // 2025-Q4
    {"keyword":"LLM","quarter":"2025-Q4","keyword_pct":5.0},
    {"keyword":"MedTech","quarter":"2025-Q4","keyword_pct":0.5},
    {"keyword":"Web3","quarter":"2025-Q4","keyword_pct":2.77},
    {"keyword":"MobilityTech","quarter":"2025-Q4","keyword_pct":0.9},
    {"keyword":"SpaceTech","quarter":"2025-Q4","keyword_pct":1.93},
    {"keyword":"QuantumTech","quarter":"2025-Q4","keyword_pct":1.27},
    {"keyword":"Robotics","quarter":"2025-Q4","keyword_pct":5.87},
    {"keyword":"Semiconductors","quarter":"2025-Q4","keyword_pct":9.63},
    {"keyword":"Infrastructure","quarter":"2025-Q4","keyword_pct":3.3},
    {"keyword":"PhysicalAI","quarter":"2025-Q4","keyword_pct":1.8},
    {"keyword":"HealthTech","quarter":"2025-Q4","keyword_pct":1.27},
    {"keyword":"Ecommerce","quarter":"2025-Q4","keyword_pct":0.7},
    {"keyword":"GameTech","quarter":"2025-Q4","keyword_pct":0.5},
    {"keyword":"FinTech","quarter":"2025-Q4","keyword_pct":3.03},
    {"keyword":"Enterprise","quarter":"2025-Q4","keyword_pct":1.2},
    {"keyword":"DefenseTech","quarter":"2025-Q4","keyword_pct":1.1},
    {"keyword":"Cybersecurity","quarter":"2025-Q4","keyword_pct":1.73},
    {"keyword":"ClimateTech","quarter":"2025-Q4","keyword_pct":2.33},
    {"keyword":"BioTech","quarter":"2025-Q4","keyword_pct":1.1},
    {"keyword":"AgriTech","quarter":"2025-Q4","keyword_pct":0.5},
    {"keyword":"AgentAI","quarter":"2025-Q4","keyword_pct":9.17},
    {"keyword":"GenAI","quarter":"2025-Q4","keyword_pct":9.7},
    // 2026-Q1
    {"keyword":"LLM","quarter":"2026-Q1","keyword_pct":6.85},
    {"keyword":"MedTech","quarter":"2026-Q1","keyword_pct":1.1},
    {"keyword":"MobilityTech","quarter":"2026-Q1","keyword_pct":1.7},
    {"keyword":"Semiconductors","quarter":"2026-Q1","keyword_pct":7.55},
    {"keyword":"QuantumTech","quarter":"2026-Q1","keyword_pct":1.6},
    {"keyword":"Robotics","quarter":"2026-Q1","keyword_pct":6.22},
    {"keyword":"Infrastructure","quarter":"2026-Q1","keyword_pct":0.95},
    {"keyword":"PhysicalAI","quarter":"2026-Q1","keyword_pct":1.55},
    {"keyword":"HealthTech","quarter":"2026-Q1","keyword_pct":3.0},
    {"keyword":"DigitalHealth","quarter":"2026-Q1","keyword_pct":0.6},
    {"keyword":"FinTech","quarter":"2026-Q1","keyword_pct":1.45},
    {"keyword":"Enterprise","quarter":"2026-Q1","keyword_pct":0.6},
    {"keyword":"Ecommerce","quarter":"2026-Q1","keyword_pct":2.1},
    {"keyword":"DefenseTech","quarter":"2026-Q1","keyword_pct":3.97},
    {"keyword":"CreatorEconomy","quarter":"2026-Q1","keyword_pct":0.6},
    {"keyword":"ClimateTech","quarter":"2026-Q1","keyword_pct":0.8},
    {"keyword":"BioTech","quarter":"2026-Q1","keyword_pct":0.6},
    {"keyword":"AgentAI","quarter":"2026-Q1","keyword_pct":8.53},
    {"keyword":"SpaceTech","quarter":"2026-Q1","keyword_pct":1.7},
    {"keyword":"GenAI","quarter":"2026-Q1","keyword_pct":13.9},
    {"keyword":"Web3","quarter":"2026-Q1","keyword_pct":4.85}
  ]
};

// ===== CONFIG =====
const MAX_KEYWORDS = 5;
let selectedKeywords = [];

// ===== DOM =====
const els = {
  list: document.getElementById('keywordsList'),
  legend: document.getElementById('trendLegend'),
  chart: document.getElementById('trendChart'),
  wrapper: document.getElementById('chartWrapper'),
  empty: document.getElementById('emptyState'),
  warning: document.getElementById('warningMsg'),
  topBtn: document.getElementById('selectTopBtn'),
  resetBtn: document.getElementById('resetBtn'),
};

// ===== HELPERS =====
function getAllKeywords() {
  return [...new Set(trendData.data.map(d => d.keyword))].sort();
}

function getAllQuarters() {
  return [...new Set(trendData.data.map(d => d.quarter))].sort((a, b) => {
    const [yA, qA] = a.split('-Q').map(Number);
    const [yB, qB] = b.split('-Q').map(Number);
    return yA !== yB ? yA - yB : qA - qB;
  });
}

function getDataForKeyword(kw) {
  return trendData.data.filter(d => d.keyword === kw).sort((a, b) => {
    const [yA, qA] = a.quarter.split('-Q').map(Number);
    const [yB, qB] = b.quarter.split('-Q').map(Number);
    return yA !== yB ? yA - yB : qA - qB;
  });
}

function median(arr) {
  if (!arr.length) return NaN;
  const s = [...arr].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 === 0 ? (s[m - 1] + s[m]) / 2 : s[m];
}

function percentile(arr, p) {
  if (!arr.length) return NaN;
  const s = [...arr].sort((a, b) => a - b);
  const i = (p / 100) * (s.length - 1);
  const lo = Math.floor(i), hi = Math.ceil(i), w = i - lo;
  return lo === hi ? s[lo] : s[lo] * (1 - w) + s[hi] * w;
}

function allLastValues() {
  return getAllKeywords().map(kw => {
    const d = getDataForKeyword(kw);
    return d.length ? d[d.length - 1].keyword_pct : 0;
  });
}

function classifyTrend(values) {
  if (!values || values.length < 2) return { label: 'Stable', emoji: '😴', momentum: 0 };

  const last = values[values.length - 1];
  const recent = values.slice(-4);
  let momentum = 0;
  if (recent.length >= 2) {
    let total = 0;
    for (let i = 1; i < recent.length; i++) total += recent[i] - recent[i - 1];
    momentum = total / (recent.length - 1);
  }

  const all = allLastValues();
  if (!all.length) return momentum > 0.15
    ? { label: 'Rising', emoji: '✨', momentum }
    : { label: 'Stable', emoji: '😴', momentum };

  const p75 = percentile(all, 75);
  const med = median(all);

  if (momentum < -0.3) return { label: 'Declining', emoji: '📉', momentum };
  if (last > p75 && momentum > 0.3) return { label: 'Hot', emoji: '🔥', momentum };
  if (last > p75 && momentum >= -0.3 && momentum <= 0.3) return { label: 'Stable', emoji: '😴', momentum };
  if (last < med && momentum > 0.3) return { label: 'Rising', emoji: '✨', momentum };
  if (momentum > 0.15) return { label: 'Rising', emoji: '✨', momentum };
  return { label: 'Stable', emoji: '😴', momentum };
}

function badgeClass(label) {
  const map = { rising: '--rising', hot: '--hot', declining: '--declining', stable: '--stable' };
  const key = (label || '').toLowerCase();
  for (const [k, v] of Object.entries(map)) if (key.includes(k)) return `trend-badge${v}`;
  return 'trend-badge--stable';
}

// ===== KEYWORD COLORS (dark-theme optimized) =====
function buildKeywordColors() {
  const keywords = getAllKeywords();
  const colors = {};
  const GOLDEN = 137.508;
  keywords.forEach((kw, i) => {
    const hue = Math.round((i * GOLDEN) % 360);
    colors[kw] = `hsl(${hue}, 65%, 58%)`;
  });
  return colors;
}
const keywordColors = buildKeywordColors();

// ===== RENDER LEGEND =====
function renderLegend(usedLabels) {
  const items = [
    { label: 'Rising', emoji: '✨', css: 'rising', desc: 'moderat & wächst' },
    { label: 'Hot', emoji: '🔥', css: 'hot', desc: 'hoch & wächst' },
    { label: 'Stable', emoji: '😴', css: 'stable', desc: 'keine klare Bewegung' },
    { label: 'Declining', emoji: '📉', css: 'declining', desc: 'Aufmerksamkeit sinkt' },
  ];

  els.legend.innerHTML = '<span class="trend-legend-label">Legende:</span>';
  items.filter(it => usedLabels.has(it.label)).forEach(it => {
    const span = document.createElement('span');
    span.className = `trend-badge trend-badge--${it.css}`;
    span.textContent = `${it.emoji} ${it.label} — ${it.desc}`;
    els.legend.appendChild(span);
  });
}

// ===== POPULATE KEYWORDS =====
function populateKeywords() {
  const keywords = getAllKeywords();
  const classified = keywords.map(kw => {
    const data = getDataForKeyword(kw);
    const values = data.map(d => d.keyword_pct);
    const trend = classifyTrend(values);
    return { kw, trend, display: `${trend.emoji} ${trend.label}` };
  });

  const usedLabels = new Set(classified.map(c => c.trend.label));
  renderLegend(usedLabels);

  const order = { Rising: 0, Hot: 1, Stable: 2, Declining: 3 };
  classified.sort((a, b) => {
    const oa = order[a.trend.label] ?? 6, ob = order[b.trend.label] ?? 6;
    return oa !== ob ? oa - ob : a.kw.localeCompare(b.kw);
  });

  els.list.innerHTML = '';
  classified.forEach(({ kw, trend, display }) => {
    const div = document.createElement('div');
    div.className = 'kw-item';
    div.innerHTML = `
      <input type="checkbox" id="kw-${kw}" value="${kw}">
      <label for="kw-${kw}">${kw} <span class="trend-badge ${badgeClass(trend.label)}">${display}</span></label>
    `;
    div.querySelector('input').addEventListener('change', onCheckboxChange);
    els.list.appendChild(div);
  });

  // Pre-select first
  if (classified.length) {
    const first = document.getElementById(`kw-${classified[0].kw}`);
    if (first) { first.checked = true; selectedKeywords = [classified[0].kw]; }
  }
}

// ===== CHECKBOX LOGIC =====
function updateCheckboxStates() {
  const checked = document.querySelectorAll('.kw-item input:checked');
  const atMax = checked.length >= MAX_KEYWORDS;
  document.querySelectorAll('.kw-item').forEach(item => {
    const cb = item.querySelector('input');
    if (atMax && !cb.checked) {
      item.classList.add('disabled');
      cb.disabled = true;
    } else {
      item.classList.remove('disabled');
      cb.disabled = false;
    }
  });
}

function onCheckboxChange(e) {
  const currentChecked = document.querySelectorAll('.kw-item input:checked').length;
  if (e.target.checked && currentChecked > MAX_KEYWORDS) {
    e.target.checked = false;
    showWarning(`⚠️ Max. ${MAX_KEYWORDS} Trends gleichzeitig. Bitte zuerst einen abwählen.`);
    return;
  }
  selectedKeywords = [...document.querySelectorAll('.kw-item input:checked')].map(cb => cb.value);
  hideWarning();
  updateCheckboxStates();
  updateChart();
}

function showWarning(msg) { els.warning.textContent = msg; els.warning.style.display = 'block'; }
function hideWarning() { els.warning.style.display = 'none'; }

// ===== BUTTONS =====
els.topBtn.addEventListener('click', () => {
  const keywords = getAllKeywords().slice(0, MAX_KEYWORDS);
  document.querySelectorAll('.kw-item input').forEach(cb => cb.checked = false);
  keywords.forEach(kw => {
    const cb = document.getElementById(`kw-${kw}`);
    if (cb) cb.checked = true;
  });
  selectedKeywords = keywords;
  hideWarning();
  updateCheckboxStates();
  updateChart();
});

els.resetBtn.addEventListener('click', () => {
  document.querySelectorAll('.kw-item input').forEach(cb => { cb.checked = false; cb.disabled = false; });
  document.querySelectorAll('.kw-item').forEach(item => item.classList.remove('disabled'));
  const first = document.querySelector('.kw-item input');
  if (first) { first.checked = true; selectedKeywords = [first.value]; }
  hideWarning();
  updateCheckboxStates();
  updateChart();
});

// ===== CHART =====
function updateChart() {
  if (!selectedKeywords.length) {
    els.empty.style.display = 'block';
    els.wrapper.style.display = 'none';
    return;
  }
  els.empty.style.display = 'none';
  els.wrapper.style.display = 'block';

  const quarters = getAllQuarters();
  const traces = selectedKeywords.map(kw => {
    const data = getDataForKeyword(kw);
    const byQ = {};
    data.forEach(d => byQ[d.quarter] = d.keyword_pct);
    const yValues = quarters.map(q => byQ[q] || 0);
    const cleanValues = data.map(d => d.keyword_pct);
    const trend = classifyTrend(cleanValues);
    const color = keywordColors[kw] || '#8B949E';

    return {
      x: quarters,
      y: yValues,
      mode: 'lines+markers',
      name: `${kw} ${trend.emoji} ${trend.label}`,
      type: 'scatter',
      line: { color, width: 2.5 },
      marker: { size: 5 },
      hovertemplate:
        `<b>${kw} ${trend.emoji}</b><br>` +
        `Q: %{x}<br>` +
        `Attention Share: %{y:.2f}%<br>` +
        `Momentum: ${trend.momentum >= 0 ? '+' : ''}${trend.momentum.toFixed(2)}%/Q<br>` +
        `<extra></extra>`
    };
  });

  const title = selectedKeywords.length === 1
    ? `Trendentwicklung: ${selectedKeywords[0]}`
    : 'Keyword Trend Comparison (Quarterly)';

  const layout = {
    title: { text: title, font: { size: 16, color: '#E6EDF3', family: 'DM Sans' } },
    xaxis: {
      title: { text: 'Quartal', font: { color: '#8B949E' } },
      tickangle: -45,
      tickfont: { color: '#8B949E', size: 11 },
      gridcolor: 'rgba(255,255,255,0.06)',
      linecolor: 'rgba(255,255,255,0.1)',
    },
    yaxis: {
      title: { text: 'Attention Share (%)', font: { color: '#8B949E' } },
      tickfont: { color: '#8B949E', size: 11 },
      gridcolor: 'rgba(255,255,255,0.06)',
      zeroline: false,
    },
    hovermode: 'closest',
    margin: { l: 60, r: 20, t: 60, b: 80 },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
    legend: {
      orientation: 'h',
      x: 0, y: -0.25,
      font: { color: '#8B949E', size: 12 },
      bgcolor: 'rgba(0,0,0,0)',
    },
    font: { family: 'DM Sans, sans-serif' },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
    displaylogo: false,
  };

  Plotly.newPlot(els.chart, traces, layout, config);
}

// ===== INIT =====
window.addEventListener('DOMContentLoaded', () => {
  populateKeywords();
  updateChart();
});
