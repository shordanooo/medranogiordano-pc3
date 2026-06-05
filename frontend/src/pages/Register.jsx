import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authService } from "../services/api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ dni: "", full_name: "", email: "", password: "", collective_name: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await authService.register(form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Error al registrarse");
    }
  };

  const field = (name, placeholder, type = "text") => (
    <input type={type} placeholder={placeholder} value={form[name]}
      onChange={(e) => setForm({ ...form, [name]: e.target.value })}
      required={name !== "collective_name"} style={styles.input} />
  );

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.heading}>Crear Cuenta</h2>
        <form onSubmit={handleSubmit} style={styles.form}>
          {field("dni", "DNI (8 dígitos)")}
          {field("full_name", "Nombre completo")}
          {field("email", "Correo electrónico", "email")}
          {field("password", "Contraseña", "password")}
          <input type="text" placeholder="Nombre del colectivo (opcional)"
            value={form.collective_name}
            onChange={(e) => setForm({ ...form, collective_name: e.target.value })}
            style={styles.input} />
          {error && <p style={styles.error}>{error}</p>}
          <button type="submit" style={styles.btn}>Registrarse</button>
        </form>
        <p style={styles.footer}>
          ¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: { display: "flex", justifyContent: "center", alignItems: "center",
    minHeight: "70vh", padding: "20px" },
  card: { background: "#fff", border: "1px solid #d0dff5", borderRadius: "10px",
    padding: "40px", width: "100%", maxWidth: "420px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" },
  heading: { color: "#1a3a6b", textAlign: "center", marginBottom: "24px" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  input: { padding: "10px 14px", border: "1px solid #d0dff5", borderRadius: "6px", fontSize: "1rem" },
  error: { color: "#c62828", margin: 0 },
  btn: { background: "#1a3a6b", color: "#fff", border: "none", padding: "12px",
    borderRadius: "6px", fontSize: "1rem", cursor: "pointer", fontWeight: "bold" },
  footer: { textAlign: "center", marginTop: "16px", color: "#555", fontSize: "0.9rem" },
};
