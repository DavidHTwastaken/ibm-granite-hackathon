import React, { useState } from "react";

export default function GenerateButton({ zipFile, transcript, setOutput }) {
  const [status, setStatus] = useState("Idle");

  const handleGenerate = async () => {
    setStatus("Running...");
    try {
      if (!zipFile) {
        setStatus("Error: No zip file uploaded");
        return;
      }
      const formData = new FormData();
      formData.append("zipFile", zipFile);
      formData.append("transcript", transcript);

      const res = await fetch("/api/generate", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setStatus(`Success: ${data.message || "Done"}`);
      if (data.output) {
        setOutput(data.output);
      }
    } catch (err) {
      setStatus(`Error: ${err.message}`);
    }
  };

  return (
    <div>
      <button onClick={handleGenerate}>Run Generate</button>
      <p style={{ marginTop: 10, color: "#ff2fe6" }}>
        Status: <strong>{status}</strong>
      </p>
    </div>
  );
}
