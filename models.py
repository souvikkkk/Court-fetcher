import sqlite3
from datetime import datetime

DB_FILE = "queries.db"

def save_query_to_db(case_type, case_number, filing_year, raw_response):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            filing_year TEXT,
            query_time TEXT,
            raw_response TEXT
        )
    ''')
    c.execute('''
        INSERT INTO logs (case_type, case_number, filing_year, query_time, raw_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_type, case_number, filing_year, datetime.now().isoformat(), raw_response))
    conn.commit()
    conn.close()
