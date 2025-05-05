import { set } from "lodash";
import React, { useRef, useState } from "react";

export default function ZipButton({ setZipFile }) {
  const fileInputRef = useRef();
  const [filename, setFilename] = useState("");

  return (
    <div>
      <button onClick={() => fileInputRef.current.click()}>
        Upload Code Zip
      </button>
      <input
        type="file"
        accept=".zip"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={(e) => setZipFile(e.target.files[0])}
      />
      {filename && (
        <div style={{ marginTop: 8 }}>
          Selected: <strong>{filename}</strong>
        </div>
      )}
    </div>
  );
}
