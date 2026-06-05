import React from "react";

const MAX = 25000;

export default function SignatureCounter({ count = 0, daysRemaining = 0, status }) {
  const percent = Math.min((count / MAX) * 100, 100).toFixed(1);

  const statusColor = {
    collecting: "#1a1a1a",
    frozen: "#2a5c27",
    submitted: "#2a5c27",
    expired: "#7a1a1a",
    draft: "#555",
  };

  return (
    <div style={styles.card}>
      <h3 style={{ color: statusColor[status] || "#333" }}>
        {count.toLocaleString()} / {MAX.toLocaleString()} firmas
      </h3>
      <div style={styles.barBg}>
        <div style={{ ...styles.bar, width: `${percent}%`,
          background: statusColor[status] || "#1a1a1a" }} />
      </div>
      <p style={styles.meta}>{percent}% completado · {daysRemaining} días restantes</p>
      {status === "frozen" && (
        <p style={{ color: "#2a5c27", fontWeight: "bold" }}>
          Congelada y enviada al Congreso
        </p>
      )}
      {status === "expired" && (
        <p style={{ color: "#7a1a1a", fontWeight: "bold" }}>Propuesta vencida</p>
      )}
    </div>
  );
}

const styles = {
  card: { background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: "8px",
    padding: "20px", marginBottom: "20px" },
  barBg: { background: "#d8d8d8", borderRadius: "6px", height: "14px", overflow: "hidden",
    margin: "8px 0" },
  bar: { height: "100%", borderRadius: "6px", transition: "width 0.5s" },
  meta: { fontSize: "0.9rem", color: "#666" },
};
