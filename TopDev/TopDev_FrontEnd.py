import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Edge(executable_path="D:\EdgeDrive\edgedriver_win64\msedgedriver.exe")
driver.get("https://topdev.vn/viec-lam-it")

list_job_title = []
list_job_skill = []
list_link_job = []


last_height = driver.execute_script("return document.body.scrollHeight")

for x in range(110):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

div_path = driver.find_elements(By.XPATH, "//*[@id='scroll-it-jobs']")
for Path_ in div_path:
    jobtitle = Path_.find_element(By.TAG_NAME, "h3").text
    jobtitle_link = Path_.find_element(By.TAG_NAME, "h3")
    div_ref = Path_.find_elements(By.TAG_NAME, "div").__getitem__(6)
    a_ref = div_ref.find_elements(By.TAG_NAME, "a")
    link_job = Path_.find_element(By.TAG_NAME, "a").get_attribute('href')
    # jobtitle_link.click()
        # driver.get(link_job)

    ##############################################################
    # Tên Công việc
    list_job_title.append(jobtitle.strip())
    # Yêu cầu
    list_new = []
    for ref in a_ref:
        list_new.append(ref.text)
    list_job_skill.append(list_new)
    # Thông tin thêm
    list_link_job.append(link_job.strip())

df = pd.DataFrame({'JobTitle': list_job_title, 'Require': list_job_skill, 'Link': list_link_job})
df['Require'] = df.Require.apply(lambda x: ','.join([str(i) for i in x]))

print(df)
df.to_csv(r'D:\0.University\5. NCKK\5.MXH\Project\CrawlData\CrawlData_Project\Results\TopDev_Job_Data_Raw.csv', header=True, encoding="utf-8-sig")
driver.quit()