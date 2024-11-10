import React, { useState } from 'react';
import axios from 'axios';

function Predict() {
  const [data, setData] = useState('');
  const [predictions, setPredictions] = useState(null);

  const handlePredict = async () => {
    const formattedData = JSON.parse(data);  // Assuming input is JSON format

    try {
      const response = await axios.post('http://localhost:8000/predict', { data: formattedData });
      setPredictions(response.data.predictions);
    } catch (error) {
      console.error('Error making prediction:', error);
      alert('Failed to make prediction');
    }
  };

  return (
    <div>
      <h2>Make Prediction</h2>
      <textarea
        rows="4"
        cols="50"
        placeholder='Enter JSON data...'
        value={data}
        onChange={(e) => setData(e.target.value)}
      />
      <button onClick={handlePredict}>Make Prediction</button>
      {predictions && (
        <div>
          <h3>Predictions:</h3>
          <pre>{JSON.stringify(predictions, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default Predict;
