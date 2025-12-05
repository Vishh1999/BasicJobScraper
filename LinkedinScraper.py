from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime, timedelta
import pandas as pd

def get_job_data(linkedin_job_link):
    driver = webdriver.Chrome()
    driver.get(linkedin_job_link)
    time.sleep(30)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    print("Data read from the net!!")
    important_data = soup.title.get_text()
    important_data_list = important_data.split(" ")
    company_name = important_data_list[0]
    start = important_data_list.index("hiring") + 1
    end = important_data_list.index("in")
    role = " ".join(important_data_list[start:end])
    city = important_data_list[end + 1]

    my_dict = {"company_name": company_name, "role": role, "city": city}
    print(my_dict)

    desc_div = soup.find("div", class_="description__text")
    if desc_div:
        job_description = desc_div.get_text(strip=True, separator="\n")
        my_dict["job_description"] = job_description
        print(job_description[:50])

    posted_span = soup.find("span", class_="posted-time-ago__text")
    if posted_span:
        posted_text = posted_span.get_text(strip=True)
        job_posted_on = (datetime.today() - timedelta(days=int(posted_text[0]))).strftime("%Y-%m-%d")
        my_dict["job_posted_on"] = job_posted_on
        print(job_posted_on)

    df = pd.DataFrame([my_dict])
    existing_df = pd.read_json('UK_jobs/UK_job_applications.json')
    new_df = pd.concat([existing_df, df])
    new_df.to_json("Jobs.json", orient="records", indent=2)
    print("Jobs saved to json!!")

linkedin_job_links = []
for linkedin_job_link in linkedin_job_links:
    get_job_data(linkedin_job_link)