from flask import Flask, request, jsonify
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = pickle.load(open('election_race_model.pkl', 'rb'))

# ID to Name Mappings
party_mapping = {
    0: "BJP",             # Bharatiya Janata Party
    1: "RJD",             # Rashtriya Janata Dal
    2: "INC",             # Indian National Congress
    3: "JD(U)",           # Janata Dal (United)
    4: "LJP",             # Lok Janshakti Party
    5: "CPI(ML)",         # Communist Party of India (Marxist–Leninist)
    6: "CPI",             # Communist Party of India
    7: "CPM",             # Communist Party of India (Marxist)
    8: "BSP",             # Bahujan Samaj Party
    9: "HAM(S)",          # Hindustani Awam Morcha (Secular)
    10: "RLSP",           # Rashtriya Lok Samata Party
    11: "AIMIM",          # All India Majlis-e-Ittehadul Muslimeen
    12: "Independent",
    13: "Others"
}


district_mapping = {
    1: "Araria",
    2: "Arwal",
    3: "Aurangabad",
    4: "Banka",
    5: "Begusarai",
    6: "Bhagalpur",
    7: "Bhojpur",
    8: "Buxar",
    9: "Darbhanga",
    10: "East Champaran",
    11: "Gaya",
    12: "Gopalganj",
    13: "Jamui",
    14: "Jehanabad",
    15: "Kaimur",
    16: "Katihar",
    17: "Khagaria",
    18: "Kishanganj",
    19: "Lakhisarai",
    20: "Madhepura",
    21: "Madhubani",
    22: "Munger",
    23: "Muzaffarpur",
    24: "Nalanda",
    25: "Nawada",
    26: "Patna",
    27: "Purnia",
    28: "Rohtas",
    29: "Saharsa",
    30: "Samastipur",
    31: "Saran",
    32: "Sheikhpura",
    33: "Sheohar",
    34: "Sitamarhi",
    35: "Siwan",
    36: "Supaul",
    37: "Vaishali",
    38: "West Champaran"
}


type_mapping = {
    0: "General",
    1: "SC",
    2: "ST"
}

# Root endpoint
from flask import Flask, request, jsonify, render_template

@app.route('/')
def home():
    return render_template("form.html", parties=party_mapping, districts=district_mapping, types=type_mapping)


# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        poll = float(request.form['poll'])
        total_votes = int(request.form['total_votes'])
        total_electors = int(request.form['total_electors'])
        party = int(request.form['party'])
        district = int(request.form['district'])
        ac_type = int(request.form['type'])

        features = [poll, total_votes, total_electors, party, district, ac_type]
        prediction = model.predict([features])[0]
        result = "tight" if prediction == 1 else "safe"

        return render_template("result.html",
                               result=result,
                               party=party_mapping.get(party, "Unknown"),
                               district=district_mapping.get(district, "Unknown"),
                               ac_type=type_mapping.get(ac_type, "Unknown"))

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)