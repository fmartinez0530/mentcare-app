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
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 15)

    script = """
    var testMessage = document.createElement('div');
    testMessage.innerText = "FEATURE #4: SEARCH THERAPIST AND ADD/REMOVE THERAPIST (Linda White)";
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
    time.sleep(1)
    
    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(1)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    wait.until(EC.url_contains("/dashboard"))
    print("Login successful, now on the dashboard.")
    time.sleep(1) 

    driver.get("http://localhost:3000/therapistlist") 
    time.sleep(1)

    gender_btn_1 = driver.find_element(By.XPATH, "//label[text()='Female']")
    gender_btn_1.click()
    time.sleep(2)

    gender_btn_2 = driver.find_element(By.XPATH, "//label[text()='Male']")
    gender_btn_2.click()
    time.sleep(2)

    gender_btn_3 = driver.find_element(By.XPATH, "//label[text()='Other']")
    gender_btn_3.click()
    time.sleep(2)

    gender_btn_1.click()
    gender_btn_2.click()
    gender_btn_3.click()
    time.sleep(1)

    dropdown = wait.until(EC.presence_of_element_located((By.ID, "sort-dropdown")))
    dropdown.click()
    time.sleep(1)

    first_option = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='sort-dropdown']/option[2]")))
    first_option.click()
    time.sleep(1)

    search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-therapists-input")))
    search_input.send_keys("Linda")
    time.sleep(3)

    buttons = driver.find_elements(By.XPATH, "//button[text()='View Profile']")
    visible_button = None
    for button in buttons:
        if button.is_displayed():
            visible_button = button
            break
    visible_button.click()
    time.sleep(1)

    wait.until(EC.url_contains("/therapistProfile"))
    time.sleep(3)

    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
    time.sleep(1)

    driver.get("http://localhost:3000/dashboard")
    wait.until(EC.url_contains("/dashboard"))
    time.sleep(5)

    driver.get("http://localhost:3000/therapistlist")
    wait.until(EC.url_contains("/therapistlist"))
    time.sleep(5)
    
    search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-therapists-input")))
    search_input.send_keys("James")
    time.sleep(3)

    buttons = driver.find_elements(By.XPATH, "//button[text()='View Profile']")
    visible_button = None
    for button in buttons:
        if button.is_displayed():
            visible_button = button
            break
    visible_button.click()
    time.sleep(1)

    wait.until(EC.url_contains("/therapistProfile"))
    time.sleep(3)


    actions.send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
    time.sleep(1)

    driver.get("http://localhost:3000/dashboard")
    wait.until(EC.url_contains("/dashboard"))
    time.sleep(5)

finally:
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while quitting the driver: {e}")
    print("Program ended.")
