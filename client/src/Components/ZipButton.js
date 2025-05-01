import React, { useRef, useState } from 'react';

export default function ZipButton() {
  const fileInputRef = useRef();
  const [filename, setFilename] = useState('');

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFilename(file.name);

    // send to server
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/zip-file', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error(await res.text());
      alert(`Uploaded ${file.name} successfully`);
    } catch (err) {
      console.error('Upload failed:', err);
      alert('Upload failed: ' + err.message);
    }
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <button onClick={handleClick}>
        Upload Code Zip File
      </button>
      <input
        type="file"
        accept=".zip"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      {filename && (
        <div style={{ marginTop: 8 }}>
          Selected file: <strong>{filename}</strong>
        </div>
      )}
    </div>
  );
}
