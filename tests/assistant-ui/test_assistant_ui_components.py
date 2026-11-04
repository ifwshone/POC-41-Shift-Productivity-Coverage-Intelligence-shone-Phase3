import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        
        time.sleep(1)
        
        # 'space exploration' does not match any keywords in intent_classifier.py
        input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Ask about shift performance...']")))
        input_field.clear()
        input_field.send_keys("Tell me about space exploration")
        
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Ask']")))
        submit_btn.click()
        
        # Wait for the Out of Scope boundary to render
        out_of_scope_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Out of Scope']")))
        assert out_of_scope_header.is_displayed()
        
    finally:
        driver.quit()