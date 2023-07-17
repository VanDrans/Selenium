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


# 获取cookie
def get_coo(driver):
    # 使用json读取cookies
    with open('cookie.json', 'r') as f:
        json_cookies = f.read()
    cookie_list = json.loads(json_cookies)
    print(cookie_list)
    # 将cookie添加到请求头中
    for cookie in cookie_list:
        # 复制cookie字典
        cookie_dict = cookie.copy()
    # 添加cookie到请求头中
    driver.add_cookie({'name': 'SESSION', 'value': cookie_dict['value']})
    print(cookie_dict)
    driver.get("http://www.ctgpaas.cn:9000/paas/cloudportal/site/")


# 遍历无状态列表中的内容
def get_Stateless_List(driver, space_name):
    # 打开工作负载中的名称
    test_name = driver.find_elements(By.XPATH,
                                     "/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div["
                                     "3]/table/tbody//button[@class='el-button el-button--text "
                                     "el-button--small']")
    print("工作负载：", len(test_name))
    for x in range(len(test_name)):
        time.sleep(1)
        name = test_name[x].text
        if not os.path.exists(f'{space_name}/{name}'):
            os.makedirs(f'{space_name}/{name}')
        print('名称:' + name)
        test_name[x].click()
        # 打开表格
        pod_out = driver.find_element(by=By.XPATH,
                                      value='//*[@id="pane-pod"]/div/div[1]/div[3]/table/tbody/tr[1]/td['
                                            '1]/div/div/i')
        pod_out.click()
        time.sleep(1)
        # pod列表
        pod_list = driver.find_elements(by=By.XPATH, value='//*[@id="pane-pod"]/div/div[1]/div[3]/table/tbody/tr['
                                                           '2]/td/div/div[3]/table/tbody//div[@class="cell"]')
        print(len(pod_list))
        plist = []
        for s in range(0, len(pod_list), 7):
            print(s, pod_list[s].text)
            dic = {'容器名称': pod_list[s].text, '容器ID': pod_list[s + 1].text, '镜像版本号': pod_list[s + 2].text,
                   '重启次数': pod_list[s + 3].text, 'CPU': pod_list[s + 4].text, '内存': pod_list[s + 5].text,
                   '状态': pod_list[s + 6].text}
            plist.append(dic)
        json_plist = json.dumps(plist, ensure_ascii=False)
        with open(f'{space_name}/{name}/pod.json', 'w') as f:
            f.write(json_plist)

        # 日志
        diary_btn = driver.find_element(by=By.ID, value='tab-log')
        diary_btn.click()
        time.sleep(1)
        diary = driver.find_element(By.TAG_NAME, "code")
        diary_list = json.dumps(diary.text.split('\n'))
        with open(f'{space_name}/{name}/diary.json', 'w') as f:
            f.write(diary_list)
        # 转到监控页面
        mon_btn = driver.find_element(By.ID, 'tab-monitor')
        mon_btn.click()
        time.sleep(1)
        # 找到canvas元素和tooltip元素
        canvas = driver.find_elements(By.TAG_NAME, "canvas")
        tooltip = driver.find_elements(By.XPATH, '//div[@class="g2-tooltip"]')
        print(len(canvas), len(tooltip))
        get_canvas(driver, canvas, tooltip, space_name, name)
        driver.get(
            'http://www.ctgpaas.cn:9000/paas/dcos/2.7.10/?ctxPath=dcos#/namespace/deployment-detail-list?clusterId'
            '=19&clusterName=dmz-fgs-ccse&namespaceName=gzsjld')


# 获取图表信息
def get_canvas(driver, canvas, tooltip, space_name, name):
    for t in range(len(canvas)):
        # 获取canvas元素的坐标和大小
        canvas_rect = canvas[t].rect
        print(canvas_rect)
        driver.execute_script("arguments[0].scrollIntoView();", canvas[t])
        print(f"{name}Canvas{t}")
        tooltip_list = []
        # #遍历曲线上的每个点
        for n in range(0, canvas_rect["width"], 10):
            # 计算点在canvas中的坐标
            x = int(n - canvas_rect["width"] / 2)
            y = 0
            # 模拟鼠标悬停事件，获取tooltip内容
            ActionChains(driver).move_to_element_with_offset(canvas[t], x, y).perform()
            tooltip_content = tooltip[t].text
            if tooltip_content != '' and (len(tooltip_list) == 0 or tooltip_content != tooltip_list[-1]):
                tooltip_list.append(tooltip_content)
                print(tooltip_content)
        tooltip_json = json.dumps(tooltip_list, ensure_ascii=False)
        with open(f'{space_name}/{name}/Canvas{t}.json', 'w') as f:
            f.write(tooltip_json)


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
    el_link.click()
    time.sleep(2)

    windows = driver.window_handles
    driver.switch_to.window(windows[-1])

    # 进入命名空间
    namespace_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[1]/div/aside/div/ul/li[3]")
    namespace_btn.click()
    time.sleep(1)
    # 选择命名空间
    small_btn = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]//div['
                                               '@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td['
                                               '1]//button')
    for s in range(len(small_btn)):
        space_name = small_btn[s].text
        print("命名空间" + space_name)
        small_btn[s].click()
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
            f.write(f'{space_name}/inf.json', )

        # 打开工作负载
        workload = driver.find_element(by=By.XPATH,
                                       value='/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div['
                                             '2]/div[1]/span[1]')
        workload.click()

        # 打开无状态列表
        node = driver.find_element(by=By.XPATH,
                                   value="/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div["
                                         "2]/div[1] "
                                   )
        node.click()

        get_Stateless_List(driver, space_name)
        driver.get('http://www.ctgpaas.cn:9000/paas/dcos/2.7.10/?ctxPath=dcos#/namespace/namespace-list')


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.ctgpaas.cn:9000/paas/cloudportal/site/")
driver.maximize_window()
driver.implicitly_wait(10)
get_coo(driver)
# login_2(driver)
get_inf(driver)
