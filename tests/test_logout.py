from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time

service = Service("./chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(service=service)

try:
    driver.get("http://localhost:3000/login") 

    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))

    email_input.send_keys("john.smith@example.com") 

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123") 

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))

    dropdown_trigger = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar-profile-pic-container")))

    actions = ActionChains(driver)
    actions.move_to_element(dropdown_trigger).perform()

    logout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))

    logout_button.click()

    wait.until(EC.url_contains("/login"))
    time.sleep(3)

    current_url = driver.current_url
    assert "/login" in current_url, f"Failed to redirect to login: {current_url}"
    print("Logout test passed!")

finally:
    driver.quit()
