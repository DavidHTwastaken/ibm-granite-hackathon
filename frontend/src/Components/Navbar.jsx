import React from "react";
import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav style={styles.nav}>
      <div style={styles.logo}>🔮 DocuScribe</div>
      <div style={styles.links}>
        <Link to="/" style={styles.link}>
          Main
        </Link>
        <Link to="/about" style={styles.link}>
          About
        </Link>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    backgroundColor: "#121225",
    padding: "14px 32px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottom: "3px solid #ff2fe6",
    boxShadow: "0 0 12px #ff2fe6",
  },
  logo: {
    color: "#00fff7",
    fontSize: "22px",
    letterSpacing: "1.5px",
    fontWeight: "bold",
    textShadow: "0 0 4px #00fff7",
  },
  links: {
    display: "flex",
    gap: "20px",
  },
  link: {
    color: "#ffffff",
    textDecoration: "none",
    fontSize: "15px",
    transition: "color 0.3s, text-shadow 0.3s",
  },
};
