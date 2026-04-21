
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import base64
import io
from PIL import Image
import pytesseract

#  Initialize Chrome driver
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    print(f" Using ChromeDriver from: {service.path}")
    return webdriver.Chrome(service=service, options=options)

#  Start process
driver = initialize_driver()
driver.get("https://anyror.gujarat.gov.in/LandRecordRural.aspx")
wait = WebDriverWait(driver, 20)

#  Select record type
record_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_drpLandRecord")))
Select(record_type_dropdown).select_by_visible_text("INTEGRATED SURVEY NO DETAILS (સરવે નંબરને લગતી સંપૂર્ણ માહિતી)")

# Target districts
target_districts_gujarati = ["નવસારી", "સુરત", "તાપી"]

wait.until(lambda d: len(Select(d.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict")).options) > 1)
district_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict"))

for district_option in district_dropdown.options:
    district_name = district_option.text.strip()
    if district_name in target_districts_gujarati:
        print(f"\n District: {district_name}")
        Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict")).select_by_visible_text(district_name)
        time.sleep(1)

        # Taluka
        wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlTaluka")))
        taluka_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlTaluka"))
        for taluka_option in [t for t in taluka_dropdown.options if t.text.strip() != "Select"]:
            taluka_name = taluka_option.text.strip()
            Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlTaluka")).select_by_visible_text(taluka_name)
            print(f"   Taluka: {taluka_name}")
            time.sleep(1)

            # Village
            wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlVillage")))
            village_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlVillage"))
            for village_option in [v for v in village_dropdown.options if v.text.strip() != "Select"]:
                village_name = village_option.text.strip()
                Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlVillage")).select_by_visible_text(village_name)
                print(f"    Village: {village_name}")
                time.sleep(1)

                # Survey No
                wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlSurveyNo")))
                survey_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlSurveyNo"))
                for survey_option in [s for s in survey_dropdown.options if s.text.strip() != "Select"]:
                    survey_no = survey_option.text.strip()
                    Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlSurveyNo")).select_by_visible_text(survey_no)
                    print(f"      Survey: {survey_no}")
                    time.sleep(1)

                    # CAPTCHA Section
                    captcha_img = driver.find_element(By.ID, "ContentPlaceHolder1_i_captcha_1")
                    src_data = captcha_img.get_attribute("src")

                    # Extract base64 image and decode
                    base64_data = src_data.split(',')[1]
                    image_data = base64.b64decode(base64_data)
                    image = Image.open(io.BytesIO(image_data))
                    captcha_text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789').strip()

                    print(" CAPTCHA:", captcha_text)

                    # Fill captcha
                    captcha_input = driver.find_element(By.ID, "ContentPlaceHolder1_txt_captcha_1")
                    captcha_input.clear()
                    captcha_input.send_keys(captcha_text)

                    # Click Submit
                    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnGo")))
                    submit_btn.click()

                    time.sleep(3)  # Wait for result to load (or add custom logic to save page)

                    # Optional: Save result page
                    with open(f"{district_name}_{taluka_name}_{village_name}_{survey_no}.html", "w", encoding='utf-8') as f:
                        f.write(driver.page_source)

                    # Navigate back to the form page
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_drpLandRecord")))
                    Select(driver.find_element(By.ID, "ContentPlaceHolder1_drpLandRecord")).select_by_visible_text(
                        "INTEGRATED SURVEY NO DETAILS (સરવે નંબરને લગતી સંપૂર્ણ માહિતી)"
                    )

                    # Re-select district, taluka, village for next iteration
                    Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlDistrict")).select_by_visible_text(district_name)
                    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlTaluka")))
                    Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlTaluka")).select_by_visible_text(taluka_name)
                    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlVillage")))
                    Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlVillage")).select_by_visible_text(village_name)
