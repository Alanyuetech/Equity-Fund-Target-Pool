from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# 启动浏览器
driver = webdriver.Chrome()

# 导航到页面
page_n=1
driver.get("https://etfdb.com/screener/#page={}&tab=overview".format(page_n))

# 延迟等待，以确保页面完全加载
wait = WebDriverWait(driver, 5)  # 等待 5 秒
table_xpath = '//*[@id="mobile_table_pills"]/div[1]/div/div[1]/table/tbody'
table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

# 用于存储所有ETF的信息
all_etfs = []

# 循环，直到没有下一页按钮
while True:
    table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
    # 获取所有行
    rows = table.find_elements(By.XPATH, ".//tr")

    # 遍历每一行（除了表头）
    for row in rows[:]:
        columns = row.find_elements(By.XPATH, ".//td")

        # 提取所需列的数据
        etf_info = {
            'Symbol': columns[0].text,
            'ETF Name': columns[1].text,
            'Asset Class': columns[2].text,
            'Total Assets ($MM)': columns[3].text,
            'YTD Price Change': columns[4].text,
            'Avg. Daily Share Volume (3mo)': columns[5].text,
            'Previous Closing Price': columns[6].text,
            'ETF Database Pro': columns[7].text
        }
        
        all_etfs.append(etf_info)
    #当前页码
    print("all_etfs:",len(all_etfs),"eft_info:",len(etf_info))
    
    # 尝试找到下一页按钮并点击
    try:
        # page_n+=1
        # if page_n == 123:
        #     break
        # driver.get("https://etfdb.com/screener/#page={}&tab=overview".format(page_n))
        # wait = WebDriverWait(driver, 5)  # 等待 5 秒
        # table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        # print("page:",page_n)
        next_page_button_xpath = '//*[@id="mobile_table_pills"]/div[1]/div/div[2]/div/ul/li[8]/a'
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_page_button_xpath)))
        next_page_button.click()

        # 等待表格重新加载
        wait.until(EC.staleness_of(table))

    except:
        print("last page")
        break

# 关闭浏览器
driver.quit()

# 输出为csv
all_etfs_df = pd.DataFrame(all_etfs)
all_etfs_df.to_csv("etf_data/etf_info.csv", index=False)
