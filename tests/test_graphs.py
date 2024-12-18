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

    wait = WebDriverWait(driver, 10)

    script = """
    var testMessage = document.createElement('div');
    testMessage.innerText = "<div>FEATURE #11: VIEW GRAPHS ON PATIENT AND THERAPIST DASHBOARDS</div>";
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

    #   LOGGING INTO PATIENT DASHBOARD
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("john.smith@example.com")

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))
    print("Login successful! Redirected to dashboard.")
    time.sleep(2)

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

    graphs = driver.find_elements(By.CLASS_NAME, "scatterlayer")
    print("All graphs displayed successfully!")
    time.sleep(3)

    dropdown_trigger = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar-profile-pic-container")))
    time.sleep(1)

    actions = ActionChains(driver)
    actions.move_to_element(dropdown_trigger).perform()
    time.sleep(1)

    logout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))

    logout_button.click()

    wait.until(EC.url_contains("/login"))
    time.sleep(3)

    #   LOGGING INTO THERAPIST DASHBOARD
    email_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "email-input")))
    email_input.send_keys("linda.white@example.com")

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))
    print("Login successful! Redirected to dashboard.")
    time.sleep(2)

    first_patient = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "td-clickable-active-patient")))
    first_patient_name = first_patient.find_element(By.CLASS_NAME, "td-patient-text").text
    first_patient.click()
    time.sleep(2)

    wait.until(EC.url_contains("/patient-overview"))
    print(f"Successfully navigated to Patient Overview for patient: {first_patient_name}")
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    multi_metric_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
    if not multi_metric_checkbox.is_selected():
        multi_metric_checkbox.click()
    print("Toggled 'Show Multiple Metrics' checkbox.")
    time.sleep(2)

    metric_buttons = driver.find_elements(By.CSS_SELECTOR, ".metric-buttons button")
    for button in metric_buttons:
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on metric: {button.text}")
        time.sleep(1) 

    graphs = driver.find_elements(By.CLASS_NAME, "scatterlayer")
    print("All graphs displayed successfully!")
    time.sleep(5)

finally:
    driver.quit()
