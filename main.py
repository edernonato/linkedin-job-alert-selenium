import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import smtplib

URL = "https://www.linkedin.com/"
LINKED_IN_USER = "edernonato47teste@hotmail.com"
LINKED_IN_PASSWORD = "Eder@teste321"

EMAIL_FROM = "edernonato47teste@hotmail.com"
PASSWORD = "Eder@teste321"
SMTP = "smtp-mail.outlook.com"
PORT = 587

connection = smtplib.SMTP(SMTP, PORT)
connection.starttls()
connection.login(user=EMAIL_FROM, password=PASSWORD)
EMAIL_TO = "edernonato@outlook.com"

data_scrapped = False
available_jobs = None
html_body = ""
driver = None
while not data_scrapped:
    try:
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        driver.get(URL)
        driver.maximize_window()

        user_field = driver.find_element(By.CSS_SELECTOR, "#session_key")
        password_field = driver.find_element(By.CSS_SELECTOR, "#session_password")
        sign_in_button = driver.find_element(By.CSS_SELECTOR, ".sign-in-form__submit-button")

        user_field.send_keys(LINKED_IN_USER)
        password_field.send_keys(LINKED_IN_PASSWORD)
        sign_in_button.click()
        driver.implicitly_wait(5)

        search_box = driver.find_element(By.CSS_SELECTOR, ".search-global-typeahead__input")
        search_box.send_keys("Python")
        search_box.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)

        filter_button = driver.find_element(By.CSS_SELECTOR, ".search-reusables__filters-bar-grouping div button")
        filter_button.click()
        driver.implicitly_wait(3)

        easy_apply_filter = driver.find_element(By.NAME, "easy-apply-filter-value")
        easy_apply_filter.send_keys(Keys.ENTER)
        easy_apply_filter.send_keys(Keys.SPACE)
        driver.implicitly_wait(5)

        finish_filter_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__actionbar .reusable-search-filters-buttons")
        finish_filter_button.click()
        driver.implicitly_wait(10)

        available_jobs = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
        for jobIndex in range(len(available_jobs)):
            img = available_jobs[jobIndex].find_element(By.CSS_SELECTOR, ".job-card-list img").get_attribute("src")
            job_title = available_jobs[jobIndex].find_element(By.CSS_SELECTOR, ".job-card-list__title").text
            company_name = available_jobs[jobIndex].find_element(By.CSS_SELECTOR,
                                                                 ".job-card-container__company-name").text
            city = available_jobs[jobIndex].find_element(By.CSS_SELECTOR, ".job-card-container__metadata-item").text
            job_link = available_jobs[jobIndex].find_element(By.CSS_SELECTOR, ".job-card-list__title").get_attribute(
                "href")
            html_body += f"""
                        <img src="{img}">
                        <a href="{job_link}" style="text-decoration:none; color: #11999E;"><h4>{job_title}</h4><a>
                        <h5>{company_name}</h5>
                        <h5>{city}</h5>
            """
        data_scrapped = True
    except Exception as exp:
        driver.close()
        print(exp)
        time.sleep(5)


html_start = """
<html>
    <head>
    <title>New Python Jobs</title>
    </head>
        <body>
"""

html_end = """
        </body>
</html>
"""

html = html_start + html_body + html_end

email_message = MIMEMultipart()
email_message["from"] = EMAIL_FROM
email_message["to"] = EMAIL_TO
email_message["subject"] = f"New Python Jobs at LinkedIN"
email_message.attach(MIMEText(html, "html"))
connection.sendmail(from_addr=EMAIL_FROM, to_addrs=EMAIL_TO, msg=email_message.as_string())
print(html)