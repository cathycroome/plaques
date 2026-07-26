from flask import Flask
import pandas as pd
from pathlib import Path
from plaque import get_filtered_data, get_plaques_for_month, random_plaque
from flask import request

app = Flask(__name__)

@app.route("/random")
def hello_world():
    month = request.args.get('month', type=str)
    max_distance = request.args.get('max_distance', type=float)
    blue_only = 'blue_only' in request.args #might need checking later with checkbox functionality
    
    data_dir = Path('/Users/cathycroome/data/plaques')
    T = pd.read_csv(data_dir / 'open-plaques-United-Kingdom-2025-12-14.csv')

    subset = get_filtered_data(T)

    # Get closest results for a given month
    plaques_for_a_month = get_plaques_for_month(month, subset, max_distance, blue_only)

    # Get random result for a given month
    randomised_result = random_plaque(plaques_for_a_month)

    if randomised_result is not None:
        return randomised_result.to_dict()
    else:
        return "No plaques found for this specification"

    
    