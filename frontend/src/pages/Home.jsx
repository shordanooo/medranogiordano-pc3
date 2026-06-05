import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={styles.container}>
      <div style={styles.hero}>
        <h1 style={styles.title}>Propuesta Popular</h1>
        <p style={styles.subtitle}>
          Plataforma oficial del Poder Legislativo para la presentación
          de Iniciativas Legislativas Ciudadanas.
        </p>
        <div style={styles.actions}>
          <Link to="/proposals" style={styles.btnPrimary}>Ver Propuestas</Link>
          <Link to="/register" style={styles.btnSecondary}>Participar</Link>
        </div>
      </div>

      <div style={styles.steps}>
        {[
          { num: "1", title: "Crea tu propuesta", desc: "Un colectivo civil redacta la iniciativa legislativa y la publica en la plataforma." },
          { num: "2", title: "Recolecta firmas", desc: "Los ciudadanos firman digitalmente. Se necesitan 25,000 firmas válidas en 90 días." },
          { num: "3", title: "Envío al Congreso", desc: "Al alcanzar el límite, el sistema congela el archivo y lo envía automáticamente al Congreso." },
        ].map((s) => (
          <div key={s.num} style={styles.stepCard}>
            <span style={styles.stepNum}>{s.num}</span>
            <h3 style={styles.stepTitle}>{s.title}</h3>
            <p style={styles.stepDesc}>{s.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: "1000px", margin: "0 auto", padding: "40px 24px" },
  hero: { textAlign: "center", padding: "60px 0 40px" },
  title: { fontSize: "2.4rem", color: "#1a1a1a", marginBottom: "16px" },
  subtitle: { fontSize: "1.1rem", color: "#555", maxWidth: "600px", margin: "0 auto 32px" },
  actions: { display: "flex", gap: "16px", justifyContent: "center" },
  btnPrimary: { background: "#1a1a1a", color: "#fff", padding: "12px 28px",
    borderRadius: "6px", textDecoration: "none", fontWeight: "bold" },
  btnSecondary: { background: "transparent", color: "#1a1a1a", padding: "12px 28px",
    borderRadius: "6px", textDecoration: "none", border: "2px solid #1a1a1a", fontWeight: "bold" },
  steps: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "20px", marginTop: "40px" },
  stepCard: { background: "#fff", border: "1px solid #e0e0e0", borderRadius: "10px",
    padding: "28px", textAlign: "center" },
  stepNum: { display: "inline-block", width: "40px", height: "40px", borderRadius: "50%",
    background: "#1a1a1a", color: "#fff", lineHeight: "40px", fontSize: "1.2rem",
    fontWeight: "bold", marginBottom: "12px" },
  stepTitle: { color: "#1a1a1a", marginBottom: "8px" },
  stepDesc: { color: "#555", fontSize: "0.9rem" },
};
