from flask import Flask, jsonify, request, render_template
from urllib.request import urlopen
import certifi
import json

app = Flask(__name__)

API_KEY = 'YzbacaXtjmhBnzUjsWcj8HfCrIxC9WyE'  # Replace with your actual API key

def get_jsonparsed_data(url):
    try:
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search_company():
    ticker_query = request.args.get('ticker')
    if not ticker_query:
        return jsonify({"error": "Ticker query is required"}), 400

    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker_query}?apikey={API_KEY}"
    data = get_jsonparsed_data(url)

    if data and isinstance(data, list) and len(data) > 0:
        company_info = data[0]  # Get the first match
        return jsonify({
            'Company Name': company_info.get('companyName'),
           
            # '': company_info.get(''),
        })
    else:
        return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)