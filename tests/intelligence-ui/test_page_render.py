from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_intelligence_page_components():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:3000/intelligence")
        wait = WebDriverWait(driver, 10)
        
        header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Data Intelligence" in header.text
        
        # Wait for data to load by ensuring the table renders
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Track" in body_text
        assert "v1.0.0" in body_text
        
        assert table.is_displayed()
        assert "OUTPUT GAP" in table.text.upper()
        
        # Use upper() to bypass Tailwind's text-transform rendering differences
        assert "LIMITATIONS" in body_text.upper()
    finally:
        driver.quit()