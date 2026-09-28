# BuildAI — Construction Intelligence Backend

FastAPI + PostgreSQL (Neon) backend powering the **Agentic AI Construction Risk Analytics** platform.

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **FastAPI** — REST API framework
- **SQLAlchemy 2.0** — ORM (declarative, mapped_column)
- **PostgreSQL (Neon Cloud, SSL)** — `psycopg` v3 driver
- **Pydantic v2** + **pydantic-settings**
- **JWT (PyJWT)** + **bcrypt** for auth
- **slowapi** — rate limiting (10/min on login)
- **pandas** for CSV ingestion in `seed.py`
- **Optional ML/vision** (`requirements-ml.txt`): ultralytics, opencv, scikit-learn, torch

---

## ⚙️ Setup

```bash
cd backend
pip install -r requirements.txt
# Optional — only for PPE vision + local ML inference:
pip install -r requirements-ml.txt
```

`.env` is preconfigured with the Neon DB connection string. Edit `JWT_SECRET` in production.

> Model binaries (`.pkl` / `.joblib` / `.pt`) are **not** in git. Place them
> under `<repo-root>/ml/models/` or set `MODEL_DIR` / `PPE_MODEL_PATH` env
> vars — see `docs/MODELS.md`. Missing files yield clear `503` responses,
> never crashes.

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

## 📚 API Endpoints (42 total)

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

### PPE vision (protected) — needs `requirements-ml.txt` + model file
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ppe/health` | Model availability status |
| POST | `/api/ppe/detect` | Detect PPE violations in uploaded image (multipart, ≤10 MB) |

### ML predictions (protected) — needs model files under `ml/models/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ml/models` | Availability status per model |
| POST | `/api/ml/predict/safety-risk` | PPE-based safety risk class |
| POST | `/api/ml/predict/injury` | Injury severity (feature dict) |
| POST | `/api/ml/predict/delay` | Delay Yes/No |
| POST | `/api/ml/predict/cost` | Cost overrun class |
| POST | `/api/ml/predict/schedule` | Schedule delay (feature dict) |
| POST | `/api/ml/predict/project-delay` | Project delay (feature dict) |
| POST | `/api/ml/predict/resource` | Resource shortage (feature dict) |
| POST | `/api/ml/predict/compliance` | Compliance class (feature dict) |
| POST | `/api/ml/predict/insurance` | Insurance class (feature dict) |

Missing models answer `503` with setup guidance (see `docs/MODELS.md`).

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
│   ├── limiter.py             # Shared slowapi limiter (10/min login)
│   ├── models/              # 16 SQLAlchemy models
│   ├── schemas/             # 17 Pydantic schemas
│   ├── routers/             # 13 API routers (auth, dashboard, ppe, ml, ...)
│   └── services/            # PPE vision + ML registry/predictors
├── seed.py                  # DB seeder
├── .env                     # Neon DB + JWT
├── .env.example
├── requirements.txt         # Core deps
├── requirements-ml.txt      # Optional vision/ML deps
└── README.md
```
