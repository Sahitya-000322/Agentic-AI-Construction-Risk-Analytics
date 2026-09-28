"""
Seed script — populates Neon PostgreSQL with realistic data matching the
frontend JSX hardcoded values.

Sources:
- ../datasets/projects.csv  -> projects table
- ../datasets/weather_history.csv -> risk_trends table (aggregated)
- All other tables -> hardcoded values that match Dashboard JSX exactly
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

# Allow running from anywhere
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import (  # noqa: E402
    AIInsight,
    AIModule,
    AISiteStatus,
    Alert,
    Hazard,
    Incident,
    KPI,
    Milestone,
    PerformanceMetric,
    Project,
    Recommendation,
    Report,
    RiskSummary,
    RiskTrend,
    User,
    Zone,
)
from app.security import hash_password  # noqa: E402


def reset_schema():
    print("[reset] Dropping & recreating all tables...")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(bind=engine)
    print("[ok] Schema ready.\n")


def seed_users(db):
    if db.query(User).count() > 0:
        print("⏭️  Users already exist, skipping.")
        return
    print("👤 Seeding users...")
    admin = User(
        email="admin@buildai.com",
        hashed_password=hash_password("admin123"),
        full_name="Site Administrator",
        role="admin",
    )
    db.add(admin)
    db.commit()
    print("   - admin@buildai.com / admin123")


def seed_projects_from_csv(db):
    if db.query(Project).count() > 0:
        print("⏭️  Projects already exist, skipping.")
        return
    csv_path = HERE.parent / "datasets" / "projects.csv"
    if not csv_path.exists():
        print(f"⚠️  {csv_path} not found, skipping projects CSV seed.")
        return
    print("🏗️  Seeding projects from CSV...")
    df = pd.read_csv(csv_path)

    risk_palette = ["#3B82F6", "#10B981", "#EF4444", "#F59E0B", "#8B5CF6", "#14B8A6", "#EC4899"]
    for i, row in df.head(8).iterrows():
        progress = int(row.get("Progress", 0))
        delay = str(row.get("Delay", "No")).lower() == "yes"
        risk = "high" if delay or progress < 50 else ("low" if progress >= 85 else "medium")
        status = "delayed" if delay else ("on track" if progress >= 85 else "in progress")
        project = Project(
            name=str(row.get("Project_Name", f"Project {i+1}")),
            code=f"P-{str(row.get('Project_ID', f'{i+1:04d}'))[-4:]}",
            progress=progress,
            color=risk_palette[i % len(risk_palette)],
            risk_level=risk,
            status=status,
            days_left=max(0, 60 - (i * 4)),
            location=str(row.get("Location", "")),
            budget=f"₹{int(row.get('Budget', 0)) // 10000000} Cr" if pd.notna(row.get("Budget")) else None,
            workers_count=int(row.get("Workers", 0)) if pd.notna(row.get("Workers")) else 0,
            deadline=["Jun 2026", "Sep 2026", "May 2026", "Dec 2026", "Aug 2026", "Oct 2026", "Jul 2026", "Nov 2026"][i % 8],
        )
        db.add(project)
    db.commit()
    print(f"   - {min(8, len(df))} projects added")


def seed_milestones(db):
    if db.query(Milestone).count() > 0:
        print("⏭️  Milestones already exist, skipping.")
        return
    print("📊 Seeding milestones (matches Dashboard Milestones.jsx)...")
    data = [
        ("Planning", "completed", 100, "Project planning and site preparation", 1),
        ("Foundation", "completed", 100, "Foundation and structural base completed", 2),
        ("Structure", "in_progress", 75, "Building structure and framework construction", 3),
        ("Roofing", "upcoming", 0, "Roof installation and weather protection", 4),
        ("Finishing", "upcoming", 0, "Interior finishing and final inspection", 5),
    ]
    for name, status, prog, desc, order in data:
        db.add(Milestone(name=name, status=status, progress=prog, description=desc, sort_order=order))
    db.commit()
    print(f"   - {len(data)} milestones added")


def seed_kpi(db):
    if db.query(KPI).count() > 0:
        print("⏭️  KPI exists, skipping.")
        return
    print("🎯 Seeding KPI (matches Dashboard 4 cards)...")
    db.add(KPI(
        overall_risk_score=72,
        risk_label="High Risk",
        safety_compliance=96,
        active_hazards=14,
        live_alerts=5,
    ))
    db.commit()


def seed_risk_summary(db):
    if db.query(RiskSummary).count() > 0:
        print("⏭️  RiskSummary exists, skipping.")
        return
    print("⚠️  Seeding Risk Summary (matches RiskMonitoring.jsx)...")
    data = [
        ("High Risk Zones", 4, "high", 1),
        ("Active Hazards", 14, "medium", 2),
        ("Safety Violations", 8, "medium", 3),
        ("Safe Zones", 18, "low", 4),
    ]
    for label, count, sev, order in data:
        db.add(RiskSummary(label=label, count=count, severity=sev, sort_order=order))
    db.commit()


def seed_incidents(db):
    if db.query(Incident).count() > 0:
        print("⏭️  Incidents exist, skipping.")
        return
    print("🚨 Seeding Incidents (matches Latest Incidents panel)...")
    data = [
        ("PPE Violation", "3 workers without helmets — Site A", "Site A", "5 min", "high", "triangle", 1),
        ("Weather Warning", "Heavy rainfall expected — Zone B", "Zone B", "18 min", "medium", "bell", 2),
        ("Equipment Alert", "Excavator EX-04 requires inspection", "Zone A", "32 min", "medium", "hardhat", 3),
        ("Zone C Cleared", "Safety inspection completed successfully", "Zone C", "1 hr", "low", "check", 4),
    ]
    for typ, desc, loc, tago, sev, icon, order in data:
        db.add(Incident(type=typ, description=desc, location=loc, time_ago=tago, severity=sev, icon_key=icon, sort_order=order))
    db.commit()


def seed_alerts(db):
    if db.query(Alert).count() > 0:
        print("⏭️  Alerts exist, skipping.")
        return
    print("🔔 Seeding Alerts (matches Live AI Alerts)...")
    data = [
        ("PPE Violation", "3 workers detected without helmets — Site A", "CRITICAL", "5 minutes ago", "active", "hardhat", 1),
        ("Weather Warning", "Heavy rainfall expected near Zone B", "WARNING", "18 minutes ago", "active", "cloud", 2),
        ("Equipment Alert", "Excavator EX-04 requires maintenance inspection", "INFO", "32 minutes ago", "active", "tools", 3),
        ("Safety Check Completed", "Zone C safety inspection completed successfully", "RESOLVED", "1 hour ago", "resolved", "check", 4),
    ]
    for title, desc, lvl, tago, status, icon, order in data:
        db.add(Alert(title=title, description=desc, level=lvl, time_ago=tago, status=status, icon_key=icon, sort_order=order))
    db.commit()


def seed_recommendations(db):
    if db.query(Recommendation).count() > 0:
        print("⏭️  Recommendations exist, skipping.")
        return
    print("🤖 Seeding AI Recommendations (matches Recommendations.jsx)...")
    data = [
        ("Increase PPE inspections", "Increase PPE inspection frequency in Zone B.", "HIGH", "Safety", "hardhat", 1),
        ("Delay crane operation", "Strong wind conditions detected near Crane Area.", "MEDIUM", "Weather", "wind", 2),
        ("Repair safety barrier", "Damaged safety barrier detected near Zone C.", "MEDIUM", "Site Safety", "triangle", 3),
        ("Inspect electrical wiring", "Preventive inspection recommended in Basement.", "LOW", "Electrical", "bolt", 4),
    ]
    for act, desc, pri, cat, icon, order in data:
        db.add(Recommendation(action=act, description=desc, priority=pri, category=cat, icon_key=icon, sort_order=order))
    db.commit()


def seed_risk_trends_from_csv(db):
    if db.query(RiskTrend).count() > 0:
        print("⏭️  RiskTrend exists, skipping.")
        return
    csv_path = HERE.parent / "datasets" / "weather_history.csv"
    if not csv_path.exists():
        print(f"⚠️  {csv_path} not found, using hardcoded 7-day trend.")
        for i, (day, val) in enumerate([
            ("Mon", 50), ("Tue", 58), ("Wed", 52), ("Thu", 68),
            ("Fri", 62), ("Sat", 73), ("Sun", 75),
        ], start=1):
            db.add(RiskTrend(day=day, value=val, sort_order=i))
        db.commit()
        return
    print("📈 Seeding Risk Trends from weather_history.csv...")
    df = pd.read_csv(csv_path)
    if "WeatherRisk" not in df.columns:
        print("   ⚠️  No WeatherRisk column, using last 7 days of Rainfall")
        df = df.tail(7).reset_index(drop=True)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, row in df.iterrows():
            val = int(min(100, max(0, row.get("Rainfall", 50) * 0.8 + 30)))
            db.add(RiskTrend(day=days[i % 7], value=val, sort_order=i + 1))
    else:
        risk_map = {"Low": 35, "Medium": 60, "High": 85}
        df = df.tail(7).reset_index(drop=True)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, row in df.iterrows():
            base = risk_map.get(str(row.get("WeatherRisk", "Medium")), 60)
            noise = int(row.get("WindSpeed", 10)) % 15
            val = min(100, max(0, base + noise - 7))
            db.add(RiskTrend(day=days[i % 7], value=val, sort_order=i + 1))
    db.commit()
    print("   - 7 risk trend points added")


def seed_ai_site_status(db):
    if db.query(AISiteStatus).count() > 0:
        print("⏭️  AISiteStatus exists, skipping.")
        return
    print("🤖 Seeding AI Site Status...")
    db.add(AISiteStatus(monitoring="24/7", zones=32, sensor_health=98))
    db.commit()


def seed_ai_modules(db):
    if db.query(AIModule).count() > 0:
        print("⏭️  AIModules exist, skipping.")
        return
    print("🧠 Seeding AI Modules (matches AIHub.jsx)...")
    data = [
        ("Safety Intelligence", "Detect PPE violations, unsafe activities and construction site hazards using AI monitoring.", "Risk Detection", "96%", "Active", "hardhat", "#2563EB", 1),
        ("Weather Risk Prediction", "Analyze weather conditions and predict potential construction disruptions and safety risks.", "Prediction", "91%", "Active", "cloud", "#10B981", 2),
        ("Schedule Intelligence", "Predict project delays and identify activities that may impact the construction timeline.", "Delay Prediction", "87%", "Active", "calendar", "#F59E0B", 3),
        ("Cost Intelligence", "Monitor project spending and predict possible budget overruns before they occur.", "Forecast Accuracy", "89%", "Active", "money", "#EF4444", 4),
        ("Resource Optimization", "Optimize allocation of workers, equipment and materials across construction activities.", "Optimization", "94%", "Active", "users", "#8B5CF6", 5),
        ("Quality Intelligence", "Identify construction defects and quality issues using intelligent inspection and analysis.", "Detection Accuracy", "93%", "Active", "search", "#14B8A6", 6),
    ]
    for name, desc, mlabel, mval, status, icon, color, order in data:
        db.add(AIModule(
            name=name, description=desc, metric_label=mlabel, metric_value=mval,
            status=status, icon_key=icon, color=color, sort_order=order,
        ))
    db.commit()


def seed_ai_insights(db):
    if db.query(AIInsight).count() > 0:
        print("⏭️  AIInsights exist, skipping.")
        return
    print("💡 Seeding AI Insights (matches AIHub insights)...")
    data = [
        ("Safety Risk Increased", "PPE violations increased in Zone B. Additional inspection is recommended.", "red", 1),
        ("Weather Impact Detected", "Heavy rainfall may affect outdoor construction activities within the next 24 hours.", "orange", 2),
        ("Schedule Risk Identified", "Structure activities are showing signs of potential schedule delay.", "blue", 3),
    ]
    for title, desc, color, order in data:
        db.add(AIInsight(title=title, description=desc, color=color, sort_order=order))
    db.commit()


def seed_hazards(db):
    if db.query(Hazard).count() > 0:
        print("⏭️  Hazards exist, skipping.")
        return
    print("⚠️  Seeding Hazards (matches RiskCenter hazard table)...")
    data = [
        ("PPE Violation", "Workers without helmets", "Zone B", "5 min ago", "critical", "active", "hardhat", 1),
        ("Unsafe Equipment", "Equipment inspection required", "Zone A", "18 min ago", "high", "active", "tools", 2),
        ("Wet Surface", "Slip hazard detected", "Zone C", "32 min ago", "medium", "active", "tint", 3),
        ("Electrical Hazard", "Unsafe wiring detected", "Basement", "45 min ago", "high", "active", "bolt", 4),
    ]
    for name, desc, loc, tago, sev, status, icon, order in data:
        db.add(Hazard(name=name, description=desc, location=loc, time_ago=tago, severity=sev, status=status, icon_key=icon, sort_order=order))
    db.commit()


def seed_zones(db):
    if db.query(Zone).count() > 0:
        print("⏭️  Zones exist, skipping.")
        return
    print("🗺️  Seeding Zones (matches RiskCenter zone list)...")
    data = [
        ("Zone A", "Structural Area", "low", 1),
        ("Zone B", "Material Storage", "high", 2),
        ("Zone C", "Equipment Area", "medium", 3),
        ("Basement", "Electrical Area", "high", 4),
    ]
    for name, area, risk, order in data:
        db.add(Zone(name=name, area=area, risk_level=risk, sort_order=order))
    db.commit()


def seed_reports(db):
    if db.query(Report).count() > 0:
        print("⏭️  Reports exist, skipping.")
        return
    print("📄 Seeding Reports (matches Reports.jsx history)...")
    data = [
        ("Weekly Risk Assessment", "RPT-2026-042", "Risk", "Today, 10:30 AM", "Completed", "#3B82F6", 1),
        ("Safety Performance Report", "RPT-2026-041", "Safety", "Yesterday, 4:15 PM", "Completed", "#10B981", 2),
        ("Schedule Performance", "RPT-2026-040", "Schedule", "2 days ago", "Completed", "#F59E0B", 3),
        ("AI Intelligence Summary", "RPT-2026-039", "AI", "3 days ago", "Completed", "#8B5CF6", 4),
    ]
    for name, code, typ, gen, status, color, order in data:
        db.add(Report(name=name, code=code, type=typ, generated_at=gen, status=status, color=color, sort_order=order))
    db.commit()


def seed_performance_metrics(db):
    if db.query(PerformanceMetric).count() > 0:
        print("⏭️  PerformanceMetrics exist, skipping.")
        return
    print("📊 Seeding Performance Metrics (matches Reports performance)...")
    data = [
        ("Project Progress", "72%", "80%", "#3B82F6", 1),
        ("Safety Compliance", "96%", "95%", "#10B981", 2),
        ("Quality Score", "93%", "90%", "#8B5CF6", 3),
        ("Schedule Health", "78%", "85%", "#F59E0B", 4),
    ]
    for label, val, target, color, order in data:
        db.add(PerformanceMetric(label=label, value=val, target=target, color=color, sort_order=order))
    db.commit()


def main():
    print("=" * 60)
    print("🌱 BuildAI — Database Seeder")
    print("=" * 60, "\n")

    reset_schema()

    db = SessionLocal()
    try:
        # Verify connection
        db.execute(text("SELECT 1"))
        print("✅ Database connection OK\n")

        seed_users(db)
        seed_projects_from_csv(db)
        seed_milestones(db)
        seed_kpi(db)
        seed_risk_summary(db)
        seed_incidents(db)
        seed_alerts(db)
        seed_recommendations(db)
        seed_risk_trends_from_csv(db)
        seed_ai_site_status(db)
        seed_ai_modules(db)
        seed_ai_insights(db)
        seed_hazards(db)
        seed_zones(db)
        seed_reports(db)
        seed_performance_metrics(db)

        print("\n" + "=" * 60)
        print("✅ Seeding complete!")
        print("=" * 60)
        print("\n📊 Summary:")
        for model in [User, Project, Milestone, KPI, RiskSummary, Incident, Alert,
                      Recommendation, RiskTrend, AISiteStatus, AIModule, AIInsight,
                      Hazard, Zone, Report, PerformanceMetric]:
            count = db.query(model).count()
            print(f"   - {model.__tablename__}: {count} rows")
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
