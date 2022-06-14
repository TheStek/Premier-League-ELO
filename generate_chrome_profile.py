from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

profile_path = r'C:\Users\User\Documents\5. Random Projects\Premier League ELO\Chrome Profile'

options = Options()
options.add_argument("user-data-dir=" + profile_path)
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://google.com")


import time

for i in range(1000):
	print(i)
	time.sleep(1)


driver.quit()