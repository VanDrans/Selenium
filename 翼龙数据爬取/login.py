import json
import os
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# ��½һ���˻�
def login_1(driver):
    # �����½ѡ��
    login_btn = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/header/div[2]/div/ul/li[3]/a")
    login_btn.click()
    time.sleep(0.5)
    # �����
    cloud_button = driver.find_element(by=By.NAME, value="cloudca")
    cloud_button.click()
    time.sleep(0.5)
    # ����߼���ť����һ��
    details_button = driver.find_element(by=By.ID, value="details-button")
    details_button.click()
    time.sleep(1)
    proceed_link = driver.find_element(by=By.ID, value="proceed-link")
    proceed_link.click()
    time.sleep(0.5)
    # ��������
    username = driver.find_element(by=By.ID, value="j_username")
    username.send_keys("71095722@GD")
    passwrd = driver.find_element(by=By.ID, value="j_password")
    passwrd.send_keys("ads!@Wen22")
    time.sleep(1)
    # ��½��ť
    login_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    login_button.click()

    time.sleep(100)

    # ��ȡҳ���cookie��Ϣ
    cookies = driver.get_cookies()
    print(cookies)
    # ��cookie���浽һ���б���
    cookie_list = []
    for cookie in cookies:
        cookie_list.append(cookie)
    # ��cookie��Ϣ���л�ΪJSON��ʽ
    json_cookies = json.dumps(cookie_list)
    # ��cookie��Ϣ���浽�ļ���
    with open('cookie.json', 'w') as f:
        f.write(json_cookies)


# ��½�����˻�
def login_2(driver):
    # �����½ѡ��
    login_btn = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/header/div[2]/div/ul/li[3]/a")
    login_btn.click()
    time.sleep(0.5)
    # �����
    cloud_button = driver.find_element(by=By.NAME, value="cloudca")
    cloud_button.click()
    time.sleep(0.5)
    # ����߼���ť����һ��
    details_button = driver.find_element(by=By.ID, value="details-button")
    details_button.click()
    time.sleep(1)
    proceed_link = driver.find_element(by=By.ID, value="proceed-link")
    proceed_link.click()
    time.sleep(0.5)
    # ��������
    username = driver.find_element(by=By.ID, value="j_username")
    username.send_keys("15688322845")
    passwrd = driver.find_element(by=By.ID, value="j_password")
    passwrd.send_keys("ITYZ@wky2023")
    time.sleep(1)
    # ��½��ť
    login_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    login_button.click()

    time.sleep(100)

    # ��ȡҳ���cookie��Ϣ
    cookies = driver.get_cookies()
    print(cookies)
    # ��cookie���浽һ���б���
    cookie_list = []
    for cookie in cookies:
        cookie_list.append(cookie)
    # ��cookie��Ϣ���л�ΪJSON��ʽ
    json_cookies = json.dumps(cookie_list)
    # ��cookie��Ϣ���浽�ļ���
    with open('cookie.json', 'w') as f:
        f.write(json_cookies)


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.ctgpaas.cn:9000/paas/cloudportal/site/")
driver.maximize_window()
driver.implicitly_wait(3)
