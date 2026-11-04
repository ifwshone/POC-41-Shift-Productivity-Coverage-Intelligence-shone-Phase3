import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_operational_map_remains_intact():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("http://localhost:3000/")
        radar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        assert radar.is_displayed()
        
        markers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "marker")))
        assert len(markers) == 6
        
        facility_b = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Facility B overview')]")))
        driver.execute_script("arguments[0].click();", facility_b)
        
        # Use visibility_of_element_located to wait for the CSS animation to finish
        sidebar_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Facility B')]")))
        assert sidebar_title.is_displayed()
        
    finally:
        driver.quit()

def test_intelligence_table_remains_intact():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("http://localhost:3000/intelligence")
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        assert table.is_displayed()
        
        filter_dropdown = driver.find_element(By.TAG_NAME, "select")
        filter_dropdown.click()
        filter_dropdown.find_element(By.XPATH, "//option[@value='high']").click()
        
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "facility_a_morning_crew" in body_text
    finally:
        driver.quit()