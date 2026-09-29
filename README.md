# 🏗️ Agentic AI for Safety Monitoring with Construction Risk Analytics

> An AI-powered construction safety and risk analytics platform that combines **Computer Vision, Machine Learning, FastAPI, React, and MySQL** to support PPE monitoring, safety assessment, construction risk analysis, alerts, dashboards, and reporting.

---

## 📌 Overview

Construction sites involve multiple safety, operational, and project-related risks. Traditional monitoring methods often depend on manual inspections, which can make safety assessment and risk identification time-consuming.

**Agentic AI for Safety Monitoring with Construction Risk Analytics** provides an integrated web-based platform for construction safety monitoring and risk analysis.

The platform combines:

- Computer Vision for PPE detection
- Machine Learning for construction risk analysis
- FastAPI REST APIs for backend services
- React for the interactive frontend
- MySQL for application data
- Dashboard-based analytics
- Safety alerts and alarm
- Project and safety reporting

The system is designed to provide **AI/ML-based decision-support information** to help users monitor site safety and understand project risks.

---

## 🎯 Objectives

- Monitor worker PPE compliance using Computer Vision
- Detect PPE violations and safety conditions
- Analyze construction risks using Machine Learning
- Monitor project progress and safety information
- Provide centralized project and risk analytics
- Generate safety alerts when violations are detected
- Provide AI/ML-based decision-support insights
- Generate project and safety reports

---

## ✨ Key Features

### 🔐 Secure Authentication
JWT-based authentication for secure login and protected API access.

### 🏗️ Project Management
Manage and monitor construction project information through the web application.

### 📷 Site Entry Monitoring
Camera-based worker check-in and PPE verification at the site entry.

### 📹 Working Place CCTV
Workplace CCTV monitoring for administrator-based safety inspection.

### 🦺 PPE Detection
YOLO-based Computer Vision detection for:

- Helmet
- Gloves
- Vest
- Boots
- Goggles
- Missing PPE

### ⚠️ Safety Risk Analysis
Analyze PPE violations and safety conditions to identify the associated risk level.

### 🤖 AI/ML Risk Analytics
Machine Learning models support analysis of:

- Safety Risk
- Injury Risk
- Delay Risk
- Cost Risk
- Schedule Risk
- Project Delay
- Resource Risk
- Compliance Risk
- Insurance Risk

### 📊 Interactive Dashboard
Centralized view of:

- Project Progress
- Safety Compliance
- Overall Risk
- Active Hazards
- Safety Alerts
- Risk Trends
- Risk Distribution
- AI Recommendations

### 🚨 Alerts & Alarm
Safety alerts and alarm notifications are triggered when PPE violations are detected.

### 📄 Reports
Generate and download project, safety, and risk-related reports.

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
├── backend/
│   ├── app/
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business and AI services
│   │   ├── models/              # Database models
│   │   └── main.py              # FastAPI application entry point
│   │
│   ├── requirements.txt         # Backend dependencies
│   └── requirements-ml.txt      # Machine Learning dependencies
│
├── frontend/
│   ├── src/
│   │   ├── api/                 # API communication
│   │   ├── components/          # Reusable UI components
│   │   └── pages/               # Application pages
│   │
│   ├── package.json             # Frontend dependencies
│   └── vite.config.js           # Vite configuration
│
├── datasets/                    # Project datasets
├── models/                      # Trained Machine Learning models
├── safety_monitoring_module/    # Safety monitoring resources
├── uploads/                     # Uploaded files
├── reports/                     # Generated reports
├── .gitignore                   # Git ignored files
└── README.md                    # Project documentation
```

---

## 🔐 Authentication

The application uses **JWT (JSON Web Token)** authentication to secure protected APIs.

### Authentication Flow

```text
User Login
     ↓
FastAPI Authentication API
     ↓
Credentials Validation
     ↓
JWT Token Generated
     ↓
Token Stored by Frontend
     ↓
Authenticated API Requests
```

### Demo Credentials

```text
Email: admin@buildai.com
Password: admin123
```

### Authentication Features

- User login
- JWT token generation
- Protected API access
- Token-based authentication
- Authenticated frontend requests

> **Security Note:** The credentials above are intended only for local/demo use. Change the credentials before using the application in a production environment.

---

## 🦺 PPE Safety Monitoring

The Safety Monitoring module uses **YOLO-based Computer Vision** to identify workers and verify PPE compliance.

### 📍 Site Entry Camera

The Site Entry Camera is designed for worker check-in and PPE verification.

The user can:

1. Open the camera
2. Capture the current frame
3. Click **Check In & Verify PPE**
4. Send the captured frame to the backend
5. Detect PPE using YOLO
6. Analyze the safety condition
7. Display the result

### Site Entry Workflow

```text
Camera
   ↓
Capture Current Frame
   ↓
YOLO PPE Detection
   ↓
PPE Verification
   ↓
Safety Risk Analysis
   ↓
Check-In / Safety Result
   ↓
Alert if Violation Detected
```

### 📹 Working Place CCTV

The Working Place CCTV is designed for administrator-based workplace safety monitoring.

Administrators can:

- View the live camera feed
- Capture the current frame
- Perform a manual PPE check
- View detected PPE
- View missing PPE
- View safety risk information
- Receive alerts for violations

### PPE Classes

The Computer Vision model supports detection related to:

```text
Helmet
Gloves
Vest
Boots
Goggles
Person
No Helmet
No Gloves
No Boots
No Goggles
```

---

## 🤖 AI & Risk Analytics

The platform integrates multiple Machine Learning models to support construction risk analysis.

| Model | Purpose |
|---|---|
| Safety Risk | Safety risk analysis |
| Injury | Injury risk analysis |
| Delay | Delay prediction |
| Cost | Cost risk analysis |
| Schedule | Schedule analysis |
| Project Delay | Project delay analysis |
| Resource | Resource risk analysis |
| Compliance | Compliance analysis |
| Insurance | Insurance risk analysis |

The AI/ML results are presented through the application as **decision-support information**.

---

## 📊 Risk Analysis

The platform supports analysis across multiple construction risk areas.

```text
                    Construction Risk
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       Safety            Injury            Delay
          │                │                │
          └────────────────┼────────────────┘
                           ↓
                    Cost & Schedule
                           ↓
                    Resources
                           ↓
                    Compliance
                           ↓
                     Insurance
```

---

## 📈 Dashboard & Analytics

The Dashboard provides a centralized view of project and safety information.

### Dashboard Components

- Overall Risk
- Safety Compliance
- Active Hazards
- Project Progress
- Safety Alerts
- Risk Trends
- Risk Distribution
- AI Recommendations
- Project Information

### Analytics

The Analytics and Risk Center modules provide detailed information related to:

- Safety
- Injury
- Delay
- Cost
- Schedule
- Resources
- Compliance
- Insurance

---

## 🚨 Safety Alerts & Alarm

When the PPE detection system identifies a safety violation, the application provides an alert.

### Alert Flow

```text
PPE Detection
      ↓
Missing PPE Identified
      ↓
Safety Violation
      ↓
Risk Analysis
      ↓
Safety Alert
      ↓
Alarm
```

The safety monitoring service also records violation information for further analysis.

---

## 📄 Reports

The Reports module provides project and safety information for documentation and analysis.

### Report Capabilities

- View project reports
- View safety information
- Generate reports
- Download reports
- Review risk-related information

The reporting functionality is integrated with the project dashboard and backend services.

---

## 🔄 System Architecture

```text
┌──────────────────────────────────────────┐
│              User / Admin                │
└────────────────────┬─────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────┐
│            React Frontend                │
│                                          │
│ Dashboard | Safety | AI Hub | Reports   │
│ Projects  | Risk Center | Analytics     │
└────────────────────┬─────────────────────┘
                     │
                 REST APIs
                     │
                     ↓
┌──────────────────────────────────────────┐
│            FastAPI Backend               │
│                                          │
│ Authentication | Projects | Safety      │
│ PPE Detection | Risk | Dashboard        │
│ AI/ML Services | Reports                │
└──────────────┬───────────────┬───────────┘
               │               │
               ↓               ↓
      ┌────────────────┐   ┌──────────────┐
      │ AI / ML Models │   │    MySQL     │
      │                │   │   Database   │
      │ YOLO           │   └──────────────┘
      │ Scikit-learn   │
      └────────────────┘
               ↑
               │
      ┌──────────────────────┐
      │ Site Entry Camera    │
      │ Working Place CCTV   │
      └──────────────────────┘
```

---

## 🔌 API Architecture

The backend is implemented using **FastAPI REST APIs**.

### Major API Areas

| API Area | Function |
|---|---|
| Authentication | User login and authentication |
| Dashboard | Dashboard KPIs and analytics |
| Projects | Project management |
| Safety | Safety monitoring |
| PPE | PPE detection and verification |
| AI/ML | Machine Learning analysis |
| Risk | Risk analytics |
| Reports | Report-related operations |

### API Documentation

FastAPI provides interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🚀 Installation & Setup

### Prerequisites

Make sure the following are installed:

- Python
- Node.js
- MySQL
- Git
- Visual Studio Code

---

### 1. Clone the Repository

```bash
git clone https://github.com/Sahitya-000322/Agentic-AI-Construction-Risk-Analytics.git
```

```bash
cd Agentic-AI-Construction-Risk-Analytics
```

---

### 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Install Machine Learning dependencies:

```bash
pip install -r requirements-ml.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

### 3. Frontend Setup

Open a new terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 🌐 Application URLs

| Service | URL |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://127.0.0.1:8000` |
| API Documentation | `http://127.0.0.1:8000/docs` |
| Health Check | `http://127.0.0.1:8000/health` |

---

## 🗄️ Database

The application uses **MySQL** as the relational database.

The database supports storage and retrieval of application information related to:

- Users
- Projects
- Safety data
- PPE monitoring
- Risk analysis
- Dashboard information
- Reports

The FastAPI backend communicates with MySQL through the application's database layer.

---

## 🧪 Testing

The application was tested across major functional areas.

### Functional Testing

- User authentication
- JWT protected APIs
- Project management
- Camera access
- Camera frame capture
- PPE detection
- PPE verification
- Safety risk analysis
- Safety alerts
- Alarm functionality
- Dashboard data
- Analytics
- AI/ML APIs
- Database connectivity
- Report generation

### API Testing

FastAPI Swagger documentation can be used to test backend endpoints:

```text
http://127.0.0.1:8000/docs
```

---

## 📦 Project Modules

| Module | Description |
|---|---|
| 🔐 Authentication | Secure user authentication |
| 🏗️ Project Management | Project information and tracking |
| 📷 Site Monitoring | Camera-based monitoring |
| 🦺 PPE & Safety | PPE detection and safety verification |
| ⚠️ Risk Analytics | Construction risk analysis |
| 🤖 AI Intelligence | AI/ML-based insights |
| 📊 Dashboard | Centralized project monitoring |
| 🚨 Alerts | Safety alerts and alarm |
| 💡 Recommendations | Risk-based decision support |
| 📄 Reports | Project and safety reporting |

---

## 🔬 AI/ML Workflow

```text
Project / Safety Data
          ↓
      Data Processing
          ↓
      ML Model Selection
          ↓
      Model Prediction
          ↓
    Risk / Safety Result
          ↓
      API Response
          ↓
     React Dashboard
          ↓
 Decision-Support Insight
```

---

## 🦺 PPE Detection Workflow

```text
Camera Input
     ↓
Frame Capture
     ↓
Image Validation
     ↓
YOLO Detection
     ↓
Worker & PPE Detection
     ↓
Missing PPE Identification
     ↓
Safety Risk Analysis
     ↓
Result Display
     ↓
Alert / Alarm if Required
```

---

## 🔒 Security

The application includes:

- JWT-based authentication
- Protected API endpoints
- Token-based API requests
- Environment-based configuration
- Password authentication
- Backend API validation

Sensitive configuration such as environment variables should not be committed to GitHub.

---

## 📁 Important Project Resources

| Directory | Purpose |
|---|---|
| `backend/` | FastAPI backend application |
| `frontend/` | React frontend application |
| `models/` | Trained Machine Learning models |
| `datasets/` | Project datasets |
| `safety_monitoring_module/` | PPE and safety monitoring resources |
| `uploads/` | Uploaded files |
| `reports/` | Report output directory |

---

## 🎓 Project Domain

**Artificial Intelligence**

**Machine Learning**

**Computer Vision**

**Construction Safety**

**Risk Analytics**

**Full-Stack Web Development**

---

## 🎯 Project Objective

The primary objective of this project is to develop an integrated construction safety and risk analytics platform using Artificial Intelligence and Machine Learning.

The platform combines:

```text
Computer Vision
       +
Machine Learning
       +
Web Technologies
       +
Database
       +
Safety Analytics
       ↓
Construction Risk Intelligence Platform
```

The system supports construction teams by providing centralized safety monitoring, PPE verification, risk analysis, alerts, analytics, and reporting.

---

## 🌟 Key Project Highlights

### Computer Vision
YOLO-based PPE detection for construction worker safety monitoring.

### Machine Learning
Multiple trained models for construction-related risk analysis.

### Full-Stack Development
React frontend integrated with a Python FastAPI backend.

### Database Integration
MySQL-based application data management.

### Safety Monitoring
Site Entry Camera and Working Place CCTV workflows.

### Decision Support
AI/ML-based risk and safety insights for supporting human decisions.

### Reporting
Project and safety information can be generated and downloaded through the Reports module.

---

## 📌 Project Information

| Property | Details |
|---|---|
| Project Title | Agentic AI for Safety Monitoring with Construction Risk Analytics |
| Domain | AI / ML / Computer Vision / Construction Safety |
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| Database | MySQL |
| Computer Vision | YOLO + Ultralytics |
| Machine Learning | Scikit-learn |
| Authentication | JWT |
| API | REST API |
| Repository | GitHub |

---

## 👩‍💻 Repository

**GitHub Repository:**

https://github.com/Sahitya-000322/Agentic-AI-Construction-Risk-Analytics

---

## 🏁 Conclusion

**Agentic AI for Safety Monitoring with Construction Risk Analytics** integrates Computer Vision, Machine Learning, and full-stack web technologies into a unified construction safety and risk analytics platform.

The system provides:

- PPE monitoring
- Safety verification
- Risk analysis
- Project monitoring
- AI/ML insights
- Safety alerts
- Dashboard analytics
- Reporting capabilities

### Overall Workflow

```text
MONITOR
   ↓
DETECT
   ↓
ANALYZE
   ↓
ALERT
   ↓
SUPPORT DECISIONS
   ↓
REPORT
```

The project demonstrates the practical application of **Artificial Intelligence, Machine Learning, Computer Vision, FastAPI, React, and MySQL** in the construction safety domain.

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Built with AI, Machine Learning, Computer Vision, and Full-Stack Technologies for Construction Safety.**