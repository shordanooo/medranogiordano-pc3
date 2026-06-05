import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authService } from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await authService.login(form.email, form.password);
      localStorage.setItem("token", res.data.access_token);
      navigate("/proposals");
    } catch {
      setError("Credenciales incorrectas");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.heading}>Iniciar Sesión</h2>
        <form onSubmit={handleSubmit} style={styles.form}>
          <input type="email" placeholder="Correo electrónico"
            value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
            required style={styles.input} />
          <input type="password" placeholder="Contraseña"
            value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
            required style={styles.input} />
          {error && <p style={styles.error}>{error}</p>}
          <button type="submit" style={styles.btn}>Ingresar</button>
        </form>
        <p style={styles.footer}>
          ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: { display: "flex", justifyContent: "center", alignItems: "center",
    minHeight: "70vh", padding: "20px" },
  card: { background: "#fff", border: "1px solid #d0d0d0", borderRadius: "10px",
    padding: "40px", width: "100%", maxWidth: "400px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" },
  heading: { color: "#1a1a1a", textAlign: "center", marginBottom: "24px" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  input: { padding: "10px 14px", border: "1px solid #d0d0d0", borderRadius: "6px", fontSize: "1rem" },
  error: { color: "#7a1a1a", margin: 0 },
  btn: { background: "#1a1a1a", color: "#fff", border: "none", padding: "12px",
    borderRadius: "6px", fontSize: "1rem", cursor: "pointer", fontWeight: "bold" },
  footer: { textAlign: "center", marginTop: "16px", color: "#555", fontSize: "0.9rem" },
};
