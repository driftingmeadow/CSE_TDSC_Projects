import concurrent.futures
import time
import os
import threading
import pandas as pd
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import csv
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from bs4 import BeautifulSoup


# Constants
BASE_URL = "https://nregastrep.nic.in/netnrega/loginframegp.aspx?lflag=eng&page=C&state_code=11&Digest=UE9tou4zFyF0ZrYMzV73zw"
FINANCIAL_YEAR = "2024-2025"
OUTPUT_DIR = "Gujarat_MGNREGA_Data"
MAX_WORKERS = 4
LOG_FILE = "scraping_log.txt"


os.makedirs(OUTPUT_DIR, exist_ok=True)

# naming the thread for understanding
def log_message(message):
    thread_name = threading.current_thread().name
    formatted = f"[{thread_name}] {message}"
    with open(LOG_FILE, "a") as log:
        log.write(formatted + "\n")
    print(formatted)

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    print(f"Using ChromeDriver from: {service.path}")
    return webdriver.Chrome(service=service, options=options)
    


def get_element_safe(driver, by, value):
    try:
        return driver.find_element(by, value)
    except:
        log_message(f" Element not found using {by}='{value}'")
        return None

def auto_find_element(driver, priority_list):
    for by, value in priority_list:
        try:
            return driver.find_element(by, value)
        except:
            continue
    return None

            # //////////////  / 
def save_job_card_data(data, district, block, panchayat):
    district_dir = os.path.join(OUTPUT_DIR, district)
    block_dir = os.path.join(district_dir, block)
    panchayat_dir = os.path.join(block_dir, panchayat)
    os.makedirs(panchayat_dir, exist_ok=True)

    csv_path = os.path.join(panchayat_dir, "data.csv")
    df = pd.DataFrame([data])

    if not os.path.isfile(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf-8-sig')

    #     # Convert to Excel
    # excel_path = os.path.join(panchayat_dir, "data.xlsx")
    # df_all = pd.read_csv(csv_path)
    # df_all.to_excel(excel_path, index=False)

    # # Convert to JSON
    # json_path = os.path.join(panchayat_dir, "data.json")
    # df_all.to_json(json_path, orient='records', indent=4, force_ascii=False)

    job_card_no = data.get("Job card No.", "Unknown")
    log_message(f"Appended job card data for {job_card_no} to {csv_path}")  #, saved Excel at {excel_path}, and JSON at {json_path}")
   
def get_value_by_label(soup, label_pattern):
    """
    Extract value from the td next to the td containing a matching label.
    Handles nested <font>, <b>, and inconsistent formatting.
    """
    label_tag = soup.find(text=re.compile(label_pattern, re.IGNORECASE))
    if label_tag:
        td = label_tag.find_parent("td")
        if td:
            next_td = td.find_next_sibling("td")
            if next_td:
                return next_td.get_text(strip=True)

            # In case colspan=2 skips a <td>, look further
            next_td = td.find_next("td")
            if next_td:
                return next_td.get_text(strip=True)
    return ""

def extract_job_card_details(soup):
    job_card_details = {}

    # Step 1: Extract standard fields by ID
    job_card_details.update({
        "Job Card No.": get_value_by_label(soup, r"Job\s*card\s*No\.?"),
        "Family Id": soup.find('span', id='lbl_familyid').text.strip() if soup.find('span', id='lbl_familyid') else "",
        "Head of Household": soup.find('span', id='lbl_house').text.strip() if soup.find('span', id='lbl_house') else "",
        "Father/Husband": soup.find('span', id='lbl_FATH_HUS').text.strip() if soup.find('span', id='lbl_FATH_HUS') else "",
        "Category": get_value_by_label(soup, r"Category"),
        "Date of Registration": soup.find('span', id='lbl_head').text.strip() if soup.find('span', id='lbl_head') else "",
        "Address": (
            soup.find('span', id='lbl_add').text.strip()
            if soup.find('span', id='lbl_add')
            else get_value_by_label(soup, r"Address")),
        "Village": soup.find('span', id='lbl_vill').text.strip() if soup.find('span', id='lbl_vill') else "",
        "Panchayat": get_value_by_label(soup, r"Panchayat"),
        "Block": get_value_by_label(soup, r"Block"),
        "District": get_value_by_label(soup, r"District")
    })

    # Step 2: Fallback table parsing
    try:
        details_table = soup.find("table", {"border": "1"})
        if details_table:
            for row in details_table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) >= 2:
                    key = cells[0].text.strip().rstrip(":")
                    value = cells[1].text.strip()
                    if key and key not in job_card_details:
                        job_card_details[key] = value
    except Exception as e:
        print(f" Error parsing fallback table: {e}")

    # Step 3: Extract applicants from GridView4 table
    applicants = []
    applicants_table = soup.find('table', id='GridView4')
    if applicants_table:
        for row in applicants_table.find_all('tr')[2:]:  # Skip header rows
            cols = row.find_all('td')
            if len(cols) == 5:
                applicants.append({
                    "S.No": cols[0].text.strip(),
                    "Name": cols[1].text.strip(),
                    "Gender": cols[2].text.strip(),
                    "Age": cols[3].text.strip(),
                    "Bank/Postoffice": cols[4].text.strip()
                })

    job_card_details["Applicants"] = applicants

    # Optional: Debug print
    import pprint
    pprint.pprint(job_card_details)

    return job_card_details


    #function call
def extract_full_job_card(soup):

    #saves data in a dictionary
    full_job_card = {}

    # Extract static job card info section
    full_job_card["job_card_details"] = extract_job_card_details(soup)
 
    return full_job_card

# Process each task in a worker thread
# # Modified Selenium loop with saving functionality
def process_task(queue):
    driver = initialize_driver()

    while not queue.empty():
        district, block, panchayat = queue.get()

        try:
            driver.get(BASE_URL)
            fin_year_dropdown = get_element_safe(driver, By.ID, "ctl00_ContentPlaceHolder1_ddlFin")
            if fin_year_dropdown:
                Select(fin_year_dropdown).select_by_visible_text(FINANCIAL_YEAR)
                log_message(f" Selected Financial Year: {FINANCIAL_YEAR}")
            time.sleep(2)

            district_dropdown = get_element_safe(driver, By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict")
            if not district_dropdown:
                continue
            district_options = [d.text.strip() for d in Select(district_dropdown).options if d.text.strip() != "Select District"]

            if district not in district_options:
                log_message(f" District {district} not found in the dropdown.")
                continue
            Select(district_dropdown).select_by_visible_text(district)
            log_message(f" Selected District: {district}")
            time.sleep(2)

            block_dropdown = get_element_safe(driver, By.ID, "ctl00_ContentPlaceHolder1_ddlBlock")
            if not block_dropdown:
                continue
            block_options = [b.text.strip() for b in Select(block_dropdown).options if b.text.strip() != "Select Block"]

            if block not in block_options:
                log_message(f" Block {block} not found in the dropdown.")
                continue
            Select(block_dropdown).select_by_visible_text(block)
            log_message(f" Selected Block: {block}")
            time.sleep(2)

            panchayat_dropdown = get_element_safe(driver, By.ID, "ctl00_ContentPlaceHolder1_ddlPanchayat")
            if not panchayat_dropdown:
                continue
            panchayat_options = [p.text.strip() for p in Select(panchayat_dropdown).options if p.text.strip() != "Select Panchayat"]

            if panchayat not in panchayat_options:
                log_message(f" Panchayat {panchayat} not found in the dropdown.")
                continue
            Select(panchayat_dropdown).select_by_visible_text(panchayat)
            log_message(f" Selected Panchayat: {panchayat}")

            proceed_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btProceed"))
            )

            if not proceed_button:
                log_message(" Proceed button not found.")
                continue

            proceed_button.click()
            time.sleep(3)
            log_message(" Proceed clicked. Loading job card page...")

            soup = BeautifulSoup(driver.page_source, "html.parser")
            job_card_table = soup.find("table")

            if not job_card_table:
                log_message(" No job card table found.")
                continue

            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table//tr[position()>1]"))
            )
            log_message(f" Found {len(rows)} job cards.")

            all_job_card_data = []  # Store the extracted data for each job card

            job_card_links = []
            job_card_elements = driver.find_elements(By.XPATH, "//table//tr[position()>1]/td[2]/a")

            for element in job_card_elements:
                href = element.get_attribute("href")
                if href:
                    job_card_links.append(href)

            log_message(f" Collected {len(job_card_links)} job card links.")

            for i, href in enumerate(job_card_links, start=1):
                try:
                    driver.get(href)
                    time.sleep(1)

                    detail_soup = BeautifulSoup(driver.page_source, "html.parser")
                    job_card_data = extract_full_job_card(detail_soup)
                    all_job_card_data.append(job_card_data)

                    save_job_card_data(job_card_data["job_card_details"], district, block, panchayat)

                    log_message(f" Processed job card {i}/{len(job_card_links)}")

                except Exception as e:
                    log_message(f" Failed to process job card {i}: {e}")

        except Exception as e:
            log_message(f"\n ERROR: {str(e)}")

        finally:
            queue.task_done()

    driver.quit()


def store_list():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    task_combinations = []

    # Step 1: Select financial year
    wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlFin")))
    fin_year_dropdown = get_element_safe(driver, By.ID, "ctl00_ContentPlaceHolder1_ddlFin")
    Select(fin_year_dropdown).select_by_visible_text(FINANCIAL_YEAR)
    log_message(f" Selected Financial Year: {FINANCIAL_YEAR}")
    time.sleep(2)

    # Step 2: Get list of districts from dropdown
    district_dropdown = get_element_safe(driver, By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict")
    select_district = Select(district_dropdown)
    districts = [d.text.strip() for d in select_district.options if d.text.strip() != "Select District"]

    # Only process selected 15 districts
    selected_districts = {
        'Chhotaudepur','PANCH MAHALS'}

    for district in districts:
        if district not in selected_districts:
            continue  #  Skip districts not in our selected list

        try:
            driver.get(BASE_URL)
            wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlFin")))
            Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlFin")).select_by_visible_text(FINANCIAL_YEAR)
            time.sleep(2)

            Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict")).select_by_visible_text(district)
            log_message(f" Selected District: {district}")
            time.sleep(2)

            wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlBlock")))
            block_dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlBlock")
            block_list = [b.text.strip() for b in Select(block_dropdown).options if b.text.strip() != "Select Block"]

            for block in block_list:
                try:
                    driver.get(BASE_URL)
                    wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlFin")))
                    Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlFin")).select_by_visible_text(FINANCIAL_YEAR)
                    time.sleep(2)

                    Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict")).select_by_visible_text(district)
                    time.sleep(2)

                    Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlBlock")).select_by_visible_text(block)
                    log_message(f" Selected Block: {block}")
                    time.sleep(2)

                    wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlPanchayat")))
                    panchayat_dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlPanchayat")
                    panchayats = [p.text.strip() for p in Select(panchayat_dropdown).options if p.text.strip() != "Select Panchayat"]

                    for panchayat in panchayats:
                        task_combinations.append((district, block, panchayat))
                        log_message(f" Added: {district}, {block}, {panchayat}")

                except Exception as e:
                    log_message(f" Error in block '{block}': {e}")
                    # log_message(f" Error in block '{block}' under district '{district}': {e}")
                    continue

        except Exception as e:
            log_message(f" Error in district '{district}': {e}")
            continue

    driver.quit()

    # Save to CSV BEFORE return
    with open("combinations.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["District", "Block", "Panchayat"])
        writer.writerows(task_combinations)

    log_message(f" Total Combinations: {len(task_combinations)}")
    log_message(" Data saved to combinations.csv")

    return task_combinations

    # return task_queue
def scrape_all():
    # Get dynamic combinations from store_list()
    task_combinations = store_list()

    if not task_combinations:
        log_message(" No task combinations found.")
        return

    # Create a queue to hold the tasks
    queue = Queue()

    # Add tasks to the queue
    for task in task_combinations:
        queue.put(task)

    # Create and start worker threads
    threads = []
    for _ in range(MAX_WORKERS):
        thread = threading.Thread(target=process_task, args=(queue,))
        thread.start()
        threads.append(thread)

    # Wait for all tasks to be completed
    for thread in threads:
        thread.join()

    log_message(" All scraping completed.")

if __name__ == "__main__":
    scrape_all()




    