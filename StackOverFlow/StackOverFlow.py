import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Edge(executable_path="D:\EdgeDrive\edgedriver_win64\msedgedriver.exe")

driver.get("https://stackoverflow.com/questions")

list_job_title = []
list_job_skill = []


for x in range(2):
    job_title = driver.find_elements(By.CSS_SELECTOR, '.s-post-summary--content-title')
    job_bottom = driver.find_elements(By.CSS_SELECTOR, '.s-post-summary--meta')
    for title in job_title:
        # print(title.text)
        list_job_title.append(title.text)
    for name in job_bottom:
        # tag_list = name.find_elements(By.CSS_SELECTOR, '.d-inline mr4 js-post-tag-list-item')
        # tag_list = name.find_elements(By.XPATH, "//li[@class='d-inline mr4 js-post-tag-list-item']/a")
        div_ref = name.find_elements(By.TAG_NAME, "li")
        list_new = []
        for skill in div_ref:
            a_ref = skill.find_elements(By.TAG_NAME, "a")
            for ref in a_ref:
                list_new.append(ref.text)
        list_job_skill.append(list_new)

    # Đợi load page rồi next page
    time.sleep(1)

    # Bắt sự kiện click next page
    job_pagination = driver.find_element(By.XPATH, "//div[@class='s-pagination site1 themed pager float-left']/a[last()]")
    if job_pagination.get_attribute('href') is None:
        break
    print(job_pagination.get_attribute('href'))
    driver.get(job_pagination.get_attribute('href'))

df = pd.DataFrame({'JobTitle': list_job_title, 'Require': list_job_skill})
df['Require'] = df.Require.apply(lambda x: ','.join([str(i) for i in x]))

df.to_csv(r'D:\0.University\5. NCKK\5.MXH\Project\CrawlData\CrawlData_Project\StackOverFlow\StackOverFlow_Job_Data_Raw_Test.csv', header=True, encoding="utf-8-sig")
driver.quit()


# df_stackoverflow = pd.read_csv('./StackOverFlow_Job_Data_Raw_Test.csv',encoding='utf-8')
# df_
# print(df_stackoverflow)


skill_list = []
# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Check if the value in 'Require' column is a string
    if isinstance(row['Require'], str):
        # Split the values in the 'Require' column by comma
        skills = row['Require'].split(',')

        # Append the split values to the skill_list
        skill_list.extend(skills)

df_new = pd.DataFrame()  # create an empty DataFrame
df_new['skill'] = skill_list  # add array1 as a new column called 'column1'
df_new['skill'].drop_duplicates(inplace=True)
new_df = df_new['skill'].drop_duplicates()

#Lấy file node của roadmap
df_node_roadmap = pd.read_csv('./nodes_all_skill.csv',encoding='utf-8')
# Find common values
common_values = pd.Series(list(set(new_df).intersection(df_node_roadmap['name'])))
df_C = pd.DataFrame({'list_tag': common_values})
# Convert the 'list_tag' DataFrame to a list
list_tag_values = list(df_C.iloc[:, 0])

# Filter the 'Require' column based on values in 'list_tag'
df['Filter'] = df['Require'].apply(lambda x: ",".join(tag for tag in str(x).split(",") if tag in list_tag_values))
df_filtered = df[df['Filter'].apply(lambda x: len(str(x).split(',')) > 1)]

# Reset the index of the filtered DataFrame
df_filtered = df_filtered.reset_index(drop=True)

filter_list = []

# Iterate over each row in the DataFrame
for index, row in df_filtered.iterrows():
    # Split the values in the 'Require' column by comma
    skills = row['Filter'].split(',')

    # Append the split values to the skill_list
    filter_list.extend(skills)

df_filter_new = pd.DataFrame()  # create an empty DataFrame
df_filter_new['skill'] = filter_list  # add array1 as a new column called 'column1'
df_filter_new['skill'].drop_duplicates(inplace=True)
new_filter_df= df_filter_new['skill'].drop_duplicates()
####
common_values = pd.Series(list(set(new_filter_df).intersection(df_C['list_tag'])))
df_E = pd.DataFrame({'name': common_values})
# Find values in A not in C
df_E.to_csv('./StackOverFlow_Node_v3.csv', index=False)
# Convert the 'list_tag' DataFrame to a list
list_tag_filter = list(df_E.iloc[:, 0])
# Filter the 'Require' column based on values in 'list_tag'
# df_filtered = df_stackoverflow[df_stackoverflow['Require'].apply(lambda x: any(tag in x for tag in list_tag_values))]
df_filtered['Filter new'] = df_filtered['Filter'].apply(lambda x: ",".join(tag for tag in x.split(",") if tag in list_tag_values))
# Split the values in the "Filter" column and create List A and List B
target = []
source = []
for tags in df_filtered['Filter'].str.split(','):
  for i, item in enumerate(tags):
    target += [item] * (len(tags) - i - 1)

  for i in range(len(tags)):
      source += [tags[j] for j in range(i + 1, len(tags))]
df_new = pd.DataFrame()  # create an empty DataFrame
df_new['source'] = source  # add array1 as a new column called 'column1'
df_new['target'] = target  # add array2 as a new column called 'column2'
# Check duplicate in the same index at 2 column
df_final = df_new.drop(df_new[df_new['source'] == df_new['target']].index)
df_final.to_csv('./Egdes_Stack_v3.csv', index=False)

#########################################################
# df_node_old= pd.read_csv('./link_node_stack_v2.csv',encoding='utf-8')
# df_edge_old= pd.read_csv('./link_edges_stack_v2.csv.csv',encoding='utf-8')
#
# df_node_new= pd.read_csv('./StackOverFlow_Node_v3.csv.csv',encoding='utf-8')
# df_edge_new= pd.read_csv('./Egdes_Stack_v3.csv.csv.csv',encoding='utf-8')