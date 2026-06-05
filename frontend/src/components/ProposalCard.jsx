import React from "react";
import { Link } from "react-router-dom";

const STATUS_LABELS = {
  collecting: { label: "Recolectando Firmas", color: "#1a3a6b" },
  frozen: { label: "Congelada", color: "#2d7d32" },
  submitted: { label: "Enviada al Congreso", color: "#2d7d32" },
  expired: { label: "Expirada", color: "#c62828" },
  draft: { label: "Borrador", color: "#777" },
};

export default function ProposalCard({ proposal }) {
  const { label, color } = STATUS_LABELS[proposal.status] || STATUS_LABELS.draft;
  const percent = Math.min((proposal.signature_count / 25000) * 100, 100).toFixed(1);

  return (
    <div style={styles.card}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <h3 style={styles.title}>{proposal.title}</h3>
        <span style={{ ...styles.badge, background: color }}>{label}</span>
      </div>
      <p style={styles.summary}>{proposal.summary.slice(0, 150)}...</p>
      <div style={styles.progressBg}>
        <div style={{ ...styles.progressBar, width: `${percent}%`, background: color }} />
      </div>
      <div style={styles.footer}>
        <span>{proposal.signature_count.toLocaleString()} firmas ({percent}%)</span>
        <Link to={`/proposals/${proposal.id}`} style={styles.btn}>Ver detalle</Link>
      </div>
    </div>
  );
}

const styles = {
  card: { background: "#fff", border: "1px solid #e0e8f5", borderRadius: "10px",
    padding: "20px", marginBottom: "16px", boxShadow: "0 2px 6px rgba(0,0,0,0.06)" },
  title: { margin: "0 0 8px 0", color: "#1a3a6b", fontSize: "1.1rem", maxWidth: "75%" },
  summary: { color: "#555", fontSize: "0.9rem", marginBottom: "12px" },
  badge: { color: "#fff", padding: "4px 10px", borderRadius: "12px", fontSize: "0.78rem",
    whiteSpace: "nowrap" },
  progressBg: { background: "#e8eef8", borderRadius: "4px", height: "8px", marginBottom: "12px" },
  progressBar: { height: "100%", borderRadius: "4px", transition: "width 0.4s" },
  footer: { display: "flex", justifyContent: "space-between", alignItems: "center",
    fontSize: "0.85rem", color: "#555" },
  btn: { background: "#1a3a6b", color: "#fff", padding: "6px 14px", borderRadius: "5px",
    textDecoration: "none", fontSize: "0.85rem" },
};
