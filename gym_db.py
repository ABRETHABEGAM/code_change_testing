import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------
# Setup: WebDriver Fixture
# -----------------------------
@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress Chrome warnings
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

# -----------------------------
# Preload Page Before Tests
# -----------------------------
@pytest.fixture(scope="module", autouse=True)
def load_page(driver):
    driver.get("https://gym-front-end.vercel.app/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)

# -----------------------------
# Test 1: Header Text Validation
# -----------------------------
def test_check_header(driver):
    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'h1.m-0.display-4.text-success.text-uppercase[style*="font-style: italic"]')
        )
    )
    assert "&KICK START" in header.text.upper()
    time.sleep(1)

# -----------------------------
# Test 2: Navigation Tabs Check
# -----------------------------
def test_check_tabs(driver):
    expected = {"HOME", "REGISTER", "LOGIN", "ABOUT", "CONTACT"}
    tabs = {tab.text.strip().upper() for tab in WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'nav a.nav-link, ul.nav-tabs li a'))
    )}
    for tab in expected:
        assert tab in tabs, f"{tab} tab is missing"
    time.sleep(1)

# -----------------------------
# Test 3: "JOIN US" Text Check
# -----------------------------
def test_check_join_us_text(driver):
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//*[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'JOIN US')]")
        )
    )
    assert elements, "'JOIN US' text not found"

# -----------------------------
# Test 4: Social Media Links
# -----------------------------
def test_check_social_media(driver):
    selectors = [
        'a[href*="facebook.com"]', 'a[href*="twitter.com"]',
        'a[href*="instagram.com"]', 'a[href*="linkedin.com"]',
        'a[href*="youtube.com"]', '.social-icon'
    ]
    for sel in selectors:
        if driver.find_elements(By.CSS_SELECTOR, sel):
            return  # Found at least one social media link
    pytest.fail("No social media links found")

# -----------------------------
# Test 5: Welcome to KICK START Text
# -----------------------------
def test_check_welcome_text(driver):
    els = driver.find_elements(By.XPATH, "//*[contains(text(),'Welcome to KICK START')]")
    assert els, "'Welcome to KICK START' text not found"
    time.sleep(1)

# -----------------------------
# Test 6: Pill Tabs: About / Why Choose Us
# -----------------------------
def test_check_pills_nav_links(driver):
    assert "ABOUT US" in driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="#pills-1"]').text.upper()
    assert "WHY CHOOSE US" in driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="#pills-2"]').text.upper()
    time.sleep(1)
