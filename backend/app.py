from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
import csv
import os
import joblib

# Load model once when server starts
model = joblib.load("passive_captcha_model.pkl")

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

CSV_FILE = "user_data.csv"


@app.route("/stats")
def get_stats():
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            human = bot = 0
            for row in reader:
                if row["label"] == "human":
                    human += 1
                elif row["label"] == "bot":
                    bot += 1
        return {"human": human, "bot": bot}
    except Exception as e:
        print("Error reading stats:", e)
        return {"error": "Could not read stats"}, 500

@app.route("/submit-data", methods=["POST"])
def receive_data():
    try:
        data = json.loads(request.data.decode("utf-8"))

        # Extract features for prediction
        mouse_count = len(data.get("mouseMoves", []))
        click_count = len(data.get("clicks", []))
        scroll_count = len(data.get("scrolls", []))
        time_on_page = data.get("timeOnPage", 0)

        # Make prediction using the model
        features = [[time_on_page, mouse_count, click_count, scroll_count]]
        prediction = model.predict(features)[0]  # 1 = human, 0 = bot
        
        # Set the predicted label
        if "label" not in data:
            predicted_label = "human" if prediction == 1 else "bot"
            data["label"] = predicted_label
        
        # Prepare row for CSV
        row = {
            "userAgent": data.get("userAgent"),
            "language": data.get("language"),
            "screenWidth": data.get("screenWidth"),
            "screenHeight": data.get("screenHeight"),
            "timeOnPage": data.get("timeOnPage"),
            "mouseMoves": json.dumps(data.get("mouseMoves")),
            "clicks": json.dumps(data.get("clicks")),
            "scrolls": json.dumps(data.get("scrolls")),
            "label": data.get("label")
        }

        # Save to CSV
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

        print("✅ Prediction:", data["label"])
        return {"prediction": data["label"]}, 200

    except Exception as e:
        print("❌ Error:", e)
        return {"error": "Processing failed"}, 400

if __name__ == "__main__":
    app.run(debug=True)