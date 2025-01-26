from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
from sklearn.ensemble import IsolationForest

service = Service("/Users/abhaybansal/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service)

def test_page(url):
    driver.get(url)
    time.sleep(2)

    load_time = driver.execute_script("return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;")

    try:
        button = driver.find_element(By.ID, "submit-button")
        button_present = True
    except:
        button_present = False
    
    return load_time, button_present

# Automated form testing (e.g., fill in a search form)
def test_form_submission():
    try:
        # Use WebDriverWait to wait for the search box to appear
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        search_box.send_keys("Selenium testing")  # Fill out form
        search_box.send_keys(Keys.RETURN)  # Submit form
        time.sleep(2)
        return "Form submitted successfully"
    except Exception as e:
        return f"Form submission failed: {e}"

# Test multiple pages and store load times
urls = ["https://atomcreations.co/login"]  # Add the URLs you want to test
load_times = []
button_status = []

for url in urls:
    load_time, button_present = test_page(url)
    load_times.append(load_time)
    button_status.append(button_present)
    print(f"Page {url} loaded in {load_time} ms")
    print(f"Button present: {button_present}")
    
    # Additional feature: Test form submission
    form_status = test_form_submission()
    print(form_status)

# Anomaly detection using Isolation Forest (AI Model)
X = np.array(load_times).reshape(-1, 1)

# Train an anomaly detection model
model = IsolationForest(contamination=0.1)
model.fit(X)

# Predict anomalies (outliers)
predictions = model.predict(X)
for idx, prediction in enumerate(predictions):
    if prediction == -1:
        print(f"Anomaly detected on page {urls[idx]} with load time {load_times[idx]} ms")
    else:
        print(f"Page {urls[idx]} is normal with load time {load_times[idx]} ms")

# Close the browser
driver.quit()
