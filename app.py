from flask import Flask, jsonify, request, render_template
from urllib.request import urlopen
import certifi
import json

app = Flask(__name__)

API_KEY = 'Key'  

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

    profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker_query}?apikey={API_KEY}"
    profile_data = get_jsonparsed_data(profile_url)

    if profile_data and isinstance(profile_data, list) and len(profile_data) > 0:
        company_info = profile_data[0]  # Get the first match

        # Fetch key metrics data
        metrics_url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker_query}?period=annual&apikey={API_KEY}"
        metrics_data = get_jsonparsed_data(metrics_url)
        
        fin_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker_query}?period=annual&apikey={API_KEY}"
        fin_data = get_jsonparsed_data(fin_url)

        dividend_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ticker_query}?apikey={API_KEY}"
        dividend_data = get_jsonparsed_data(dividend_url)

        if metrics_data and isinstance(metrics_data, list) and len(metrics_data) > 0 and \
            fin_data and len(fin_data) > 0 and \
            dividend_data and "historical" in dividend_data and len(dividend_data['historical']) > 0:
            key_metrics = metrics_data[0]  
            income_statement = fin_data[0]
            dividend = dividend_data['historical'][0]

            # Combine company profile and key metrics
            return jsonify({
                'Company Name': company_info.get('companyName'),
                'Capital': company_info.get('mktCap'),
                'Industry': company_info.get('industry'),
                'Total Revenue': income_statement.get('revenue'),
                'P/E Ratio': key_metrics.get('peRatio'),
                'P/B Ratio': key_metrics.get('pbRatio'),
                'Free Cash Flow': key_metrics.get('freeCashFlowPerShare'),
                'Dividend Per Share': key_metrics.get('dividend'),
            })
        else:
            return jsonify({"error": "Key metrics not found"}), 404

    else:
        return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)




