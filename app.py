from pathlib import Path
import pandas as pd
from flask import Flask, jsonify, render_template, request
from plaque import get_filtered_data, get_plaques_for_month, random_plaque

app = Flask(__name__)

# ---------- Load and prepare data once at startup ----------
DATA_DIR = Path(__file__).parent
T = pd.read_csv(DATA_DIR / 'open-plaques-United-Kingdom-2025-12-14.csv')

SUBSET = get_filtered_data(T)

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

@app.route("/")
def index():
    return render_template("index.html", months=MONTHS)

@app.route("/random")
def random_plaque_route():
    month = request.args.get('month', type=str)
    max_distance = request.args.get('max_distance', type=float)
    blue_only = 'blue_only' in request.args  

    plaques_for_a_month = get_plaques_for_month(month, SUBSET, max_distance, blue_only)
    randomised_result = random_plaque(plaques_for_a_month)

    if randomised_result is not None:
        return jsonify(found=True, plaque=randomised_result.to_dict())
    else:
        return jsonify(found=False, message="No plaques found for this specification")


# ---------- to run locally ----------
if __name__ == "__main__":
    app.run(debug=True, port=5001)