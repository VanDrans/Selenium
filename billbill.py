import json
import time

from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.bilibili.com/")
driver.implicitly_wait(4)

# time.sleep(20)
# # 获取页面的cookie信息
# cookies = driver.get_cookies()
# # 将cookie保存到一个列表中
# cookie_list = []
# for cookie in cookies:
#     cookie_list.append(cookie)
#
# # 将cookie信息序列化为JSON格式
# json_cookies = json.dumps(cookie_list)
#
# # 将cookie信息保存到文件中
# with open('cookies.json', 'w') as f:
#     f.write(json_cookies)

with open('cookies.json', 'r') as f:
    json_cookies = f.read()
cookie_list = json.loads(json_cookies)
# 将cookie添加到请求头中
for cookie in cookie_list:
    # 复制cookie字典
    cookie_dict = cookie.copy()
    # 修改SameSite属性为None
    cookie_dict['sameSite'] = 'None'
    # 添加cookie到请求头中
    driver.add_cookie(cookie_dict)

driver.get("https://www.bilibili.com/")
time.sleep(1)
mes_btn = driver.find_element(by=By.XPATH, value='//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[2]/a')
mes_btn.click()
time.sleep(1)
print(driver.title)
windows = driver.window_handles
driver.switch_to.window(windows[-1])
my_btn = driver.find_element(by=By.LINK_TEXT, value='我的消息')
my_btn.click()
time.sleep(1)
for i in range(6):
    list = driver.find_elements(by=By.CLASS_NAME, value='list-item')
    driver.execute_script("arguments[0].scrollIntoView();", list[-1])
    list[-1].click()
    time.sleep(1)
print(len(list))
mes_list = []
for item in list:
    # if not item.is_displayed():
    #     driver.execute_script("arguments[0].scrollIntoView();",item)
    #     # ActionChains(driver).move_to_element(item).perform()
    # item.click()
    # time.sleep(0.5)
    # 将cookie信息保存到文件中
    driver.execute_script("arguments[0].scrollIntoView();", item)
    item.click()
    time.sleep(0.1)
    # print(item.text)
    # mes_list.append(item.text)
    # with open('item.txt', 'a', encoding='utf-8') as f:
    #     f.write(item.text)
driver.quit()
