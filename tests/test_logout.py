from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-software-rasterizer")

#service = Service("./chromedriver-linux64/chromedriver")
#service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("http://localhost:3000/")
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "FEATURE #1: <strong>VIEW LANDING PAGE</strong>, SIGN UP, LOG IN, AND <strong>LOG OUT</strong>";
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
    time.sleep(3)
    
    driver.get("http://localhost:3000/login") 

    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))

    email_input.send_keys("john.smith@example.com") 
    time.sleep(1)

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(1)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    time.sleep(1)

    wait.until(EC.url_contains("/dashboard"))

    dropdown_trigger = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar-profile-pic-container")))
    time.sleep(1)

    actions = ActionChains(driver)
    actions.move_to_element(dropdown_trigger).perform()
    time.sleep(1)

    logout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))

    logout_button.click()

    wait.until(EC.url_contains("/login"))
    time.sleep(3)

    current_url = driver.current_url
    assert "/login" in current_url, f"Failed to redirect to login: {current_url}"
    print("Logout test passed!")

finally:
    driver.quit()
