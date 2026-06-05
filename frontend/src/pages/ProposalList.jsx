import React, { useState, useEffect } from "react";
import { proposalService } from "../services/api";
import ProposalCard from "../components/ProposalCard";

export default function ProposalList() {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    proposalService.list()
      .then((res) => setProposals(res.data))
      .catch(() => setError("Error al cargar propuestas"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={styles.center}>Cargando propuestas...</p>;
  if (error) return <p style={{ ...styles.center, color: "#7a1a1a" }}>{error}</p>;

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Propuestas Legislativas</h2>
      {proposals.length === 0 ? (
        <p style={styles.empty}>No hay propuestas activas. ¡Sé el primero en crear una!</p>
      ) : (
        proposals.map((p) => <ProposalCard key={p.id} proposal={p} />)
      )}
    </div>
  );
}

const styles = {
  container: { maxWidth: "800px", margin: "0 auto", padding: "32px 24px" },
  heading: { color: "#1a1a1a", marginBottom: "24px" },
  center: { textAlign: "center", marginTop: "60px", color: "#555" },
  empty: { textAlign: "center", color: "#777", marginTop: "40px" },
};
