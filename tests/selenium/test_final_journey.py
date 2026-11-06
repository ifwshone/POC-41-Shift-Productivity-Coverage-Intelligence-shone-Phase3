"""Phase 3 Post #6 - Final Selenium journey (guide section 20).

Runs against ANY deployment: set BASE_URL (default http://localhost:3000).
    BASE_URL=https://<live-url> python -m pytest tests/selenium/test_final_journey.py -v
"""
import json
import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000").rstrip("/")
EVID = ROOT / "final-evidence"
SHOTS = EVID / "14-screenshots"
LOGDIR = EVID / "11-selenium"
SUMMARY = json.loads((ROOT / "data-science/outputs/intelligence_summary.json").read_text("utf-8"))
MANIFEST = json.loads((ROOT / "data/manifest.json").read_text("utf-8"))

LOG = []


def log(step, status, detail=""):
    LOG.append({"step": step, "status": status, "detail": detail, "t": time.strftime("%Y-%m-%dT%H:%M:%S")})


def make_driver(width, height):
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--no-sandbox")
    
    if width < 500:
        # Proper mobile emulation bypasses the Windows minimum window width limit
        mobile_emulation = {
            "deviceMetrics": { "width": width, "height": height, "pixelRatio": 1.0 },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }
        o.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        o.add_argument(f"--window-size={width},{height}")
        
    return webdriver.Chrome(options=o)


def shot(driver, name):
    SHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SHOTS / f"{name}.png"))


@pytest.fixture(scope="module", autouse=True)
def write_log_at_end():
    yield
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / "final_selenium_log.json").write_text(
        json.dumps({"base_url": BASE_URL, "steps": LOG}, indent=2) + "\n", "utf-8")


def test_final_journey_desktop():
    d = make_driver(1440, 900)
    w = WebDriverWait(d, 30)
    try:
        d.get(BASE_URL + "/")
        w.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        log("1-2 open operational view", "PASS", d.current_url)

        markers = w.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "marker")))
        assert len(markers) == 6
        shot(d, "desktop_01_operational")
        log("3 primary visual", "PASS", "6 markers")

        fb = w.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Facility B overview')]")))
        d.execute_script("arguments[0].click();", fb)
        w.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Facility B')]")))
        shot(d, "desktop_02_operational_interaction")
        log("4 operational interaction", "PASS")

        link = w.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/intelligence')]")))
        d.execute_script("arguments[0].click();", link)
        w.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Data Intelligence"))
        w.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        log("5 navigate to Data Intelligence", "PASS")

        body = d.find_element(By.TAG_NAME, "body").text
        assert f"v{SUMMARY['data_version']}" in body and f"v{SUMMARY['method_version']}" in body
        assert SUMMARY["data_version"] == MANIFEST["data_version"]
        assert "Track" in body
        shot(d, "desktop_03_intelligence")
        log("6 track and versions", "PASS", f"data v{SUMMARY['data_version']} method v{SUMMARY['method_version']}")

        sel = Select(d.find_element(By.TAG_NAME, "select"))
        sel.select_by_value("low")
        rows_low = len(d.find_elements(By.CSS_SELECTOR, "tbody tr"))
        sel.select_by_value("high")
        rows_high = len(d.find_elements(By.CSS_SELECTOR, "tbody tr"))
        assert rows_low + rows_high == SUMMARY["result_count"]
        sel.select_by_value("All")
        assert len(d.find_elements(By.CSS_SELECTOR, "tbody tr")) == SUMMARY["result_count"]
        log("7 filter", "PASS", f"low={rows_low} high={rows_high}")

        first = d.find_element(By.CSS_SELECTOR, "tbody tr")
        assert "n=" in first.text
        log("8 result + evidence", "PASS", first.text.replace("\n", " ")[:120])

        page = d.find_element(By.TAG_NAME, "body").text.upper()
        assert "METHODOLOGY" in page and "LIMITATIONS" in page
        for lim in SUMMARY["important_limitations"]:
            assert lim in d.page_source, f"limitation not visible: {lim}"
        log("9 methodology and limitations", "PASS")

        d.find_element(By.XPATH, "//button[contains(text(), 'Ask Assistant')]").click()
        w.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Data Assistant')]")))
        s = w.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Which group ranks highest')]")))
        s.click()
        w.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Limitation')]")))
        shot(d, "desktop_04_assistant")
        log("10 assistant answer with limitation", "PASS")

        d.get(BASE_URL + "/intelligence")
        back = w.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Back to Operational Map')]")))
        d.execute_script("arguments[0].click();", back)
        w.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        fb = w.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Facility B overview')]")))
        d.execute_script("arguments[0].click();", fb)
        w.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Facility B')]")))
        shot(d, "desktop_05_operational_after_return")
        log("11-12 return and re-verify interaction", "PASS")
    except Exception as e:
        log("FAILED", "FAIL", repr(e))
        shot(d, "desktop_FAILURE")
        raise
    finally:
        d.quit()


def test_final_journey_mobile():
    d = make_driver(390, 844)
    w = WebDriverWait(d, 30)
    try:
        d.get(BASE_URL + "/")
        w.until(EC.presence_of_element_located((By.CLASS_NAME, "radar")))
        shot(d, "mobile_01_operational")
        d.get(BASE_URL + "/intelligence")
        w.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        width = d.execute_script("return document.documentElement.scrollWidth")
        offenders = d.execute_script("""
              return Array.from(document.querySelectorAll('*'))
                .filter(el => el.getBoundingClientRect().right > 390)
                .map(el => {
                  var cn = (typeof el.className === 'string') ? el.className : (el.className.baseVal || '');
                  return el.tagName + ' ' + cn.substring(0, 80) + ' right=' + Math.round(el.getBoundingClientRect().right);
                });
            """)
        print("OFFENDING ELEMENTS:")
        for o in offenders:
                print(" ", o)
                
        # With proper emulation, this will now successfully be 390
        assert width <= 390 + 2, f"page scrolls horizontally on mobile (scrollWidth={width})"

        shot(d, "mobile_02_intelligence")
        log("mobile", "PASS", f"scrollWidth={width}")
    except Exception as e:
        log("MOBILE FAILED", "FAIL", repr(e))
        shot(d, "mobile_FAILURE")
        raise
    finally:
        d.quit()