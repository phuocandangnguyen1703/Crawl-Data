import pandas as pd
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

df = pd.read_csv('TopDev_Job_Data_Raw.csv')
driver = webdriver.Edge(executable_path="D:\EdgeDrive\edgedriver_win64\msedgedriver.exe")
list_job_year = []
list_job_rank = []

for index, row in df.iterrows():
    link_value = row['Link']
    time.sleep(2)
    try:
        driver.get(link_value)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Số năm kinh nghiệm tối thiểu')]")))
        print(f"Link value for row {index} is {link_value}")
    except TimeoutException:
        print(f"Timed out loading link value for row {index}")
        list_job_year.append('N/A')
        list_job_rank.append('N/A')
        continue
    time.sleep(1)

    #Số năm kinh nghiệm
    try:
        header_year_element = driver.find_element_by_xpath("//h3[contains(text(), 'Số năm kinh nghiệm tối thiểu')]")
        year_element = header_year_element.find_element_by_xpath(".//following-sibling::div//span").text
        list_job_year.append(year_element)
        print(year_element)
    except NoSuchElementException:
        list_job_year.append('N/A')
        print('Year not found')

    #Cấp bậc
    try:
        header_rank_element = driver.find_element_by_xpath("//h3[contains(text(), 'Cấp bậc')]")
        rank_element = header_rank_element.find_elements_by_xpath(".//following-sibling::div//span")
        list_new = []
        for ref in rank_element:
            list_new.append(ref.text)
        list_job_rank.append(list_new)
        print(list_new)
    except NoSuchElementException:
        list_job_rank.append('N/A')
        print('Rank not found')

driver.quit()

df['Year'] = list_job_year
df['Rank'] = list_job_rank
df['Rank'] = df.Rank.apply(lambda x: ','.join([str(i) for i in x]))
print(df)
df.info()
df.to_csv(r'D:\0.University\5. NCKK\5.MXH\Project\CrawlData\CrawlData_Project\Results\TopDev_Job_Data_Done.csv', header=True, encoding="utf-8-sig")





