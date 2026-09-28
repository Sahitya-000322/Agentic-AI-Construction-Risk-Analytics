import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../api/client";
import "./Login.css";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("admin@buildai.com");
  const [password, setPassword] = useState("admin123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.message || "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-brand">
          <div className="login-logo">🏗️</div>
          <h1>BuildAI</h1>
          <p>Construction Intelligence Platform</p>
        </div>

        <div className="login-header">
          <h2>Welcome Back</h2>
          <p>Sign in to access your construction risk dashboard</p>
        </div>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <div className="demo-info">
          <strong>Demo Account</strong>
          <span>admin@buildai.com</span>
          <span>admin123</span>
        </div>
      </div>
    </div>
  );
}

export default Login;