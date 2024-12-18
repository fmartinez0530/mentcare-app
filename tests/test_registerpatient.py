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
    driver.get("http://localhost:3000/register")
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "<div>FEATURE #2: SIGN UP AS A PATIENT</div>";
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

    print("Filling personal details...")
    first_name = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='First Name']/following-sibling::input")))
    first_name.send_keys("John")
    time.sleep(1)

    last_name = driver.find_element(By.XPATH, "//label[text()='Last Name']/following-sibling::input")
    last_name.send_keys("Doe")
    time.sleep(1)

    email = driver.find_element(By.XPATH, "//label[text()='Email']/following-sibling::input")
    email.send_keys("john12.doe@example.com")
    time.sleep(1)

    password = driver.find_element(By.XPATH, "//label[text()='Password']/following-sibling::input")
    password.send_keys("password123")
    time.sleep(1)

    tos_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
    tos_checkbox.click()
    time.sleep(1)

    print("Selecting gender...")
    male_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Male') or .//*[local-name()='svg']]"))
    )
    male_button.click()
    time.sleep(1)


    next_button = driver.find_element(By.XPATH, "//button[text()='NEXT']")
    next_button.click()
    time.sleep(2)

    print("Waiting for insurance details page...")

    insurance_section_visible = driver.execute_script(
        "return document.querySelector('.register-form.flex-col.flex-centered').classList.contains('visible');"
    )

    print("Filling insurance details...")
    insurance_company = driver.find_element(By.XPATH, "//label[text()='Insurance Company']/following-sibling::input")
    insurance_company.send_keys("HealthCare Inc.")
    time.sleep(1)

    insurance_id = driver.find_element(By.XPATH, "//label[text()='Insurance ID']/following-sibling::input")
    insurance_id.send_keys("12345")
    time.sleep(1)

    insurance_tier = driver.find_element(By.XPATH, "//label[text()='Insurance Tier']/following-sibling::input")
    insurance_tier.send_keys("Gold")
    time.sleep(1)

    next_button = driver.find_element(By.XPATH, "//input[@type='button' and @value='NEXT']")
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    next_button.click()
    time.sleep(2)

    print("Insurance details successfully submitted!")
    time.sleep(1)

    print("Filling initial questionnaire...")
    weight = driver.find_element(By.XPATH, "//label[text()='What is your current weight? (in pounds)']/following-sibling::input")
    weight.send_keys("100")
    time.sleep(1)

    height = driver.find_element(By.XPATH, "//label[text()='How tall are you? (in feet)']/following-sibling::input")
    height.send_keys("5.9")
    time.sleep(1)

    calories = driver.find_element(By.XPATH, "//label[text()='On average, how many calories do you consume per day? (in kcal)']/following-sibling::input")
    calories.send_keys("2500")
    time.sleep(1)

    water = driver.find_element(By.XPATH, "//label[text()='How many liters of water do you drink daily?']/following-sibling::input")
    water.send_keys("2")
    time.sleep(1)

    next_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='NEXT']")
    next_button.click()
    time.sleep(1)

    print("Filling final questionnaire...")
    exercise = driver.find_element(By.XPATH, "//label[text()='How many minutes do you exercise each day on average?']/following-sibling::input")
    exercise.send_keys("120")
    time.sleep(1)

    sleep = driver.find_element(By.XPATH, "//label[text()='How many hours of sleep do you get per night on average?']/following-sibling::input")
    sleep.send_keys("8")
    time.sleep(1)

    energy = driver.find_element(By.XPATH, "//label[text()='On a scale of 1 to 10, how would you rate your energy level this week?']/following-sibling::input")
    energy.send_keys("7")
    time.sleep(1)

    stress = driver.find_element(By.XPATH, "//label[text()='On a scale of 1 to 10, how would you rate your stress level this week?']/following-sibling::input")
    stress.send_keys("7")
    time.sleep(1)

    print("Submitting the registration form...")
    register_button = driver.find_element(By.XPATH, "//button[text()='REGISTER']")
    ActionChains(driver).move_to_element(register_button).click().perform()
    time.sleep(1)

    wait.until(EC.url_contains("/dashboard"))
    print("Patient registration test passed!")
    time.sleep(4)

except Exception as e:
    print(f"Test failed: {e}")

finally:
    driver.quit()
