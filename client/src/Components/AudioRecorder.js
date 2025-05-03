import React from 'react';
import { useReactMediaRecorder } from "react-media-recorder";

export function AudioRecorder() {
  const {
    status,            // “idle” | “recording” | “stopped”…
    startRecording,
    stopRecording,
    mediaBlobUrl       // URL you can plug into an <audio>
  } = useReactMediaRecorder({ audio: true });

  return (
    <div>
      <p>Status: <strong>{status}</strong></p>
      <button onClick={startRecording}>Start</button>
      <button onClick={stopRecording}>Stop</button>
      {mediaBlobUrl && <audio src={mediaBlobUrl} controls style={{ marginTop: 10 }} />}
    </div>
  );
}