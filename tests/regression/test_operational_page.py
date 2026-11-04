from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_operational_regression():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:3000/")
        wait = WebDriverWait(driver, 10)
        
        radar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        assert radar.is_displayed()
        
        markers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "marker")))
        assert len(markers) == 6
        
        # Select by href instead of exact nested text
        nav_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/intelligence')]")))
        assert nav_button.is_displayed()
    finally:
        driver.quit()