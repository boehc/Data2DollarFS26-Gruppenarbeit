import { useState } from "react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, ScatterChart, Scatter, ReferenceLine, Label, ComposedChart } from "recharts";

/* ════════════════════════════════════════════
   DATA
   ════════════════════════════════════════════ */
const TOTALS=[{quarter:"2023-Q1",total_deals:119,total_funding_chf_m:6183.9},{quarter:"2023-Q2",total_deals:90,total_funding_chf_m:4605.4},{quarter:"2023-Q3",total_deals:82,total_funding_chf_m:8526.1},{quarter:"2023-Q4",total_deals:106,total_funding_chf_m:3195.9},{quarter:"2024-Q1",total_deals:96,total_funding_chf_m:5003.8},{quarter:"2024-Q2",total_deals:102,total_funding_chf_m:5791.3},{quarter:"2024-Q3",total_deals:105,total_funding_chf_m:2861.1},{quarter:"2024-Q4",total_deals:98,total_funding_chf_m:4227.4},{quarter:"2025-Q1",total_deals:110,total_funding_chf_m:8280.9},{quarter:"2025-Q2",total_deals:69,total_funding_chf_m:2774.9},{quarter:"2025-Q3",total_deals:122,total_funding_chf_m:6409.0},{quarter:"2025-Q4",total_deals:117,total_funding_chf_m:8736.4},{quarter:"2026-Q1",total_deals:106,total_funding_chf_m:8916.1}];

const F1_TOP5=[{quarter:"2023-Q1",BioTech:32,FinTech:46,ClimateTech:16,HealthTech:6,GenAI:2,Übrige:17},{quarter:"2023-Q2",BioTech:25,FinTech:29,ClimateTech:20,HealthTech:3,GenAI:3,Übrige:10},{quarter:"2023-Q3",BioTech:22,FinTech:33,ClimateTech:13,HealthTech:2,GenAI:1,Übrige:11},{quarter:"2023-Q4",BioTech:31,FinTech:38,ClimateTech:18,HealthTech:6,GenAI:1,Übrige:12},{quarter:"2024-Q1",BioTech:43,FinTech:23,ClimateTech:7,HealthTech:3,GenAI:1,Übrige:19},{quarter:"2024-Q2",BioTech:31,FinTech:40,ClimateTech:13,HealthTech:2,GenAI:4,Übrige:12},{quarter:"2024-Q3",BioTech:32,FinTech:37,ClimateTech:11,HealthTech:2,GenAI:3,Übrige:20},{quarter:"2024-Q4",BioTech:30,FinTech:33,ClimateTech:17,HealthTech:3,GenAI:5,Übrige:10},{quarter:"2025-Q1",BioTech:36,FinTech:39,ClimateTech:15,HealthTech:6,GenAI:3,Übrige:11},{quarter:"2025-Q2",BioTech:24,FinTech:20,ClimateTech:4,HealthTech:5,GenAI:1,Übrige:15},{quarter:"2025-Q3",BioTech:34,FinTech:51,ClimateTech:12,HealthTech:1,GenAI:5,Übrige:19},{quarter:"2025-Q4",BioTech:35,FinTech:41,ClimateTech:10,HealthTech:5,GenAI:8,Übrige:18},{quarter:"2026-Q1",BioTech:38,FinTech:35,ClimateTech:13,HealthTech:4,GenAI:5,Übrige:11}];

const F1_SM={"AgriTech":[{q:"23Q1",d:1},{q:"23Q2",d:1},{q:"23Q3",d:1},{q:"23Q4",d:0},{q:"24Q1",d:2},{q:"24Q2",d:1},{q:"24Q3",d:2},{q:"24Q4",d:1},{q:"25Q1",d:1},{q:"25Q2",d:1},{q:"25Q3",d:0},{q:"25Q4",d:3},{q:"26Q1",d:0}],"BioTech":[{q:"23Q1",d:32},{q:"23Q2",d:25},{q:"23Q3",d:22},{q:"23Q4",d:31},{q:"24Q1",d:43},{q:"24Q2",d:31},{q:"24Q3",d:32},{q:"24Q4",d:30},{q:"25Q1",d:36},{q:"25Q2",d:24},{q:"25Q3",d:34},{q:"25Q4",d:35},{q:"26Q1",d:38}],"ClimateTech":[{q:"23Q1",d:16},{q:"23Q2",d:20},{q:"23Q3",d:13},{q:"23Q4",d:18},{q:"24Q1",d:7},{q:"24Q2",d:13},{q:"24Q3",d:11},{q:"24Q4",d:17},{q:"25Q1",d:15},{q:"25Q2",d:4},{q:"25Q3",d:12},{q:"25Q4",d:10},{q:"26Q1",d:13}],"Cybersecurity":[{q:"23Q1",d:0},{q:"23Q2",d:0},{q:"23Q3",d:1},{q:"23Q4",d:2},{q:"24Q1",d:0},{q:"24Q2",d:0},{q:"24Q3",d:1},{q:"24Q4",d:0},{q:"25Q1",d:0},{q:"25Q2",d:0},{q:"25Q3",d:0},{q:"25Q4",d:2},{q:"26Q1",d:0}],"Ecommerce":[{q:"23Q1",d:0},{q:"23Q2",d:2},{q:"23Q3",d:1},{q:"23Q4",d:2},{q:"24Q1",d:1},{q:"24Q2",d:1},{q:"24Q3",d:2},{q:"24Q4",d:0},{q:"25Q1",d:1},{q:"25Q2",d:3},{q:"25Q3",d:3},{q:"25Q4",d:0},{q:"26Q1",d:3}],"EdTech":[{q:"23Q1",d:0},{q:"23Q2",d:0},{q:"23Q3",d:2},{q:"23Q4",d:1},{q:"24Q1",d:2},{q:"24Q2",d:0},{q:"24Q3",d:0},{q:"24Q4",d:0},{q:"25Q1",d:0},{q:"25Q2",d:0},{q:"25Q3",d:1},{q:"25Q4",d:0},{q:"26Q1",d:0}],"Enterprise":[{q:"23Q1",d:5},{q:"23Q2",d:1},{q:"23Q3",d:3},{q:"23Q4",d:1},{q:"24Q1",d:3},{q:"24Q2",d:2},{q:"24Q3",d:3},{q:"24Q4",d:3},{q:"25Q1",d:1},{q:"25Q2",d:0},{q:"25Q3",d:1},{q:"25Q4",d:1},{q:"26Q1",d:4}],"FinTech":[{q:"23Q1",d:46},{q:"23Q2",d:29},{q:"23Q3",d:33},{q:"23Q4",d:38},{q:"24Q1",d:23},{q:"24Q2",d:40},{q:"24Q3",d:37},{q:"24Q4",d:33},{q:"25Q1",d:39},{q:"25Q2",d:20},{q:"25Q3",d:51},{q:"25Q4",d:41},{q:"26Q1",d:35}],"GenAI":[{q:"23Q1",d:2},{q:"23Q2",d:3},{q:"23Q3",d:1},{q:"23Q4",d:1},{q:"24Q1",d:1},{q:"24Q2",d:4},{q:"24Q3",d:3},{q:"24Q4",d:5},{q:"25Q1",d:3},{q:"25Q2",d:1},{q:"25Q3",d:5},{q:"25Q4",d:8},{q:"26Q1",d:5}],"HealthTech":[{q:"23Q1",d:6},{q:"23Q2",d:3},{q:"23Q3",d:2},{q:"23Q4",d:6},{q:"24Q1",d:3},{q:"24Q2",d:2},{q:"24Q3",d:2},{q:"24Q4",d:3},{q:"25Q1",d:6},{q:"25Q2",d:5},{q:"25Q3",d:1},{q:"25Q4",d:5},{q:"26Q1",d:4}],"MedTech":[{q:"23Q1",d:6},{q:"23Q2",d:3},{q:"23Q3",d:3},{q:"23Q4",d:2},{q:"24Q1",d:9},{q:"24Q2",d:3},{q:"24Q3",d:9},{q:"24Q4",d:5},{q:"25Q1",d:3},{q:"25Q2",d:7},{q:"25Q3",d:8},{q:"25Q4",d:3},{q:"26Q1",d:4}],"PropTech":[{q:"23Q1",d:2},{q:"23Q2",d:2},{q:"23Q3",d:0},{q:"23Q4",d:1},{q:"24Q1",d:1},{q:"24Q2",d:1},{q:"24Q3",d:1},{q:"24Q4",d:0},{q:"25Q1",d:0},{q:"25Q2",d:1},{q:"25Q3",d:2},{q:"25Q4",d:4},{q:"26Q1",d:0}],"Robotics":[{q:"23Q1",d:1},{q:"23Q2",d:1},{q:"23Q3",d:0},{q:"23Q4",d:2},{q:"24Q1",d:1},{q:"24Q2",d:3},{q:"24Q3",d:2},{q:"24Q4",d:1},{q:"25Q1",d:5},{q:"25Q2",d:3},{q:"25Q3",d:4},{q:"25Q4",d:5},{q:"26Q1",d:0}],"SpaceTech":[{q:"23Q1",d:2},{q:"23Q2",d:0},{q:"23Q3",d:0},{q:"23Q4",d:1},{q:"24Q1",d:0},{q:"24Q2",d:1},{q:"24Q3",d:0},{q:"24Q4",d:0},{q:"25Q1",d:0},{q:"25Q2",d:0},{q:"25Q3",d:0},{q:"25Q4",d:0},{q:"26Q1",d:0}]};

const FV_SM={"AgriTech":[{q:"23Q1",f:0},{q:"23Q2",f:0},{q:"23Q3",f:0},{q:"23Q4",f:0},{q:"24Q1",f:0},{q:"24Q2",f:0},{q:"24Q3",f:0},{q:"24Q4",f:0},{q:"25Q1",f:0},{q:"25Q2",f:0},{q:"25Q3",f:0},{q:"25Q4",f:0},{q:"26Q1",f:0}],"BioTech":[{q:"23Q1",f:2201},{q:"23Q2",f:1745},{q:"23Q3",f:2501},{q:"23Q4",f:1150},{q:"24Q1",f:2761},{q:"24Q2",f:2205},{q:"24Q3",f:1212},{q:"24Q4",f:1543},{q:"25Q1",f:3036},{q:"25Q2",f:1188},{q:"25Q3",f:2611},{q:"25Q4",f:3280},{q:"26Q1",f:2934}],"ClimateTech":[{q:"23Q1",f:1333},{q:"23Q2",f:76},{q:"23Q3",f:1022},{q:"23Q4",f:962},{q:"24Q1",f:235},{q:"24Q2",f:451},{q:"24Q3",f:10},{q:"24Q4",f:200},{q:"25Q1",f:120},{q:"25Q2",f:68},{q:"25Q3",f:272},{q:"25Q4",f:286},{q:"26Q1",f:1456}],"Cybersecurity":[{q:"23Q1",f:68},{q:"23Q2",f:0},{q:"23Q3",f:583},{q:"23Q4",f:8},{q:"24Q1",f:5},{q:"24Q2",f:72},{q:"24Q3",f:14},{q:"24Q4",f:208},{q:"25Q1",f:40},{q:"25Q2",f:14},{q:"25Q3",f:267},{q:"25Q4",f:18},{q:"26Q1",f:78}],"EdTech":[{q:"23Q1",f:58},{q:"23Q2",f:185},{q:"23Q3",f:182},{q:"23Q4",f:25},{q:"24Q1",f:252},{q:"24Q2",f:39},{q:"24Q3",f:282},{q:"24Q4",f:445},{q:"25Q1",f:920},{q:"25Q2",f:106},{q:"25Q3",f:221},{q:"25Q4",f:645},{q:"26Q1",f:1691}],"Enterprise":[{q:"23Q1",f:7},{q:"23Q2",f:0},{q:"23Q3",f:58},{q:"23Q4",f:1},{q:"24Q1",f:0},{q:"24Q2",f:0},{q:"24Q3",f:0},{q:"24Q4",f:23},{q:"25Q1",f:0},{q:"25Q2",f:0},{q:"25Q3",f:0},{q:"25Q4",f:0},{q:"26Q1",f:80}],"FinTech":[{q:"23Q1",f:1968},{q:"23Q2",f:1646},{q:"23Q3",f:1917},{q:"23Q4",f:422},{q:"24Q1",f:985},{q:"24Q2",f:2229},{q:"24Q3",f:656},{q:"24Q4",f:900},{q:"25Q1",f:2792},{q:"25Q2",f:815},{q:"25Q3",f:1661},{q:"25Q4",f:1420},{q:"26Q1",f:1620}],"GenAI":[{q:"23Q1",f:5},{q:"23Q2",f:173},{q:"23Q3",f:0},{q:"23Q4",f:41},{q:"24Q1",f:20},{q:"24Q2",f:51},{q:"24Q3",f:21},{q:"24Q4",f:3},{q:"25Q1",f:7},{q:"25Q2",f:0},{q:"25Q3",f:278},{q:"25Q4",f:95},{q:"26Q1",f:89}],"HealthTech":[{q:"23Q1",f:486},{q:"23Q2",f:395},{q:"23Q3",f:1321},{q:"23Q4",f:130},{q:"24Q1",f:502},{q:"24Q2",f:480},{q:"24Q3",f:286},{q:"24Q4",f:456},{q:"25Q1",f:1221},{q:"25Q2",f:544},{q:"25Q3",f:174},{q:"25Q4",f:2180},{q:"26Q1",f:601}],"MedTech":[{q:"23Q1",f:23},{q:"23Q2",f:139},{q:"23Q3",f:18},{q:"23Q4",f:5},{q:"24Q1",f:54},{q:"24Q2",f:11},{q:"24Q3",f:196},{q:"24Q4",f:24},{q:"25Q1",f:3},{q:"25Q2",f:10},{q:"25Q3",f:26},{q:"25Q4",f:163},{q:"26Q1",f:156}],"PropTech":[{q:"23Q1",f:19},{q:"23Q2",f:10},{q:"23Q3",f:916},{q:"23Q4",f:434},{q:"24Q1",f:9},{q:"24Q2",f:24},{q:"24Q3",f:31},{q:"24Q4",f:69},{q:"25Q1",f:112},{q:"25Q2",f:6},{q:"25Q3",f:282},{q:"25Q4",f:257},{q:"26Q1",f:32}],"Robotics":[{q:"23Q1",f:16},{q:"23Q2",f:237},{q:"23Q3",f:9},{q:"23Q4",f:13},{q:"24Q1",f:180},{q:"24Q2",f:229},{q:"24Q3",f:153},{q:"24Q4",f:357},{q:"25Q1",f:31},{q:"25Q2",f:24},{q:"25Q3",f:618},{q:"25Q4",f:394},{q:"26Q1",f:180}],"SpaceTech":[{q:"23Q1",f:0},{q:"23Q2",f:0},{q:"23Q3",f:0},{q:"23Q4",f:6},{q:"24Q1",f:0},{q:"24Q2",f:2},{q:"24Q3",f:0},{q:"24Q4",f:0},{q:"25Q1",f:0},{q:"25Q2",f:0},{q:"25Q3",f:0},{q:"25Q4",f:0},{q:"26Q1",f:0}],"Ecommerce":[{q:"23Q1",f:0},{q:"23Q2",f:0},{q:"23Q3",f:0},{q:"23Q4",f:0},{q:"24Q1",f:0},{q:"24Q2",f:0},{q:"24Q3",f:0},{q:"24Q4",f:0},{q:"25Q1",f:0},{q:"25Q2",f:0},{q:"25Q3",f:0},{q:"25Q4",f:0},{q:"26Q1",f:0}]};

const STAGES=[{quarter:"2023-Q1","Pre-Seed":16,Seed:42,"Series A":24,"Series B":14,"Series C+":7,Strategic:5,Grant:5,Award:47,Sonstige:66},{quarter:"2023-Q2","Pre-Seed":17,Seed:31,"Series A":8,"Series B":3,"Series C+":6,Strategic:7,Grant:4,Award:36,Sonstige:53},{quarter:"2023-Q3","Pre-Seed":16,Seed:35,"Series A":18,"Series B":3,"Series C+":4,Strategic:0,Grant:4,Award:19,Sonstige:56},{quarter:"2023-Q4","Pre-Seed":7,Seed:51,"Series A":22,"Series B":3,"Series C+":6,Strategic:1,Grant:1,Award:33,Sonstige:63},{quarter:"2024-Q1","Pre-Seed":17,Seed:28,"Series A":30,"Series B":14,"Series C+":3,Strategic:5,Grant:2,Award:36,Sonstige:69},{quarter:"2024-Q2","Pre-Seed":15,Seed:52,"Series A":16,"Series B":4,"Series C+":12,Strategic:3,Grant:0,Award:18,Sonstige:61},{quarter:"2024-Q3","Pre-Seed":18,Seed:29,"Series A":13,"Series B":14,"Series C+":2,Strategic:7,Grant:3,Award:53,Sonstige:76},{quarter:"2024-Q4","Pre-Seed":12,Seed:38,"Series A":23,"Series B":10,"Series C+":5,Strategic:4,Grant:1,Award:20,Sonstige:57},{quarter:"2025-Q1","Pre-Seed":16,Seed:37,"Series A":23,"Series B":3,"Series C+":2,Strategic:4,Grant:5,Award:36,Sonstige:61},{quarter:"2025-Q2","Pre-Seed":8,Seed:23,"Series A":19,"Series B":6,"Series C+":0,Strategic:3,Grant:3,Award:26,Sonstige:45},{quarter:"2025-Q3","Pre-Seed":21,Seed:37,"Series A":21,"Series B":3,"Series C+":4,Strategic:10,Grant:5,Award:47,Sonstige:73},{quarter:"2025-Q4","Pre-Seed":16,Seed:29,"Series A":14,"Series B":6,"Series C+":3,Strategic:12,Grant:8,Award:42,Sonstige:66},{quarter:"2026-Q1","Pre-Seed":22,Seed:47,"Series A":17,"Series B":7,"Series C+":6,Strategic:10,Grant:2,Award:28,Sonstige:64}];

const NEWS_IND=[{quarter:"2023-Q1",FinTech:40,HealthTech:13,ClimateTech:8,BioTech:2,Ecommerce:9,DefenseTech:10,SpaceTech:1,MedTech:3,Enterprise:2,MobilityTech:2,EdTech:0,PropTech:1,AgriTech:0},{quarter:"2023-Q2",FinTech:27,HealthTech:14,ClimateTech:12,BioTech:4,Ecommerce:9,DefenseTech:7,SpaceTech:2,MedTech:1,Enterprise:0,MobilityTech:0,EdTech:2,PropTech:1,AgriTech:2},{quarter:"2023-Q3",FinTech:31,HealthTech:13,ClimateTech:4,BioTech:3,Ecommerce:3,DefenseTech:7,SpaceTech:1,MedTech:0,Enterprise:3,MobilityTech:1,EdTech:2,PropTech:1,AgriTech:1},{quarter:"2023-Q4",FinTech:21,HealthTech:17,ClimateTech:13,BioTech:4,Ecommerce:5,DefenseTech:6,SpaceTech:1,MedTech:2,Enterprise:0,MobilityTech:3,EdTech:1,PropTech:1,AgriTech:1},{quarter:"2024-Q1",FinTech:22,HealthTech:9,ClimateTech:4,BioTech:6,Ecommerce:2,DefenseTech:7,SpaceTech:1,MedTech:1,Enterprise:2,MobilityTech:2,EdTech:1,PropTech:1,AgriTech:0},{quarter:"2024-Q2",FinTech:18,HealthTech:10,ClimateTech:10,BioTech:2,Ecommerce:0,DefenseTech:7,SpaceTech:2,MedTech:0,Enterprise:0,MobilityTech:2,EdTech:1,PropTech:0,AgriTech:0},{quarter:"2024-Q3",FinTech:18,HealthTech:10,ClimateTech:9,BioTech:6,Ecommerce:1,DefenseTech:12,SpaceTech:1,MedTech:0,Enterprise:0,MobilityTech:0,EdTech:0,PropTech:1,AgriTech:0},{quarter:"2024-Q4",FinTech:17,HealthTech:10,ClimateTech:10,BioTech:10,Ecommerce:2,DefenseTech:11,SpaceTech:2,MedTech:0,Enterprise:0,MobilityTech:3,EdTech:0,PropTech:1,AgriTech:1},{quarter:"2025-Q1",FinTech:22,HealthTech:6,ClimateTech:5,BioTech:9,Ecommerce:3,DefenseTech:11,SpaceTech:1,MedTech:0,Enterprise:0,MobilityTech:4,EdTech:1,PropTech:0,AgriTech:0},{quarter:"2025-Q2",FinTech:18,HealthTech:5,ClimateTech:1,BioTech:0,Ecommerce:1,DefenseTech:6,SpaceTech:1,MedTech:0,Enterprise:0,MobilityTech:5,EdTech:0,PropTech:1,AgriTech:0},{quarter:"2025-Q3",FinTech:13,HealthTech:5,ClimateTech:3,BioTech:1,Ecommerce:1,DefenseTech:13,SpaceTech:4,MedTech:0,Enterprise:0,MobilityTech:5,EdTech:0,PropTech:0,AgriTech:0},{quarter:"2025-Q4",FinTech:17,HealthTech:7,ClimateTech:6,BioTech:2,Ecommerce:4,DefenseTech:6,SpaceTech:3,MedTech:1,Enterprise:2,MobilityTech:5,EdTech:0,PropTech:0,AgriTech:1},{quarter:"2026-Q1",FinTech:4,HealthTech:8,ClimateTech:1,BioTech:1,Ecommerce:3,DefenseTech:9,SpaceTech:3,MedTech:2,Enterprise:1,MobilityTech:3,EdTech:0,PropTech:0,AgriTech:0}];

const NEWS_TECH=[{quarter:"2023-Q1",GenAI:99,LLM:41,Cybersecurity:40,Web3:54,Semiconductors:19,Robotics:17,Infrastructure:11,AgentAI:0,PhysicalAI:5,QuantumTech:2},{quarter:"2023-Q2",GenAI:138,LLM:74,Cybersecurity:49,Web3:32,Semiconductors:23,Robotics:18,Infrastructure:13,AgentAI:2,PhysicalAI:1,QuantumTech:4},{quarter:"2023-Q3",GenAI:142,LLM:66,Cybersecurity:58,Web3:51,Semiconductors:27,Robotics:24,Infrastructure:12,AgentAI:2,PhysicalAI:5,QuantumTech:6},{quarter:"2023-Q4",GenAI:144,LLM:55,Cybersecurity:49,Web3:18,Semiconductors:23,Robotics:27,Infrastructure:7,AgentAI:3,PhysicalAI:7,QuantumTech:4},{quarter:"2024-Q1",GenAI:134,LLM:61,Cybersecurity:9,Web3:28,Semiconductors:26,Robotics:29,Infrastructure:7,AgentAI:5,PhysicalAI:0,QuantumTech:5},{quarter:"2024-Q2",GenAI:131,LLM:57,Cybersecurity:4,Web3:10,Semiconductors:33,Robotics:23,Infrastructure:10,AgentAI:9,PhysicalAI:3,QuantumTech:1},{quarter:"2024-Q3",GenAI:127,LLM:30,Cybersecurity:2,Web3:11,Semiconductors:20,Robotics:17,Infrastructure:8,AgentAI:10,PhysicalAI:3,QuantumTech:0},{quarter:"2024-Q4",GenAI:115,LLM:43,Cybersecurity:4,Web3:11,Semiconductors:32,Robotics:29,Infrastructure:10,AgentAI:19,PhysicalAI:8,QuantumTech:3},{quarter:"2025-Q1",GenAI:91,LLM:41,Cybersecurity:4,Web3:9,Semiconductors:50,Robotics:25,Infrastructure:11,AgentAI:23,PhysicalAI:5,QuantumTech:5},{quarter:"2025-Q2",GenAI:93,LLM:16,Cybersecurity:1,Web3:11,Semiconductors:24,Robotics:17,Infrastructure:6,AgentAI:33,PhysicalAI:3,QuantumTech:1},{quarter:"2025-Q3",GenAI:91,LLM:30,Cybersecurity:9,Web3:10,Semiconductors:39,Robotics:30,Infrastructure:8,AgentAI:53,PhysicalAI:10,QuantumTech:5},{quarter:"2025-Q4",GenAI:78,LLM:30,Cybersecurity:5,Web3:14,Semiconductors:55,Robotics:32,Infrastructure:18,AgentAI:50,PhysicalAI:7,QuantumTech:7},{quarter:"2026-Q1",GenAI:43,LLM:15,Cybersecurity:0,Web3:9,Semiconductors:20,Robotics:20,Infrastructure:3,AgentAI:35,PhysicalAI:4,QuantumTech:2}];

const MATRIX_A=[{keyword:"BioTech",n25:3.0,d25:32.2,dg:4.7,td:413,n23:3.2,d23:27.5},{keyword:"FinTech",n25:17.5,d25:37.8,dg:1.3,td:465,n23:29.8,d23:36.5},{keyword:"ClimateTech",n25:3.8,d25:10.2,dg:-6.6,td:169,n23:9.2,d23:16.8},{keyword:"HealthTech",n25:5.8,d25:4.2,dg:0.0,td:48,n23:14.2,d23:4.2},{keyword:"MedTech",n25:0.2,d25:5.2,dg:1.7,td:65,n23:1.5,d23:3.5},{keyword:"PropTech",n25:0.2,d25:1.8,dg:0.6,td:15,n23:1.0,d23:1.2},{keyword:"Enterprise",n25:0.5,d25:0.8,dg:-1.7,td:28,n23:1.2,d23:2.5},{keyword:"SpaceTech",n25:2.2,d25:0.01,dg:-0.8,td:4,n23:1.2,d23:0.8},{keyword:"Ecommerce",n25:2.2,d25:1.8,dg:0.6,td:19,n23:6.5,d23:1.2},{keyword:"AgriTech",n25:0.2,d25:1.2,dg:0.4,td:14,n23:1.0,d23:0.8}];

const HEATMAP=[{t:"GenAI",i:"BioTech",n:15},{t:"GenAI",i:"FinTech",n:24},{t:"GenAI",i:"HealthTech",n:18},{t:"GenAI",i:"ClimateTech",n:8},{t:"GenAI",i:"DefenseTech",n:16},{t:"GenAI",i:"Ecommerce",n:6},{t:"GenAI",i:"EdTech",n:1},{t:"GenAI",i:"MedTech",n:0},{t:"LLM",i:"BioTech",n:6},{t:"LLM",i:"FinTech",n:8},{t:"LLM",i:"HealthTech",n:11},{t:"LLM",i:"ClimateTech",n:7},{t:"LLM",i:"DefenseTech",n:4},{t:"LLM",i:"Ecommerce",n:3},{t:"LLM",i:"EdTech",n:0},{t:"LLM",i:"MedTech",n:1},{t:"AgentAI",i:"BioTech",n:0},{t:"AgentAI",i:"FinTech",n:11},{t:"AgentAI",i:"HealthTech",n:5},{t:"AgentAI",i:"ClimateTech",n:0},{t:"AgentAI",i:"DefenseTech",n:4},{t:"AgentAI",i:"Ecommerce",n:3},{t:"AgentAI",i:"EdTech",n:0},{t:"AgentAI",i:"MedTech",n:0},{t:"Robotics",i:"BioTech",n:4},{t:"Robotics",i:"FinTech",n:10},{t:"Robotics",i:"HealthTech",n:11},{t:"Robotics",i:"ClimateTech",n:10},{t:"Robotics",i:"DefenseTech",n:11},{t:"Robotics",i:"Ecommerce",n:1},{t:"Robotics",i:"EdTech",n:0},{t:"Robotics",i:"MedTech",n:1}];

const TECH_DIVE=[{quarter:"2023-Q1",news_GenAI:99,news_LLM:41,news_AgentAI:0,news_Robotics:17,vc_GenAI:2,vc_Robotics:1},{quarter:"2023-Q2",news_GenAI:138,news_LLM:74,news_AgentAI:2,news_Robotics:18,vc_GenAI:3,vc_Robotics:1},{quarter:"2023-Q3",news_GenAI:142,news_LLM:66,news_AgentAI:2,news_Robotics:24,vc_GenAI:1,vc_Robotics:0},{quarter:"2023-Q4",news_GenAI:144,news_LLM:55,news_AgentAI:3,news_Robotics:27,vc_GenAI:1,vc_Robotics:2},{quarter:"2024-Q1",news_GenAI:134,news_LLM:61,news_AgentAI:5,news_Robotics:29,vc_GenAI:1,vc_Robotics:1},{quarter:"2024-Q2",news_GenAI:131,news_LLM:57,news_AgentAI:9,news_Robotics:23,vc_GenAI:4,vc_Robotics:3},{quarter:"2024-Q3",news_GenAI:127,news_LLM:30,news_AgentAI:10,news_Robotics:17,vc_GenAI:3,vc_Robotics:2},{quarter:"2024-Q4",news_GenAI:115,news_LLM:43,news_AgentAI:19,news_Robotics:29,vc_GenAI:5,vc_Robotics:1},{quarter:"2025-Q1",news_GenAI:91,news_LLM:41,news_AgentAI:23,news_Robotics:25,vc_GenAI:3,vc_Robotics:5},{quarter:"2025-Q2",news_GenAI:93,news_LLM:16,news_AgentAI:33,news_Robotics:17,vc_GenAI:1,vc_Robotics:3},{quarter:"2025-Q3",news_GenAI:91,news_LLM:30,news_AgentAI:53,news_Robotics:30,vc_GenAI:5,vc_Robotics:4},{quarter:"2025-Q4",news_GenAI:78,news_LLM:30,news_AgentAI:50,news_Robotics:32,vc_GenAI:8,vc_Robotics:5},{quarter:"2026-Q1",news_GenAI:43,news_LLM:15,news_AgentAI:35,news_Robotics:20,vc_GenAI:5,vc_Robotics:0}];

/* ════════════════════════════════════════════
   COLORS & HELPERS
   ════════════════════════════════════════════ */
const C={BioTech:'#0d9488',FinTech:'#f97316',ClimateTech:'#8b5cf6',HealthTech:'#ec4899',GenAI:'#84cc16',MedTech:'#eab308',Robotics:'#a16207',Cybersecurity:'#6b7280',Enterprise:'#3b82f6',Ecommerce:'#22d3ee',EdTech:'#f43f5e',PropTech:'#fb923c',AgriTech:'#a78bfa',SpaceTech:'#14b8a6',Übrige:'#475569','Pre-Seed':'#a7f3d0',Seed:'#6ee7b7','Series A':'#fbbf24','Series B':'#f97316','Series C+':'#ef4444',Strategic:'#8b5cf6',Grant:'#38bdf8',Award:'#94a3b8',Sonstige:'#334155',DefenseTech:'#dc2626',MobilityTech:'#06b6d4',LLM:'#3b82f6',AgentAI:'#f97316',Semiconductors:'#ef4444',Web3:'#06b6d4',Infrastructure:'#22c55e',PhysicalAI:'#eab308',QuantumTech:'#a855f7'};
const QS=q=>q.replace('20','').replace('-','');

const Tip=({active,payload,label})=>{
  if(!active||!payload?.length)return null;
  const items=payload.filter(p=>p.value>0).sort((a,b)=>b.value-a.value);
  return <div style={{background:'#111827',border:'1px solid #374151',borderRadius:8,padding:'10px 14px',fontSize:11,color:'#d1d5db',maxHeight:280,overflowY:'auto',boxShadow:'0 4px 20px rgba(0,0,0,.5)'}}>
    <div style={{fontWeight:700,marginBottom:6,color:'#f9fafb',fontSize:12}}>{label}</div>
    {items.map((p,i)=><div key={i} style={{display:'flex',gap:8,alignItems:'center',padding:'1px 0'}}>
      <span style={{width:8,height:8,borderRadius:2,background:p.color,flexShrink:0}}/>
      <span style={{flex:1,color:'#9ca3af'}}>{p.name}</span>
      <span style={{fontWeight:600,color:'#f3f4f6',fontVariantNumeric:'tabular-nums'}}>{typeof p.value==='number'&&p.value>=100?Math.round(p.value).toLocaleString():p.value}</span>
    </div>)}
  </div>;
};

const Card=({title,sub,children,h=360})=><div style={{background:'#111827',borderRadius:14,padding:'20px 18px 14px',marginBottom:24,border:'1px solid #1f2937'}}>
  <h3 style={{margin:0,fontSize:14,fontWeight:700,color:'#f3f4f6'}}>{title}</h3>
  {sub&&<p style={{margin:'3px 0 0',fontSize:11,color:'#6b7280'}}>{sub}</p>}
  <div style={{marginTop:14,height:h}}>{children}</div>
</div>;

const Pills=({keys,sel,onSel})=><div style={{display:'flex',flexWrap:'wrap',gap:3,marginBottom:10}}>
  <button onClick={()=>onSel(null)} style={{fontSize:9,padding:'3px 10px',borderRadius:8,border:`1px solid ${!sel?'#6b7280':'#374151'}`,cursor:'pointer',fontFamily:'inherit',background:!sel?'#1f2937':'transparent',color:!sel?'#f3f4f6':'#6b7280',fontWeight:!sel?700:400}}>Alle</button>
  {keys.map(k=><button key={k} onClick={()=>onSel(sel===k?null:k)} style={{fontSize:9,padding:'3px 10px',borderRadius:8,border:`1px solid ${sel===k?C[k]||'#6b7280':'#374151'}`,cursor:'pointer',fontFamily:'inherit',background:sel===k?(C[k]||'#6b7280')+'20':'transparent',color:sel===k?C[k]||'#f3f4f6':'#6b7280',fontWeight:sel===k?700:400}}>
    <span style={{display:'inline-block',width:6,height:6,borderRadius:2,background:C[k]||'#6b7280',marginRight:4,verticalAlign:'middle'}}/>{k}
  </button>)}
</div>;

/* ════════════════════════════════════════════
   COMPONENTS
   ════════════════════════════════════════════ */
const Sparklines=({data,keys,valKey='d',label='Total',unit=''})=><div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill, minmax(195px, 1fr))',gap:10}}>
  {keys.map(kw=>{const d=data[kw]||[];const mx=Math.max(...d.map(r=>r[valKey]),1);const tot=d.reduce((s,r)=>s+r[valKey],0);
    return <div key={kw} style={{background:'#111827',border:'1px solid #1f2937',borderRadius:10,padding:'10px 10px 4px'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'baseline',marginBottom:2}}>
        <span style={{fontSize:11,fontWeight:700,color:C[kw]||'#9ca3af'}}>{kw}</span>
        <span style={{fontSize:9,color:'#6b7280'}}>{unit}{tot>=1000?(tot/1000).toFixed(1)+'k':tot} {label}</span>
      </div>
      <div style={{height:55}}><ResponsiveContainer>
        <AreaChart data={d} margin={{top:2,right:0,bottom:0,left:0}}>
          <Area dataKey={valKey} stroke={C[kw]||'#6b7280'} fill={C[kw]||'#6b7280'} fillOpacity={0.12} strokeWidth={1.5} dot={false}/>
          <YAxis domain={[0,mx]} hide/><XAxis dataKey="q" hide/>
          <Tooltip content={({active,payload})=>{if(!active||!payload?.length)return null;return<div style={{background:'#1f2937',border:'1px solid #374151',borderRadius:6,padding:'4px 8px',fontSize:10,color:'#f3f4f6'}}>{payload[0]?.payload?.q}: <b>{unit}{Math.round(payload[0]?.value).toLocaleString()}</b></div>}}/>
        </AreaChart>
      </ResponsiveContainer></div>
    </div>;
  })}
</div>;

const LineTimeline=({data,keys,title,sub,valKey})=>{
  const [sel,setSel]=useState(null);
  const vis=sel?[sel]:keys;
  return <Card title={title} sub={sub} h={380}>
    <Pills keys={keys} sel={sel} onSel={setSel}/>
    <div style={{height:300}}><ResponsiveContainer>
      <LineChart data={data} margin={{top:5,right:10,bottom:30,left:10}}>
        <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
        <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
        <YAxis tick={{fontSize:9,fill:'#6b7280'}}/>
        <Tooltip content={<Tip/>}/>
        {vis.map(k=><Line key={k} dataKey={k} stroke={C[k]||'#6b7280'} strokeWidth={sel?2.5:1.5} dot={sel?{r:3,fill:C[k]}:false} name={k} connectNulls/>)}
      </LineChart>
    </ResponsiveContainer></div>
  </Card>;
};

const StackedTimeline=({data,keys,title,sub,type='area',yFmt})=>{
  const [sel,setSel]=useState(null);
  const vis=sel?[sel]:keys;
  return <Card title={title} sub={sub} h={400}>
    <Pills keys={keys} sel={sel} onSel={setSel}/>
    <div style={{height:320}}><ResponsiveContainer>
      {type==='bar'?
        <BarChart data={data} margin={{top:5,right:5,bottom:30,left:10}}>
          <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
          <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
          <YAxis tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={yFmt}/>
          <Tooltip content={<Tip/>}/>
          {vis.map(k=><Bar key={k} dataKey={k} stackId="s" fill={C[k]||'#6b7280'} name={k}/>)}
        </BarChart>
      :
        <AreaChart data={data} margin={{top:5,right:5,bottom:30,left:10}}>
          <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
          <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
          <YAxis tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={yFmt}/>
          <Tooltip content={<Tip/>}/>
          {vis.map(k=><Area key={k} dataKey={k} stackId={sel?'':'s'} stroke={C[k]||'#6b7280'} fill={C[k]||'#6b7280'} fillOpacity={sel?0.2:0.6} strokeWidth={sel?2.5:0} name={k} dot={sel?{r:3,fill:C[k]}:false}/>)}
        </AreaChart>
      }
    </ResponsiveContainer></div>
  </Card>;
};

const ALL_IND=['BioTech','FinTech','ClimateTech','HealthTech','GenAI','MedTech','Robotics','Cybersecurity','Enterprise','Ecommerce','EdTech','PropTech','AgriTech','SpaceTech'];
const TOP5K=['BioTech','FinTech','ClimateTech','HealthTech','GenAI','Übrige'];
const STAGE_K=['Pre-Seed','Seed','Series A','Series B','Series C+','Strategic','Grant','Award','Sonstige'];
const N_IND=['FinTech','HealthTech','DefenseTech','ClimateTech','BioTech','Ecommerce','MobilityTech','SpaceTech','MedTech','Enterprise','EdTech','PropTech','AgriTech'];
const N_TECH=['GenAI','LLM','Semiconductors','Robotics','Web3','AgentAI','Cybersecurity','Infrastructure','PhysicalAI','QuantumTech'];
const TF=['GenAI','LLM','AgentAI','Robotics'];
const IF=['BioTech','FinTech','HealthTech','ClimateTech','DefenseTech','Ecommerce','EdTech','MedTech'];

const DEAL_SIZE=[{keyword:"FinTech",deals:465,fund:19032,avg:40.9},{keyword:"BioTech",deals:413,fund:28373,avg:68.7},{keyword:"ClimateTech",deals:169,fund:6492,avg:38.4},{keyword:"MedTech",deals:65,fund:828,avg:12.7},{keyword:"HealthTech",deals:48,fund:8774,avg:182.8},{keyword:"GenAI",deals:42,fund:781,avg:18.6},{keyword:"Robotics",deals:28,fund:2441,avg:87.2},{keyword:"Enterprise",deals:28,fund:169,avg:6.0},{keyword:"Ecommerce",deals:19,fund:0,avg:0},{keyword:"PropTech",deals:15,fund:2201,avg:146.7},{keyword:"AgriTech",deals:14,fund:0,avg:0},{keyword:"Cybersecurity",deals:6,fund:1376,avg:229.2},{keyword:"EdTech",deals:6,fund:5048,avg:841.3},{keyword:"SpaceTech",deals:4,fund:8,avg:2.0}];

const DealSizeMatrix=()=>{
  const data = DEAL_SIZE.map(d=>({...d,r:Math.max(Math.sqrt(d.avg)*1.2,6)}));
  return <Card title="Deal Count vs. Funding-Volumen pro Kategorie" sub="X = Anzahl Deals · Y = Total Funding (Mrd CHF) · Grösse = Ø Deal Size · 2023–2026 kumuliert" h={440}>
    <div style={{height:400}}><ResponsiveContainer>
      <ScatterChart margin={{top:10,right:20,bottom:45,left:25}}>
        <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
        <XAxis type="number" dataKey="deals" tick={{fontSize:10,fill:'#6b7280'}} domain={[0,500]}>
          <Label value="Anzahl Deals (2023–2026)" position="bottom" offset={20} style={{fontSize:10,fill:'#4b5563'}}/>
        </XAxis>
        <YAxis type="number" dataKey="fund" tick={{fontSize:10,fill:'#6b7280'}} tickFormatter={v=>`${(v/1000).toFixed(0)} Mrd`} domain={[0,30000]}>
          <Label value="Total Funding (Mrd CHF)" angle={-90} position="insideLeft" offset={-12} style={{fontSize:10,fill:'#4b5563'}}/>
        </YAxis>
        <Tooltip content={({active,payload})=>{
          if(!active||!payload?.length)return null;const d=payload[0].payload;
          return <div style={{background:'#111827',border:`2px solid ${C[d.keyword]||'#6b7280'}`,borderRadius:10,padding:'12px 16px',fontSize:12,color:'#d1d5db'}}>
            <div style={{fontWeight:800,fontSize:15,color:'#f9fafb'}}>{d.keyword}</div>
            <div style={{fontSize:11,lineHeight:1.8,marginTop:4}}>
              <div>Deals: <b style={{color:'#f9fafb'}}>{d.deals}</b></div>
              <div>Funding: <b style={{color:'#f9fafb'}}>{(d.fund/1000).toFixed(1)} Mrd CHF</b></div>
              <div>Ø Deal: <b style={{color:'#f9fafb'}}>{d.avg.toFixed(1)} Mio CHF</b></div>
            </div>
          </div>;
        }}/>
        <Scatter data={data} shape={({cx,cy,payload:p})=>{
          const col = C[p.keyword]||'#6b7280';
          const labelBelow = p.keyword==='MedTech'||p.keyword==='GenAI'||p.keyword==='Enterprise';
          return <g>
            <circle cx={cx} cy={cy} r={p.r} fill={col} fillOpacity={0.3} stroke={col} strokeWidth={2}/>
            <text x={cx} y={labelBelow?cy+p.r+12:cy-p.r-5} textAnchor="middle" fill={col} fontSize={10} fontWeight={700}>{p.keyword}</text>
          </g>;
        }}/>
      </ScatterChart>
    </ResponsiveContainer></div>
  </Card>;
};

const DealBars=()=>{
  const barData = DEAL_SIZE.slice(0,5).map(d=>({...d,fund_mrd:Math.round(d.fund/1000*10)/10}));
  const rest = DEAL_SIZE.slice(5);
  barData.push({keyword:'Übrige',deals:rest.reduce((s,r)=>s+r.deals,0),fund:rest.reduce((s,r)=>s+r.fund,0),fund_mrd:Math.round(rest.reduce((s,r)=>s+r.fund,0)/1000*10)/10,avg:Math.round(rest.reduce((s,r)=>s+r.fund,0)/rest.reduce((s,r)=>s+r.deals,0)*10)/10});
  return <Card title="Top 5 + Übrige: Deals vs. Funding" sub="Vergleich: Wer bekommt die meisten Deals vs. wer bekommt das meiste Geld" h={300}>
    <div style={{height:270}}><ResponsiveContainer>
      <BarChart data={barData} layout="vertical" margin={{top:5,right:30,bottom:5,left:80}}>
        <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
        <XAxis type="number" tick={{fontSize:9,fill:'#6b7280'}}/>
        <YAxis type="category" dataKey="keyword" tick={{fontSize:11,fill:'#d1d5db',fontWeight:600}} width={80}/>
        <Tooltip content={({active,payload})=>{
          if(!active||!payload?.length)return null;const d=payload[0]?.payload;
          return <div style={{background:'#111827',border:'1px solid #374151',borderRadius:8,padding:'8px 12px',fontSize:11,color:'#d1d5db'}}>
            <div style={{fontWeight:700,color:'#f9fafb'}}>{d?.keyword}</div>
            <div>{d?.deals} Deals · {(d?.fund/1000).toFixed(1)} Mrd CHF · Ø {d?.avg?.toFixed(0)} Mio</div>
          </div>;
        }}/>
        <Bar dataKey="deals" fill="#f97316" fillOpacity={0.7} radius={[0,4,4,0]} name="Deals" barSize={12}/>
        <Bar dataKey="fund_mrd" fill="#8b5cf6" fillOpacity={0.7} radius={[0,4,4,0]} name="Funding (Mrd)" barSize={12}/>
      </BarChart>
    </ResponsiveContainer></div>
  </Card>;
};

const DIAG_SLOPE = 2.0;
const growthColor=(dg)=> dg>0.5?'#22c55e':dg<-0.5?'#ef4444':'#94a3b8';
const zone=(n,d,dg)=>{
  const above = d > n * DIAG_SLOPE;
  if(above && dg>0) return {l:'💎 CH-Stärke + wachsend',c:'#f97316'};
  if(above && dg<=0) return {l:'📉 CH-Stärke, schrumpfend',c:'#6b7280'};
  if(!above && dg>0) return {l:'🌱 Aufholpotenzial',c:'#22c55e'};
  if(!above && n>2) return {l:'🫧 Hype > Investment',c:'#ec4899'};
  return {l:'🔬 Nische',c:'#8b5cf6'};
};

const MatrixA=()=>{
  const data=MATRIX_A.map(d=>({...d,...zone(d.n25,d.d25,d.dg),r:Math.max(Math.sqrt(d.td)*1.4,10)}));
  // Manual label positions to avoid overlap
  const labelOffset = {
    BioTech:{dx:0,dy:-1},FinTech:{dx:0,dy:-1},ClimateTech:{dx:0,dy:-1},
    HealthTech:{dx:0,dy:-1},MedTech:{dx:-3,dy:-1},PropTech:{dx:3,dy:0},
    Enterprise:{dx:3,dy:0},SpaceTech:{dx:0,dy:-1},Ecommerce:{dx:0,dy:-1},AgriTech:{dx:0,dy:1.5}
  };
  return <Card title="⭐ Opportunity Matrix — Globale News vs. CH VC-Deals (2025)" sub="Jeder Punkt = Branche · Position = aktuelle Lage 2025 · Farbe = Deal-Trend · Diagonale = Gleichgewicht (2 Deals pro News)" h={600}>
    <div style={{position:'relative',height:500}}>
      <ResponsiveContainer>
        <ComposedChart margin={{top:15,right:30,bottom:55,left:35}} data={[{dn:0,dd:0},{dn:20,dd:40}]}>
          <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
          <XAxis dataKey="dn" type="number" tick={{fontSize:10,fill:'#6b7280'}} domain={[0,20]} tickCount={6}>
            <Label value="← wenig globale News          News pro Quartal (2025)          viel globale News →" position="bottom" offset={25} style={{fontSize:9,fill:'#4b5563'}}/>
          </XAxis>
          <YAxis dataKey="dd" type="number" tick={{fontSize:10,fill:'#6b7280'}} domain={[0,42]} tickCount={7}>
            <Label value="CH Deals pro Quartal (2025)" angle={-90} position="insideLeft" offset={-18} style={{fontSize:10,fill:'#4b5563'}}/>
          </YAxis>
          <Line dataKey="dd" stroke="#374151" strokeWidth={1.5} strokeDasharray="8 4" dot={false} legendType="none" isAnimationActive={false}/>
          <Tooltip content={()=>null}/>
          {data.map((p,i)=>{
            const col = growthColor(p.dg);
            return <Scatter key={p.keyword} data={[{dn:p.n25,dd:p.d25}]} fill={col} isAnimationActive={false}
              shape={({cx,cy})=>{
                const lo = labelOffset[p.keyword]||{dx:0,dy:-1};
                return <g>
                  <circle cx={cx} cy={cy} r={p.r} fill={col} fillOpacity={0.25} stroke={p.c} strokeWidth={2.5}/>
                  <text x={cx+lo.dx*8} y={cy+lo.dy*p.r-6+lo.dy*4} textAnchor="middle" fill={p.c} fontSize={11} fontWeight={700}>{p.keyword}</text>
                </g>;
              }}
            />;
          })}
        </ComposedChart>
      </ResponsiveContainer>
      {/* Floating annotation boxes */}
      <div style={{position:'absolute',top:20,left:60,background:'#f9731510',border:'1px solid #f9731530',borderRadius:8,padding:'6px 10px'}}>
        <div style={{fontSize:10,fontWeight:700,color:'#f97316'}}>💎 CH investiert mehr</div>
        <div style={{fontSize:8,color:'#9ca3af'}}>als die Welt berichtet</div>
      </div>
      <div style={{position:'absolute',bottom:70,right:40,background:'#ec489910',border:'1px solid #ec489930',borderRadius:8,padding:'6px 10px'}}>
        <div style={{fontSize:10,fontWeight:700,color:'#ec4899'}}>🫧 Globaler Hype</div>
        <div style={{fontSize:8,color:'#9ca3af'}}>übersteigt CH-Investment</div>
      </div>
    </div>
    <div style={{display:'flex',justifyContent:'center',gap:20,marginTop:4,flexWrap:'wrap'}}>
      <div style={{display:'flex',alignItems:'center',gap:5}}><span style={{width:12,height:12,borderRadius:'50%',background:'#22c55e',opacity:.5}}/><span style={{fontSize:10,color:'#9ca3af'}}>Deals wachsend</span></div>
      <div style={{display:'flex',alignItems:'center',gap:5}}><span style={{width:12,height:12,borderRadius:'50%',background:'#ef4444',opacity:.5}}/><span style={{fontSize:10,color:'#9ca3af'}}>Deals schrumpfend</span></div>
      <div style={{display:'flex',alignItems:'center',gap:5}}><span style={{width:12,height:12,borderRadius:'50%',background:'#94a3b8',opacity:.5}}/><span style={{fontSize:10,color:'#9ca3af'}}>Deals stabil</span></div>
      <div style={{display:'flex',alignItems:'center',gap:5}}><span style={{width:20,height:0,borderTop:'2px dashed #374151'}}/><span style={{fontSize:10,color:'#9ca3af'}}>Gleichgewicht (2:1)</span></div>
    </div>
  </Card>;
};

const HeatmapB=()=>{
  const mx=Math.max(...HEATMAP.map(d=>d.n));
  return <Card title="Matrix B — Technologie × Branche (News-Überschneidungen)" sub="Wie oft Tech-Keywords im Kontext einer Branche erwähnt werden (TechCrunch & HackerNews)" h={300}>
    <div style={{overflowX:'auto'}}><table style={{borderCollapse:'separate',borderSpacing:3,width:'100%',fontSize:11}}>
      <thead><tr><th style={{textAlign:'left',padding:'6px 10px',color:'#9ca3af',fontSize:10}}></th>
        {IF.map(i=><th key={i} style={{padding:'6px 4px',color:C[i]||'#9ca3af',fontSize:9,fontWeight:700,textAlign:'center',minWidth:55}}>{i}</th>)}
      </tr></thead>
      <tbody>{TF.map(t=><tr key={t}>
        <td style={{padding:'8px 10px',color:C[t]||'#f3f4f6',fontWeight:700,fontSize:11,whiteSpace:'nowrap'}}>{t}</td>
        {IF.map(i=>{const v=HEATMAP.find(x=>x.t===t&&x.i===i)?.n||0;const int=v/mx;
          return <td key={i} style={{padding:'8px 4px',textAlign:'center',fontWeight:700,fontSize:13,borderRadius:6,color:v===0?'#374151':'#f9fafb',background:v===0?'#0f172a':`rgba(249,115,22,${Math.max(int*0.85,0.1)})`}}>{v||'–'}</td>;
        })}
      </tr>)}</tbody>
    </table></div>
    <p style={{fontSize:10,color:'#6b7280',marginTop:12,textAlign:'center'}}>Lesebeispiel: GenAI wird 24× im Kontext von FinTech erwähnt, 18× bei HealthTech, 15× bei BioTech</p>
  </Card>;
};

const TechDive=()=><>
  <Card title="GenAI — Globale News vs. Schweizer VC-Deals" sub="Linke Achse: News-Artikel · Rechte Achse: CH VC-Deals · LLM als Referenz (gestrichelt)" h={300}>
    <div style={{height:260}}><ResponsiveContainer>
      <ComposedChart data={TECH_DIVE} margin={{top:5,right:10,bottom:30,left:10}}>
        <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
        <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
        <YAxis yAxisId="n" tick={{fontSize:9,fill:'#6b7280'}} orientation="left" label={{value:'News',angle:-90,position:'insideLeft',style:{fontSize:9,fill:'#6b7280'}}}/>
        <YAxis yAxisId="v" tick={{fontSize:9,fill:'#6b7280'}} orientation="right" domain={[0,10]} label={{value:'CH Deals',angle:90,position:'insideRight',style:{fontSize:9,fill:'#6b7280'}}}/>
        <Tooltip content={<Tip/>}/>
        <Area yAxisId="n" dataKey="news_GenAI" stroke="#84cc16" fill="#84cc16" fillOpacity={0.08} strokeWidth={2} name="News: GenAI" dot={{r:2.5,fill:'#84cc16'}}/>
        <Line yAxisId="n" dataKey="news_LLM" stroke="#3b82f6" strokeWidth={1.5} strokeDasharray="5 3" name="News: LLM" dot={false}/>
        <Bar yAxisId="v" dataKey="vc_GenAI" fill="#84cc16" fillOpacity={0.5} name="CH Deals: GenAI" radius={[3,3,0,0]} barSize={14}/>
      </ComposedChart>
    </ResponsiveContainer></div>
  </Card>
  <Card title="Robotics & AgentAI — News-Explosion vs. CH-Realität" sub="AgentAI dominiert global die News, aber null CH-Deals. Robotics: beide Seiten wachsen." h={300}>
    <div style={{height:260}}><ResponsiveContainer>
      <ComposedChart data={TECH_DIVE} margin={{top:5,right:10,bottom:30,left:10}}>
        <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
        <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
        <YAxis yAxisId="n" tick={{fontSize:9,fill:'#6b7280'}} orientation="left"/>
        <YAxis yAxisId="v" tick={{fontSize:9,fill:'#6b7280'}} orientation="right" domain={[0,6]}/>
        <Tooltip content={<Tip/>}/>
        <Area yAxisId="n" dataKey="news_Robotics" stroke="#a16207" fill="#a16207" fillOpacity={0.08} strokeWidth={2} name="News: Robotics" dot={{r:2.5,fill:'#a16207'}}/>
        <Line yAxisId="n" dataKey="news_AgentAI" stroke="#f97316" strokeWidth={1.5} strokeDasharray="5 3" name="News: AgentAI" dot={false}/>
        <Bar yAxisId="v" dataKey="vc_Robotics" fill="#a16207" fillOpacity={0.5} name="CH Deals: Robotics" radius={[3,3,0,0]} barSize={14}/>
      </ComposedChart>
    </ResponsiveContainer></div>
  </Card>
</>;

/* ════════════════════════════════════════════
   MAIN
   ════════════════════════════════════════════ */
const TABS=[{id:'overview',label:'Übersicht'},{id:'deals',label:'Deal Count'},{id:'volume',label:'Funding CHF'},{id:'stages',label:'Stages'},{id:'news',label:'News'},{id:'tech',label:'Tech Deep Dive'},{id:'matrix',label:'⭐ Matrices'}];

export default function Dashboard(){
  const [tab,setTab]=useState('overview');
  return <div style={{minHeight:'100vh',background:'#030712',color:'#e5e7eb',fontFamily:"'DM Sans',system-ui,sans-serif"}}>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&display=swap" rel="stylesheet"/>
    <div style={{maxWidth:880,margin:'0 auto',padding:'28px 16px 80px'}}>
      <div style={{marginBottom:28}}>
        <h1 style={{margin:0,fontSize:28,fontWeight:800,letterSpacing:'-0.04em',color:'#f9fafb'}}>
          <span style={{background:'linear-gradient(135deg,#f97316,#ec4899)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>Data2Dollar</span>
          <span style={{fontSize:14,fontWeight:400,color:'#6b7280',marginLeft:12}}>Swiss Startup Ecosystem</span>
        </h1>
        <p style={{margin:'6px 0 0',fontSize:11,color:'#4b5563'}}>VC-Investments (Startupticker) × Medien-Coverage (TechCrunch, HackerNews) · Q1/2023 – Q1/2026</p>
      </div>

      <div style={{display:'flex',gap:2,flexWrap:'wrap',marginBottom:24,background:'#111827',borderRadius:10,padding:3}}>
        {TABS.map(t=><button key={t.id} onClick={()=>setTab(t.id)} style={{fontSize:11,padding:'8px 16px',borderRadius:8,border:'none',cursor:'pointer',fontFamily:'inherit',fontWeight:tab===t.id?700:400,background:tab===t.id?'#1f2937':'transparent',color:tab===t.id?'#f9fafb':'#6b7280',transition:'all .15s'}}>{t.label}</button>)}
      </div>

      {tab==='overview'&&<>
        <Card title="Startup-Investments pro Quartal" sub="Anzahl Deals (ohne Doppelzählung)" h={260}>
          <div style={{height:240}}><ResponsiveContainer><BarChart data={TOTALS} margin={{top:5,right:5,bottom:30,left:5}}>
            <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
            <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
            <YAxis tick={{fontSize:9,fill:'#6b7280'}}/>
            <Tooltip content={<Tip/>}/>
            <Bar dataKey="total_deals" fill="#f97316" radius={[4,4,0,0]} name="Deals" barSize={28}/>
          </BarChart></ResponsiveContainer></div>
        </Card>
        <Card title="Funding-Volumen pro Quartal" sub="Mio. CHF · EUR/USD umgerechnet · nur bekannte Beträge" h={260}>
          <div style={{height:240}}><ResponsiveContainer><AreaChart data={TOTALS} margin={{top:5,right:5,bottom:30,left:10}}>
            <defs><linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.4}/><stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.02}/></linearGradient></defs>
            <CartesianGrid stroke="#1f2937" strokeDasharray="3 3"/>
            <XAxis dataKey="quarter" tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={QS} angle={-40} textAnchor="end"/>
            <YAxis tick={{fontSize:9,fill:'#6b7280'}} tickFormatter={v=>`${(v/1000).toFixed(1)} Mrd`}/>
            <Tooltip content={({active,payload,label})=>{if(!active||!payload?.length)return null;return<div style={{background:'#111827',border:'1px solid #374151',borderRadius:8,padding:'8px 12px',fontSize:12,color:'#d1d5db'}}><div style={{fontWeight:700,color:'#f9fafb'}}>{label}</div><div>{Math.round(payload[0].value).toLocaleString()} Mio. CHF</div></div>}}/>
            <Area dataKey="total_funding_chf_m" fill="url(#gf)" stroke="#8b5cf6" strokeWidth={2.5} name="Mio. CHF" dot={{r:3,fill:'#8b5cf6'}}/>
          </AreaChart></ResponsiveContainer></div>
        </Card>
        <DealBars/>
        <DealSizeMatrix/>
      </>}

      {tab==='deals'&&<>
        <StackedTimeline data={F1_TOP5} keys={TOP5K} title="Deal Count — Top 5 + Übrige (gestapelt)" sub="Anteil der grössten Kategorien am Gesamtmarkt"/>
        <LineTimeline data={F1_TOP5} keys={['BioTech','FinTech','ClimateTech','HealthTech','GenAI']} title="Deal Count — Einzelne Linien pro Kategorie" sub="Klicke auf eine Kategorie um sie zu isolieren"/>
        <div style={{marginTop:8}}>
          <h3 style={{fontSize:13,fontWeight:700,color:'#f3f4f6',marginBottom:8}}>Alle 14 Kategorien im Detail</h3>
          <Sparklines data={F1_SM} keys={ALL_IND} valKey="d" label="Deals"/>
        </div>
      </>}

      {tab==='volume'&&<>
        <StackedTimeline data={F1_TOP5.map((r,i)=>{const fv=FV_SM;return{quarter:r.quarter,BioTech:fv.BioTech[i]?.f||0,FinTech:fv.FinTech[i]?.f||0,ClimateTech:fv.ClimateTech[i]?.f||0,HealthTech:fv.HealthTech[i]?.f||0,GenAI:fv.GenAI[i]?.f||0}})} keys={['BioTech','FinTech','ClimateTech','HealthTech','GenAI']} title="Funding Top 5 (Mio. CHF)" sub="BioTech zieht konsistent das meiste Kapital" yFmt={v=>`${Math.round(v).toLocaleString()}`}/>
        <LineTimeline data={F1_TOP5.map((r,i)=>{const fv=FV_SM;return{quarter:r.quarter,BioTech:fv.BioTech[i]?.f||0,FinTech:fv.FinTech[i]?.f||0,ClimateTech:fv.ClimateTech[i]?.f||0,HealthTech:fv.HealthTech[i]?.f||0,GenAI:fv.GenAI[i]?.f||0,Robotics:fv.Robotics[i]?.f||0,EdTech:fv.EdTech[i]?.f||0}})} keys={['BioTech','FinTech','ClimateTech','HealthTech','GenAI','Robotics','EdTech']} title="Funding — Einzelne Linien (Mio. CHF)" sub="Klicke auf eine Kategorie für den isolierten Verlauf"/>
        <div style={{marginTop:8}}>
          <h3 style={{fontSize:13,fontWeight:700,color:'#f3f4f6',marginBottom:8}}>Alle Kategorien — Funding (Mio. CHF)</h3>
          <Sparklines data={FV_SM} keys={ALL_IND} valKey="f" label="Mio." unit=""/>
        </div>
      </>}

      {tab==='stages'&&<StackedTimeline data={STAGES} keys={STAGE_K} title="Investment-Stages pro Quartal" sub="Seed dominiert · Pre-Seed wächst · Award = Preise · Grant = Fördergelder · Sonstige = unkategorisiert" type="bar"/>}

      {tab==='news'&&<>
        <StackedTimeline data={NEWS_IND} keys={N_IND} title="News Industry Layer" sub="TechCrunch & HackerNews Branchen-Erwähnungen pro Quartal"/>
        <StackedTimeline data={NEWS_TECH} keys={N_TECH} title="News Tech Layer" sub="GenAI dominiert seit 2023 · AgentAI explodiert 2025 · Web3 & Cybersecurity sinken"/>
      </>}

      {tab==='tech'&&<TechDive/>}
      {tab==='matrix'&&<><MatrixA/><HeatmapB/></>}
    </div>
  </div>;
}
