from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    driver.maximize_window()
    driver.get("http://localhost:3000/login")
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "<div>FEATURE: LOGGED IN USER CAN SUBMIT A TESTIMONIAL</div>";
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

    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("john.smith@example.com")

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))
    print("Login successful!")
    time.sleep(2)

    driver.get("http://localhost:3000/")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    review_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "review-box")))
    driver.execute_script("arguments[0].scrollIntoView(true);", review_box)
    review_box.clear()
    review_box.send_keys("This platform has been amazing for my mental health!")
    time.sleep(2)

    send_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "send-button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
    send_button.click()
    print("Testimonial submitted!")

    time.sleep(4)
    print("Testimonial submission test passed!")

finally:
    driver.quit()
