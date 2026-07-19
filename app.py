from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model once when the app starts
model = joblib.load('traffic_model.pkl')

@app.route('/')
def home():
    return "Traffic Prediction API is running!"

@app.route('/predict', methods=['GET'])
def predict():
    # Read inputs from the URL, e.g. ?hour=8&day=1&weekend=0&junction=1
    hour = int(request.args.get('hour'))
    day = int(request.args.get('day'))
    weekend = int(request.args.get('weekend'))
    junction = int(request.args.get('junction'))

    # Build the input row matching the model's expected columns
    input_data = pd.DataFrame([{
        'hour': hour,
        'days_of_week': day,
        'is_weekend': weekend,
        'Junction_1': junction == 1,
        'Junction_2': junction == 2,
        'Junction_3': junction == 3,
        'Junction_4': junction == 4,
    }])

    prediction = model.predict(input_data)[0]
    return jsonify({'predicted_vehicles': round(float(prediction), 1)})

if __name__ == '__main__':
    app.run()