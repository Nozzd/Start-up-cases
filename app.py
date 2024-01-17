from flask import Flask, jsonify, request
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the data
data = pd.read_csv('App_ds_2021_halles.csv')
data['Date de début'] = pd.to_datetime(data['Date de début'])

# Endpoint to get data for a specific date or date range
@app.route('/data', methods=['GET'])
def get_data():
    start_date = request.args.get('start', None)
    end_date = request.args.get('end', None)
    
    if start_date:
        start_date = pd.to_datetime(start_date)
        if end_date:
            end_date = pd.to_datetime(end_date)
            filtered_data = data[(data['Date de début'] >= start_date) & (data['Date de début'] <= end_date)]
        else:
            filtered_data = data[data['Date de début'] == start_date]
    else:
        filtered_data = data

    return jsonify(filtered_data.to_dict(orient='records'))

# Endpoint to get average levels of a specific pollutant over a date range
@app.route('/average', methods=['GET'])
def get_average():
    pollutant = request.args.get('pollutant', None)
    start_date = request.args.get('start', None)
    end_date = request.args.get('end', None)

    if not pollutant or not start_date or not end_date:
        return jsonify({"error": "Please specify pollutant, start date, and end date."}), 400

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if pollutant not in data.columns:
        return jsonify({"error": "Invalid pollutant specified."}), 400

    filtered_data = data[(data['Date de début'] >= start_date) & (data['Date de début'] <= end_date)]
    average = filtered_data[pollutant].mean()

    return jsonify({"pollutant": pollutant, "average": average})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


# http://localhost:5000/data?start=2021-01-01&end=2021-01-02