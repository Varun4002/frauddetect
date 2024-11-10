import React, { useState } from 'react';
import axios from 'axios';

function UploadData() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload-data', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert(response.data.message);
    } catch (error) {
      console.error('Error uploading data:', error);
      alert('Failed to upload data');
    }
  };

  return (
    <div>
      <h2>Upload Data</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Preprocess</button>
    </div>
  );
}

export default UploadData;
