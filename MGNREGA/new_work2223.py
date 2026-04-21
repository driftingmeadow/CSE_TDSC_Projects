
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

def collect_block_links(driver):
    selected_districts = {
        # 'ARVALLI', 'BANAS KANTHA',
        #  'BHARUCH', 'CHHOTAUDEPUR', 'DANG', 'DOHAD',
        # 'MAHISAGAR', 'NARMADA', 'NAVSARI', 'PANCH MAHALS', 'SABAR KANTHA',
        # 'SURAT', 'TAPI','VADODARA',
         'VALSAD'
    }
    #change the url for yearly extraction
    base_url = "https://nregastrep.nic.in/Netnrega/writereaddata/citizen_out/phy_prf_11_2223_out.html"

    wait = WebDriverWait(driver, 20)
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
    # Add any options you want, e.g. headless
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
    wait = WebDriverWait(driver, 15)
    comp_links = []

    try:
        driver.get(main_url)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

        rows = driver.find_elements(By.TAG_NAME, "tr")

        for i, row in enumerate(rows):
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) > 58:
                cell = tds[58]  # 58th td, zero-indexed 57
                try:
                    a_tag = cell.find_element(By.TAG_NAME, "a")
                    href = a_tag.get_attribute("href")
                    if href:
                        full_url = urljoin(main_url, href)
                        comp_links.append(full_url)
                        print(f"Row {i}: get_comp_links Found  {full_url}")
                except Exception:
                    print(f"Row {i}: No link found in 58th td")
                    continue
            else:
                print(f"Row {i}: Less than 58 td elements")

    except TimeoutException as e:
        print(f"Timeout while loading rows: {e}")

    return comp_links



def append_local_links_to_asset_page(asset_path, saved_work_code_to_file):
    from bs4 import BeautifulSoup
    import os
    import re

    print(f"\n[INFO] Called append_local_links_to_asset_page for: {asset_path}")
    print(f"[INFO] Number of saved work codes: {len(saved_work_code_to_file)}")

    # Step 1: Read HTML
    try:
        with open(asset_path, "r", encoding="utf-8") as f:
            final_html = f.read()
        print("[INFO] Successfully read parent HTML file.")
    except Exception as e:
        print(f"[ERROR] Failed to read parent HTML: {e}")
        return

    soup = BeautifulSoup(final_html, "html.parser")

    # Step 2: Find target table
    table = None
    for t in soup.find_all("table"):
        if "Work Name" in t.text:
            table = t
            break

    if not table:
        print("[ERROR] Could not find table with 'Work Name'.")
        raise Exception("Could not find data table during final modification.")
    print("[INFO] Found target table containing 'Work Name'.")

    # Step 3: Add new column header
    header_row = table.find("tr")
    new_header = soup.new_tag("th")
    new_header.string = "Local Project saved"
    header_row.append(new_header)
    print("[INFO] Added new column header: 'Local Project saved'")

    # Step 4: Append links to each row
    data_rows = table.find_all("tr")[1:]
    print(f"[INFO] Total data rows found: {len(data_rows)}")

    for i, row in enumerate(data_rows):
        cells = row.find_all("td")
        new_td = soup.new_tag("td")

        if len(cells) > 0:
            work_name_cell = cells[4].text if len(cells) > 4 else ""
            match = re.search(r"\(([^)]+)\)", work_name_cell)
            work_code = match.group(1).replace("/", "_") if match else None

            if work_code:
                work_code = work_code.strip().lower()
                basename = os.path.basename(asset_path)
                match = re.search(r'asset_([a-f0-9]+)', basename)
                panchayat_code = match.group(1) if match else ""
                lookup_key = f"{panchayat_code}_{work_code}"

                print(f"[DEBUG] Row {i+1}: Extracted work_code: {lookup_key}")

                if lookup_key in saved_work_code_to_file:
                    file_name = saved_work_code_to_file[lookup_key]
                    link_tag = soup.new_tag("a", href=file_name)
                    link_tag.string = work_code.split("/")[-1]
                    new_td.append(link_tag)
                    print(f"[INFO] Row {i+1}: Linked to file {file_name}")
                else:
                    new_td.string = "Not Found"
                    print(f"[WARN] Row {i+1}: No file found for {lookup_key}")
                    print(f"[DEBUG] Available keys: {list(saved_work_code_to_file.keys())}")
            else:
                new_td.string = ""
                print(f"[WARN] Row {i+1}: No work code found in cell text: {work_name_cell}")
        else:
            new_td.string = ""
            print(f"[WARN] Row {i+1}: No <td> cells found.")

        row.append(new_td)

    # Step 5: Write updated HTML back
    try:
        with open(asset_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"[SUCCESS] Updated parent HTML saved: {asset_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save updated HTML: {e}")



def download_asset_child_pages_by_click(driver, asset_url, root_dir="detailed_work2223_project"):
    import os
    import hashlib
    import time
    from urllib.parse import urlparse, parse_qs
    from bs4 import BeautifulSoup
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    os.makedirs(root_dir, exist_ok=True)
    driver.get(asset_url)
    time.sleep(10)  # Ideally replace with smarter waits

    # parsed_url = urlparse(asset_url)
    # query_params = parse_qs(parsed_url.query)
    # panchayat_code = query_params.get('Panchayat_Code', [None])[0]
    # if not panchayat_code:
    #     panchayat_code = f"asset_{hashlib.md5(asset_url.encode()).hexdigest()[:8]}"
    # panchayat_folder = os.path.join(root_dir, f"panchayat_{panchayat_code}")
    # os.makedirs(panchayat_folder, exist_ok=True)

    # asset_path = os.path.join(panchayat_folder, f"main_asset_page_{panchayat_code}.html")
    # with open(asset_path, "w", encoding="utf-8") as f:
    #     f.write(driver.page_source)
    # print(f" Main asset page saved as: {asset_path}")

    parsed_url = urlparse(asset_url)
    query_params = parse_qs(parsed_url.query)

    district_name = query_params.get('district_name', ['UnknownDistrict'])[0]
    block_name = query_params.get('block_name', ['UnknownBlock'])[0]
    panchayat_name = query_params.get('Panchayat_name', ['UnknownPanchayat'])[0]
    panchayat_code = query_params.get('Panchayat_Code', [None])[0]

    if not panchayat_code:
        panchayat_code = f"asset_{hashlib.md5(asset_url.encode()).hexdigest()[:8]}"
    url_hash = hashlib.md5(asset_url.encode()).hexdigest()[:8]

    base_path = os.path.join(root_dir, district_name, block_name, panchayat_name)
    panchayat_folder_name = f"panchayat_asset_{url_hash}_{panchayat_code}"
    panchayat_folder = os.path.join(base_path, panchayat_folder_name)
    os.makedirs(panchayat_folder, exist_ok=True)

    asset_path = os.path.join(panchayat_folder, f"panchayat_{panchayat_code}_assets_with_links.html")
    with open(asset_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f" Main asset page saved as: {asset_path}")

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Locate table
    table = None
    for t in soup.find_all("table"):
        if "Work Name" in t.text:
            table = t
            break

    if not table:
        raise Exception(" Could not find the correct data table.")

    # # Get all data rows using Selenium for click handling
    selenium_rows = driver.find_elements(By.XPATH, "//table//tr")[1:]

    saved_files = []

    for index, row in enumerate(selenium_rows):
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells or not cells[0].text.strip().isdigit():
                saved_files.append(None)
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
                wkcode = params.get('wkcode', ['unknown'])[0].replace('/', '_').strip().lower()
                file_name = f"{panchayat_code}_{wkcode}.html"

                print(f" Clicking link: {full_url}")
                link_element.click()

                WebDriverWait(driver, 15).until(lambda d: d.current_url != asset_url_before_click)
                time.sleep(5)

                child_soup = BeautifulSoup(driver.page_source, "html.parser")
                save_pages_with_subfolders(
                    soup=child_soup,
                    asset_url=asset_url,
                    root_dir=root_dir,
                    file_name=file_name
                )

                saved_files.append(file_name)
                print(f" Saved file: {file_name} for wkcode: {wkcode}")

                driver.back()
                WebDriverWait(driver, 10).until(lambda d: d.current_url == asset_url_before_click)
                time.sleep(5)
            else:
                saved_files.append(None)

        except Exception as e:
            print(f" Error in row {index}: {e}")
            saved_files.append(None)

    saved_work_code_to_file = {}
    for file_name in saved_files:
        if file_name:
            wkcode = file_name.split("_", 1)[-1].replace(".html", "").strip().lower()
            saved_work_code_to_file[wkcode] = file_name

    append_local_links_to_asset_page(asset_path, saved_work_code_to_file)
    print(f" Local links embedded in: {asset_path}")

    # Get initial number of rows to iterate over
    row_count = len(driver.find_elements(By.XPATH, "//table//tr")[1:])

    for index in range(row_count):
        try:
            # Re-fetch the row on every iteration to avoid stale references
            selenium_rows = driver.find_elements(By.XPATH, "//table//tr")[1:]
            row = selenium_rows[index]

            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells or not cells[0].text.strip().isdigit():
                saved_files.append(None)
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
                wkcode = params.get('wkcode', ['unknown'])[0].replace('/', '_').strip().lower()
                file_name = f"{panchayat_code}_{wkcode}.html"

                print(f" Clicking link: {full_url}")
                link_element.click()

                WebDriverWait(driver, 15).until(lambda d: d.current_url != asset_url_before_click)
                time.sleep(5)

                child_soup = BeautifulSoup(driver.page_source, "html.parser")
                save_pages_with_subfolders(
                    soup=child_soup,
                    asset_url=asset_url,
                    root_dir=root_dir,
                    file_name=file_name
                )

                saved_files.append(file_name)
                print(f" Saved file: {file_name} for wkcode: {wkcode}")

                driver.back()
                WebDriverWait(driver, 10).until(lambda d: d.current_url == asset_url_before_click)
                time.sleep(5)
            else:
                saved_files.append(None)

        except Exception as e:
            print(f" Error in row {index}: {e}")
            saved_files.append(None)




def save_pages_with_subfolders(soup, asset_url, root_dir="root", file_name=None):
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

    # Compose folder hierarchy
    base_path = os.path.join(root_dir, district_name, block_name, panchayat_name)
    panchayat_folder_name = f"panchayat_asset_{url_hash}_{panchayat_code}"
    full_folder_path = os.path.join(base_path, panchayat_folder_name)

    os.makedirs(full_folder_path, exist_ok=True)

    if file_name:
        local_path = os.path.join(full_folder_path, file_name)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f" Saved child page: {local_path}")
        return local_path

    output_filename = f"{panchayat_code}_assets_with_links.html"
    output_file = os.path.join(full_folder_path, output_filename)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f" Saved parent asset page: {output_file}")
    return output_file


#2nd
def main():
    driver = initialize_driver()  # create driver once
    
    try:
        # Step 1: Get all block URLs for selected districts
        all_blocks = collect_block_links(driver)  # returns list of dicts with keys: district, block, url
        
        all_component_links = []

        # Step 2: For each block, get component links using the driver
        for block in all_blocks:
            block_url = block['url']
            print(f"\n Processing block: {block['block']} in district: {block['district']}")
            
            comp_links = get_comp_links(driver, block_url)  # pass driver here
            
            # Optional: Keep track of all component links across blocks
            all_component_links.extend(comp_links)

        print(f"\n Finished processing all blocks. Total component links collected: {len(all_component_links)}")

        # Step 3: Process each component link with the same driver
        for url in all_component_links:
            try:
                print(f"\nProcessing component link: {url}")
                download_asset_child_pages_by_click(driver, url)
            except Exception as e:
                print(f"Failed processing {url}: {e}")

    finally:
        driver.quit()  # quit driver once all done


if __name__ == "__main__":
    main()