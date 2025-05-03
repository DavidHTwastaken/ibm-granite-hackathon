// client/src/Pages/Main.js
import React, { useState, useEffect } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import Speechbox from '../Components/Speechbox';
import ZipButton from '../Components/ZipButton';
import GenerateButton from '../Components/GenerateButton';


export default function Main() {
  const [data, setData] = useState([]);
  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  } = useReactMediaRecorder({ audio: true });

  const uploadRecording = async () => {
    if (!mediaBlobUrl) {
      return alert('No recording to upload!');
    }

    try {
      const blob = await fetch(mediaBlobUrl).then(r => r.blob());
      const formData = new FormData();
      formData.append('file', blob, 'recording.wav');

      const res = await fetch('/audio-input', {
        method: 'POST',
        body: formData,
      });

      const json = await res.json();
      if (!res.ok) throw new Error(json.error || res.statusText);
      alert('Upload success: ' + JSON.stringify(json));
    } catch (err) {
      console.error('Upload failed:', err);
      alert('Upload failed: ' + err.message);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <div>
      <h4>Audio Recorder</h4>
      <p>Status: <strong>{status}</strong></p>
      <button onClick={startRecording}>Start Recording</button>
      <button onClick={stopRecording}>Stop Recording</button>
      {mediaBlobUrl && (
        <audio
          src={mediaBlobUrl}
          controls
          style={{ display: 'block', margin: '10px 0' }}
        />
      )}
      <button onClick={uploadRecording} disabled={!mediaBlobUrl}>
        Upload to Server
      </button>
      <ZipButton />
      </div>
      <Speechbox />
      <GenerateButton />
    </div>
  );
}
