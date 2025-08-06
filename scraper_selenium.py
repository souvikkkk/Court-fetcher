from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time


def fetch_case_details(case_type, case_number, filing_year):
    try:
        # Setup headless browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # remove this line to see the browser
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 30)  # Increased wait time

        # Step 1: Open the eCourts website
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
        
        # Step 2: Select State
        state_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sess_state_code"))))
        state_select.select_by_visible_text("Haryana")

        time.sleep(2)  # wait for districts to load

        # Step 3: Select District
        district_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sess_dist_code"))))
        district_select.select_by_visible_text("Faridabad")

        time.sleep(3)

        # Step 4: Click on "Case Status" tab
        case_status_tab = wait.until(EC.element_to_be_clickable((By.ID, "tabcasestatus")))
        case_status_tab.click()

        time.sleep(2)

        # Step 5: Fill the form
        case_type_select = Select(wait.until(EC.presence_of_element_located((By.ID, "cstype"))))
        case_type_select.select_by_value(case_type)

        driver.find_element(By.ID, "csno").send_keys(case_number)
        driver.find_element(By.ID, "csyr").send_keys(filing_year)

        # Step 6: Submit the form
        driver.find_element(By.ID, "csSubmit").click()

        # Step 7: Wait for results to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "partyName")))
        wait.until(EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "Filing Date")]')))

        # Step 8: Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "lxml")

        parties = soup.find("div", class_="partyName").text.strip()

        filing_date_td = soup.find("td", string="Filing Date")
        filing_date = filing_date_td.find_next_sibling("td").text.strip() if filing_date_td else "N/A"

        next_hearing_td = soup.find("td", string="Next Hearing Date")
        next_hearing = next_hearing_td.find_next_sibling("td").text.strip() if next_hearing_td else "N/A"

        pdf_tag = soup.find("a", href=True, text="View")
        pdf_link = "https://services.ecourts.gov.in" + pdf_tag["href"] if pdf_tag else "No PDF found"

        driver.quit()

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "pdf_link": pdf_link
        }

    except TimeoutException:
        driver.quit()
        return {"error": "Request timed out. Court site might be slow or structure may have changed."}
    except Exception as e:
        driver.quit()
        return {"error": f"Error occurred: {str(e)}"}
