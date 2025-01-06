# #code for saving the data into database
import os
import requests
import base64
import time
from datetime import datetime
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector

# Flask app
app = Flask(__name__)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-web-security')

# Setup the web driver
service = Service(executable_path='C:/Users/renuka/chromedriver.exe')

# AntiCaptcha API Key
ANTI_CAPTCHA_API_KEY = "001ded428ac28b34c5b4a693d2945922"
# Aadhaar Verification URL
UDYAM_URL = "https://udyamregistration.gov.in/Udyam_Verify.aspx"

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',     
        user='root',  # MySQL username
        password='',  # MySQL password
        database='udyam_details_schema'  # MySQL database name
    )

#function to convert date format from DD/MM/YYYY to YYYY-MM-DD
def convert_date_format(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format:{date_str}")
        return None

# Solve CAPTCHA via AntiCaptcha
def solve_captcha_with_anticaptcha(captcha_image_path, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            if not os.path.exists(captcha_image_path):
                raise FileNotFoundError(f"Captcha image not found at path: {captcha_image_path}")
            if os.path.getsize(captcha_image_path) == 0:
                raise ValueError("Captcha image file is empty.")
            
            # Open the image and convert it to PNG if necessary
            with open(captcha_image_path, 'rb') as captcha_file:
                captcha_image_data = captcha_file.read()
                captcha_image = Image.open(BytesIO(captcha_image_data))
                captcha_image_path_converted = 'uploads/udyam_captchas/captcha_image_converted.png'
                captcha_image.save(captcha_image_path_converted, 'PNG')
            
            # Re-encode the image as base64 after conversion
            with open(captcha_image_path_converted, 'rb') as captcha_file:
                captcha_image_data = captcha_file.read()
                captcha_image_base64 = base64.b64encode(captcha_image_data).decode('utf-8')
            
            # Create CAPTCHA task with AntiCaptcha API
            response = requests.post(
                'https://api.anti-captcha.com/createTask',
                json={
                    "clientKey": ANTI_CAPTCHA_API_KEY,
                    "task": {
                        "type": "ImageToTextTask",
                        "body": captcha_image_base64
                    }
                }
            )
            response_json = response.json()
            print("AntiCaptcha API Response:", response_json)
            if response_json.get("errorCode"):
                print(f"AntiCaptcha error code: {response_json['errorCode']}")
                print(f"AntiCaptcha error description: {response_json['errorDescription']}")
                raise Exception(f"AntiCaptcha API error: {response_json.get('errorDescription')}")
            
            task_id = response_json.get('taskId')
            if not task_id:
                raise ValueError("Failed to retrieve task ID.")
            
            while True:
                result_response = requests.post(
                    'https://api.anti-captcha.com/getTaskResult',
                    json={
                        "clientKey": ANTI_CAPTCHA_API_KEY,
                        "taskId": task_id
                    }
                )
                result_json = result_response.json()
                if result_json['status'] == 'ready':
                    return result_json['solution']['text']
                time.sleep(5)
        except Exception as e:
            print(f"Error solving CAPTCHA on attempt {attempt + 1}: {e}")
            if attempt < max_attempts - 1:
                print("Retrying CAPTCHA...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise Exception("Max CAPTCHA attempts reached. Please try again later.")

# Interact with the "Print / Verify" dropdown
def click_dropdown(driver):
    try:
        dropdown_menu = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.XPATH, "//li[@class='drop-down']/a[contains(text(), 'Print / Verify')]"))
        )
        ActionChains(driver).move_to_element(dropdown_menu).perform()
        verify_option = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Verify Udyam Registration Number')]"))
        )
        verify_option.click()
        print("Successfully clicked on 'Verify Udyam Registration Number'.")
    except Exception as e:
        print(f"Failed to interact with the dropdown: {e}")

# Verify UDYAM Registration Details
def verify_udyam_details(udyam_registration_number: str) -> dict:
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(UDYAM_URL)
    try:
        click_dropdown(driver)
        
        # Wait for the registration number input to be visible
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$txtUdyamNo"))
        )
        udyam_registration_input = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtUdyamNo")
        udyam_registration_input.send_keys(udyam_registration_number)
        
        # Wait for the CAPTCHA image element to load
        captcha_image_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_imgCaptcha"))
        )
        
        # Get the location and size of the CAPTCHA image
        location = captcha_image_element.location
        size = captcha_image_element.size
        
        # Take a screenshot of the full page
        driver.save_screenshot('uploads/udyam_captchas/full_page_screenshot.png')
        image = Image.open('uploads/udyam_captchas/full_page_screenshot.png')
        
        # Define the cropping box
        left, top = location['x'], location['y']
        right, bottom = left + size['width'], top + size['height']
        
        # Crop the CAPTCHA from the screenshot
        captcha_image = image.crop((left, top, right, bottom))
        captcha_image_path = 'uploads/udyam_captchas/captcha_image.png'
        captcha_image.save(captcha_image_path)
        print(f"Cropped CAPTCHA image saved at {captcha_image_path}")
        
        # Solve the CAPTCHA using AntiCaptcha service
        captcha_text = solve_captcha_with_anticaptcha(captcha_image_path)
        print("Solved CAPTCHA text:", captcha_text)
        
        # Enter the CAPTCHA text
        captcha_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$txtCaptcha'))
        )
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)
        time.sleep(1)
        
        # Click the "Verify" button
        verify_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_ContentPlaceHolder1_btnVerify'))
        )
        driver.execute_script("arguments[0].click();", verify_button)
        
        # Wait for the confirmation message
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'card-title'))
        )
        
        # Extract enterprise details
        enterprise_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lblEnterpriseName"))
        ).text
        organisation_type = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lblOrganisationType").text
        date_of_incorporation = convert_date_format(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lbldateofincorporation").text)
        
        # Extract all relevant data from the enterprise table
        enterprise_data = []
        enterprise_table = driver.find_element(By.XPATH, "//table[contains(@class, 'table-bordered')]")
        rows = enterprise_table.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:  # Skip the header row
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 5:  # Ensure there are enough columns
                data_entry = {
                    "s_no": cols[0].text.strip(),  # SNo.
                    "classification_year": cols[2].text.strip(),  # Classification Year
                    "enterprise_type": cols[3].text.strip(),  # Enterprise Type
                    "classification_date": convert_date_format(cols[4].text.strip())  # Classification Date
                }
                enterprise_data.append(data_entry)

        # Extract unit/plant location data
        unit_location_data = []
        location_table = driver.find_element(By.XPATH, "//table[contains(@class, 'table-bordered') and contains(., 'Unit Name')]")
        location_rows = location_table.find_elements(By.TAG_NAME, "tr")
        for location_row in location_rows[1:]:  # Skip the header row
            location_cols = location_row.find_elements(By.TAG_NAME, "td")
            if len(location_cols) >= 11:  # Ensure there are enough columns
                location_entry = {
                    "sn": location_cols[0].text.strip(),  # SN
                    "unit_name": location_cols[1].text.strip(),  # Unit Name
                    "flat": location_cols[2].text.strip(),  # Flat
                    "building": location_cols[3].text.strip(),  # Building
                    "village_town": location_cols[4].text.strip(),  # Village/Town
                    "block": location_cols[5].text.strip(),  # Block
                    "road": location_cols[6].text.strip(),  # Road
                    "city": location_cols[7].text.strip(),  # City
                    "pin": location_cols[8].text.strip(),  # Pin
                    "state": location_cols[9].text.strip(),  # State
                    "district": location_cols[10].text.strip()  # District
                }
                unit_location_data.append(location_entry)

        # Extract Date of Udyam Registration
        date_of_udyam_registration = convert_date_format(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lblACKNOWLEDGEMENT").text)
        
        data = {
            "enterprise_name": enterprise_name,
            "organisation_type": organisation_type,
            "date_of_incorporation": date_of_incorporation,
            "enterprise_data": enterprise_data,  # Add all enterprise data to the result
            "unit_location_data": unit_location_data,  # Add unit/plant location data
            "date_of_udyam_registration": date_of_udyam_registration  # Add Date of Udyam Registration
        }
        
        # Save data to the database
        save_message = save_data_to_db(data)

        return {"message": "UDYAM details fetched successfully and data saved successfully", "status": True, "data": data}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"message": f"Error occurred: {e}", "status": False}
    finally:
        driver.quit()

def save_data_to_db(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert enterprise data
    cursor.execute('''
    INSERT INTO enterprises (enterprise_name, organisation_type, date_of_incorporation, date_of_udyam_registration)
    VALUES (%s, %s, %s, %s)
    ''', (data['enterprise_name'], data['organisation_type'], data['date_of_incorporation'], data['date_of_udyam_registration']))

    # Get the last inserted enterprise ID
    enterprise_id = cursor.lastrowid

    # Insert unit location data
    for unit in data['unit_location_data']:
        cursor.execute('''
        INSERT INTO unit_locations (enterprise_id, unit_name, flat, building, village_town, block, road, city, pin, state, district, sn)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (enterprise_id, unit['unit_name'], unit['flat'], unit['building'], unit['village_town'], unit['block'], unit['road'], unit['city'], unit['pin'], unit['state'], unit['district'], unit['sn']))

    # Insert enterprise classification data
    for classification in data['enterprise_data']:
        cursor.execute('''
        INSERT INTO enterprise_classifications (enterprise_id, classification_year, enterprise_type, classification_date, s_no)
        VALUES (%s, %s, %s, %s, %s)
        ''', (enterprise_id, classification['classification_year'], classification['enterprise_type'], classification['classification_date'], classification['s_no']))

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/get-udyam-details', methods=['POST'])
def get_udyam_details():
    data = request.get_json()
    udyam_registration_number = data.get("udyam_registration_number")
    if not udyam_registration_number:
        return jsonify({"message": "Invalid UDYAM Number", "status": False}), 400
    result = verify_udyam_details(udyam_registration_number)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)










































