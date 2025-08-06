# 🏛️ Court-Data Fetcher & Mini-Dashboard

A simple web application to fetch case details from the Indian eCourts portal using Selenium and display them in a user-friendly dashboard built with Flask.

---

## 📌 Features

- 🔍 Fetch case details based on:
  - Case type
  - Case number
  - Filing year
- 🧾 Extracted data includes:
  - Parties involved
  - Filing date
  - Next hearing date
  - PDF link (if available)
- 💾 All queries are stored in a SQLite database.
- 🖥️ Attractive and responsive frontend using HTML + CSS.

---

## 🚀 Tech Stack

- **Backend:** Python, Flask, Selenium, BeautifulSoup
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Browser Driver:** ChromeDriver (via `webdriver-manager`)

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/yourusername/court-fetcher-dashboard.git
cd court-fetcher-dashboard

python -m venv venv    
source venv/bin/activate  # For Windows: venv\Scripts\activate    

pip install -r requirements.txt   

python app.py    
