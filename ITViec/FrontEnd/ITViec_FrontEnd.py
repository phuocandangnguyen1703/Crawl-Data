# Import thư viện
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Setup EdgeDriver version=112.0.1722.64 và get URL
browser = webdriver.Edge(executable_path="D:\EdgeDrive\edgedriver_win64\msedgedriver.exe")
browser.get("https://itviec.com/viec-lam-it/frontend?search_by_skill=true")

time.sleep(5)
# Khai báo mảng lưu trữ thông tin
list_job_title = []
list_job_skill = []

for i in range(10):
    job_title = browser.find_elements(By.CSS_SELECTOR, '.title.job-details-link-wrapper')
    job_bottom = browser.find_elements(By.CSS_SELECTOR, '.job-bottom>.tag-list')
    for title in job_title:
        # print(title.text)
        list_job_title.append(title.text)

    for name in job_bottom:
        tag_list = name.find_elements(By.CSS_SELECTOR, '.job__skill.ilabel.mkt-track')
        # print(len(tag_list))
        skills = ""
        for item in tag_list:
            skills += item.text + ","
        # print(skills[:-1])
        list_job_skill.append(skills[:-1])

    # Đợi load page rồi next page
    time.sleep(2)

    # Bắt sự kiện click next page
    job_pagination = browser.find_element(By.XPATH, "//div[@class='search-page__jobs-pagination']/ul/li[last()]/a")
    if job_pagination.get_attribute('href') is None:
        break
    # job_pagination.click()
    print(job_pagination.get_attribute('href'))
    browser.get(job_pagination.get_attribute('href'))

df = pd.DataFrame({'JobTitle': list_job_title, 'Require': list_job_skill})

print(df)
df.to_csv(r'D:\0.University\5. NCKK\5.MXH\Project\CrawlData\CrawlData_Project\Results\ITViet_Fresher_FrontEnd_Master.csv', header=True, encoding="utf-8-sig")



