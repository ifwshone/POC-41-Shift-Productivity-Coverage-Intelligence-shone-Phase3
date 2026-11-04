from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_intelligence_journey():
    driver = webdriver.Chrome()
    
    # Increased wait time to 30s to allow Next.js dev server to compile on first load
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get("http://localhost:3000")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        
        # Wait for the link to exist in the DOM
        intel_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/intelligence')]")))
        
        # Force click via JavaScript to bypass any CSS overlay interferences
        driver.execute_script("arguments[0].click();", intel_link)
        
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Data Intelligence"))
        
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        filter_dropdown = driver.find_element(By.TAG_NAME, "select")
        filter_dropdown.click()
        filter_dropdown.find_element(By.XPATH, "//option[@value='low']").click()
        
        assert "n=5" in driver.page_source
        assert "Descriptive comparison on 5 days of synthetic data only" in driver.page_source
        
        back_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Back to Operational Map')]")
        driver.execute_script("arguments[0].click();", back_link)
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        
        print("E2E Journey: PASS")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_intelligence_journey()