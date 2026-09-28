import "./Cards.css";

import {
  FaExclamationTriangle,
  FaHardHat,
  FaBell,
  FaRobot
} from "react-icons/fa";


function Cards({ data }) {

  const overallRisk =
    data?.overall_risk_score ??
    data?.risk_score ??
    0;

  const safetyCompliance =
    data?.safety_compliance ??
    data?.compliance ??
    0;

  const activeHazards =
    data?.active_hazards ??
    data?.hazards ??
    0;

  const liveAlerts =
    data?.live_alerts ??
    data?.alerts ??
    0;


  return (
    <div className="cards">

      {/* Overall Risk */}
      <div className="card risk">

        <div className="card-top">

          <div className="iconBox riskIcon">
            <FaExclamationTriangle />
          </div>

          <span className="card-status risk-status">
            {overallRisk >= 70
              ? "HIGH"
              : overallRisk >= 40
              ? "MEDIUM"
              : "LOW"}
          </span>

        </div>

        <h4>Overall Risk Score</h4>

        <h2>{overallRisk}%</h2>

        <p>
          {overallRisk >= 70
            ? "High Risk"
            : overallRisk >= 40
            ? "Medium Risk"
            : "Low Risk"}
        </p>

        <span className="card-info">
          Live backend data
        </span>

        <div className="card-line risk-line"></div>

      </div>


      {/* Safety Compliance */}
      <div className="card safety">

        <div className="card-top">

          <div className="iconBox safetyIcon">
            <FaHardHat />
          </div>

          <span className="card-status safety-status">
            {safetyCompliance >= 90
              ? "EXCELLENT"
              : safetyCompliance >= 75
              ? "GOOD"
              : "LOW"}
          </span>

        </div>

        <h4>Safety Compliance</h4>

        <h2>{safetyCompliance}%</h2>

        <p>
          {safetyCompliance >= 90
            ? "Excellent"
            : safetyCompliance >= 75
            ? "Good"
            : "Needs Attention"}
        </p>

        <span className="card-info">
          PPE Detection Active
        </span>

        <div className="card-line safety-line"></div>

      </div>


      {/* Active Hazards */}
      <div className="card hazard">

        <div className="card-top">

          <div className="iconBox hazardIcon">
            <FaBell />
          </div>

          <span className="card-status hazard-status">
            {activeHazards} ACTIVE
          </span>

        </div>

        <h4>Active Hazards</h4>

        <h2>{activeHazards}</h2>

        <p>Detected Today</p>

        <span className="card-info">
          Monitoring Site
        </span>

        <div className="card-line hazard-line"></div>

      </div>


      {/* Live Alerts */}
      <div className="card alerts">

        <div className="card-top">

          <div className="iconBox alertIcon">
            <FaRobot />
          </div>

          <span className="card-status alert-status">
            LIVE
          </span>

        </div>

        <h4>Live Alerts</h4>

        <h2>
          {String(liveAlerts).padStart(2, "0")}
        </h2>

        <p>AI Monitoring</p>

        <span className="card-info">
          Real-Time Alerts
        </span>

        <div className="card-line alert-line"></div>

      </div>

    </div>
  );
}

export default Cards;