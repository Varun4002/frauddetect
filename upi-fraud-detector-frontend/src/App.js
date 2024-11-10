import React from 'react';
import UploadData from './components/UploadData';
import TrainModel from './components/TrainModel';
import Predict from './components/Predict';
import SaveLoadModel from './components/SaveLoadModel';

function App() {
  return (
    <div className="App">
      <h1>UPI Fraud Detection</h1>
      <UploadData />
      <TrainModel />
      <Predict />
      <SaveLoadModel />
    </div>
  );
}

export default App;
