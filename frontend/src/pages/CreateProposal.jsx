import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { proposalService } from "../services/api";

export default function CreateProposal() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ title: "", summary: "", full_text: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await proposalService.create(form);
      navigate(`/proposals/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al crear propuesta");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Nueva Iniciativa Legislativa</h2>
      <p style={styles.info}>
        Al publicar esta propuesta, se abre un plazo de <strong>90 días</strong> para
        recolectar <strong>25,000 firmas digitales</strong>.
      </p>
      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>Título de la propuesta</label>
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          required
          placeholder="Ej: Ley de Transparencia en el Uso de Datos Públicos"
          style={styles.input}
        />

        <label style={styles.label}>Resumen ejecutivo</label>
        <textarea
          name="summary"
          value={form.summary}
          onChange={handleChange}
          required
          rows={3}
          placeholder="Describe brevemente el objetivo de la propuesta..."
          style={styles.input}
        />

        <label style={styles.label}>Texto completo de la propuesta</label>
        <textarea
          name="full_text"
          value={form.full_text}
          onChange={handleChange}
          required
          rows={10}
          placeholder="Artículo 1: ..."
          style={styles.input}
        />

        {error && <p style={styles.error}>{error}</p>}

        <button type="submit" disabled={loading} style={styles.btn}>
          {loading ? "Publicando..." : "Publicar Propuesta"}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: { maxWidth: "700px", margin: "0 auto", padding: "32px 24px" },
  heading: { color: "#1a1a1a", marginBottom: "8px" },
  info: { color: "#555", marginBottom: "24px", background: "#f8f8f8",
    padding: "12px 16px", borderRadius: "6px", border: "1px solid #e0e0e0" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  label: { fontWeight: "600", color: "#333" },
  input: { padding: "10px", border: "1px solid #d0d0d0", borderRadius: "6px",
    fontSize: "0.95rem", width: "100%", boxSizing: "border-box" },
  error: { color: "#7a1a1a" },
  btn: { background: "#1a1a1a", color: "#fff", border: "none", padding: "12px",
    borderRadius: "6px", fontSize: "1rem", cursor: "pointer", fontWeight: "bold" },
};
