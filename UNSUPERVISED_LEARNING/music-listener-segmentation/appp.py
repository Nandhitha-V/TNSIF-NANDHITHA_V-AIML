import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template

# Load saved artifacts
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
cluster_mapping = joblib.load("cluster_mapping.pkl")

app = Flask(__name__)

def predict_segment(listening_hours, songs_per_day, skip_rate, playlist_count):
    # Format input array
    raw_input = np.array([[listening_hours, songs_per_day, skip_rate, playlist_count]])
    # Scale input
    scaled_input = scaler.transform(raw_input)
    # Predict raw cluster ID
    cluster_id = model.predict(scaled_input)[0]
    # Map to segment name
    segment = cluster_mapping.get(cluster_id, "Unknown Segment")
    return segment

# Route to render the HTML form interface
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Terminal Interactive Interface
def run_cli():
    print("\n--- Music Listener Segment Predictor ---")
    try:
        hours = float(input("Enter Listening Hours per Week: "))
        songs = float(input("Enter Songs per Day: "))
        skip = float(input("Enter Skip Rate (0.0 to 1.0): "))
        playlists = float(input("Enter Playlist Count: "))
        
        segment = predict_segment(hours, songs, skip, playlists)
        print(f"\nPredicted Listener Segment: >>> {segment} <<<\n")
    except ValueError:
        print("Invalid input. Please enter numerical values.")

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    # Handle requests coming from either HTML form or JSON API
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    try:
        segment = predict_segment(
            float(data['listening_hours_per_week']),
            float(data['songs_per_day']),
            float(data['skip_rate']),
            float(data['playlist_count'])
        )
        # Return web page view if requested via form submit
        if not request.is_json:
            return render_template('index.html', segment=segment)
            
        return jsonify({"segment": segment})
    except Exception as e:
        if not request.is_json:
            return render_template('index.html', error=str(e))
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    import sys
    # Default to CLI mode if run directly, or run web server if 'server' arg passed
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        app.run(port=5000, debug=True)
    else:
        run_cli()