
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
import os
import time

import os
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

# def collect_block_links(driver):
#     selected_districts = {
#         'ARVALLI', 
#         'BANAS KANTHA',
#          'BHARUCH', 'CHHOTAUDEPUR', 'DANG', 'DOHAD' , 'MAHISAGAR', 'NARMADA', 'NAVSARI', 'PANCH MAHALS', 'SABAR KANTHA', 'SURAT',  'VALSAD',
#     }


def collect_block_links(driver):
    selected_districts = {
         'VADODARA'
    }

    #change the url for yearly extraction
    base_url = "https://nregastrep.nic.in/Netnrega/writereaddata/citizen_out/phy_prf_11_2223_out.html"

    wait = WebDriverWait(driver, 15)
    block_links_collected = []

    try:
        driver.get(base_url)
        print(" Fetching district links...")

        district_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//a[contains(@href, 'physicalperf_dist.aspx')]")))
        district_info = [(d.text.strip(), d.get_attribute("href")) for d in district_links]

        for district_name, district_url in district_info:
            district_name_upper = district_name.upper()

            if district_name_upper not in selected_districts:
                print(f" Skipping District: {district_name}")
                continue

            print(f"\n Processing District: {district_name}")
            driver.get(district_url)

            # Replace time.sleep(2) with explicit wait for block links
            block_links = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//a[contains(@href, 'physicalperf_blk.aspx')]")))
            block_info = [(b.text.strip(), b.get_attribute("href")) for b in block_links]

            for block_name, block_url in block_info:
                print(f"   Found Block: {block_name} → {block_url}")
                block_links_collected.append({
                    "district": district_name,
                    "block": block_name,
                    "url": block_url
                })

            # Go back to base URL to reload fresh district links
            driver.get(base_url)
            district_links = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//a[contains(@href, 'physicalperf_dist.aspx')]")))
            district_info = [(d.text.strip(), d.get_attribute("href")) for d in district_links]

    except Exception as e:
        print(f"\n Error during process: {e}")
    #here
    print(f" collect_block_links {block_links_collected}")

    # **DO NOT QUIT DRIVER HERE**
    return block_links_collected

def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    
    return driver

# Main control
driver = initialize_driver()

try:
    block_links = collect_block_links(driver)
    print(f"Collected {len(block_links)} blocks in total.")
    # call other functions here, pass `driver` as argument
finally:
    print("Closing driver now.")
    driver.quit()

def get_with_retry(url, max_retries=2, retry_delay=10, timeout=15):
    attempt = 0
    while attempt <= max_retries:
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                return resp
            elif resp.status_code == 503:
                print(f" Service Unavailable (503) for {url}. Retrying in {retry_delay}s...")
            else:
                print(f" HTTP {resp.status_code} for {url}. Not retrying.")
                return resp
        except requests.RequestException as e:
            print(f" Request failed for {url}: {e}. Retrying in {retry_delay}s...")
        time.sleep(retry_delay)
        attempt += 1
    print(f" Max retries exceeded for {url}")
    return None

###yy
def get_comp_links(driver, main_url):
    if not isinstance(main_url, str):
        raise ValueError(f"Expected string URL but got {type(main_url)}: {main_url}")

    wait = WebDriverWait(driver, 15)
    comp_links = []

    try:
        driver.get(main_url)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
        rows = driver.find_elements(By.TAG_NAME, "tr")

        for i, row in enumerate(rows):
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) > 58:
                cell = tds[58]
                try:
                    a_tag = cell.find_element(By.TAG_NAME, "a")
                    href = a_tag.get_attribute("href")
                    if href:
                        full_url = urljoin(main_url, href)
                        comp_links.append(full_url)
                        print(f"Row {i}: get_comp_links Found  {full_url}")
                except Exception:
                    print(f"Row {i}: No link found in 58th td")
            else:
                print(f"Row {i}: Less than 58 td elements")

    except TimeoutException as e:
        print(f"Timeout while loading rows: {e}")

    return comp_links


#replace the href with locally saved links

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os

def append_local_links_to_asset_page(asset_path, saved_work_code_to_file):
    with open(asset_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all rows in the main table
    rows = soup.select("table tr")

    for row in rows:
        cells = row.find_all("td")
        if not cells:
            continue

        for cell in cells:
            link = cell.find("a", href=True)
            if link and "wkcode=" in link["href"]:
                # Extract wkcode from original link
                params = parse_qs(urlparse(link["href"]).query)
                wkcode_raw = params.get("wkcode", ["unknown"])[0]
                wkcode_key = wkcode_raw.replace("/", "_").strip().lower()

                # Try finding local file using this key
                for key, local_file in saved_work_code_to_file.items():
                    if key.endswith(wkcode_key):  # Match suffix
                        link["href"] = os.path.basename(local_file)  # Replace with local file name
                        link["target"] = "_blank"  # Optional: open in new tab
                        break

    # Write the modified HTML back
    with open(asset_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Updated local links in {asset_path}")


def download_asset_child_pages_by_click(driver, asset_url, root_dir="Detailed_work2223_project"):
    import os
    import hashlib
    import time
    import traceback
    from urllib.parse import urlparse, parse_qs
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    os.makedirs(root_dir, exist_ok=True)
    driver.get(asset_url)

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
    time.sleep(2)

    parsed_url = urlparse(asset_url)
    query_params = parse_qs(parsed_url.query)

    #metadata
    district_name = query_params.get('district_name', ['UnknownDistrict'])[0]
    block_name = query_params.get('block_name', ['UnknownBlock'])[0]
    panchayat_name = query_params.get('Panchayat_name', ['UnknownPanchayat'])[0]
    panchayat_code = query_params.get('Panchayat_Code', [None])[0]
    if not panchayat_code:
        panchayat_code = f"asset_{hashlib.md5(asset_url.encode()).hexdigest()[:8]}"
    url_hash = hashlib.md5(asset_url.encode()).hexdigest()[:8]

    #directory
    base_path = os.path.join(root_dir, district_name, block_name, panchayat_name)
    panchayat_folder_name = f"panchayat_asset_{url_hash}_{panchayat_code}"
    panchayat_folder = os.path.join(base_path, panchayat_folder_name)
    os.makedirs(panchayat_folder, exist_ok=True)

    #path
    asset_path = os.path.join(panchayat_folder, f"panchayat_{panchayat_code}_assets_with_links.html")
    with open(asset_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f" Main asset page saved as: {asset_path}")

    saved_files = []
    row_index = 0

    while True:
        selenium_rows = driver.find_elements(By.XPATH, "//table//tr")[1:]
        if row_index >= len(selenium_rows):
            break

        try:
            row = selenium_rows[row_index]
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells or not cells[0].text.strip().isdigit():
                saved_files.append(None)
                row_index += 1
                continue

            link_element = None
            for cell in cells:
                try:
                    link = cell.find_element(By.XPATH, ".//a[contains(@href, 'wkcode=')]")
                    link_element = link
                    break
                except:
                    continue

            if link_element:
                asset_url_before_click = driver.current_url
                full_url = link_element.get_attribute("href")
                params = parse_qs(urlparse(full_url).query)
                wkcode_raw = params.get('wkcode', ['unknown'])[0]
                # Normalize work code (lowercase + replace slash with underscore)
                wkcode = wkcode_raw.replace("/", "_").strip().lower()

                file_name = f"{panchayat_code}_{wkcode}.html"

                print(f" Clicking link: {full_url}")
                link_element.click()

                WebDriverWait(driver, 15).until(lambda d: d.current_url != asset_url_before_click)
                time.sleep(2)

                from bs4 import BeautifulSoup
                child_soup = BeautifulSoup(driver.page_source, "html.parser")
                save_pages_with_subfolders(
                    soup=child_soup,
                    asset_url=asset_url,
                    root_dir=root_dir,
                    file_name=file_name
                )

                saved_files.append(file_name)
                print(f"Saved file: {file_name} for wkcode: {wkcode}")

                driver.back()
                WebDriverWait(driver, 10).until(lambda d: d.current_url == asset_url_before_click)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
                time.sleep(2)

            else:
                saved_files.append(None)

        except Exception as e:
            print(f" Error in row {row_index}: {e}")
            traceback.print_exc()
            saved_files.append(None)

        row_index += 1

    # Create lookup dictionary with consistent keys including panchayat_code prefix
    saved_work_code_to_file = {}
    for file_name in saved_files:
        if file_name:
            # file_name format: <panchayat_code>_<wkcode>.html
            base = os.path.basename(file_name)
            if base.endswith(".html"):
                key = base[:-5].lower()  # Remove '.html' and lowercase
                saved_work_code_to_file[key] = file_name

    append_local_links_to_asset_page(asset_path, saved_work_code_to_file)
    print(f"Local links embedded in: {asset_path}")


def save_pages_with_subfolders(soup, asset_url, root_dir="root", file_name=None):
    import os
    import hashlib
    from urllib.parse import urlparse, parse_qs

    os.makedirs(root_dir, exist_ok=True)

    parsed_url = urlparse(asset_url)
    query_params = parse_qs(parsed_url.query)

    district_name = query_params.get('district_name', ['UnknownDistrict'])[0]
    block_name = query_params.get('block_name', ['UnknownBlock'])[0]
    panchayat_name = query_params.get('Panchayat_name', ['UnknownPanchayat'])[0]
    panchayat_code = query_params.get('Panchayat_Code', [None])[0]

    if not panchayat_code:
        url_hash = hashlib.md5(asset_url.encode()).hexdigest()[:8]
        panchayat_code = f"asset_{url_hash}"
    else:
        url_hash = hashlib.md5(asset_url.encode()).hexdigest()[:8]

    base_path = os.path.join(root_dir, district_name, block_name, panchayat_name)
    panchayat_folder_name = f"panchayat_asset_{url_hash}_{panchayat_code}"
    full_folder_path = os.path.join(base_path, panchayat_folder_name)

    os.makedirs(full_folder_path, exist_ok=True)

    if file_name:
        local_path = os.path.join(full_folder_path, file_name)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Saved child page: {local_path}")
        return local_path

    output_filename = f"{panchayat_code}_assets_with_links.html"
    output_file = os.path.join(full_folder_path, output_filename)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f" Saved parent asset page: {output_file}")
    return output_file

def threaded_download(comp_link):
    driver = initialize_driver()
    try:
        download_asset_child_pages_by_click(driver, comp_link)
    finally:
        driver.quit()

# --- MAIN FUNCTION ---

def main():
    # Use a single driver to get block_links and comp_links
    driver = initialize_driver()
    block_links = collect_block_links(driver)

    comp_links_all = []
    for block_link in block_links:
        comp_links = get_comp_links(driver, block_link['url'])
        comp_links_all.extend(comp_links)

    driver.quit()  # Done using shared driver

    # --- THREADING HERE: DOWNLOAD 5 LINKS IN PARALLEL ---
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(threaded_download, link) for link in comp_links_all]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] Download failed: {e}")

    # Process saved HTML pages (can also be threaded if needed)
    for html_path in os.listdir('html_assets'):
        append_local_links_to_asset_page(html_path)

if __name__ == "__main__":
    main()