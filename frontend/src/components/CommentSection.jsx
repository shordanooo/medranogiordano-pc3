import React, { useState } from "react";
import { proposalService } from "../services/api";

export default function CommentSection({ proposalId, comments = [], onNewComment }) {
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await proposalService.addComment({ proposal_id: proposalId, content: text });
      onNewComment(res.data);
      setText("");
    } catch (err) {
      setError(err.response?.data?.detail || "Error al enviar comentario");
    }
  };

  return (
    <div style={styles.container}>
      <h4 style={styles.heading}>Comentarios ({comments.length})</h4>
      {comments.map((c) => (
        <div key={c.id} style={styles.comment}>
          <p style={styles.commentText}>{c.content}</p>
          <small style={styles.meta}>
            {new Date(c.created_at).toLocaleDateString("es-PE")}
          </small>
        </div>
      ))}
      {localStorage.getItem("token") && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Escribe un comentario..."
            style={styles.textarea}
            rows={3}
            required
          />
          {error && <p style={styles.error}>{error}</p>}
          <button type="submit" style={styles.btn}>Enviar comentario</button>
        </form>
      )}
    </div>
  );
}

const styles = {
  container: { marginTop: "24px" },
  heading: { color: "#1a3a6b", marginBottom: "12px" },
  comment: { background: "#f5f8ff", border: "1px solid #d0dff5", borderRadius: "6px",
    padding: "12px", marginBottom: "10px" },
  commentText: { margin: "0 0 4px 0", color: "#333" },
  meta: { color: "#888" },
  form: { marginTop: "16px", display: "flex", flexDirection: "column", gap: "8px" },
  textarea: { padding: "10px", border: "1px solid #d0dff5", borderRadius: "6px",
    fontSize: "0.95rem", resize: "vertical" },
  error: { color: "#c62828", margin: 0 },
  btn: { alignSelf: "flex-end", background: "#1a3a6b", color: "#fff", border: "none",
    padding: "8px 20px", borderRadius: "5px", cursor: "pointer" },
};
