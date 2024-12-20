from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# driver_path = "E:/CS490/cs490_gp/tests/chromedriver-win64/chromedriver.exe"
# brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# option = webdriver.ChromeOptions()
# option.binary_location = brave_path
# service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service, options=option)

try:
    driver.maximize_window()
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 15)

    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "<div>FEATURE: ACCEPTING PATIENTS INDICATOR</div>";
    testMessage.style.position = "fixed";
    testMessage.style.bottom = "10px";
    testMessage.style.left = "10px";
    testMessage.style.backgroundColor = "yellow";
    testMessage.style.color = "black";
    testMessage.style.zIndex = "9999";
    testMessage.style.padding = "10px";
    testMessage.style.fontSize = "16pt";
    document.body.appendChild(testMessage);
    """
    driver.execute_script(script)

    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("linda.white@example.com")
    time.sleep(1)
    
    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(1)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    wait.until(EC.url_contains("/dashboard"))
    print("Login successful, now on the dashboard.")

    time.sleep(3) 
    acceptance_btn = driver.find_element(By.CLASS_NAME, "acceptanceBtn")
    acceptance_btn.click()

    time.sleep(2)
    acceptance_btn.click()

    time.sleep(2)

finally:
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while quitting the driver: {e}")
    print("Program ended.")
