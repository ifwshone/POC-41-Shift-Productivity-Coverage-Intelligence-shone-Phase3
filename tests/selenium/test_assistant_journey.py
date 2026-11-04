import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_assistant_panel_integration():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get("http://localhost:3000/intelligence")
        
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ask Assistant')]")))
        btn.click()
        
        panel = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Data Assistant')]")))
        assert panel.is_displayed()
        
        suggested = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Which group ranks highest')]")))
        suggested.click()
        
        # Verify limitation warning is preserved in the response (our custom component has no colon)
        limitation = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Limitation')]")))
        assert limitation.is_displayed()
        
    finally:
        driver.quit()