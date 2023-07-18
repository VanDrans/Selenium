import json
import os
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# 登陆一号账户
def login_1(driver):
    # 点击登陆选项
    login_btn = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/header/div[2]/div/ul/li[3]/a")
    login_btn.click()
    time.sleep(0.5)
    # 点击云
    cloud_button = driver.find_element(by=By.NAME, value="cloudca")
    cloud_button.click()
    time.sleep(0.5)
    # 点击高级按钮和下一步
    details_button = driver.find_element(by=By.ID, value="details-button")
    details_button.click()
    time.sleep(1)
    proceed_link = driver.find_element(by=By.ID, value="proceed-link")
    proceed_link.click()
    time.sleep(0.5)
    # 输入密码
    username = driver.find_element(by=By.ID, value="j_username")
    username.send_keys("71095722@GD")
    passwrd = driver.find_element(by=By.ID, value="j_password")
    passwrd.send_keys("ads!@Wen22")
    time.sleep(1)
    # 登陆按钮
    login_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    login_button.click()

    time.sleep(100)

    # 获取页面的cookie信息
    cookies = driver.get_cookies()
    print(cookies)
    # 将cookie保存到一个列表中
    cookie_list = []
    for cookie in cookies:
        cookie_list.append(cookie)
    # 将cookie信息序列化为JSON格式
    json_cookies = json.dumps(cookie_list)
    # 将cookie信息保存到文件中
    with open('cookie.json', 'w') as f:
        f.write(json_cookies)


# 登陆二号账户
def login_2(driver):
    # 点击登陆选项
    login_btn = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/header/div[2]/div/ul/li[3]/a")
    login_btn.click()
    time.sleep(0.5)
    # 点击云
    cloud_button = driver.find_element(by=By.NAME, value="cloudca")
    cloud_button.click()
    time.sleep(0.5)
    # 点击高级按钮和下一步
    details_button = driver.find_element(by=By.ID, value="details-button")
    details_button.click()
    time.sleep(1)
    proceed_link = driver.find_element(by=By.ID, value="proceed-link")
    proceed_link.click()
    time.sleep(0.5)
    # 输入密码
    username = driver.find_element(by=By.ID, value="j_username")
    username.send_keys("15688322845")
    passwrd = driver.find_element(by=By.ID, value="j_password")
    passwrd.send_keys("ITYZ@wky2023")
    time.sleep(1)
    # 登陆按钮
    login_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    login_button.click()

    time.sleep(100)

    # 获取页面的cookie信息
    cookies = driver.get_cookies()
    print(cookies)
    # 将cookie保存到一个列表中
    cookie_list = []
    for cookie in cookies:
        cookie_list.append(cookie)
    # 将cookie信息序列化为JSON格式
    json_cookies = json.dumps(cookie_list)
    # 将cookie信息保存到文件中
    with open('cookie.json', 'w') as f:
        f.write(json_cookies)


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.ctgpaas.cn:9000/paas/cloudportal/site/")
driver.maximize_window()
driver.implicitly_wait(3)
