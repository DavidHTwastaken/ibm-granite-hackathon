import React, { useState } from 'react';

export default function GenerateButton() {
  const [status, setStatus] = useState('Idle');

  const handleGenerate = async () => {
    setStatus('Running...');
    try {
      const res = await fetch('/generate', { method: 'POST' });
      const data = await res.json();
      setStatus(`Success: ${data.message || 'Done'}`);
    } catch (err) {
      setStatus(`Error: ${err.message}`);
    }
  };

  return (
    <div>
      <button onClick={handleGenerate}>Run Generate</button>
      <p style={{ marginTop: 10, color: '#ff2fe6' }}>Status: <strong>{status}</strong></p>
    </div>
  );
}
