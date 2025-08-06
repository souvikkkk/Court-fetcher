import requests
from bs4 import BeautifulSoup

def fetch_case_details(case_type, case_number, filing_year):
    session = requests.Session()

    try:
        # Use eCourts v6 search endpoint for Faridabad
        search_url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&app_token=1"

        payload = {
            "stateCode": "HR",       # Haryana
            "distCode": "FBD",       # Faridabad
            "court_code": "",        # Can be blank
            "case_type": case_type,  # e.g. 'CS'
            "case_number": case_number,
            "case_year": filing_year,
            "submit": "Submit"
        }

        response = session.post(search_url, data=payload, timeout=30)  # Increase timeout

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # DEBUG - Print the HTML title
        page_title = soup.title.text if soup.title else "No title"
        print("Fetched page:", page_title)

        # Check for "No records" text
        if "No record found" in soup.text or "No Record Found" in soup.text:
            return {"error": "No case found with given inputs."}

        # Defensive scraping with .find checks
        party_block = soup.find('div', class_='col-sm-12 partyName')
        filing_date_block = soup.find('td', string='Filing Date')
        next_hearing_block = soup.find('td', string='Next Hearing Date')

        if not party_block or not filing_date_block or not next_hearing_block:
            return {"error": "Could not locate some case elements. The structure may have changed."}

        parties = party_block.text.strip()
        filing_date = filing_date_block.find_next_sibling('td').text.strip()
        next_hearing = next_hearing_block.find_next_sibling('td').text.strip()

        # Look for a PDF link if any
        pdf_tag = soup.find('a', href=True, text='View')
        pdf_link = "https://services.ecourts.gov.in" + pdf_tag['href'] if pdf_tag else "No PDF found"

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "pdf_link": pdf_link
        }

    except Exception as e:
        return {"error": f"Failed to fetch case details: {str(e)}"}
