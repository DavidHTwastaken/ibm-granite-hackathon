import React, { useState, useEffect, useRef } from "react";

const API_BASE = "http://localhost:5000";

export default function Speechbox({ transcript, setTranscript }) {
  const lastSent = useRef("");
  const lastServer = useRef("");
  const transcriptRef = useRef("");

  // const updateTranscript = (value) => {
  //   setTranscript(value);
  //   transcriptRef.current = value;
  // };

  // useEffect(() => {
  //   fetch(`${API_BASE}/transcript`)
  //     .then((res) => res.json())
  //     .then((data) => {
  //       const txt = data.transcript || "";
  //       updateTranscript(txt);
  //       lastSent.current = txt;
  //       lastServer.current = txt;
  //     })
  //     .catch((err) => console.error("Initial load error:", err));
  // }, []);

  // useEffect(() => {
  //   const id = setInterval(async () => {
  //     const data = await fetch(`${API_BASE}/transcript`)
  //       .then((res) => res.json())
  //       .catch((err) => {
  //         console.error("Error polling transcript:", err);
  //         return {};
  //       });
  //     const serverText = data.transcript || "";
  //     if (
  //       serverText !== lastServer.current &&
  //       transcriptRef.current === lastSent.current
  //     ) {
  //       updateTranscript(serverText);
  //       lastSent.current = serverText;
  //       lastServer.current = serverText;
  //     }
  //   }, 1000);
  //   return () => clearInterval(id);
  // }, []);

  // useEffect(() => {
  //   const id = setInterval(async () => {
  //     if (transcriptRef.current !== lastSent.current) {
  //       await fetch(`${API_BASE}/transcript`, {
  //         method: "POST",
  //         headers: { "Content-Type": "application/json" },
  //         body: JSON.stringify({ transcript: transcriptRef.current }),
  //       })
  //         .then((e) => {
  //           lastSent.current = transcriptRef.current;
  //         })
  //         .catch((err) =>
  //           console.error("Error sending transcript to server:", err)
  //         );
  //     }
  //   }, 1000);
  //   return () => clearInterval(id);
  // }, []);

  return (
    <div>
      <h3>Transcript</h3>
      <textarea
        rows={10}
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
      />
    </div>
  );
}
