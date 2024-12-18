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
    script = """
    var testMessage = document.createElement('div');
    testMessage.innerHTML = "<div>FEATURE #14: PATIENT CAN PAY INVOICES</div>";
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
    time.sleep(1)

    password_input = driver.find_element(By.CLASS_NAME, "password-input")
    password_input.send_keys("password123")
    time.sleep(1)

    password_toggle = driver.find_element(By.CLASS_NAME, "password-toggle-btn")
    ActionChains(driver).move_to_element(password_toggle).click().perform()
    time.sleep(1)

    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()
    time.sleep(1)

    wait.until(EC.url_contains("/dashboard"))
    print("Login successful!")
    time.sleep(1)

    print("Navigating to an invoice...")
    invoice_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'card-buttons') and contains(@value, 'Invoice')]"))
    )
    invoice_button.click()
    time.sleep(2)

    wait.until(EC.url_contains("/payment"))
    print("Redirected to the payment page.")
    time.sleep(2)

    print("Filling out the payment form...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 100  # Pixels to scroll each step
    scroll_pause_time = 0.1  # Time to wait between steps

    current_position = 0
    while current_position < last_height:
        current_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)

    card_number_input = wait.until(EC.presence_of_element_located((By.NAME, "cardNum")))
    card_number_input.send_keys("99999999")
    time.sleep(1)

    exp_month_input = driver.find_element(By.NAME, "month")
    exp_month_input.send_keys("12")
    time.sleep(1)

    exp_year_input = driver.find_element(By.NAME, "year")
    exp_year_input.send_keys("2025")
    time.sleep(1)

    cvc_input = driver.find_element(By.NAME, "cvc")
    cvc_input.send_keys("123")
    time.sleep(1)

    first_name_input = driver.find_element(By.NAME, "firstName")
    first_name_input.send_keys("John")
    time.sleep(1)

    last_name_input = driver.find_element(By.NAME, "lastName")
    last_name_input.send_keys("Smith")
    time.sleep(1)

    city_input = driver.find_element(By.NAME, "city")
    city_input.send_keys("New York")
    time.sleep(1)

    billing_address_input = driver.find_element(By.NAME, "billingAddress")
    billing_address_input.send_keys("123 Main St")
    time.sleep(1)

    state_input = driver.find_element(By.NAME, "state")
    state_input.send_keys("NY")
    time.sleep(1)

    country_input = driver.find_element(By.NAME, "country")
    country_input.send_keys("USA")
    time.sleep(1)

    zip_input = driver.find_element(By.NAME, "zip")
    zip_input.send_keys("10001")
    time.sleep(1)

    phone_input = driver.find_element(By.NAME, "phone")
    phone_input.send_keys("5551234567")
    time.sleep(1)

    save_payment_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
    save_payment_checkbox.click()

    print("Submitting the payment form...")
    submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
    submit_button.click()

    print("Verifying payment success notification...")
    toast_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast--success")))
    assert "Payment Successful" in toast_message.text, f"Unexpected toast message: {toast_message.text}"
    print("Payment test passed!")
    time.sleep(3)

except Exception as e:
    print(f"Test failed: {e}")

finally:
    driver.quit()
