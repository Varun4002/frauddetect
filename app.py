import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Load the model (ensure this is the correct path for your model.pkl)
model = joblib.load('/app/model.pkl')
  # Use absolute or relative path depending on the container setup

# Define a route to handle predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON input
        data = request.get_json()

        # Convert input into DataFrame (assuming the input features are in a dict format)
        df = pd.DataFrame(data, index=[0])

        # Make predictions
        prediction = model.predict(df)

        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
