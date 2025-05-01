import React, { useState } from 'react';

export default function GenerateButton() {
  const [status, setStatus] = useState('Idle');

  const handleGenerate = async () => {
    setStatus('Connecting to backend...');
    try {
      const res = await fetch('/generate', { method: 'POST' });
      if (!res.ok) throw new Error(res.statusText);
      const data = await res.json();
      setStatus(`Success: ${data.message || 'Backend reached!'}`);
    } catch (err) {
      console.error('Error:', err);
      setStatus(`Error: ${err.message}`);
    }
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <button onClick={handleGenerate}>Run Generate</button>
      <p style={{ marginTop: 8 }}>Status: <strong>{status}</strong></p>
    </div>
  );
}
