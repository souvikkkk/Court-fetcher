from flask import Flask, render_template, request
from models import save_query_to_db
from scraper_selenium import fetch_case_details


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    case_type = request.form['case_type']
    case_number = request.form['case_number']
    filing_year = request.form['filing_year']
    
    result = fetch_case_details(case_type, case_number, filing_year)
    
    if result.get("error"):
        return f"<h3>Error: {result['error']}</h3>"

    save_query_to_db(case_type, case_number, filing_year, str(result))
    
    return render_template('result.html', data=result)

if __name__ == '__main__':
    app.run(debug=True)
