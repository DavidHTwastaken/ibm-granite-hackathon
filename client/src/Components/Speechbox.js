import React, { useState, useEffect, useRef } from 'react';

const API_BASE = 'http://localhost:5000'; // Explicit backend URL

export default function Speechbox() {
  const [transcript, setTranscript] = useState('');

  // Refs to track last sent and server values, and current transcript
  const lastSent = useRef('');
  const lastServer = useRef('');
  const transcriptRef = useRef('');

  // Helper to update both state and ref
  const updateTranscript = (value) => {
    setTranscript(value);
    transcriptRef.current = value;
  };

  // Initial load from server
  useEffect(() => {
    fetch(`${API_BASE}/transcript`)
      .then(res => res.json())
      .then(data => {
        const txt = data.transcript || '';
        updateTranscript(txt);
        lastSent.current = txt;
        lastServer.current = txt;
      })
      .catch(err => console.error('Initial load error:', err));
  }, []);

  // Poll server every second for external changes
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/transcript`);
        if (!res.ok) throw new Error(res.statusText);
        const data = await res.json();
        const serverText = data.transcript || '';
        if (serverText !== lastServer.current) {
          lastServer.current = serverText;
          // Only overwrite if no pending local edits
          if (transcriptRef.current === lastSent.current) {
            updateTranscript(serverText);
            lastSent.current = serverText;
          }
        }
      } catch (err) {
        console.error('Error polling transcript:', err);
      }
    }, 1000);
    return () => clearInterval(id);
  }, []);

  // Send local edits every second
  useEffect(() => {
    const id = setInterval(async () => {
      if (transcriptRef.current !== lastSent.current) {
        try {
          const res = await fetch(`${API_BASE}/transcript`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ transcript: transcriptRef.current }),
          });
          if (!res.ok) throw new Error(res.statusText);
          lastSent.current = transcriptRef.current;
        } catch (err) {
          console.error('Error sending transcript:', err);
        }
      }
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ marginTop: 20 }}>
      <h4>Transcript</h4>
      <textarea
        value={transcript}
        onChange={e => updateTranscript(e.target.value)}
        rows={10}
        style={{ width: '100%', padding: 8, fontSize: 14 }}
      />
    </div>
  );
}
