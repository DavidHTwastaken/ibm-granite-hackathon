import React, { useState, useEffect, useRef } from 'react';

const API_BASE = 'http://localhost:5000';

export default function Speechbox() {
  const [transcript, setTranscript] = useState('');
  const lastSent = useRef('');
  const lastServer = useRef('');
  const transcriptRef = useRef('');

  const updateTranscript = (value) => {
    setTranscript(value);
    transcriptRef.current = value;
  };

  useEffect(() => {
    fetch(`${API_BASE}/transcript`)
      .then(res => res.json())
      .then(data => {
        const txt = data.transcript || '';
        updateTranscript(txt);
        lastSent.current = txt;
        lastServer.current = txt;
      });
  }, []);

  useEffect(() => {
    const id = setInterval(async () => {
      const res = await fetch(`${API_BASE}/transcript`);
      const data = await res.json();
      const serverText = data.transcript || '';
      if (serverText !== lastServer.current && transcriptRef.current === lastSent.current) {
        updateTranscript(serverText);
        lastSent.current = serverText;
        lastServer.current = serverText;
      }
    }, 1000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    const id = setInterval(async () => {
      if (transcriptRef.current !== lastSent.current) {
        await fetch(`${API_BASE}/transcript`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transcript: transcriptRef.current }),
        });
        lastSent.current = transcriptRef.current;
      }
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div>
      <h3>Transcript</h3>
      <textarea rows={10} value={transcript} onChange={e => updateTranscript(e.target.value)} />
    </div>
  );
}
