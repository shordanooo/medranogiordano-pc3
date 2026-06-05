import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.brand}>
        Propuesta Popular
      </Link>
      <div style={styles.links}>
        <Link to="/proposals" style={styles.link}>Propuestas</Link>
        {token ? (
          <>
            <Link to="/create" style={styles.link}>Nueva Propuesta</Link>
            <button onClick={handleLogout} style={styles.btn}>Cerrar Sesión</button>
          </>
        ) : (
          <>
            <Link to="/login" style={styles.link}>Ingresar</Link>
            <Link to="/register" style={styles.link}>Registrarse</Link>
          </>
        )}
      </div>
    </nav>
  );
}

const styles = {
  nav: { display: "flex", justifyContent: "space-between", alignItems: "center",
    padding: "12px 32px", background: "#1a1a1a", color: "#fff" },
  brand: { color: "#fff", textDecoration: "none", fontWeight: "bold", fontSize: "1.2rem" },
  links: { display: "flex", gap: "16px", alignItems: "center" },
  link: { color: "#cccccc", textDecoration: "none" },
  btn: { background: "transparent", border: "1px solid #888", color: "#ccc",
    padding: "6px 14px", borderRadius: "4px", cursor: "pointer" },
};
