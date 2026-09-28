import React, { useEffect, useRef, useState } from "react";
import Sidebar from "../../components/Sidebar/Sidebar";
import "./Safety.css";

const PPE_API = "/api/ppe/detect";

/* =========================================================
   PPE API
========================================================= */

async function detectPPE(blob, filename = "camera-frame.jpg") {
  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("Please login again.");
  }

  const formData = new FormData();

  formData.append("file", blob, filename);

  const response = await fetch(PPE_API, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
        `PPE detection failed with status ${response.status}`
    );
  }

  return data;
}

/* =========================================================
   SHARED PPE RESULT
========================================================= */

function CameraResult({
  result,
  title = "AI PPE Verification Result",
}) {
  if (!result) return null;

  return (
    <div className="camera-result">
      <div className="result-header">
        <div>
          <h3>🤖 {title}</h3>

          <p>
            Result returned by the PPE detection model.
          </p>
        </div>

        <span
          className={
            result.violations > 0
              ? "result-badge danger"
              : "result-badge safe"
          }
        >
          {result.violations > 0
            ? "⚠ VIOLATION"
            : "✓ SAFE"}
        </span>
      </div>

      <div className="result-summary">
        <div>
          <strong>
            {result.workers_detected ?? 0}
          </strong>

          <span>Workers</span>
        </div>

        <div>
          <strong>
            {result.violations ?? 0}
          </strong>

          <span>Violations</span>
        </div>
      </div>

      {result.workers?.length > 0 ? (
        result.workers.map((worker, index) => (
          <div
            className="worker-result"
            key={index}
          >
            <div className="worker-result-title">
              👷 Worker {index + 1}
            </div>

            <div className="ppe-grid">
              <span
                className={
                  worker.helmet
                    ? "present"
                    : "missing"
                }
              >
                🪖 Helmet:{" "}
                <b>
                  {worker.helmet
                    ? "Present"
                    : "Missing"}
                </b>
              </span>

              <span
                className={
                  worker.vest
                    ? "present"
                    : "missing"
                }
              >
                🦺 Vest:{" "}
                <b>
                  {worker.vest
                    ? "Present"
                    : "Missing"}
                </b>
              </span>

              <span
                className={
                  worker.gloves
                    ? "present"
                    : "missing"
                }
              >
                🧤 Gloves:{" "}
                <b>
                  {worker.gloves
                    ? "Present"
                    : "Missing"}
                </b>
              </span>

              <span
                className={
                  worker.boots
                    ? "present"
                    : "missing"
                }
              >
                🥾 Boots:{" "}
                <b>
                  {worker.boots
                    ? "Present"
                    : "Missing"}
                </b>
              </span>
            </div>

            <div className="risk-row">
              <span>
                Risk:{" "}
                <b>
                  {worker.risk || "Unknown"}
                </b>
              </span>

              <span>
                Status:{" "}
                <b>
                  {worker.status || "Unknown"}
                </b>
              </span>
            </div>

            {worker.missing?.length > 0 && (
              <div className="missing-ppe">
                🚨 Missing PPE:{" "}
                <b>
                  {worker.missing.join(", ")}
                </b>
              </div>
            )}
          </div>
        ))
      ) : (
        <div className="no-worker">
          ⚠️ No worker detected in this frame.
          Please position the worker clearly in
          front of the camera and check again.
        </div>
      )}
    </div>
  );
}

/* =========================================================
   SITE ENTRY CAMERA
   OVERVIEW
========================================================= */

function LiveCamera() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const [cameraActive, setCameraActive] =
    useState(false);

  const [checking, setChecking] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");

  useEffect(() => {
    let mounted = true;

    const startCamera = async () => {
      try {
        setError("");

        if (
          !navigator.mediaDevices?.getUserMedia
        ) {
          throw new Error(
            "Camera is not supported by this browser."
          );
        }

        const stream =
          await navigator.mediaDevices.getUserMedia(
            {
              video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: "user",
              },
              audio: false,
            }
          );

        if (!mounted) {
          stream
            .getTracks()
            .forEach((track) =>
              track.stop()
            );

          return;
        }

        streamRef.current = stream;

        setCameraActive(true);

        if (videoRef.current) {
          videoRef.current.srcObject =
            stream;

          await videoRef.current
            .play()
            .catch(() => {});
        }
      } catch (err) {
        console.error(
          "Site Entry camera error:",
          err
        );

        setError(
          err.message ||
            "Camera permission denied or camera unavailable."
        );
      }
    };

    startCamera();

    return () => {
      mounted = false;

      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) =>
            track.stop()
          );

        streamRef.current = null;
      }
    };
  }, []);

  const checkInAndVerifyPPE = async () => {
    try {
      setChecking(true);
      setError("");
      setResult(null);

      const video = videoRef.current;
      const canvas = canvasRef.current;

      if (!video || !canvas) {
        throw new Error(
          "Camera is not ready."
        );
      }

      if (
        video.readyState < 2 ||
        video.videoWidth === 0 ||
        video.videoHeight === 0
      ) {
        throw new Error(
          "Camera frame is not ready. Please wait a moment."
        );
      }

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const context =
        canvas.getContext("2d");

      context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
      );

      const blob =
        await new Promise((resolve) => {
          canvas.toBlob(
            (imageBlob) =>
              resolve(imageBlob),
            "image/jpeg",
            0.9
          );
        });

      if (!blob) {
        throw new Error(
          "Could not capture camera frame."
        );
      }

      const data = await detectPPE(
        blob,
        "site-entry-frame.jpg"
      );

      console.log(
        "SITE ENTRY PPE RESULT:",
        data
      );

      setResult(data);
    } catch (err) {
      console.error(
        "Site Entry PPE Error:",
        err
      );

      setError(
        err.message ||
          "PPE verification failed."
      );
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="site-entry-camera">

      <div className="camera-frame">

        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
        />

        <div className="camera-topbar">
          <span>
            📹 Site Entry
          </span>

          <span className="live-indicator">
            ●{" "}
            {cameraActive
              ? "LIVE"
              : "CONNECTING"}
          </span>
        </div>

        <div className="camera-bottom-overlay">

          <div className="camera-ai-text">
            🤖 AI PPE Verification
          </div>

          <button
            type="button"
            className="overview-check-button"
            onClick={
              checkInAndVerifyPPE
            }
            disabled={
              !cameraActive ||
              checking
            }
          >
            {checking
              ? "🤖 Checking PPE..."
              : "✅ Check In & Verify PPE"}
          </button>

        </div>
      </div>

      <canvas
        ref={canvasRef}
        style={{
          display: "none",
        }}
      />

      {error && (
        <div className="camera-error">
          ⚠️ {error}
        </div>
      )}

      {result && (
        <CameraResult
          result={result}
        />
      )}
    </div>
  );
}

/* =========================================================
   WORKING PLACE CCTV
========================================================= */

function WorkingPlaceCamera() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const [active, setActive] =
    useState(false);

  const [ready, setReady] =
    useState(false);

  const [checking, setChecking] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) =>
            track.stop()
          );
      }
    };
  }, []);

  useEffect(() => {
    if (
      active &&
      videoRef.current &&
      streamRef.current
    ) {
      videoRef.current.srcObject =
        streamRef.current;

      videoRef.current
        .play()
        .catch(() => {});
    }
  }, [active]);

  const startCCTV = async () => {
    try {
      setError("");
      setResult(null);
      setReady(false);

      if (
        !navigator.mediaDevices?.getUserMedia
      ) {
        throw new Error(
          "Camera is not supported by this browser."
        );
      }

      const stream =
        await navigator.mediaDevices.getUserMedia(
          {
            video: {
              width: { ideal: 1280 },
              height: { ideal: 720 },
              facingMode: "environment",
            },
            audio: false,
          }
        );

      streamRef.current = stream;

      setActive(true);
    } catch (err) {
      console.error(
        "Working Place CCTV error:",
        err
      );

      setError(
        err.message ||
          "CCTV camera permission denied or unavailable."
      );
    }
  };

  const stopCCTV = () => {
    if (streamRef.current) {
      streamRef.current
        .getTracks()
        .forEach((track) =>
          track.stop()
        );

      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject =
        null;
    }

    setActive(false);
    setReady(false);
    setResult(null);
  };

  const checkPPE = async () => {
    try {
      setChecking(true);
      setError("");
      setResult(null);

      const video = videoRef.current;
      const canvas = canvasRef.current;

      if (!video || !canvas) {
        throw new Error(
          "CCTV camera is not ready."
        );
      }

      if (
        video.readyState < 2 ||
        video.videoWidth === 0 ||
        video.videoHeight === 0
      ) {
        throw new Error(
          "CCTV frame is not ready. Please wait."
        );
      }

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const context =
        canvas.getContext("2d");

      context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
      );

      const blob =
        await new Promise((resolve) => {
          canvas.toBlob(
            (imageBlob) =>
              resolve(imageBlob),
            "image/jpeg",
            0.9
          );
        });

      if (!blob) {
        throw new Error(
          "Could not capture CCTV frame."
        );
      }

      const data = await detectPPE(
        blob,
        "working-place-cctv.jpg"
      );

      console.log(
        "WORKING PLACE PPE RESULT:",
        data
      );

      setResult(data);
    } catch (err) {
      console.error(
        "Working Place PPE Error:",
        err
      );

      setError(
        err.message ||
          "PPE detection failed."
      );
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="working-camera-card">

      <div className="camera-frame">

        {active ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="camera-video"
            onLoadedMetadata={() =>
              setReady(true)
            }
            onCanPlay={() =>
              setReady(true)
            }
          />
        ) : (
          <div className="camera-placeholder">

            <div className="placeholder-icon">
              📹
            </div>

            <h3>
              Working Place CCTV
            </h3>

            <p>
              Admin live construction-area
              monitoring
            </p>

            <button
              type="button"
              className="secondary-camera-button"
              onClick={startCCTV}
            >
              🎥 View CCTV
            </button>

          </div>
        )}

        <div className="camera-topbar">

          <span>
            📹 Working Place CCTV
          </span>

          <span
            className={
              active
                ? "live-indicator"
                : "offline-indicator"
            }
          >
            ●{" "}
            {active
              ? "CCTV LIVE"
              : "OFFLINE"}
          </span>

        </div>

      </div>

      <canvas
        ref={canvasRef}
        style={{
          display: "none",
        }}
      />

      {active && (
        <div className="camera-controls">

          <button
            type="button"
            className="check-ppe-button"
            onClick={checkPPE}
            disabled={
              !ready || checking
            }
          >
            {checking
              ? "🤖 Checking PPE..."
              : !ready
              ? "⏳ Preparing CCTV..."
              : "🔍 Check PPE"}
          </button>

          <button
            type="button"
            className="stop-button"
            onClick={stopCCTV}
          >
            Stop CCTV
          </button>

        </div>
      )}

      {error && (
        <div className="camera-error">
          ⚠️ {error}
        </div>
      )}

      {result && (
        <CameraResult
          result={result}
          title="Admin PPE Verification"
        />
      )}

    </div>
  );
}

/* =========================================================
   OVERVIEW
========================================================= */

function Overview({ onOpenCameras }) {
  return (
    <>
      <div className="stats-grid">

        <SimpleStat
          title="Safety Compliance"
          value="96%"
          text="↑ 3.2% this week"
          color="green"
        />

        <SimpleStat
          title="Active Hazards"
          value="14"
          text="4 high priority"
          color="red"
        />

        <SimpleStat
          title="AI Cameras"
          value="2"
          text="Site Entry + Working Place"
          color="blue"
        />

        <SimpleStat
          title="Workers Monitored"
          value="486"
          text="Live monitoring"
          color="purple"
        />

      </div>

      <div className="content-card">

        <div className="section-header">

          <div>
            <h2>
              📹 Live AI Safety Monitoring
            </h2>

            <p>
              Check workers entering the site
              and verify required PPE using AI
              computer vision.
            </p>
          </div>

          <span className="live-badge">
            ● AI MONITORING
          </span>

        </div>

        <div className="overview-monitor">

          <div className="overview-entry">
            <LiveCamera />
          </div>

          <div className="camera-list">

            <div className="camera-location selected">

              <div>
                <strong>
                  📹 Site Entry
                </strong>

                <p>
                  Entry & Check-in ·
                  PPE Verification
                </p>

                <small>
                  Check the worker PPE
                  using the button on
                  the camera.
                </small>
              </div>

              <span className="online">
                ● LIVE
              </span>

            </div>

            <div
  className="camera-location working-place-clickable"
  onClick={onOpenCameras}
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      onOpenCameras();
    }
  }}
>
  <div>
    <strong>
      📹 Working Place
    </strong>

    <p>
      Construction Area · Admin CCTV
    </p>

    <small>
      Click to open Working Place CCTV and
      manually check PPE.
    </small>
  </div>

  <span className="online">
    ● LIVE
  </span>
</div>

          </div>

        </div>

      </div>

      <div className="content-card">

        <div className="section-header">

          <div>
            <h2>
              🤖 AI Safety Detection
            </h2>

            <p>
              Intelligent detection systems
              running across the construction site.
            </p>
          </div>

        </div>

        <div className="detection-grid">

          <DetectionCard
            icon="🦺"
            title="PPE Detection"
            description="Helmets, vests, gloves and boots"
            value="96%"
            label="Compliance"
            color="green"
          />

          <DetectionCard
            icon="⚠️"
            title="Hazard Detection"
            description="Unsafe areas and hazardous activities"
            value="14"
            label="Active Hazards"
            color="red"
          />

          <DetectionCard
            icon="👷"
            title="Worker Monitoring"
            description="Worker activity and restricted zones"
            value="486"
            label="Workers"
            color="blue"
          />

          <DetectionCard
            icon="📹"
            title="Camera Monitoring"
            description="Site Entry and Working Place"
            value="2"
            label="Locations"
            color="purple"
          />

        </div>

      </div>

      <div className="two-column">
        <Alerts />
        <Recommendation />
      </div>

      <SystemStatus />
    </>
  );
}

/* =========================================================
   PPE PHOTO DETECTION
========================================================= */

function PPEDetection() {
  const [selectedFile, setSelectedFile] =
    useState(null);

  const [preview, setPreview] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");

  const [checking, setChecking] =
    useState(false);

  const handleFileChange = (
    event
  ) => {
    const file =
      event.target.files?.[0];

    if (!file) return;

    setSelectedFile(file);

    setPreview(
      URL.createObjectURL(file)
    );

    setResult(null);
    setError("");
  };

  const detect = async () => {
    if (!selectedFile) {
      setError(
        "Please select an image first."
      );

      return;
    }

    try {
      setChecking(true);
      setError("");
      setResult(null);

      const data = await detectPPE(
        selectedFile,
        selectedFile.name
      );

      setResult(data);
    } catch (err) {
      console.error(
        "PPE Detection Error:",
        err
      );

      setError(
        err.message ||
          "PPE detection failed."
      );
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="detail-page">

      <div className="detail-hero green-bg">

        <div className="large-icon">
          🦺
        </div>

        <div>
          <h2>
            PPE Detection System
          </h2>

          <p>
            Upload a worker image and
            let AI check required
            protective equipment.
          </p>
        </div>

        <div className="active-status">
          ● AI ACTIVE
        </div>

      </div>

      <div className="content-card">

        <div className="upload-row">

          <input
            id="ppe-image-upload"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            hidden
          />

          <label
            htmlFor="ppe-image-upload"
            className="secondary-camera-button"
          >
            📁 Choose Photo
          </label>

          <button
            type="button"
            className="check-ppe-button"
            onClick={detect}
            disabled={
              !selectedFile ||
              checking
            }
          >
            {checking
              ? "🤖 Detecting..."
              : "🔍 Detect PPE"}
          </button>

        </div>

        {preview && (
          <img
            className="uploaded-preview"
            src={preview}
            alt="Worker preview"
          />
        )}

        {error && (
          <div className="camera-error">
            ⚠️ {error}
          </div>
        )}

        {result && (
          <CameraResult
            result={result}
          />
        )}

      </div>

    </div>
  );
}

/* =========================================================
   HAZARD DETECTION
========================================================= */

function HazardDetection() {
  const hazards = [
    [
      "PPE Violation",
      "Zone B",
      "5 min ago",
      "Critical",
    ],
    [
      "Unsafe Equipment",
      "Zone A",
      "18 min ago",
      "High",
    ],
    [
      "Wet Surface",
      "Zone C",
      "32 min ago",
      "Medium",
    ],
    [
      "Electrical Hazard",
      "Basement",
      "45 min ago",
      "High",
    ],
  ];

  return (
    <div className="detail-page">

      <div className="detail-hero red-bg">

        <div className="large-icon">
          ⚠️
        </div>

        <div>
          <h2>
            AI Hazard Detection
          </h2>

          <p>
            Identify unsafe conditions and
            hazardous construction activities.
          </p>
        </div>

        <div className="active-status red-status">
          ● 14 ACTIVE
        </div>

      </div>

      <div className="content-card">

        <div className="section-header">

          <div>
            <h2>
              🚨 Active Hazards
            </h2>

            <p>
              Hazards identified by
              AI-powered monitoring.
            </p>
          </div>

        </div>

        <div className="hazard-table">

          <div className="table-head">
            <span>Hazard</span>
            <span>Location</span>
            <span>Detected</span>
            <span>Severity</span>
          </div>

          {hazards.map(
            (hazard, index) => (
              <div
                className="table-row"
                key={index}
              >
                <strong>
                  {hazard[0]}
                </strong>

                <span>
                  {hazard[1]}
                </span>

                <span>
                  {hazard[2]}
                </span>

                <b
                  className={`severity ${hazard[3].toLowerCase()}`}
                >
                  {hazard[3]}
                </b>
              </div>
            )
          )}

        </div>

      </div>

    </div>
  );
}

/* =========================================================
   WORKER MONITORING
========================================================= */

function WorkerMonitoring() {
  return (
    <div className="detail-page">

      <div className="detail-hero blue-bg">

        <div className="large-icon">
          👷
        </div>

        <div>
          <h2>
            Worker Monitoring
          </h2>

          <p>
            AI-powered worker tracking
            and restricted-zone monitoring.
          </p>
        </div>

        <div className="active-status">
          ● LIVE
        </div>

      </div>

      <div className="stats-grid">

        <SimpleStat
          title="Workers Monitored"
          value="486"
          text="Live"
          color="blue"
        />

        <SimpleStat
          title="Active Zones"
          value="32"
          text="Monitored"
          color="purple"
        />

        <SimpleStat
          title="Restricted Entries"
          value="04"
          text="Today"
          color="red"
        />

        <SimpleStat
          title="Worker Safety"
          value="96%"
          text="Compliance"
          color="green"
        />

      </div>

      <div className="content-card">

        <h2>
          👷 Worker Monitoring Status
        </h2>

        <div className="worker-list">

          <Worker
            name="Zone A Workers"
            count="128"
            status="Safe"
          />

          <Worker
            name="Zone B Workers"
            count="164"
            status="Attention"
          />

          <Worker
            name="Zone C Workers"
            count="112"
            status="Safe"
          />

          <Worker
            name="Basement Workers"
            count="82"
            status="Safe"
          />

        </div>

      </div>

    </div>
  );
}

/* =========================================================
   CAMERA MONITORING
========================================================= */

function CameraMonitoring() {
  return (
    <div className="detail-page">

      <div className="detail-hero purple-bg">

        <div className="large-icon">
          📹
        </div>

        <div>
          <h2>
            Working Place CCTV
          </h2>

          <p>
            Live construction site CCTV
            monitoring for admin safety verification.
          </p>
        </div>

        <div className="active-status">
          ● ADMIN MONITORING
        </div>

      </div>

      <div className="content-card">
        <WorkingPlaceCamera />
      </div>

    </div>
  );
}

/* =========================================================
   ALERTS
========================================================= */

function Alerts() {
  return (
    <div className="content-card">

      <div className="section-header">

        <div>
          <h2>
            🔔 Live Safety Alerts
          </h2>

          <p>
            Latest hazards detected by
            the AI safety agent.
          </p>
        </div>

      </div>

      <AlertRow
        icon="⚠️"
        title="PPE Violation Detected"
        description="Worker without required PPE detected"
        time="2 min ago"
        level="HIGH"
      />

      <AlertRow
        icon="🔔"
        title="Restricted Zone Entry"
        description="Worker entered restricted area"
        time="8 min ago"
        level="MEDIUM"
      />

      <AlertRow
        icon="✓"
        title="Safety Check Completed"
        description="Zone C safety inspection completed"
        time="22 min ago"
        level="RESOLVED"
      />

    </div>
  );
}

function AlertRow({
  icon,
  title,
  description,
  time,
  level,
}) {
  return (
    <div className="alert-row">

      <div className="alert-icon">
        {icon}
      </div>

      <div className="alert-content">
        <strong>
          {title}
        </strong>

        <p>
          {description}
        </p>
      </div>

      <span className="alert-time">
        {time}
      </span>

      <span
        className={`alert-level ${level.toLowerCase()}`}
      >
        {level}
      </span>

    </div>
  );
}

/* =========================================================
   RECOMMENDATION
========================================================= */

function Recommendation() {
  return (
    <div className="recommendation">

      <div className="recommendation-icon">
        🤖
      </div>

      <h2>
        AI Safety Recommendation
      </h2>

      <p>
        Based on current site conditions
        and detected safety patterns, the
        AI agent recommends preventive actions.
      </p>

      <div className="recommendation-list">

        <div>
          🦺 Increase PPE inspections in Zone A
        </div>

        <div>
          🚧 Restrict access to excavation area
        </div>

        <div>
          📹 Review working-place CCTV
        </div>

      </div>

    </div>
  );
}

/* =========================================================
   SYSTEM STATUS
========================================================= */

function SystemStatus() {
  return (
    <div className="system-status">

      <div>
        <strong>
          ✓ AI Safety System Status
        </strong>

        <p>
          All connected safety monitoring
          systems are operating normally.
        </p>
      </div>

      <div className="system-metrics">

        <span>
          <b>24/7</b>
          Monitoring
        </span>

        <span>
          <b>2</b>
          Active Locations
        </span>

        <span>
          <b>486</b>
          Workers
        </span>

        <span>
          <b>98%</b>
          System Health
        </span>

      </div>

    </div>
  );
}

/* =========================================================
   SIMPLE STAT
========================================================= */

function SimpleStat({
  title,
  value,
  text,
  color,
}) {
  return (
    <div
      className={`stat-card ${color}`}
    >

      <div className="stat-icon">
        📊
      </div>

      <div>
        <p>{title}</p>

        <h2>{value}</h2>

        <span>{text}</span>
      </div>

    </div>
  );
}

/* =========================================================
   DETECTION CARD
========================================================= */

function DetectionCard({
  icon,
  title,
  description,
  value,
  label,
  color,
}) {
  return (
    <div
      className={`detection-card ${color}`}
    >

      <div className="detection-top">

        <div className="detection-icon">
          {icon}
        </div>

        <span className="ai-active">
          AI ACTIVE
        </span>

      </div>

      <h3>
        {title}
      </h3>

      <p>
        {description}
      </p>

      <div className="detection-value">
        {value}
      </div>

      <span className="detection-label">
        {label}
      </span>

    </div>
  );
}

/* =========================================================
   WORKER
========================================================= */

function Worker({
  name,
  count,
  status,
}) {
  return (
    <div className="worker-item">

      <div className="worker-icon">
        👷
      </div>

      <div>
        <strong>
          {name}
        </strong>

        <p>
          {count} workers currently monitored
        </p>
      </div>

      <span
        className={
          status === "Safe"
            ? "worker-safe"
            : "worker-attention"
        }
      >
        {status}
      </span>

    </div>
  );
}

/* =========================================================
   MAIN SAFETY AGENT
========================================================= */

function SafetyAgent() {
  const [activeTab, setActiveTab] =
    useState("overview");

  const tabs = [
    ["overview", "🏠", "Overview"],
    ["ppe", "🦺", "PPE Detection"],
    ["hazards", "⚠️", "Hazard Detection"],
    ["workers", "👷", "Worker Monitoring"],
    ["cameras", "📹", "Camera Monitoring"],
  ];

  return (
    <div className="safety-page">

      <Sidebar />

      <main className="safety-main-content">

        <header className="safety-header">

          <div className="header-left">

            <div className="header-icon">
              🛡️
            </div>

            <div>

              <h1>
                Safety Intelligence Agent
              </h1>

              <p>
                AI-powered worker protection
                and construction safety monitoring.
              </p>

            </div>

          </div>

          <div className="agent-status">

            <span className="status-dot">
              ●
            </span>{" "}
            AI Agent Online

          </div>

        </header>

        <div className="safety-tabs">

          {tabs.map(
            ([id, icon, label]) => (
              <button
                key={id}
                type="button"
                className={`safety-tab ${
                  activeTab === id
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  setActiveTab(id)
                }
              >
                <span>
                  {icon}
                </span>

                {label}
              </button>
            )
          )}

        </div>

        {activeTab === "overview" && (
  <Overview
    onOpenCameras={() =>
      setActiveTab("cameras")
    }
  />
)}
        {activeTab === "ppe" && (
          <PPEDetection />
        )}

        {activeTab === "hazards" && (
          <HazardDetection />
        )}

        {activeTab === "workers" && (
          <WorkerMonitoring />
        )}

        {activeTab === "cameras" && (
          <CameraMonitoring />
        )}

      </main>

    </div>
  );
}

export default SafetyAgent;