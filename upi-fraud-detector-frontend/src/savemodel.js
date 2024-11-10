import React, { useState } from 'react';
import axios from 'axios';

function SaveLoadModel() {
  const [path, setPath] = useState('');

  const handleSave = async () => {
    try {
      const response = await axios.post('http://localhost:8000/save-model', { path });
      alert(response.data.message);
    } catch (error) {
      console.error('Error saving model:', error);
      alert('Failed to save model');
    }
  };

  const handleLoad = async () => {
    try {
      const response = await axios.post('http://localhost:8000/load-model', { path });
      alert(response.data.message);
    } catch (error) {
      console.error('Error loading model:', error);
      alert('Failed to load model');
    }
  };

  return (
    <div>
      <h2>Save/Load Model</h2>
      <input 
        type="text" 
        placeholder="Enter model path" 
        value={path} 
        onChange={(e) => setPath(e.target.value)} 
      />
      <div>
        <button onClick={handleSave}>Save Model</button>
        <button onClick={handleLoad}>Load Model</button>
      </div>
    </div>
  );
}

export default SaveLoadModel;
