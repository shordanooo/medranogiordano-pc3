import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { proposalService } from "../services/api";
import SignatureCounter from "../components/SignatureCounter";
import CommentSection from "../components/CommentSection";

export default function ProposalDetail() {
  const { id } = useParams();
  const [proposal, setProposal] = useState(null);
  const [status, setStatus] = useState(null);
  const [comments, setComments] = useState([]);
  const [signing, setSigning] = useState(false);
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    proposalService.get(id).then((r) => setProposal(r.data));
    proposalService.getStatus(id).then((r) => setStatus(r.data));
    proposalService.getComments(id).then((r) => setComments(r.data));
  }, [id]);

  const handleSign = async () => {
    setSigning(true);
    setMsg("");
    setError("");
    try {
      const res = await proposalService.sign(id);
      setMsg(res.data.message || "¡Firma registrada exitosamente!");
      proposalService.getStatus(id).then((r) => setStatus(r.data));
    } catch (err) {
      setError(err.response?.data?.detail || "Error al firmar");
    } finally {
      setSigning(false);
    }
  };

  if (!proposal) return <p style={styles.center}>Cargando...</p>;

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>{proposal.title}</h2>
      <p style={styles.summary}>{proposal.summary}</p>

      {status && (
        <SignatureCounter
          count={status.signature_count}
          daysRemaining={status.days_remaining}
          status={status.status}
        />
      )}

      {proposal.status === "collecting" && localStorage.getItem("token") && (
        <div style={styles.signBox}>
          <button onClick={handleSign} disabled={signing} style={styles.signBtn}>
            {signing ? "Registrando..." : "Firmar esta propuesta"}
          </button>
          {msg && <p style={{ color: "#2d7d32", marginTop: "8px" }}>{msg}</p>}
          {error && <p style={{ color: "#c62828", marginTop: "8px" }}>{error}</p>}
        </div>
      )}

      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Texto Completo</h3>
        <p style={styles.fullText}>{proposal.full_text}</p>
      </div>

      {proposal.crypto_hash && (
        <div style={styles.hashBox}>
          <strong>Hash Criptográfico (SHA-512):</strong>
          <code style={styles.hash}>{proposal.crypto_hash}</code>
          {proposal.congress_ticket && (
            <p><strong>Ticket Congreso:</strong> {proposal.congress_ticket}</p>
          )}
        </div>
      )}

      <CommentSection
        proposalId={parseInt(id)}
        comments={comments}
        onNewComment={(c) => setComments((prev) => [...prev, c])}
      />
    </div>
  );
}

const styles = {
  container: { maxWidth: "800px", margin: "0 auto", padding: "32px 24px" },
  title: { color: "#1a3a6b", marginBottom: "8px" },
  summary: { color: "#555", marginBottom: "20px", fontSize: "1.05rem" },
  signBox: { marginBottom: "24px" },
  signBtn: { background: "#1a3a6b", color: "#fff", border: "none", padding: "12px 28px",
    borderRadius: "6px", fontSize: "1rem", cursor: "pointer", fontWeight: "bold" },
  section: { marginBottom: "24px" },
  sectionTitle: { color: "#1a3a6b", marginBottom: "8px" },
  fullText: { color: "#333", lineHeight: "1.7", whiteSpace: "pre-wrap" },
  hashBox: { background: "#e8f5e9", border: "1px solid #a5d6a7", borderRadius: "6px",
    padding: "16px", marginBottom: "24px" },
  hash: { display: "block", wordBreak: "break-all", fontSize: "0.78rem",
    marginTop: "8px", color: "#1b5e20" },
  center: { textAlign: "center", marginTop: "60px" },
};
