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
    driver.maximize_window()
    driver.get("http://localhost:3000/")
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "<div>FEATURE: VIEW LANDING PAGE, SIGN UP, LOG IN, AND LOG OUT</div><div>FEATURE: PATIENT CAN LOGIN AND VIEW DASHBOARD</div><div>FEATURE: THERAPIST CAN LOGIN AND VIEW DASHBOARD</div>";
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

    # Scroll down slowly to the bottom of the landing page
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 100  # Pixels to scroll each step
    scroll_pause_time = 0.1  # Time to wait between steps

    current_position = 0
    while current_position < last_height:
        current_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)
    
    # Scroll back slowly to the top of the landing page
    while current_position > 0:
        current_position -= scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)
    
    register_now = driver.find_element(By.CLASS_NAME, "landing-register-now")
    register_now.click()
    
    wait.until(EC.url_contains("/register"))
    time.sleep(3)

    driver.get("http://localhost:3000/login")

    #   LOGGING IN AS PATIENT
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("john.smith@example.com")
    time.sleep(1)

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(1)

    password_toggle = driver.find_element(By.CLASS_NAME, "password-toggle-btn")
    ActionChains(driver).move_to_element(password_toggle).click().perform()
    time.sleep(1)
    
    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    wait.until(EC.url_contains("/dashboard"))
    print("Login successful, now on the dashboard.")
    time.sleep(1)

    wait.until(EC.url_contains("/dashboard"))
    time.sleep(3)

    current_url = driver.current_url
    assert "/dashboard" in current_url, f"Failed to redirect to dashboard: {current_url}"
    print("Login test passed!")

    # Scroll down slowly to the bottom of the screen
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 100  # Pixels to scroll each step
    scroll_pause_time = 0.1  # Time to wait between steps

    current_position = 0
    while current_position < last_height:
        current_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)
    
    # Scroll back slowly to the top of the landing page
    while current_position > 0:
        current_position -= scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)
    
    dropdown_trigger = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar-profile-pic-container")))
    time.sleep(1)

    actions = ActionChains(driver)
    actions.move_to_element(dropdown_trigger).perform()
    time.sleep(1)

    logout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))

    logout_button.click()

    wait.until(EC.url_contains("/login"))
    time.sleep(3)
    
    #   LOGGING IN AS THERAPIST
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("linda.white@example.com")
    time.sleep(1)

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(1)

    password_toggle = driver.find_element(By.CLASS_NAME, "password-toggle-btn")
    ActionChains(driver).move_to_element(password_toggle).click().perform()
    time.sleep(1)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    wait.until(EC.url_contains("/dashboard"))
    print("Login successful, now on the dashboard.")
    time.sleep(1)

    wait.until(EC.url_contains("/dashboard"))
    time.sleep(3)

    current_url = driver.current_url
    assert "/dashboard" in current_url, f"Failed to redirect to dashboard: {current_url}"
    print("Login test passed!")

finally:
    driver.quit()
