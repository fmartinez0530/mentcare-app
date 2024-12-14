from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time


service = Service("./chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(service=service)

try:
    driver.get("http://localhost:3000/login")

    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))

    email_input.send_keys("linda.white@example.com")

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")  

    password_toggle = driver.find_element(By.CLASS_NAME, "password-toggle-btn")
    ActionChains(driver).move_to_element(password_toggle).click().perform()

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))
    time.sleep(3)

    current_url = driver.current_url
    assert "/dashboard" in current_url, f"Failed to redirect to dashboard: {current_url}"
    print("Login test passed!")

finally:
    driver.quit()
