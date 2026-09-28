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

## 🔐 Authentication

The application uses **JWT (JSON Web Token)** authentication to secure protected APIs.

**Login Flow:**  
`User Login → FastAPI → JWT Token → Authenticated API Requests`

### Demo Credentials

```text
Email: admin@buildai.com
Password: admin123