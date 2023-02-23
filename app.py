from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
# import time

app = Flask(__name__)
CORS(app)

def load_data():
    with open('./portfolio_scraper/portfolio.json', 'r') as f:
        return json.load(f)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', None)
    results = {}
    data = load_data()
    for item in data:
        URL, company_obj = list(item.items())[0]
        results[URL] = [company_info for company_info in company_obj if query is None or query.lower() in company_info['company_name'].lower()]
    return jsonify(results)

@app.route('/reload', methods=['GET'])
def re_run_scrapy():
    os.system('scrapy crawl portfolio -O ./portfolio_scraper/portfolio.json')
    return "Scraping completed."

@app.route('/industry', methods=['GET'])
def industry():
    pass

if __name__ == "__main__":
    re_run_scrapy()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
