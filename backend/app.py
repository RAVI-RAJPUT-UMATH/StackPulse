from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app = Flask(__name__, static_folder=None)
CORS(app)  # Enable CORS

# Path to the CSV file
CSV_FILE = os.path.join(BASE_DIR, "computed_data.csv")

def read_csv_data():
    """Reads CSV and returns data for line and bar charts."""
    if not os.path.exists(CSV_FILE):
        return {"error": "CSV file not found"}

    try:
        df = pd.read_csv(CSV_FILE, encoding="utf-8")

        if "year_month" not in df.columns:
            return {"error": "'year_month' column is missing in the CSV"}

        data = {"year_month": df["year_month"].astype(str).tolist()}

        for col in df.columns[1:]:  
            data[col] = df[col].fillna(0).tolist()

        return data

    except Exception as e:
        return {"error": str(e)}

@app.route('/api/data', methods=['GET'])
def get_data():
    """Returns line and bar chart data."""
    return jsonify(read_csv_data())

@app.route('/api/pie_data', methods=['GET'])
@app.route('/pie_data', methods=['GET'])
def get_pie_data():
    """Returns pie chart data for a specific month."""
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "CSV file not found"}), 500

    try:
        df = pd.read_csv(CSV_FILE)
        df["year_month"] = df["year_month"].astype(str)
        month = request.args.get("month", df["year_month"].iloc[-1])

        if month not in df["year_month"].values:
            return jsonify({"error": "Month not found"}), 400

        row = df[df["year_month"] == month].iloc[0]

        pie_data = {
            "labels": row.index[1:].tolist(),
            "values": row.values[1:].astype(float).tolist()
        }

        return jsonify(pie_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Serve the frontend from the sibling frontend/ folder ---

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
