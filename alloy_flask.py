from flask import Flask, render_template, request, jsonify
from itertools import product

app = Flask(__name__)

alloys = {
    "Bismuth Bronze": {
        "Copper": (50, 65),
        "Zinc": (20, 30),
        "Bismuth": (10, 20),
    },
    "Black Bronze": {
        "Copper": (50, 70),
        "Gold": (10, 25),
        "Silver": (10, 25),
    },
    "Bronze": {
        "Copper": (88, 92),
        "Tin": (8, 12),
    },
    "Brass": {
        "Copper": (88, 92),
        "Zinc": (8, 12),
    },
}

def calculate_alloy(ingots, proportions, granularities):
    total_mb = ingots * 144
    min_values = {comp: (total_mb * pct[0]) // 100 for comp, pct in proportions.items()}
    max_values = {comp: (total_mb * pct[1]) // 100 for comp, pct in proportions.items()}
    
    min_values = {comp: (val // granularities[comp]) * granularities[comp] for comp, val in min_values.items()}
    max_values = {comp: (val // granularities[comp]) * granularities[comp] for comp, val in max_values.items()}
    
    valid_combinations = [
        combo for combo in product(
            *(range(min_values[comp], max_values[comp] + 1, granularities[comp]) for comp in proportions)
        ) if sum(combo) == total_mb
    ]
    
    if not valid_combinations:
        return {"error": "Невозможно создать сплав с заданными параметрами."}
    
    return [{comp: amount for comp, amount in zip(proportions.keys(), combo)} for combo in valid_combinations]

@app.route('/')
def index():
    return render_template('index.html', alloys=alloys)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    ingots = int(data['ingots'])
    alloy = data['alloy']
    granularities = {comp: int(val) for comp, val in data['granularities'].items()}
    
    if alloy not in alloys:
        return jsonify({"error": "Неизвестный сплав."})
    
    result = calculate_alloy(ingots, alloys[alloy], granularities)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
