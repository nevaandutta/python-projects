# alibaba_scraper.py
# Requires: selenium, pandas, chromedriver_autoinstaller

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from datetime import datetime

# Auto-install chromedriver
chromedriver_autoinstaller.install()

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# URL
url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"
driver.get(url)
print("Page loaded. Waiting for RFQs to appear...")
time.sleep(10)

# Collect data
data = []

# Example: Scrape only first page for demonstration
rfqs = driver.find_elements(By.CSS_SELECTOR, ".rfq-item-container")
print(f"Found {len(rfqs)} RFQ items.")
for rfq in rfqs:
    try:
        title = rfq.find_element(By.CSS_SELECTOR, ".title-text").text.strip()
    except: title = ""
    try:
        description = rfq.find_element(By.CSS_SELECTOR, ".desc").text.strip()
    except: description = ""
    try:
        quantity = rfq.find_element(By.XPATH, ".//*[contains(text(),'Quantity Required')]/following-sibling::*").text.strip()
    except: quantity = ""
    try:
        country = rfq.find_element(By.CLASS_NAME, "country-flag").get_attribute("title")
    except: country = ""
    try:
        quotes_left = rfq.find_element(By.XPATH, ".//*[contains(text(),'Quotes Left')]/following-sibling::*").text.strip()
    except: quotes_left = ""
    try:
        inquiry_time = rfq.find_element(By.XPATH, ".//*[contains(text(),'Date Posted')]/following-sibling::*").text.strip()
    except: inquiry_time = ""
    try:
        buyer_name = rfq.find_element(By.CLASS_NAME, "name").text.strip()
    except: buyer_name = ""
    try:
        email_confirmed = "Yes" if "Email Confirmed" in rfq.text else "No"
    except: email_confirmed = "No"
    try:
        typical_replies = "Yes" if "Typically replies" in rfq.text else "No"
    except: typical_replies = "No"

    # Add row (simplified for demo)
    data.append({
        "RFQ ID": "",
        "Title": title,
        "Buyer Name": buyer_name,
        "Buyer Image": "",
        "Inquiry Time": inquiry_time,
        "Quotes Left": quotes_left,
        "Country": country,
        "Quantity Required": quantity,
        "Email Confirmed": email_confirmed,
        "Experienced Buyer": "No",
        "Complete Order via RFQ": "No",
        "Typical Replies": typical_replies,
        "Interactive User": "No",
        "Inquiry URL": "",
        "Inquiry Date": datetime.today().strftime("%d-%m-%Y"),
        "Scraping Date": datetime.today().strftime("%d-%m-%Y")
    })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("rfq_data.csv", index=False)

driver.quit()
print("Scraping complete. Data saved to rfq_data.csv")
