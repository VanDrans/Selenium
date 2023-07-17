from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
windows = driver.window_handles

driver.get("https://www.w3school.com.cn/xpath/xpath_syntax.asp")
time.sleep(3)

inf = driver.find_elements(by=By.XPATH, value='//*[@id="maincontent"]/div[4]/table[2]//th')
for i in inf:
    print(i.text)

driver.quit()
