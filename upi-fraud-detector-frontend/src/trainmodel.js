import React from 'react';
import axios from 'axios';

function TrainModel() {
  const handleTrain = async () => {
    try {
      const response = await axios.post('http://localhost:8000/train-model');
      alert(response.data.message);
    } catch (error) {
      console.error('Error training model:', error);
      alert('Failed to train model');
    }
  };

  return (
    <div>
      <h2>Train Model</h2>
      <button onClick={handleTrain}>Train Model</button>
    </div>
  );
}

export default TrainModel;
