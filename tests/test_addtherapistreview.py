from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import time

service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    driver.maximize_window()
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 15)

    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "FEATURE: Add therapist review";
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
    email_input.send_keys("john.smith@example.com")
    time.sleep(0.5)
    
    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(0.5)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    wait.until(EC.url_contains("/dashboard"))
    print("Login successful, now on the dashboard.")
    time.sleep(0.5) 

    driver.get("http://localhost:3000/therapistlist") 
    time.sleep(0.5)

    search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-therapists-input")))
    search_input.send_keys("Linda White")
    time.sleep(3)

    buttons = driver.find_elements(By.XPATH, "//button[text()='View Profile']")
    visible_button = None
    for button in buttons:
        if button.is_displayed():
            visible_button = button
            break
    visible_button.click()
    time.sleep(0.5)

    wait.until(EC.url_contains("/therapistProfile"))
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 100  # Pixels to scroll each step
    scroll_pause_time = 0.1  # Time to wait between steps

    current_position = 0
    while current_position < last_height:
        current_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)

    review_button = driver.find_element(By.XPATH, "//button[@class='td-btn' and contains(text(), 'Add Review')]")
    review_button.click()
    time.sleep(2)

    textarea = driver.find_element(By.CSS_SELECTOR, "div.popUp-background textarea")
    textarea.send_keys("Linda White is a great therapist!")
    time.sleep(0.5)

    textarea.send_keys(Keys.TAB + (Keys.ARROW_RIGHT * 5))
    time.sleep(0.5)

    # star_input = driver.find_element(By.XPATH, "(//div[@class='popUp']//form//div//spam//label)")
    # star_input.click()
    # time.sleep(0.5)

    send_review_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Send Review']")
    send_review_button.click()
    time.sleep(3)

    driver.get("http://localhost:3000/therapistlist")

    search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-therapists-input")))
    search_input.send_keys("Linda White")
    time.sleep(0.5)

    buttons = driver.find_elements(By.XPATH, "//button[text()='View Profile']")
    visible_button = None
    for button in buttons:
        if button.is_displayed():
            visible_button = button
            break
    visible_button.click()
    time.sleep(0.5)

    wait.until(EC.url_contains("/therapistProfile"))
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 100  # Pixels to scroll each step
    scroll_pause_time = 0.1  # Time to wait between steps

    current_position = 0
    while current_position < last_height:
        current_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)
    
    time.sleep(5)
    
finally:
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while quitting the driver: {e}")
    print("Program ended.")
