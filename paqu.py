from selenium import webdriver
import time
import json

from selenium.webdriver.common.by import By

# 填写webdriver的保存目录
driver = webdriver.Chrome()

# 记得写完整的url 包括http和https
driver.get('http://www.ctgpaas.cn:9000/paas/cloudportal/console/#/ytj/index')

# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()

with open('cookies.txt', 'r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)

# el_link = driver.find_element(by=By.XPATH,
#                               value="/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[1]/div["
#                                     "2]/div/div/div[2]/div/div[2]/span/div[4]/a")
# el_link.click()

# 进入命名空间
namespace = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[1]/div/aside/div/ul/li[3]/span")
namespace.click()

# 进入gzs
gzs = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div["
                                             "3]/table/tbody/tr/td[1]/div/button/span")
gzs.click()
# 打开工作负载
workload = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div['
                                                  '2]/div/span[2]')
workload.click()
# 打开无状态列表
node = driver.find_element(by=By.XPATH,
                           value="/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]"
                           )

node.click()

# 打开test
name = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div["
                                              "1]/div[3]/table/tbody/tr/td[2]/div/button/span")
name.click()

# 打开表格
pod_out = driver.find_element(by=By.CLASS_NAME, value='el-table__expand-icon')
pod_out.click()
# pod列表
pod_list = driver.find_elements(by=By.CLASS_NAME, value="cell")
# 日志
diary = driver.find_element(by=By.XPATH, value='//*[@id="pane-log"]/div/div[2]/div/div/div[2]/code')

print(diary.text)
for item in pod_list:
    print(item.text)

driver.quit()