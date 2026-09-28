import { Navigate, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/Dashboard/Dashboard";
import Projects from "./pages/Projects/Projects";
import Safety from "./pages/Safety/Safety";
import AIHub from "./pages/AIHub/AIHub";
import Analytics from "./pages/Analytics/Analytics";
import RiskCenter from "./pages/RiskCenter/RiskCenter";
import Reports from "./pages/Reports/Reports";
import Settings from "./pages/Settings/Settings";

import Login from "./pages/Login/Login";
import { isAuthenticated } from "./api/client";

function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/projects"
        element={
          <ProtectedRoute>
            <Projects />
          </ProtectedRoute>
        }
      />

      <Route
        path="/safety"
        element={
          <ProtectedRoute>
            <Safety />
          </ProtectedRoute>
        }
      />

      <Route
        path="/aihub"
        element={
          <ProtectedRoute>
            <AIHub />
          </ProtectedRoute>
        }
      />

      <Route
        path="/analytics"
        element={
          <ProtectedRoute>
            <Analytics />
          </ProtectedRoute>
        }
      />

      <Route
        path="/riskcenter"
        element={
          <ProtectedRoute>
            <RiskCenter />
          </ProtectedRoute>
        }
      />

      <Route
        path="/reports"
        element={
          <ProtectedRoute>
            <Reports />
          </ProtectedRoute>
        }
      />

      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;