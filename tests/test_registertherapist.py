from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Start WebDriver
service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    driver.maximize_window()
    driver.get("http://localhost:3000/register")
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "<div>FEATURE: SIGN UP AS A THERAPIST</div>";
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
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    print("Switching to therapist registration form...")
    therapist_button = driver.find_element(By.XPATH, "//input[@value='THERAPIST']")
    therapist_button.click()
    time.sleep(0.5)

    print("Filling personal details...")
    first_name = driver.find_element(By.XPATH, "//div[contains(@class, 'therapist-input-container')]//label[text()='First Name']/following-sibling::input")
    first_name.send_keys("James")
    time.sleep(0.5)

    last_name = driver.find_element(By.XPATH, "//div[contains(@class, 'therapist-input-container')]//label[text()='Last Name']/following-sibling::input")
    last_name.send_keys("Doe")
    time.sleep(0.5)

    email = driver.find_element(By.XPATH, "//div[contains(@class, 'therapist-input-container')]//label[text()='Email']/following-sibling::input")
    email.send_keys("james.doe@example.com")
    time.sleep(0.5)

    password = driver.find_element(By.XPATH, "//div[contains(@class, 'therapist-input-container')]//label[text()='Password']/following-sibling::input")
    password.send_keys("password")
    time.sleep(0.5)

    tos_checkbox = driver.find_element(By.XPATH, "//div[contains(@class, 'therapist-input-container')]//input[@type='checkbox']")
    tos_checkbox.click()
    time.sleep(0.5)

    print("Selecting gender...")
    female_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex-row therapistgenders')]//button[contains(., 'Female') or .//*[local-name()='svg']]"))
    )
    print(female_button.get_attribute('class'))
    female_button.click()
    time.sleep(0.5)


    next_button = driver.find_element(By.XPATH, "//input[contains(@class, 'pageBtn') and contains(@class, 'therapist') and @value='NEXT']")
    next_button.click()
    time.sleep(2)

    print("Filling therapist-specific details...")
    license_number = driver.find_element(By.XPATH, "//div[contains(@class, 'therapistinfo')]//label[text()='License Number']/following-sibling::input")
    license_number.send_keys("THER123456")
    time.sleep(0.5)

    print("Selecting specializations...")
    specializations = driver.find_elements(By.XPATH, "//div[contains(@class, 'therapistinfo')]//input[@class='grid-spec']")
    for specialization in specializations[:3]:
        driver.execute_script("arguments[0].scrollIntoView(true);", specialization)
        specialization.click()
        time.sleep(0.5)

    time.sleep(2)
    register_button = driver.find_element(By.XPATH, "//div[contains(@class, 'therapistinfo')]//button[text()='REGISTER']")
    driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
    register_button.click()
    time.sleep(6)

    print("Validating registration success...")
    if "/dashboard" in driver.current_url:
        print("Therapist registration test passed!")
    else:
        print("Therapist registration test failed. Dashboard not reached.")

except Exception as e:
    print(f"Test failed: {e}")

finally:
    driver.quit()
