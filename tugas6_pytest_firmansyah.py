from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture
def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')

    yield driver
    driver.quit()


def test_login_positive(setup):
    setup.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys('Admin')
    setup.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys('admin123')
    setup.find_element(By.XPATH, "//button[normalize-space()='Login']").click()

    dashboard_title = WebDriverWait(setup, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']"))
    ).text

    # Assertion
    assert dashboard_title == 'Dashboard'

error_sample = [
    ('', 'admin123', 'Requiredd'),
    ('Admin', '', 'Required'),
    ('Admin', 'admin1234', 'Invalid credentials'),
    ('Adminn', 'admin123', 'Invalid credentials')
]

@pytest.mark.parametrize('username,password,error_message', error_sample)
def test_login_negative(setup, username, password, error_message):
    setup.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys(username)
    setup.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(password)
    setup.find_element(By.XPATH, "//button[normalize-space()='Login']").click()

    try:
        error_message_xpath = "//span[contains(@class, 'oxd-input-field-error-message')]"
        error_text = WebDriverWait(setup, 15).until(
            EC.visibility_of_element_located((By.XPATH, error_message_xpath))
        ).text
    except:
        error_message_xpath = "//div[@class='oxd-alert-content oxd-alert-content--error']"
        error_text = WebDriverWait(setup, 15).until(
            EC.visibility_of_element_located((By.XPATH, error_message_xpath))
        ).text

    # Assertion
    assert error_text == error_message
