import time
import json
from selenium import webdriver

with open('cookies.json', 'r') as f:
    json_cookies = f.read()
cookie_list = json.loads(json_cookies)

# 创建Chrome浏览器对象，并添加cookie
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 最大化窗口
driver = webdriver.Chrome(options=options)
time.sleep(1)
driver.get("http://www.ctgpaas.cn:9000/paas/cloudportal/console/#/ytj/index")
# 将cookie添加到请求头中
for cookie in cookie_list:
    print(cookie)
    driver.add_cookie(cookie)
time.sleep(1)
# 刷新页面，使用添加的cookie进行访问
driver.refresh()

# 获取网页内容
html = driver.page_source
print(html)
time.sleep(1)
# 关闭浏览器
# driver.quit()
#
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)
# driver.maximize_window()
# driver.get("http://www.ctgpaas.cn:9000/paas/cloudportal/console/#/user-account/security?tabUrl=user-account-security"
#            "%5B%E5%AE%89%E5%85%A8%E8%AE%BE%E7%BD%AE%5Bself&tabResourceCode=personal_setting")
# # 读取保存的cookie信息
# with open('cookies.json', 'r') as f:
#     json_cookies = f.read()
# cookie_list = json.loads(json_cookies)
#
# # 将cookie添加到请求头中
# for cookie in cookie_list:
#     driver.add_cookie(cookie)
#
# driver.refresh()


# # 点击登陆选项
# login = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/header/div[2]/div/ul/li[3]/a")
# login.click()
# time.sleep(0.5)
# # 点击云
# cloud_button = driver.find_element(by=By.NAME, value="cloudca")
# cloud_button.click()
# time.sleep(0.5)
# # 点击高级按钮和下一步
# details_button = driver.find_element(by=By.ID, value="details-button")
# details_button.click()
# time.sleep(1)
# proceed_link = driver.find_element(by=By.ID, value="proceed-link")
# proceed_link.click()
# time.sleep(0.5)
# # 输入密码
# username = driver.find_element(by=By.ID, value="j_username")
# username.send_keys("71095722@GD")
# passwrd = driver.find_element(by=By.ID, value="j_password")
# passwrd.send_keys("ads!@Wen22")
# time.sleep(1)
# # 登陆按钮
# login_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
# login_button.click()
# time.sleep(10)


# 获取页面的cookie信息
# cookies = driver.get_cookies()
#
# # 将cookie保存到一个列表中
# cookie_list = []
# for cookie in cookies:
#     cookie_list.append(cookie)
#
# # 将cookie信息序列化为JSON格式
# json_cookies = json.dumps(cookie_list)

## 将cookie信息保存到文件中
# with open('cookies.json', 'w') as f:
#     f.write(json_cookies)
