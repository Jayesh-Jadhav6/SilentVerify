from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

def test_bot_detection():
    # Use forward slashes or raw string for Windows paths
    chromedriver_path = r"C:\Users\Jayesh\Desktop\Passive captcha\backend\chromedriver.exe"
    
    # Check if chromedriver exists
    if not os.path.exists(chromedriver_path):
        print("❌ ChromeDriver not found at:", chromedriver_path)
        print("Please download ChromeDriver and update the path")
        return
    
    service = Service(chromedriver_path)
    options = Options()
    # Remove headless mode to see what's happening
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("🔍 Opening Flask app...")
        driver.get("http://127.0.0.1:5000/")
        
        # Wait for page to load
        time.sleep(2)

        # Find Aadhaar input and enter value
        aadhaar_input = driver.find_element(By.ID, "aadhaar")
        aadhaar_input.send_keys("123456789012")

        # Click submit button
        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()

        # Wait for prediction to appear
        time.sleep(3)

        # Get result message
        result = driver.find_element(By.ID, "result").text
        print("🤖 Bot Test Result:", result)

    except Exception as e:
        print("❌ Error during bot test:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_bot_detection()