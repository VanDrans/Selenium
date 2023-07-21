import json
import time
import requests
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def ans_mes():
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


def get_res():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82 '
                      ,
        'Referer': 'https://www.bilibili.com/',
        'Cookie': "buvid3=734433D6-79F8-4AAE-BA25-E938BF782199148807infoc; LIVE_BUVID=AUTO8616301563824831; "
                   "buvid_fp=8cc2c716bece4ee71ecf49a573de7671; "
                   "buvid4=51D3007F-C7B5-EDCA-84BD-A7FB5A3EECA333261-022012614-oVduAfGVROylwFkPkGnfQw%3D%3D; "
                   "_uuid=1C6A10B1010-21075-6681-4C3A-E943710C4787D84522infoc; "
                   "fingerprint3=a7547cdc76fcabf879930e305a7d3eb7; b_nut=100; rpdid=|(kuuuJ~u|~m0J'uYY)l~Jukm; "
                   "blackside_state=0; CURRENT_BLACKGAP=0; SESSDATA=b87fed7f%2C1692531372%2Cbb843%2A21; "
                   "bili_jct=eb6c0b5d8f52391e21a178310e1614bc; DedeUserID=273084021; "
                   "DedeUserID__ckMd5=0ad6fdaf7a688b2d; i-wanna-go-back=-1; b_ut=5; "
                   "CURRENT_PID=cf0b5440-c892-11ed-94b2-c10acdd5a642; nostalgia_conf=-1; hit-dyn-v2=1; "
                   "FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; CURRENT_FNVAL=4048; CURRENT_QUALITY=80; "
                   "fingerprint=525fdd38952601a98d998b405c551a66; home_feed_column=5; PVID=1; innersign=0; "
                   "b_lsid=BEC1996E_18970C8D74B; bp_video_offset_273084021=820241953575665700; hit-new-style-dyn=1; "
                   "browser_resolution=1536-308 "
    }
    res = requests.get('https://data.bilibili.com/v2/log/web?content_type=pbrequest&logid=021436',
                       headers=headers
                       )
    print(res)


if __name__ == '__main__':
    get_res()
