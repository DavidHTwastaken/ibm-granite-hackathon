import React from 'react';
import { Link } from 'react-router-dom';

export function Navbar() {
  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.link}>Main</Link>
      <Link to="/about" style={styles.link}>About</Link>
    </nav>
  );
}

const styles = {
  nav: {
    margin: '20px',
    display: 'flex',
    gap: '10px',
  },
  link: {
    textDecoration: 'none',
    color: '#61dafb',
  },
};