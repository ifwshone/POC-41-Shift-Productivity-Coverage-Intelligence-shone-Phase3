import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_unsupported_state_renders():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get("http://localhost:3000/intelligence")
        
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ask Assistant')]")))
        btn.click()
        
        # Wait a moment for the sidebar animation to complete
        time.sleep(1)
        
        # Locate input and send text that is out of scope but NOT a blocked security term
        input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Ask about shift performance...']")))
        input_field.clear()
        input_field.send_keys("What is the weather tomorrow?")
        
        # Explicitly locate and click the Ask button
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Ask']")))
        submit_btn.click()
        
        # Verify Out of Scope boundary renders
        out_of_scope_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Out of Scope']")))
        assert out_of_scope_header.is_displayed()
        
    finally:
        driver.quit()