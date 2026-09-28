import { useEffect, useState } from "react";

import Sidebar from "../../components/Sidebar/Sidebar";
import Navbar from "../../components/Navbar/Navbar";

import Cards from "../../components/Cards/Cards";
import ProgressChart from "../../components/Charts/ProgressChart";
import RiskGauge from "../../components/RiskGauge/RiskGauge";
import Recommendations from "../../components/Alerts/Recommendations";
import Alerts from "../../components/Alerts/Alerts";
import RiskMonitoring from "../../components/RiskMonitoring/RiskMonitoring";
import Milestones from "../../components/Milestones/Milestones";
import RiskTrend from "../../components/RiskTrend/RiskTrend";
import ProjectsTable from "../../components/ProjectsTable/ProjectsTable";

import {
  getDashboardKPIs,
  getProjectProgress,
  getRiskGauge,
  getRiskTrend,
  getRiskSummary,
  getDashboardIncidents,
  getAISiteStatus,
  getRiskDistribution,
} from "../../api/client";

import "./Dashboard.css";


function Dashboard() {
  // ============================================================
  // DASHBOARD STATE
  // ============================================================

  const [dashboardData, setDashboardData] = useState({
    kpis: null,
    projectProgress: null,
    riskGauge: null,
    riskTrend: null,
    riskSummary: null,
    incidents: [],
    aiSiteStatus: null,
    riskDistribution: null,
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // ============================================================
  // LOAD DASHBOARD DATA
  // AUTO REFRESH EVERY 10 SECONDS
  // ============================================================

  useEffect(() => {
    let mounted = true;

    const loadDashboard = async () => {
      try {
        setError("");

        const [
          kpis,
          projectProgress,
          riskGauge,
          riskTrend,
          riskSummary,
          incidents,
          aiSiteStatus,
          riskDistribution,
        ] = await Promise.all([
          getDashboardKPIs(),
          getProjectProgress(),
          getRiskGauge(),
          getRiskTrend(7),
          getRiskSummary(),
          getDashboardIncidents(),
          getAISiteStatus(),
          getRiskDistribution(),
        ]);

        if (!mounted) {
          return;
        }

        setDashboardData({
          kpis,
          projectProgress,
          riskGauge,
          riskTrend,
          riskSummary,
          incidents,
          aiSiteStatus,
          riskDistribution,
        });

        setLoading(false);
      } catch (err) {
        console.error("Dashboard API Error:", err);

        if (mounted) {
          setError(
            err.message || "Failed to load dashboard data"
          );

          setLoading(false);
        }
      }
    };

    // Initial dashboard load
    loadDashboard();

    // Refresh dashboard data every 10 seconds
    const interval = setInterval(() => {
      loadDashboard();
    }, 10000);

    // Cleanup
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);


  // ============================================================
  // LOADING STATE
  // ============================================================

  if (loading) {
    return (
      <div className="dashboard">
        <Sidebar />

        <div className="dashboard-main">
          <Navbar />

          <div className="content">
            <div className="page-header">
              <h1>
                🏗 Construction Intelligence Hub
              </h1>

              <p>
                Loading live dashboard data from backend...
              </p>
            </div>

            <div className="content-card">
              <h2>🔄 Loading Dashboard</h2>

              <p>
                Connecting to the FastAPI backend and
                retrieving the latest site intelligence data.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }


  // ============================================================
  // ERROR STATE
  // ============================================================

  if (error) {
    return (
      <div className="dashboard">
        <Sidebar />

        <div className="dashboard-main">
          <Navbar />

          <div className="content">
            <div className="page-header">
              <h1>
                🏗 Construction Intelligence Hub
              </h1>

              <p>
                Dashboard data could not be loaded.
              </p>
            </div>

            <div className="content-card">
              <h2>
                ⚠️ Backend Connection Error
              </h2>

              <p>{error}</p>

              <button
                onClick={() => window.location.reload()}
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }


  // ============================================================
  // MAIN DASHBOARD
  // ============================================================

  return (
    <div className="dashboard">

      {/* ========================================================
          SIDEBAR
      ======================================================== */}

      <Sidebar />


      {/* ========================================================
          MAIN AREA
      ======================================================== */}

      <div className="dashboard-main">

        {/* ======================================================
            NAVBAR
        ====================================================== */}

        <Navbar />


        {/* ======================================================
            CONTENT
        ====================================================== */}

        <div className="content">

          {/* ====================================================
              PAGE HEADER
          ==================================================== */}

          <div className="page-header">
            <h1>
              🏗 Construction Intelligence Hub
            </h1>

            <p>
              AI-powered Site Risk Monitoring and Safety
              Intelligence Platform for proactive hazard detection,
              worker protection, and intelligent construction
              management.
            </p>

            <div
              style={{
                marginTop: "10px",
                fontSize: "13px",
                color: "#16a34a",
                fontWeight: "600",
              }}
            >
              ● LIVE DATA • Auto-refreshing every 10 seconds
            </div>
          </div>


          {/* ====================================================
              KPI CARDS
          ==================================================== */}

          <Cards
            data={dashboardData.kpis}
          />


          {/* ====================================================
              PROJECT PROGRESS + RISK
          ==================================================== */}

          <div className="chartSection">

            <ProgressChart
              data={dashboardData.projectProgress}
            />

            <RiskGauge
              data={dashboardData.riskGauge}
            />

            <RiskMonitoring
              data={dashboardData.riskSummary}
            />

            <Milestones
              data={dashboardData.projectProgress}
            />

            <RiskTrend
              data={dashboardData.riskTrend}
            />

            <ProjectsTable
              data={dashboardData.riskDistribution}
            />

          </div>


          {/* ====================================================
              RECOMMENDATIONS + ALERTS
          ==================================================== */}

          <div className="bottom-section">

            <Recommendations
              data={dashboardData.aiSiteStatus}
            />

            <Alerts
              data={dashboardData.incidents}
            />

          </div>

        </div>
      </div>
    </div>
  );
}


export default Dashboard;