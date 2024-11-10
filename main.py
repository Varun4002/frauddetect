from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from io import BytesIO
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten, Dropout
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

app = FastAPI()

class UPIFraudDetector:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()

    def preprocess_data(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek

        feature_columns = [
            'amount', 'hour', 'day_of_week', 
            'sender_account_age', 'recipient_account_age',
            'sender_transaction_count', 'recipient_transaction_count'
        ]

        X = df[feature_columns].values
        y = df['is_fraud'].values
        X_scaled = self.scaler.fit_transform(X)
        X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

        return X_reshaped, y

    def build_model(self, input_shape):
        model = Sequential([
            Conv1D(32, 2, activation='relu', input_shape=input_shape),
            MaxPooling1D(2),
            Conv1D(64, 2, activation='relu'),
            MaxPooling1D(2),
            Conv1D(64, 2, activation='relu'),
            Flatten(),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy', tf.keras.metrics.AUC()])
        self.model = model
        return model

    def train(self, X, y, epochs=10, batch_size=32, validation_split=0.2):
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        return history

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)
        pred_probs = self.model.predict(X_reshaped)
        return pred_probs

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = load_model(path)

detector = UPIFraudDetector()

class PredictionRequest(BaseModel):
    data: list

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    X, y = detector.preprocess_data(df)
    return {"message": "Data preprocessed successfully", "features_shape": X.shape, "labels_shape": y.shape}

@app.post("/train-model")
async def train_model():
    if detector.model is None:
        detector.build_model((7, 1))
    X, y = detector.preprocess_data(df)  # Assumes df is loaded globally or passed
    history = detector.train(X, y)
    return {"message": "Model trained successfully", "history": history.history}

@app.post("/predict")
async def predict(data: PredictionRequest):
    data_array = np.array(data.data)
    predictions = detector.predict(data_array)
    return {"predictions": predictions.tolist()}

@app.post("/save-model")
async def save_model(path: str):
    detector.save_model(path)
    return {"message": "Model saved successfully"}

@app.post("/load-model")
async def load_model(path: str):
    detector.load_model(path)
    return {"message": "Model loaded successfully"}
