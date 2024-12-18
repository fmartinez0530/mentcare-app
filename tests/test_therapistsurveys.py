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

# options.binary_location = brave_path
# service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service, options=options)



try:
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 45)
    time.sleep(1)

    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("john.smith@example.com")
    element_class = email_input.get_attribute("class")
    print("Class of the element:", element_class)
    time.sleep(1)
    
    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    element_class = password_input.get_attribute("class")
    print("Class of the element:", element_class)
    time.sleep(1)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    element_class = login_button.get_attribute("class")
    print("Class of the element:", element_class)
    login_button.click()
    time.sleep(3)
    print("got here 1")
    logs = driver.get_log('browser') 
    for log in logs:
        print(f"Console Error: {log['message']}")
    print(driver.current_url)
    wait.until(EC.url_contains("/dashboard"))
    print(driver.current_url)
    print("Login successful, now on the dashboard.")

    time.sleep(5) 
    survey_buttons = driver.find_elements(By.CSS_SELECTOR, ".card-buttons")
    survey_clicked = False
    for button in survey_buttons:
        if "(NEW) Survey" in button.get_attribute("value"):
            print(f"Found an incomplete therapist survey button: {button.get_attribute('value')}")
            button.click()
            survey_clicked = True
            break

    while True:
        breakLoop = False
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
            # submit_button = driver.find_element(By.CSS_SELECTOR, ".pd-action-btn[type='submit']")
            #submit_buttons = wait.until(
            #    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pd-action-btn[type='submit']"))
            #)
            #for submit_button in submit_buttons:
            #    if submit_button.is_displayed() and submit_button.is_enabled():
            #        print("SUBMIT button found, clicking to submit the survey.")
            #        #driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            #        submit_button.click()
            #        print("Survey submitted successfully. Exiting program.")
            #        breakLoop = True
            #        break 
            #if breakLoop:
            #    break
            submit_button = driver.find_element(By.XPATH, "//form[@incomptherapistsurveyid]//input[@type='submit']")
            actions = ActionChains(driver)
            actions.move_to_element(submit_button).click().perform()
            
            #actions.moveToElement(element).click().perform();
            #submit_button.click()
            print("Survey submitted successfully. Exiting program.")
            break
        except Exception as e:
            breakLoop = True
            print(f"Error occurred: {e}")
            #print("No SUBMIT button found. Checking for NEXT button.")

        if breakLoop == False:
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
        else:
            break
finally:
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while quitting the driver: {e}")
    print("Program ended.")
