from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    driver.maximize_window()
    # driver.get("http://localhost:3000/")
    # time.sleep(3)

    driver.get("http://localhost:3000/login")
    time.sleep(2)

    wait = WebDriverWait(driver, 10)
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "FEATURE: VIEWING, CREATING AND SAVING JOURNALS";
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

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")  

    password_toggle = driver.find_element(By.CLASS_NAME, "password-toggle-btn")
    ActionChains(driver).move_to_element(password_toggle).click().perform()

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))
    time.sleep(3)

    print("Navigating to Patient Dashboard...")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "patient-dashboard-container")))

    print("Creating a new journal...")
    create_journal_button = driver.find_element(By.XPATH, "//input[@value='CREATE NEW JOURNAL']")
    create_journal_button.click()
    time.sleep(2)

    print("Editing the journal content...")
    journal_textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='Type here...']")
    new_content = "This is a test journal entry."
    journal_textarea.clear()
    journal_textarea.send_keys(new_content)
    time.sleep(0.5)

    print("Saving the journal...")
    save_button = driver.find_element(By.XPATH, "//input[@value='SAVE']")
    save_button.click()
    time.sleep(2)

    print("Closing the journal...")
    close_button = driver.find_element(By.XPATH, "//input[@value='CLOSE']")
    close_button.click()
    time.sleep(0.5)

    print("Reopening the journal to verify saved content...")
    journal_button = driver.find_element(By.XPATH, "//input[contains(@class, 'card-buttons') and contains(@value, 'Journal')]")
    journal_button.click()
    time.sleep(0.5)

    print("Verifying the saved journal content...")
    reopened_textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='Type here...']")
    saved_content = reopened_textarea.get_attribute("value")
    assert saved_content == new_content, f"Test failed: Content mismatch. Expected: '{new_content}', Found: '{saved_content}'"
    time.sleep(3)

    print("Test passed: Journal entry was successfully saved and verified.")

except Exception as e:
    print(f"Test failed: {e}")

finally:
    driver.quit()
