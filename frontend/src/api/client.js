const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";


// ============================================================
// COMMON API REQUEST
// ============================================================

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    ...(options.headers || {}),
  };

  // Attach JWT token
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  // JSON content type
  // Do not add it for FormData requests
  if (
    options.body &&
    !(options.body instanceof FormData)
  ) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers,
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  // Token expired / invalid
  if (response.status === 401) {
    localStorage.removeItem("access_token");
  }

  // API error
  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      `API request failed with status ${response.status}`;

    throw new Error(message);
  }

  return data;
}


// ============================================================
// AUTH
// ============================================================

export async function login(email, password) {
  const body = new URLSearchParams();

  body.append("username", email);
  body.append("password", password);

  const response = await fetch(
    `${API_BASE_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
      body,
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
        `Login failed with status ${response.status}`
    );
  }

  if (data?.access_token) {
    localStorage.setItem(
      "access_token",
      data.access_token
    );
  }

  return data;
}


export function logout() {
  localStorage.removeItem("access_token");
}


export function isAuthenticated() {
  return Boolean(
    localStorage.getItem("access_token")
  );
}


// ============================================================
// GENERAL API
// ============================================================

export async function get(endpoint) {
  return apiRequest(endpoint, {
    method: "GET",
  });
}


export async function post(endpoint, body) {
  return apiRequest(endpoint, {
    method: "POST",
    body: JSON.stringify(body),
  });
}


export async function put(endpoint, body) {
  return apiRequest(endpoint, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}


export async function del(endpoint) {
  return apiRequest(endpoint, {
    method: "DELETE",
  });
}


// ============================================================
// HEALTH
// ============================================================

export async function getHealth() {
  return get("/health");
}


// ============================================================
// ML MODELS
// ============================================================

export async function getMLModels() {
  return get("/ml/models");
}


export async function predictSafetyRisk(data) {
  return post(
    "/ml/predict/safety-risk",
    data
  );
}


export async function predictInjury(features) {
  return post(
    "/ml/predict/injury",
    {
      features,
    }
  );
}


export async function predictDelay(data) {
  return post(
    "/ml/predict/delay",
    data
  );
}


export async function predictCost(data) {
  return post(
    "/ml/predict/cost",
    data
  );
}


export async function predictSchedule(features) {
  return post(
    "/ml/predict/schedule",
    {
      features,
    }
  );
}


export async function predictProjectDelay(features) {
  return post(
    "/ml/predict/project-delay",
    {
      features,
    }
  );
}


export async function predictResource(features) {
  return post(
    "/ml/predict/resource",
    {
      features,
    }
  );
}


export async function predictCompliance(features) {
  return post(
    "/ml/predict/compliance",
    {
      features,
    }
  );
}


export async function predictInsurance(features) {
  return post(
    "/ml/predict/insurance",
    {
      features,
    }
  );
}


// ============================================================
// DASHBOARD
// ============================================================

export async function getDashboardKPIs() {
  return get("/dashboard/kpis");
}


export async function getProjectProgress() {
  return get("/dashboard/project-progress");
}


export async function getRiskGauge() {
  return get("/dashboard/risk-gauge");
}


export async function getRiskTrend(days = 7) {
  return get(
    `/dashboard/risk-trend?days=${days}`
  );
}


export async function getRiskSummary() {
  return get("/dashboard/risk-summary");
}


export async function getDashboardIncidents() {
  return get("/dashboard/incidents");
}


export async function getAISiteStatus() {
  return get("/dashboard/ai-site-status");
}


export async function getRiskDistribution() {
  return get("/dashboard/risk-distribution");
}


// ============================================================
// PPE
// ============================================================

export async function getPPEHealth() {
  return get("/ppe/health");
}


export async function detectPPE(file) {
  const formData = new FormData();

  formData.append("file", file);

  return apiRequest(
    "/ppe/detect",
    {
      method: "POST",
      body: formData,
    }
  );
}


// ============================================================
// REPORTS
// ============================================================

// Reports history
export async function getReports() {
  return get("/reports");
}


// Reports summary cards
export async function getReportsSummary() {
  return get("/reports/summary");
}


// Project performance
export async function getReportsPerformance() {
  return get("/reports/performance");
}


// AI report insight
export async function getReportsInsight() {
  return get("/reports/insight");
}


// ============================================================
// DEFAULT API OBJECT
// ============================================================

const api = {
  // Auth
  login,
  logout,
  isAuthenticated,

  // General
  get,
  post,
  put,
  del,

  // Health
  getHealth,

  // ML
  getMLModels,
  predictSafetyRisk,
  predictInjury,
  predictDelay,
  predictCost,
  predictSchedule,
  predictProjectDelay,
  predictResource,
  predictCompliance,
  predictInsurance,

  // Dashboard
  getDashboardKPIs,
  getProjectProgress,
  getRiskGauge,
  getRiskTrend,
  getRiskSummary,
  getDashboardIncidents,
  getAISiteStatus,
  getRiskDistribution,

  // PPE
  getPPEHealth,
  detectPPE,

  // Reports
  getReports,
  getReportsSummary,
  getReportsPerformance,
  getReportsInsight,
};


export default api;