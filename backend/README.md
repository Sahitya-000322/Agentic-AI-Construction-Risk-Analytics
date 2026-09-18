# BuildAI — Construction Intelligence Backend

FastAPI + PostgreSQL (Neon) backend powering the **Agentic AI Construction Risk Analytics** platform.

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **FastAPI** — REST API framework
- **SQLAlchemy 2.0** — ORM (declarative, mapped_column)
- **PostgreSQL (Neon Cloud, SSL)** — `psycopg` v3 driver
- **Pydantic v2** + **pydantic-settings**
- **JWT (python-jose)** + **bcrypt** for auth
- **pandas** for CSV ingestion in `seed.py`

---

## ⚙️ Setup

```bash
cd backend
pip install -r requirements.txt
```

`.env` is preconfigured with the Neon DB connection string. Edit `JWT_SECRET` in production.

---

## 🌱 Seed Database

```bash
python seed.py
```

This script:
- Drops & recreates all 16 tables
- Seeds `users` (admin@buildai.com / admin123)
- Loads `projects` from `../datasets/projects.csv`
- Loads `risk_trends` from `../datasets/weather_history.csv`
- Inserts hardcoded values matching the **frontend JSX exactly** for: milestones, KPIs, alerts, recommendations, incidents, etc.

---

## 🚀 Run Server

```bash
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health:** http://localhost:8000/health

Tables are auto-created on startup (`Base.metadata.create_all`).

---

## 🔐 Authentication

1. **Register:** `POST /api/auth/register` JSON `{email, password, full_name, role}`
2. **Login:** `POST /api/auth/login` form-data `username=<email>&password=<pwd>` → `{access_token}`
3. **Use:** `Authorization: Bearer <token>` header for all protected routes

---

## 📚 API Endpoints (30 total)

### System (public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | DB connection status |

### Auth (public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login (form-data) → JWT |
| GET | `/api/auth/me` | Current user (protected) |

### Dashboard (protected) — `/`
| Method | Endpoint | Returns |
|--------|----------|---------|
| GET | `/api/dashboard/kpis` | 4 KPI cards |
| GET | `/api/dashboard/project-progress` | 5 phases [{phase, value}] |
| GET | `/api/dashboard/risk-gauge` | {value, level} |
| GET | `/api/dashboard/risk-trend?days=7` | {current, previous, change, data} |
| GET | `/api/dashboard/risk-summary` | 4 risk counters |
| GET | `/api/dashboard/incidents` | latest incidents |
| GET | `/api/dashboard/ai-site-status` | {monitoring, zones, sensor_health} |
| GET | `/api/dashboard/risk-distribution` | severity distribution |

### Projects (protected) — `/projects`
| Method | Endpoint | Returns |
|--------|----------|---------|
| GET | `/api/projects` | list |
| GET | `/api/projects/{id}` | detail |
| GET | `/api/projects/summary` | 4 summary cards |
| GET | `/api/projects/performance` | 4 performance metrics |

### Other (protected)
| Method | Endpoint | Page |
|--------|----------|------|
| GET | `/api/milestones` | / |
| GET | `/api/alerts` | / |
| GET | `/api/alerts/notifications` | Navbar bell |
| GET | `/api/recommendations` | / |
| GET | `/api/hazards` | /riskcenter, /safety |
| GET | `/api/zones` | /riskcenter |
| GET | `/api/risks/kpis` | /riskcenter |
| GET | `/api/risks/summary` | /riskcenter |
| GET | `/api/aihub/overview` | /aihub |
| GET | `/api/aihub/modules` | /aihub |
| GET | `/api/aihub/insights` | /aihub |
| GET | `/api/reports` | /reports |
| GET | `/api/reports/summary` | /reports |
| GET | `/api/reports/performance` | /reports |
| GET | `/api/reports/insight` | /reports |

---

## 🗄️ Database Models (16)

`users`, `projects`, `milestones`, `kpis`, `risk_summary`, `incidents`, `alerts`, `recommendations`, `risk_trends`, `ai_site_status`, `ai_modules`, `ai_insights`, `hazards`, `zones`, `reports`, `performance_metrics`

---

## 🌐 CORS

Preconfigured to allow:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (CRA default)

Edit `CORS_ORIGINS` in `.env` to add more.

---

## 📁 Folder Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry
│   ├── config.py            # env settings
│   ├── database.py          # SQLAlchemy engine
│   ├── security.py          # JWT + bcrypt
│   ├── dependencies.py      # get_current_user
│   ├── models/              # 16 SQLAlchemy models
│   ├── schemas/             # 16 Pydantic schemas
│   └── routers/             # 10 API routers
├── seed.py                  # DB seeder
├── .env                     # Neon DB + JWT
├── .env.example
├── requirements.txt
└── README.md
```
