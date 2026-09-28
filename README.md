# 🏗️ Agentic AI for Safety Monitoring with Construction Risk Analytics

> An AI-powered construction safety and risk analytics platform that combines Computer Vision, Machine Learning, FastAPI, React, and MySQL to support PPE monitoring, safety analysis, project risk analytics, alerts, and reporting.

---

## 📌 Overview

Construction projects involve multiple safety and project management challenges such as PPE violations, worker safety risks, delays, cost variations, resource issues, and compliance risks.

**Agentic AI for Safety Monitoring with Construction Risk Analytics** is an integrated web-based platform developed to support construction teams with AI-assisted safety monitoring and risk analytics.

The system provides:

- AI-based PPE detection
- Site safety monitoring
- Construction risk analysis
- Machine learning predictions
- Project analytics
- Safety alerts
- AI-based insights
- Report generation

The platform connects a React frontend with a FastAPI backend, MySQL database, and trained AI/ML models.

---

## ✨ Key Features

- 🔐 JWT-based User Authentication
- 🏗️ Construction Project Management
- 📷 Site Entry Camera
- 🎥 Working Place CCTV
- 👷 YOLO-based PPE Detection
- 🦺 PPE Compliance Verification
- ⚠️ Safety Violation Detection
- 📊 Construction Risk Analytics
- 🧠 Machine Learning Risk Prediction
- 🤖 AI-based Risk Analysis
- 🚨 Safety Alerts and Alarm
- 📈 Project Analytics Dashboard
- 📉 Risk Trends and Distribution
- 💡 Risk-based Recommendations
- 📄 Report Generation
- 🗄️ MySQL Database Integration
- 🔌 FastAPI REST APIs

---

# 🏗️ System Architecture

```text
                    CONSTRUCTION SITE
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      SITE ENTRY CAMERA          WORKING PLACE CCTV
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                  YOLO PPE DETECTION
                           │
                           ▼
                   PPE VERIFICATION
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          PPE VIOLATION          RISK ANALYSIS
                │                     │
                └──────────┬──────────┘
                           │
                           ▼
                    FASTAPI BACKEND
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
         AI / ML MODELS            MYSQL DATABASE
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                     REACT FRONTEND
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         DASHBOARD      SAFETY        REPORTS
                       MONITORING
                       | Category          | Technologies                        |
| 🛠️ Technology Stack | ----------------------------------- |
| Frontend          | React, Vite, JavaScript, HTML, CSS  |
| Backend           | Python, FastAPI, Uvicorn            |
| Database          | MySQL                               |
| Computer Vision   | YOLO, Ultralytics                   |
| Machine Learning  | Scikit-learn                        |
| Data Processing   | Pandas, NumPy                       |
| Authentication    | JWT                                 |
| API Communication | REST APIs, Axios                    |
| Visualization     | Chart.js                            |
| Version Control   | Git, GitHub                         |
| Development Tools | Visual Studio Code, MySQL Workbench |
