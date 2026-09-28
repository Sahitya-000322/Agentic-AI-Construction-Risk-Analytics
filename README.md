# 🏗️ Agentic AI for Safety Monitoring with Construction Risk Analytics

An AI-powered construction safety and risk analytics platform that combines Computer Vision, Machine Learning, and full-stack technologies to support PPE monitoring, safety assessment, project risk analysis, and data-driven decision support.

---

## 📌 Overview

Construction sites involve multiple safety and operational risks that require continuous attention. This project provides an integrated platform for monitoring worker safety, analyzing construction risks, and presenting project insights through an interactive web application.

The system uses **YOLO-based PPE detection**, **Machine Learning models**, **FastAPI**, **React**, and **MySQL** to provide safety monitoring, risk analytics, alerts, dashboards, and reporting capabilities.

### Key Objectives

- Monitor worker PPE compliance using Computer Vision
- Identify PPE violations and safety risks
- Analyze construction-related risks using Machine Learning
- Monitor project progress and performance
- Provide AI/ML-based decision-support insights
- Generate safety alerts and project reports

---

## ✨ Key Features

- **Secure Authentication** – JWT-based user authentication and protected API access
- **Project Management** – Manage and monitor construction project information
- **Site Entry Monitoring** – Camera-based worker check-in and PPE verification
- **Working Place CCTV** – Workplace safety monitoring through CCTV
- **PPE Detection** – YOLO-based detection of helmet, gloves, vest, boots, and goggles
- **Safety Risk Analysis** – Analyze PPE violations and safety conditions
- **AI/ML Risk Analytics** – Safety, injury, delay, cost, schedule, resource, compliance, and insurance analysis
- **Interactive Dashboard** – Centralized project, safety, and risk information
- **Alerts & Alarm** – Safety alerts when PPE violations are detected
- **Reports** – Generate and download project, safety, and risk reports

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, HTML, CSS |
| Backend | Python, FastAPI, Uvicorn |
| Database | MySQL |
| Computer Vision | YOLO, Ultralytics |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Authentication | JWT |
| API Communication | REST API, Axios |
| Visualization | Chart.js |
| Development Tools | Git, GitHub, VS Code, MySQL Workbench |

---

## 📂 Project Structure

```text
Agentic-AI-Construction-Risk-Analytics/
│
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── routers/            # API endpoints
│   │   ├── services/           # Business and AI services
│   │   ├── models/             # Database models
│   │   └── main.py             # Application entry point
│   ├── requirements.txt
│   └── requirements-ml.txt
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   └── vite.config.js
│
├── datasets/                   # Project datasets
├── models/                     # Trained ML models
├── safety_monitoring_module/   # Safety monitoring resources
├── uploads/                    # Uploaded files
├── reports/                    # Generated reports
├── .gitignore
└── README.md

🔐 Authentication

The application uses JWT (JSON Web Token) authentication to secure protected APIs.

User Login → FastAPI → JWT Token → Authenticated API Requests
Demo Credentials
Email: admin@buildai.com
Password: admin123
🦺 PPE Safety Monitoring

The safety monitoring module uses YOLO-based Computer Vision to identify workers and check PPE compliance.

Site Entry Camera

The Site Entry Camera is used for worker check-in and PPE verification.

Capture Frame
      ↓
PPE Detection
      ↓
PPE Verification
      ↓
Risk Analysis
      ↓
Safety Result

The system checks:

Helmet
Gloves
Vest
Boots
Goggles
Missing PPE
Working Place CCTV

The Working Place CCTV is designed for administrator monitoring. The administrator can capture the current frame and manually perform a PPE check to view violations and risk information.

🤖 AI & Risk Analytics

The platform integrates multiple Machine Learning models to support construction risk analysis.

Model	Analysis
Safety Risk	Safety risk prediction
Injury	Injury risk analysis
Delay	Delay prediction
Cost	Cost analysis
Schedule	Schedule analysis
Project Delay	Project delay analysis
Resource	Resource analysis
Compliance	Compliance analysis
Insurance	Insurance analysis

The AI/ML results are presented as decision-support information through the application.

📊 Dashboard & Analytics

The dashboard provides a centralized view of construction project information, including:

Project Progress
Safety Compliance
Overall Risk
Active Hazards
Safety Alerts
Risk Trends
Risk Distribution
AI Recommendations

The Analytics and Risk Center modules provide detailed insights into safety, injury, delay, cost, schedule, resource, compliance, and insurance risks.

🚨 Alerts & Reports

When a PPE violation is identified, the system provides a safety alert and alarm.

The Reports module provides project and safety information for documentation and analysis, with support for report generation and download.

🔄 System Architecture
Site Entry Camera / Working Place CCTV
                 ↓
          YOLO PPE Detection
                 ↓
          Safety & Risk Analysis
                 ↓
            FastAPI Backend
              ↙        ↘
        AI/ML Models    MySQL
              ↘        ↙
            REST APIs
                 ↓
          React Frontend
                 ↓
       Dashboard / Analytics
       Safety / Reports / Alerts
🔌 API

The backend is implemented using FastAPI REST APIs.

Major API areas include:

Authentication
Dashboard
Projects
Safety & PPE
AI/ML
Risk Analytics
Reports
API Documentation

Once the backend is running:

http://127.0.0.1:8000/docs
🚀 Installation & Setup
Prerequisites
Python
Node.js
MySQL
Git
Visual Studio Code
Clone Repository
git clone https://github.com/Sahitya-000322/Agentic-AI-Construction-Risk-Analytics.git
cd Agentic-AI-Construction-Risk-Analytics
Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-ml.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
Frontend

Open a new terminal:

cd frontend
npm install
npm run dev

Application:

Frontend: http://localhost:5173
Backend:  http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs
🧪 Testing

The application was tested across the major functional areas:

Authentication and JWT access
Project management
Camera access and frame capture
PPE detection and verification
Safety risk analysis
Alerts and alarm
AI/ML APIs
Dashboard and analytics
Database connectivity
Report generation
📌 Project Modules
Module	Description
Authentication	Secure user access
Project Management	Project information and tracking
Site Monitoring	Camera-based monitoring
PPE & Safety	PPE detection and verification
Risk Analytics	Construction risk analysis
AI Intelligence	AI/ML-based insights
Dashboard	Centralized project monitoring
Alerts & Recommendations	Safety alerts and decision support
Reports	Project and safety reporting
🎯 Project Objective

The objective of this project is to develop an integrated platform that combines Computer Vision, Machine Learning, and full-stack web technologies to support construction safety monitoring and risk analytics.

The platform enables construction teams to monitor PPE compliance, identify safety issues, analyze project risks, access AI/ML insights, and generate reports from a centralized system.

👩‍💻 Project Information

Project Title:
Agentic AI for Safety Monitoring with Construction Risk Analytics

Project Domain:
Artificial Intelligence | Machine Learning | Computer Vision | Full-Stack Development | Construction Safety

Repository:
https://github.com/Sahitya-000322/Agentic-AI-Construction-Risk-Analytics

🏁 Conclusion

The project integrates React, FastAPI, MySQL, YOLO, and Machine Learning models into a unified construction safety and risk analytics platform.

Monitor → Detect → Analyze → Alert → Support Decisions → Report