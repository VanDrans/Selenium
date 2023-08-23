# This Python file uses the following encoding: utf-8
import json
import os
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
url = 'http://www.ctgpaas.cn:9000/paas/cloudportal/site/'
driver.get(url)
# 使用json读取cookies
with open('cookie.json', 'r') as f:
    json_cookies = f.read()
cookie_list = json.loads(json_cookies)
for cookie in cookie_list:
    # 复制cookie字典
    cookie_dict = cookie.copy()
    print(type(cookie_dict['value']))
    driver.add_cookie({'name': 'SESSION', 'value': cookie_dict['value']})
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(10)


# 遍历列表中的内容
def get_List(driver, space_name):
    next = 0
    if not driver.find_element(By.XPATH,
                               '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]').text == '暂无数据':
        while True:
            # 判断是否需要翻页
            next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div['
                                                      '2]/div[2]/button[2]')
            print('页数:', next + 1)
            if next_page.is_enabled() and next != 0:
                driver.execute_script("arguments[0].click();", next_page)
            time.sleep(0.5)
            # 打开工作负载中的名称
            test_name = driver.find_elements(By.XPATH,
                                             "/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div["
                                             "3]/table/tbody//button[@class='el-button el-button--text "
                                             "el-button--small']")
            print("数量：", len(test_name))
            for x in range(len(test_name)):
                time.sleep(0.2)
                name = test_name[x].text
                if not os.path.exists(f'{space_name}/{name}'):
                    os.makedirs(f'{space_name}/{name}')
                print('正在爬取podName:' + name)
                driver.execute_script("arguments[0].click();", test_name[x])
                time.sleep(0.2)
                # 判断是否有数据
                if not driver.find_element(By.XPATH, '//*[@id="pane-pod"]/div/div[1]/div[3]').text == '暂无数据':
                    podname = driver.find_element(By.XPATH, '//*[@id="pane-pod"]/div/div[1]/div[3]/table/tbody/tr/td['
                                                            '2]/div').text

                    # 打开表格
                    pod_out = driver.find_element(by=By.XPATH,
                                                  value='//*[@id="pane-pod"]/div/div[1]/div[3]/table/tbody/tr[1]/td['
                                                        '1]/div/div/i')
                    driver.execute_script("arguments[0].click();", pod_out)
                    # pod列表

                    pod_list = driver.find_elements(by=By.XPATH, value='//*[@id="pane-pod"]/div/div[1]/div['
                                                                       '3]/table/tbody/tr[2]/td/div/div['
                                                                       '3]/table/tbody//div[@class="cell"]')
                    plist = []
                    containername = []
                    for s in range(0, len(pod_list), 7):
                        containername.append(pod_list[s].text)
                        dic = {'容器名称': pod_list[s].text, '容器ID': pod_list[s + 1].text,
                               '镜像版本号': pod_list[s + 2].text,
                               '重启次数': pod_list[s + 3].text, 'CPU': pod_list[s + 4].text,
                               '内存': pod_list[s + 5].text,
                               '状态': pod_list[s + 6].text}
                        plist.append(dic)
                    json_plist = json.dumps(plist, ensure_ascii=False)
                    with open(f'{space_name}/{name}/pod.json', 'w') as f:
                        f.write(json_plist)
                    time.sleep(1)
                    picture_get(space_name, podname, name, containername)
                    # 日志
                    diary_btn = driver.find_element(by=By.ID, value='tab-log')
                    diary_btn.click()
                    time.sleep(0.2)
                    diary = driver.find_element(By.TAG_NAME, "code")
                    diary_list = json.dumps(diary.text.split('\n'))
                    with open(f'{space_name}/{name}/diary.json', 'w') as f:
                        f.write(diary_list)

                driver.back()
                for n in range(next):
                    if next_page.is_enabled():
                        driver.execute_script("arguments[0].click();", next_page)
                        time.sleep(0.5)
            if not next_page.is_enabled():
                break
            time.sleep(0.5)
            next += 1


# 进入命名空间
def get_namespace(driver):
    # 进入命名空间
    namespace_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[1]/div/aside/div/ul/li[3]")
    namespace_btn.click()
    time.sleep(0.5)

    page_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/span['
                                             '2]/div/div/input')
    driver.execute_script("arguments[0].click();", page_btn)
    page100 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/ul/li[6]')
    driver.execute_script("arguments[0].click();", page100)
    time.sleep(0.5)

    # 选择命名空间
    small_btn = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]//button')
    for s in range(int(len(small_btn) / 4)):
        space_name = small_btn[s].text
        print("命名空间" + space_name)
        driver.execute_script("arguments[0].click();", small_btn[s])
        if not os.path.exists(f'{space_name}'):
            os.makedirs(space_name)

        # 打开基本信息
        inf_btn = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/div/div['
                                                         '1]/div/div/div[1]/div[1]/span[2]')
        inf_btn.click()
        # 爬取基本信息
        label = driver.find_elements(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/div/div['
                                                        '2]/div/div/form/div[8]/div/div//label')
        inf = driver.find_elements(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/div/div['
                                                      '2]/div/div/form/div[8]/div/div//span')
        inf_list = []
        label_list = []
        for l in range(len(label)):
            inf_list.append(inf[2 * l].text + '  ' + inf[2 * l + 1].text)
            label_list.append(label[l].text)
        inf_dic = dict(zip(label_list, inf_list))
        inf_json = json.dumps(inf_dic, ensure_ascii=False)
        with open(f'{space_name}/inf.json', 'w') as f:
            f.write(inf_json)

        # 打开工作负载
        workload = driver.find_element(by=By.XPATH,
                                       value='/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div['
                                             '2]/div[1]/span[1]')
        workload.click()
        time.sleep(0.5)
        # 打开无状态列表
        Stateless_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div[2]/div/div["
                                                               "1]/div/div/div[2]/div[2]/div[1] "
                                            )
        Stateless_btn.click()
        time.sleep(0.5)
        get_List(driver, space_name)

        Stateful_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div['
                                                     '1]/div/div/div[2]/div[2]/div[2]/div')
        Stateful_btn.click()
        time.sleep(0.5)
        get_List(driver, space_name)

        Daemon_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div['
                                                   '1]/div/div/div[2]/div[2]/div[3]/div[1]')
        Daemon_btn.click()
        time.sleep(0.5)
        get_List(driver, space_name)
        massion_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div['
                                                    '1]/div/div/div[2]/div[2]/div[4]/div[1]')
        massion_btn.click()
        time.sleep(0.5)
        get_List(driver, space_name)
        driver.get('http://www.ctgpaas.cn:9000/paas/dcos/2.7.10/?ctxPath=dcos#/namespace/namespace-list')


# 爬取信息
def get_inf(driver):
    # 打开管理中心
    manage_btn = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/header/div[2]/div/ul/li[1]/a")
    manage_btn.click()
    time.sleep(2)
    # 进入容器
    el_link = driver.find_element(by=By.XPATH,
                                  value="/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[1]/div["
                                        "2]/div/div/div[2]/div/div[2]/span/div[4]/a")
    if not el_link.is_displayed():
        open_btn = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[2]/div[2]/div/div/div['
                                                          '2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div['
                                                          '1]/h3/button')
        open_btn.click()
    driver.execute_script("arguments[0].click();", el_link)
    time.sleep(2)

    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    while True:
        # 进入命名空间
        namespace_btn = driver.find_element(by=By.XPATH,
                                            value="/html/body/div[2]/div/div/div[1]/div/aside/div/ul/li[3]")
        namespace_btn.click()
        time.sleep(0.5)
        get_namespace(driver)
        # time.sleep(3600)


# 爬取图片的数据
def picture_get(spacename, podname, name, containername):
    now = time.time()
    now = int(now)
    print(datetime.datetime.fromtimestamp(now))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    list = []
    res1 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podCpuUsage?clusterName=dmz-fgs-ccse&namespaceName={spacename}&podName={podname}&startTime={now - 3600}&endTime={now}',
        headers=headers
    ).json()
    # print(res1['data']['values'])
    list.append(res1['data']['values'])
    res2 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podNetworkUsage?clusterName=dmz-fgs-ccse&namespaceName={spacename}&podName={podname}&startTime={now - 3600}&endTime={now}',
        headers=headers
    ).json()
    # print(res2['data']['values'])
    list.append(res2['data']['values'])
    res3 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podMemoryUsage?clusterName=dmz-fgs-ccse&namespaceName={spacename}&podName={podname}&startTime={now - 3600}&endTime={now}',
        headers=headers
    ).json()
    # print(res3['data']['values'])
    list.append(res3['data']['values'])
    for con in containername:
        res4 = requests.get(
            f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/containerCpuUsage?clusterName=dmz-fgs-ccse&namespaceName={spacename}&podName={podname}&containerName={con}&startTime={now - 3600}&endTime={now}',
            headers=headers
        ).json()
        # print(res4['data']['values'])
        list.append(res4['data']['values'])
        res5 = requests.get(
            f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/containerMemoryUsage?clusterName=dmz-fgs-ccse&namespaceName={spacename}&podName={podname}&containerName={con}&startTime={now - 3600}&endTime={now}',
            headers=headers
        ).json()
        # print(res5['data']['values'])
        list.append(res5['data']['values'])
    list = json.dumps(list, ensure_ascii=False)
    with open(f'{spacename}/{name}/res.json', 'w') as f:
        f.write(list)


# 爬取日志信息
# def diary_get()

get_inf(driver)
