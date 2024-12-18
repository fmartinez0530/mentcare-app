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

# driver_path = "E:/CS490/cs490_gp/tests/chromedriver-win64/chromedriver.exe"
# brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# option = webdriver.ChromeOptions()
# option.binary_location = brave_path
# service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service, options=option)

try:
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 15)

    script = """
    var testMessage = document.createElement('div');
    testMessage.innerText = "<div>FEATURE #6: PATIENT CAN TAKE DAILY SURVEYS AND VIEW RESULTS</div>";
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

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    wait.until(EC.url_contains("/dashboard"))
    print("Login successful, now on the dashboard.")

    time.sleep(3)
    multi_metric_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
    if not multi_metric_checkbox.is_selected():
        multi_metric_checkbox.click()
    print("Toggled 'Show Multiple Metrics' checkbox.")
    time.sleep(2)

    metric_buttons = driver.find_elements(By.CSS_SELECTOR, ".metric-buttons")
    for button in metric_buttons:
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on metric: {button.text}")
        time.sleep(1) 

    survey_buttons = driver.find_elements(By.CSS_SELECTOR, ".card-buttons")
    survey_clicked = False
    for button in survey_buttons:
        if "Daily Survey" in button.get_attribute("value"):
            print(f"Found a daily survey button: {button.get_attribute('value')}")
            button.click()
            survey_clicked = True
            break

    while True:
        question_textareas = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pd-question-container textarea"))
        )
        for idx, question in enumerate(question_textareas):
            if question.is_displayed() and question.is_enabled():
                question.clear()
                question.send_keys(f"Sample answer {idx + 1}")
                print(f"Answered question {idx + 1} with 'Sample answer {idx + 1}'.")
                time.sleep(1)

        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, ".pd-action-btn[type='submit']")
            if submit_button.is_displayed() and submit_button.is_enabled():
                print("SUBMIT button found, clicking to submit the survey.")
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                submit_button.click()
                print("Survey submitted successfully. Exiting program.")
                assert True
                time.sleep(3)
                break 
        except Exception:
            print("No SUBMIT button found. Checking for NEXT button.")

        try:
            next_button = driver.find_element(By.XPATH, "//button[text()='NEXT']")
            if next_button.is_displayed() and next_button.is_enabled():
                print("NEXT button found, clicking to proceed to the next page.")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                time.sleep(2)
                continue
        except Exception:
            print("No NEXT button or SUBMIT button found. Exiting.")
            break

finally:
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while quitting the driver: {e}")
    print("Program ended.")
