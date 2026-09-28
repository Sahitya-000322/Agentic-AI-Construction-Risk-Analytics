import { useEffect, useState } from "react";

import Sidebar from "../../components/Sidebar/Sidebar";
import Navbar from "../../components/Navbar/Navbar";

import "./Reports.css";

import {
  FaChartBar,
  FaDownload,
  FaFileAlt,
  FaShieldAlt,
  FaExclamationTriangle,
  FaRobot,
  FaArrowUp,
  FaSyncAlt,
} from "react-icons/fa";

import {
  getReports,
  getReportsSummary,
  getReportsPerformance,
  getReportsInsight,
} from "../../api/client";


function Reports() {

  // ============================================================
  // STATE
  // ============================================================

  const [reports, setReports] = useState([]);

  const [generatedReports, setGeneratedReports] = useState([]);

  const [summary, setSummary] = useState(null);

  const [performance, setPerformance] = useState(null);

  const [insight, setInsight] = useState(null);

  const [loading, setLoading] = useState(true);

  const [generating, setGenerating] = useState(false);

  const [error, setError] = useState("");

  const [lastUpdated, setLastUpdated] = useState(null);


  // ============================================================
  // GET VALUE
  // ============================================================

  const getValue = (object, keys, fallback = 0) => {

    if (!object) {
      return fallback;
    }

    for (const key of keys) {

      if (
        object[key] !== undefined &&
        object[key] !== null &&
        object[key] !== ""
      ) {
        return object[key];
      }

    }

    return fallback;
  };


  // ============================================================
  // NUMBER
  // ============================================================

  const toNumber = (value, fallback = 0) => {

    if (
      typeof value === "number" &&
      Number.isFinite(value)
    ) {
      return value;
    }

    if (typeof value === "string") {

      const cleaned =
        value.replace("%", "").trim();

      const number =
        Number(cleaned);

      if (Number.isFinite(number)) {
        return number;
      }

    }

    return fallback;
  };


  // ============================================================
  // NORMALIZE PERFORMANCE
  // ============================================================

  const normalizePerformance = (raw) => {

    if (!raw) {

      return {
        project_progress: 0,
        safety_compliance: 0,
        quality_score: 0,
        schedule_health: 0,
      };

    }

    let data = raw;


    if (
      raw.data &&
      !Array.isArray(raw.data)
    ) {
      data = raw.data;
    }


    if (
      raw.performance &&
      !Array.isArray(raw.performance)
    ) {
      data = raw.performance;
    }


    if (
      data.performance_metrics &&
      !Array.isArray(data.performance_metrics)
    ) {
      data = data.performance_metrics;
    }


    // ----------------------------------------------------------
    // ARRAY RESPONSE
    // ----------------------------------------------------------

    if (Array.isArray(data)) {

      const result = {

        project_progress: 0,

        safety_compliance: 0,

        quality_score: 0,

        schedule_health: 0,

      };


      data.forEach((item) => {

        if (!item) {
          return;
        }


        const label =
          String(
            item.metric ||
            item.name ||
            item.title ||
            item.label ||
            item.type ||
            ""
          ).toLowerCase();


        const value =
          toNumber(
            item.value ??
            item.score ??
            item.percentage ??
            item.progress ??
            item.metric_value ??
            item.amount,
            0
          );


        if (
          label.includes("project") &&
          label.includes("progress")
        ) {

          result.project_progress = value;

        } else if (
          label.includes("safety") ||
          label.includes("compliance")
        ) {

          result.safety_compliance = value;

        } else if (
          label.includes("quality")
        ) {

          result.quality_score = value;

        } else if (
          label.includes("schedule")
        ) {

          result.schedule_health = value;

        }

      });


      return result;

    }


    // ----------------------------------------------------------
    // OBJECT RESPONSE
    // ----------------------------------------------------------

    return {

      project_progress:
        toNumber(
          getValue(
            data,
            [
              "project_progress",
              "projectProgress",
              "progress",
              "projectProgressPercentage",
              "progress_percentage",
            ],
            0
          )
        ),


      safety_compliance:
        toNumber(
          getValue(
            data,
            [
              "safety_compliance",
              "safetyCompliance",
              "safety_score",
              "safetyScore",
              "compliance",
            ],
            0
          )
        ),


      quality_score:
        toNumber(
          getValue(
            data,
            [
              "quality_score",
              "qualityScore",
              "quality",
            ],
            0
          )
        ),


      schedule_health:
        toNumber(
          getValue(
            data,
            [
              "schedule_health",
              "scheduleHealth",
              "schedule",
              "schedule_score",
            ],
            0
          )
        ),

    };

  };


  // ============================================================
  // DATE FORMAT
  // ============================================================

  const formatDate = (value) => {

    if (!value) {
      return "—";
    }

    const date =
      new Date(value);

    if (
      Number.isNaN(
        date.getTime()
      )
    ) {
      return String(value);
    }

    return date.toLocaleString();

  };


  // ============================================================
  // LOAD REPORT DATA
  // ============================================================

  const loadReports = async () => {

    try {

      setError("");


      const [
        reportsData,
        summaryData,
        performanceData,
        insightData,
      ] = await Promise.all([

        getReports(),

        getReportsSummary(),

        getReportsPerformance(),

        getReportsInsight(),

      ]);


      // --------------------------------------------------------
      // REPORTS
      // --------------------------------------------------------

      const reportRows =
        Array.isArray(reportsData)
          ? reportsData
          : reportsData?.reports ||
            reportsData?.data ||
            reportsData?.items ||
            [];


      // --------------------------------------------------------
      // SUMMARY
      // --------------------------------------------------------

      const cleanSummary =
        summaryData?.data ||
        summaryData?.summary ||
        summaryData ||
        {};


      // --------------------------------------------------------
      // PERFORMANCE
      // --------------------------------------------------------

      const cleanPerformance =
        normalizePerformance(
          performanceData
        );


      // --------------------------------------------------------
      // INSIGHT
      // --------------------------------------------------------

      const cleanInsight =
        insightData?.data ||
        insightData?.insight ||
        insightData ||
        {};


      setReports(reportRows);

      setSummary(cleanSummary);

      setPerformance(cleanPerformance);

      setInsight(cleanInsight);

      setLastUpdated(
        new Date()
      );


    } catch (err) {

      console.error(
        "Reports API Error:",
        err
      );

      setError(
        err.message ||
        "Failed to load report data"
      );

    } finally {

      setLoading(false);

    }

  };


  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {

    loadReports();


    const interval =
      setInterval(
        loadReports,
        30000
      );


    return () => {

      clearInterval(
        interval
      );

    };

  }, []);


  // ============================================================
  // SUMMARY VALUES
  // ============================================================

  const totalReports =
    toNumber(
      getValue(
        summary,
        [
          "total_reports",
          "totalReports",
          "count",
          "total",
        ],
        reports.length
      ),
      reports.length
    );


  const safetyScore =
    toNumber(
      getValue(
        summary,
        [
          "safety_score",
          "safetyScore",
          "safety_compliance",
          "safetyCompliance",
        ],
        performance?.safety_compliance ||
        0
      )
    );


  const riskEvents =
    toNumber(
      getValue(
        summary,
        [
          "risk_events",
          "riskEvents",
          "risk_count",
          "riskCount",
          "events",
        ],
        0
      )
    );


  const aiInsights =
    toNumber(
      getValue(
        summary,
        [
          "ai_insights",
          "aiInsights",
          "insights",
          "insight_count",
        ],
        0
      )
    );


  // ============================================================
  // PERFORMANCE
  // ============================================================

  const projectProgress =
    toNumber(
      performance?.project_progress,
      0
    );


  const safetyCompliance =
    toNumber(
      performance?.safety_compliance,
      safetyScore
    );


  const qualityScore =
    toNumber(
      performance?.quality_score,
      0
    );


  const scheduleHealth =
    toNumber(
      performance?.schedule_health,
      0
    );


  // ============================================================
  // AI INSIGHT
  // ============================================================

  const insightText =
    typeof insight === "string"
      ? insight
      : getValue(
          insight,
          [
            "insight",
            "message",
            "summary",
            "description",
            "text",
          ],
          "No AI insight is currently available."
        );


  const aiConfidence =
    toNumber(
      getValue(
        insight,
        [
          "confidence",
          "ai_confidence",
          "aiConfidence",
        ],
        0
      )
    );


  // ============================================================
  // GENERATE REPORT
  // ============================================================

  const generateReport = async () => {

    try {

      setGenerating(true);

      setError("");


      // Get latest backend data

      const [
        latestSummaryRaw,
        latestPerformanceRaw,
        latestInsightRaw,
      ] = await Promise.all([

        getReportsSummary(),

        getReportsPerformance(),

        getReportsInsight(),

      ]);


      const latestSummary =
        latestSummaryRaw?.data ||
        latestSummaryRaw?.summary ||
        latestSummaryRaw ||
        {};


      const latestPerformance =
        normalizePerformance(
          latestPerformanceRaw
        );


      const latestInsight =
        latestInsightRaw?.data ||
        latestInsightRaw?.insight ||
        latestInsightRaw ||
        {};


      // --------------------------------------------------------
      // UNIQUE REPORT ID
      // --------------------------------------------------------

      const now =
        new Date();


      const reportId =
        `RPT-${now.getFullYear()}-${String(
          now.getMonth() + 1
        ).padStart(2, "0")}${String(
          now.getDate()
        ).padStart(2, "0")}-${String(
          now.getHours()
        ).padStart(2, "0")}${String(
          now.getMinutes()
        ).padStart(2, "0")}${String(
          now.getSeconds()
        ).padStart(2, "0")}`;


      const generatedAt =
        now.toLocaleString();


      // --------------------------------------------------------
      // LATEST VALUES
      // --------------------------------------------------------

      const reportSafetyScore =
        toNumber(
          getValue(
            latestSummary,
            [
              "safety_score",
              "safetyScore",
              "safety_compliance",
              "safetyCompliance",
            ],
            latestPerformance.safety_compliance
          )
        );


      const reportRiskEvents =
        toNumber(
          getValue(
            latestSummary,
            [
              "risk_events",
              "riskEvents",
              "risk_count",
              "riskCount",
              "events",
            ],
            0
          )
        );


      const reportAIInsights =
        toNumber(
          getValue(
            latestSummary,
            [
              "ai_insights",
              "aiInsights",
              "insights",
              "insight_count",
            ],
            0
          )
        );


      const reportInsightText =
        typeof latestInsight === "string"
          ? latestInsight
          : getValue(
              latestInsight,
              [
                "insight",
                "message",
                "summary",
                "description",
                "text",
              ],
              "No AI insight is currently available."
            );


      const reportConfidence =
        toNumber(
          getValue(
            latestInsight,
            [
              "confidence",
              "ai_confidence",
              "aiConfidence",
            ],
            0
          )
        );


      // --------------------------------------------------------
      // NEW REPORT
      // --------------------------------------------------------

      const newReport = {

        id: reportId,

        name:
          "Construction Intelligence Report",

        title:
          "Construction Intelligence Report",

        type:
          "AI",

        category:
          "Intelligence",

        generated_at:
          now.toISOString(),

        status:
          "Completed",

        safety_score:
          reportSafetyScore,

        risk_events:
          reportRiskEvents,

        ai_insights:
          reportAIInsights,

        project_progress:
          latestPerformance.project_progress,

        safety_compliance:
          latestPerformance.safety_compliance,

        quality_score:
          latestPerformance.quality_score,

        schedule_health:
          latestPerformance.schedule_health,

      };


      // Add new report to UI

      setGeneratedReports(
        (previous) => [
          newReport,
          ...previous,
        ]
      );


      // --------------------------------------------------------
      // CREATE HTML REPORT
      // --------------------------------------------------------

      const reportHTML = `

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
Construction Intelligence Report
</title>

<style>

body {
  font-family: Arial, sans-serif;
  margin: 40px;
  color: #1f2937;
}

.header {
  border-bottom: 2px solid #2563eb;
  padding-bottom: 20px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-top: 20px;
}

.metric {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 18px;
  background: #f9fafb;
}

.metric span {
  display: block;
  color: #6b7280;
  font-size: 13px;
}

.metric strong {
  display: block;
  font-size: 28px;
  margin-top: 8px;
}

.performance {
  margin-top: 20px;
}

.performance-row {
  margin: 18px 0;
}

.performance-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.bar {
  width: 100%;
  height: 10px;
  background: #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
}

.fill {
  height: 100%;
  background: #2563eb;
}

.insight {
  margin-top: 25px;
  padding: 20px;
  background: #f5f3ff;
  border-radius: 10px;
}

.footer {
  margin-top: 40px;
  color: #6b7280;
  font-size: 12px;
}

</style>

</head>

<body>


<div class="header">

<h1>
Construction Intelligence Report
</h1>

<p>
AI-powered project performance, safety,
risk and construction intelligence report.
</p>

<p>
Report ID:
<strong>
${reportId}
</strong>
</p>

<p>
Generated:
${generatedAt}
</p>

</div>


<h2>
Executive Summary
</h2>


<div class="metrics">


<div class="metric">

<span>
Total Reports
</span>

<strong>
${totalReports + 1}
</strong>

</div>


<div class="metric">

<span>
Safety Score
</span>

<strong>
${reportSafetyScore}%
</strong>

</div>


<div class="metric">

<span>
Risk Events
</span>

<strong>
${reportRiskEvents}
</strong>

</div>


<div class="metric">

<span>
AI Insights
</span>

<strong>
${reportAIInsights}
</strong>

</div>


</div>


<h2>
Project Performance
</h2>


<div class="performance">


<div class="performance-row">

<div class="performance-label">

<strong>
Project Progress
</strong>

<strong>
${latestPerformance.project_progress}%
</strong>

</div>

<div class="bar">

<div
class="fill"
style="
width:${latestPerformance.project_progress}%
"
></div>

</div>

</div>


<div class="performance-row">

<div class="performance-label">

<strong>
Safety Compliance
</strong>

<strong>
${latestPerformance.safety_compliance}%
</strong>

</div>

<div class="bar">

<div
class="fill"
style="
width:${latestPerformance.safety_compliance}%
"
></div>

</div>

</div>


<div class="performance-row">

<div class="performance-label">

<strong>
Quality Score
</strong>

<strong>
${latestPerformance.quality_score}%
</strong>

</div>

<div class="bar">

<div
class="fill"
style="
width:${latestPerformance.quality_score}%
"
></div>

</div>

</div>


<div class="performance-row">

<div class="performance-label">

<strong>
Schedule Health
</strong>

<strong>
${latestPerformance.schedule_health}%
</strong>

</div>

<div class="bar">

<div
class="fill"
style="
width:${latestPerformance.schedule_health}%
"
></div>

</div>

</div>


</div>


<h2>
AI Report Insight
</h2>


<div class="insight">

<p>
${reportInsightText}
</p>

<p>
AI Confidence:
<strong>
${reportConfidence}%
</strong>
</p>

</div>


<div class="footer">

Construction Intelligence Hub

</div>


</body>

</html>

`;


      // --------------------------------------------------------
      // DOWNLOAD
      // --------------------------------------------------------

      const blob =
        new Blob(
          [reportHTML],
          {
            type: "text/html",
          }
        );


      const url =
        URL.createObjectURL(
          blob
        );


      const link =
        document.createElement(
          "a"
        );


      link.href = url;


      link.download =
        `${reportId}.html`;


      document.body.appendChild(
        link
      );


      link.click();


      document.body.removeChild(
        link
      );


      URL.revokeObjectURL(
        url
      );


    } catch (err) {

      console.error(
        "Generate Report Error:",
        err
      );

      setError(
        err.message ||
        "Failed to generate report"
      );

    } finally {

      setGenerating(false);

    }

  };


  // ============================================================
  // COMBINED REPORT LIST
  // ============================================================

  const allReports = [
    ...generatedReports,
    ...reports,
  ];


  // ============================================================
  // LOADING
  // ============================================================

  if (loading) {

    return (
      <>

        <Sidebar />

        <div className="reportsPage">

          <Navbar />

          <div className="reportsContent">

            <div className="reportsHeader">

              <div>

                <h1>
                  <FaChartBar />
                  Construction Reports
                </h1>

                <p>
                  Loading live report data from backend...
                </p>

              </div>

            </div>

          </div>

        </div>

      </>
    );

  }


  // ============================================================
  // PAGE
  // ============================================================

  return (

    <>

      <Sidebar />


      <div className="reportsPage">


        <Navbar />


        <div className="reportsContent">


          {/* ==================================================
              HEADER
          ================================================== */}

          <div className="reportsHeader">


            <div>

              <h1>

                <FaChartBar />

                Construction Reports

              </h1>


              <p>

                Project performance, safety, risk and AI
                intelligence reports in one place.

              </p>

            </div>


            <button

              className="generateReport"

              onClick={
                generateReport
              }

              disabled={
                generating
              }

            >

              {generating ? (

                <>

                  <FaSyncAlt />

                  Generating...

                </>

              ) : (

                <>

                  <FaDownload />

                  Generate Report

                </>

              )}

            </button>


          </div>


          {/* ==================================================
              ERROR
          ================================================== */}

          {error && (

            <div className="content-card">

              <p>

                ⚠️ {error}

              </p>


              <button
                onClick={
                  loadReports
                }
              >

                Retry

              </button>

            </div>

          )}


          {/* ==================================================
              SUMMARY
          ================================================== */}

          <div className="reportSummary">


            <div className="reportCard">

              <div className="reportIcon blue">

                <FaFileAlt />

              </div>


              <span>
                Total Reports
              </span>


              <strong>
                {totalReports}
              </strong>


              <small>
                Live backend data
              </small>

            </div>


            <div className="reportCard">

              <div className="reportIcon green">

                <FaShieldAlt />

              </div>


              <span>
                Safety Score
              </span>


              <strong>
                {safetyScore}%
              </strong>


              <small className="positive">

                <FaArrowUp />

                Live safety data

              </small>

            </div>


            <div className="reportCard">

              <div className="reportIcon orange">

                <FaExclamationTriangle />

              </div>


              <span>
                Risk Events
              </span>


              <strong>
                {riskEvents}
              </strong>


              <small className="negative">

                Current risk activity

              </small>

            </div>


            <div className="reportCard">

              <div className="reportIcon purple">

                <FaRobot />

              </div>


              <span>
                AI Insights
              </span>


              <strong>
                {aiInsights}
              </strong>


              <small className="positive">

                Backend intelligence

              </small>

            </div>


          </div>


          {/* ==================================================
              PERFORMANCE
          ================================================== */}

          <section className="performancePanel">


            <div className="reportSectionHeader">


              <div>

                <h2>
                  Project Performance
                </h2>


                <p>
                  Current construction performance indicators
                </p>

              </div>


              <span className="periodBadge">
                Live
              </span>


            </div>


            <div className="performanceGrid">


              {/* PROJECT */}

              <div className="performanceItem">

                <div className="performanceTop">

                  <span>
                    Project Progress
                  </span>


                  <strong>
                    {projectProgress}%
                  </strong>

                </div>


                <div className="reportProgress">

                  <div

                    className="
                      reportProgressFill
                      blueProgress
                    "

                    style={{
                      width:
                        `${Math.min(
                          Math.max(
                            projectProgress,
                            0
                          ),
                          100
                        )}%`,
                    }}

                  />

                </div>


                <small>
                  Live backend value
                </small>

              </div>


              {/* SAFETY */}

              <div className="performanceItem">

                <div className="performanceTop">

                  <span>
                    Safety Compliance
                  </span>


                  <strong>
                    {safetyCompliance}%
                  </strong>

                </div>


                <div className="reportProgress">

                  <div

                    className="
                      reportProgressFill
                      greenProgress
                    "

                    style={{
                      width:
                        `${Math.min(
                          Math.max(
                            safetyCompliance,
                            0
                          ),
                          100
                        )}%`,
                    }}

                  />

                </div>


                <small>
                  Live backend value
                </small>

              </div>


              {/* QUALITY */}

              <div className="performanceItem">

                <div className="performanceTop">

                  <span>
                    Quality Score
                  </span>


                  <strong>
                    {qualityScore}%
                  </strong>

                </div>


                <div className="reportProgress">

                  <div

                    className="
                      reportProgressFill
                      purpleProgress
                    "

                    style={{
                      width:
                        `${Math.min(
                          Math.max(
                            qualityScore,
                            0
                          ),
                          100
                        )}%`,
                    }}

                  />

                </div>


                <small>
                  Live backend value
                </small>

              </div>


              {/* SCHEDULE */}

              <div className="performanceItem">

                <div className="performanceTop">

                  <span>
                    Schedule Health
                  </span>


                  <strong>
                    {scheduleHealth}%
                  </strong>

                </div>


                <div className="reportProgress">

                  <div

                    className="
                      reportProgressFill
                      orangeProgress
                    "

                    style={{
                      width:
                        `${Math.min(
                          Math.max(
                            scheduleHealth,
                            0
                          ),
                          100
                        )}%`,
                    }}

                  />

                </div>


                <small>
                  Live backend value
                </small>

              </div>


            </div>

          </section>


          {/* ==================================================
              REPORT HISTORY
          ================================================== */}

          <section className="reportHistory">


            <div className="reportSectionHeader">

              <div>

                <h2>

                  <FaFileAlt />

                  Recent Reports

                </h2>


                <p>
                  Generated project intelligence reports
                </p>

              </div>

            </div>


            <div className="reportTable">


              <div className="reportTableHeader">

                <span>
                  Report
                </span>

                <span>
                  Type
                </span>

                <span>
                  Generated
                </span>

                <span>
                  Status
                </span>

                <span>
                  Action
                </span>

              </div>


              {allReports.length === 0 ? (

                <div className="reportRow">

                  <div className="reportName">

                    <div className="fileIcon blue">

                      <FaFileAlt />

                    </div>


                    <div>

                      <strong>
                        No reports available
                      </strong>

                      <small>
                        Backend returned no reports
                      </small>

                    </div>

                  </div>


                  <span>—</span>

                  <span>—</span>

                  <span>—</span>

                  <span>—</span>

                </div>

              ) : (

                allReports
                  .slice(0, 10)
                  .map(
                    (
                      report,
                      index
                    ) => {


                      const reportName =
                        report.name ||
                        report.title ||
                        report.report_name ||
                        "Construction Report";


                      const reportType =
                        report.type ||
                        report.category ||
                        "Report";


                      const generated =
                        report.generated_at ||
                        report.generatedAt ||
                        report.created_at ||
                        report.createdAt;


                      const status =
                        report.status ||
                        "Completed";


                      return (

                        <div

                          className="reportRow"

                          key={
                            report.id ||
                            `${reportName}-${index}`
                          }

                        >


                          <div className="reportName">


                            <div className="fileIcon blue">

                              <FaFileAlt />

                            </div>


                            <div>

                              <strong>

                                {reportName}

                              </strong>


                              <small>

                                {report.id ||
                                  report.report_id ||
                                  `RPT-${index + 1}`}

                              </small>

                            </div>


                          </div>


                          <span>

                            {reportType}

                          </span>


                          <span>

                            {formatDate(
                              generated
                            )}

                          </span>


                          <span className="completedReport">

                            {status}

                          </span>


                          <button

                            className="downloadButton"

                            onClick={
                              generateReport
                            }

                            title="
                              Generate new report
                            "

                          >

                            <FaDownload />

                          </button>


                        </div>

                      );

                    }
                  )

              )}


            </div>

          </section>


          {/* ==================================================
              AI INSIGHT
          ================================================== */}

          <section className="reportInsight">


            <div className="insightRobot">

              <FaRobot />

            </div>


            <div>

              <h3>
                AI Report Insight
              </h3>


              <p>
                {insightText}
              </p>

            </div>


            <div className="insightScore">

              <span>
                AI Confidence
              </span>


              <strong>
                {aiConfidence}%
              </strong>

            </div>


          </section>


          {/* ==================================================
              FOOTER
          ================================================== */}

          <div className="reportsFooter">


            <span>

              Reports powered by
              Construction Intelligence Hub

            </span>


            <span>

              Last updated:{" "}

              {lastUpdated
                ? lastUpdated.toLocaleTimeString()
                : "—"}

            </span>


          </div>


        </div>

      </div>

    </>

  );

}


export default Reports;