from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

#  Function to initialize Chrome driver using webdriver-manager
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Optional, if you want to run headless

    service = Service(ChromeDriverManager().install())
    print(f" Using ChromeDriver from: {service.path}")
    return webdriver.Chrome(service=service, options=options)

#  Use the function to initialize driver
driver = initialize_driver()
driver.get("https://anyror.gujarat.gov.in/LandRecordRural.aspx")

wait = WebDriverWait(driver, 20)

# Select "INTEGRATED SURVEY NO DETAILS"
# Wait for the dropdown to appear
record_type_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_drpLandRecord"))
)
# Wrap it in a Select object
select = Select(record_type_dropdown)
# Print all options (to debug and confirm the actual visible text)
for option in select.options:
    print("-", option.text.strip())
# Select the desired option (use the exact text you see printed above)
select.select_by_visible_text("INTEGRATED SURVEY NO DETAILS (સરવે નંબરને લગતી સંપૂર્ણ માહિતી)")


# Define target districts by their visible Gujarati text
target_districts_gujarati = ["નવસારી", "સુરત", "તાપી"]

# Wait for district dropdown to be populated after service selection
wait.until(lambda d: len(Select(d.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict")).options) > 1)

# Get the updated district dropdown
district_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict"))

# Print available district options (for verification)
print("\nAvailable District Options:")
for option in district_dropdown.options:
    print("-", option.text.strip())

# Loop through and select only matching Gujarati district names
for district_option in district_dropdown.options:
    district_name = district_option.text.strip()
    if district_name in target_districts_gujarati:
        print(f"\nSelecting district: {district_name}")
        # Refresh dropdown reference before selecting
        district_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict"))
        district_dropdown.select_by_visible_text(district_name)
        time.sleep(1)  # Or add a wait here if next dropdown loads dynamically


    #  Select Taluka
    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlTaluka")))
    taluka_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlTaluka"))
    taluka_options = [opt for opt in taluka_dropdown.options if opt.text.strip() != "Select"]

    for taluka_option in taluka_options:
        taluka_name = taluka_option.text.strip()
        taluka_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlTaluka"))
        taluka_dropdown.select_by_visible_text(taluka_name)
        print(f"  Taluka selected: {taluka_name}")
        
        # 3. Select Village
        wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlVillage")))
        village_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlVillage"))
        village_options = [opt for opt in village_dropdown.options if opt.text.strip() != "Select"]

        for village_option in village_options:
            village_name = village_option.text.strip()
            village_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlVillage"))
            village_dropdown.select_by_visible_text(village_name)
            print(f" Village selected: {village_name}")


            # 4. Select Survey
            wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlSurveyNo")))
            survey_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlSurveyNo"))
            survey_options = [opt for opt in survey_dropdown.options if opt.text.strip() != "Select"]

            for survey_option in survey_options:
                survey_no = survey_option.text.strip()
                survey_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlSurveyNo"))
                survey_dropdown.select_by_visible_text(survey_no)
                print(f"      🔍 Survey selected: {survey_no}")

                #  Add scraping or saving logic here

# # 6. Show CAPTCHA and wait for manual entry
# input(" Please fill in the CAPTCHA manually on the page, then press Enter here to continue...")


# 7. Click "Get Details" button
submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnDetails")))
submit_btn.click()

# 8. Wait for final result page to load
time.sleep(5)

# 9. Save the page as HTML
with open("gujarat_land_record_result.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print(" Page saved as 'gujarat_land_record_result.html'")
driver.quit()