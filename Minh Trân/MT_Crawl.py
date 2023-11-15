# Import thư viện
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Setup EdgeDriver version=112.0.1722.64 và get URL
browser = webdriver.Edge(executable_path="D:\EdgeDrive\edgedriver_win64\msedgedriver.exe")
browser.get("http://nicd.co.jp/?fbclid=IwAR3mncaClX5_gG992XHNIWWGmc4amzKHhJAQyZcNubyyIi0tvw2kurXjwhE")
list_title = []
list_href = []
time.sleep(5)
# Find all elements with class 'vlightbox1'
titles = browser.find_elements(By.CSS_SELECTOR, '.vlightbox1')

for i, title in enumerate(titles):
    # Get the 'href' attribute of the 'a' tag inside each element
    href = title.get_attribute('href')
    print(title.text)
    print(href)
    list_title.append(title.text)
    list_href.append(href)

# Close the browser
browser.quit()
df = pd.DataFrame({'Tiêu đề': list_title, 'Link': list_href})

print(df)
df.to_csv(r'D:\0.University\5. NCKK\5.MXH\Project\CrawlData\CrawlData_Project\Results\MinhTran.csv', header=True, encoding="utf-8")



# df.to_csv(r'D:\0.University\5. NCKK\5.MXH\Project\CrawlData\CrawlData_Project\Results\ITViet_Fresher_BacktEnd_Manager.csv', header=True, encoding="utf-8-sig")



