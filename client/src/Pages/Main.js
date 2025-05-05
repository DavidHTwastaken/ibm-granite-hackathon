import React, { useState } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import Speechbox from '../Components/Speechbox';
import ZipButton from '../Components/ZipButton';
import GenerateButton from '../Components/GenerateButton';

export default function Main() {
  const { status, startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder({ audio: true });

  const uploadRecording = async () => {
    if (!mediaBlobUrl) return alert('No recording to upload!');
    try {
      const blob = await fetch(mediaBlobUrl).then(r => r.blob());
      const formData = new FormData();
      formData.append('file', blob, 'recording.wav');
      const res = await fetch('/audio-input', { method: 'POST', body: formData });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || res.statusText);
      alert('Upload success: ' + JSON.stringify(json));
    } catch (err) {
      alert('Upload failed: ' + err.message);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2>Status: <span style={{ color: '#ff2fe6' }}>{status}</span></h2>
        <div style={styles.buttons}>
          <button onClick={startRecording}>Start</button>
          <button onClick={stopRecording}>Stop</button>
          <button onClick={uploadRecording} disabled={!mediaBlobUrl}>
            Upload
          </button>
        </div>
        {mediaBlobUrl && <audio src={mediaBlobUrl} controls />}
      </div>

      <div style={styles.card}><ZipButton /></div>
      <div style={styles.card}><Speechbox /></div>
      <div style={styles.card}><GenerateButton /></div>
    </div>
  );
}

const styles = {
  page: {
    padding: '30px',
    maxWidth: '900px',
    margin: '0 auto',
  },
  card: {
    backgroundColor: '#1a1a2e',
    padding: '20px',
    borderRadius: '12px',
    marginBottom: '24px',
    boxShadow: '0 0 15px rgba(255, 47, 230, 0.3)',
  },
  buttons: {
    display: 'flex',
    gap: '10px',
    flexWrap: 'wrap',
    marginTop: '12px',
  },
};
