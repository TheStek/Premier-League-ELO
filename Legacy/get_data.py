from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By



def get_data_for_year(start_year_abbrev):

	start_year = 2000 + start_year_abbrev
	end_year = start_year + 1

	website_url = f"https://fbref.com/en/comps/9/1631/schedule/{start_year}-{end_year}-Premier-League-Scores-and-Fixtures"
	print(website_url)


	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")

	
	driver = webdriver.Chrome(executable_path = "chromedriver.exe")
	driver.maximize_window()
	driver.get(website_url)


	driver.find_element(By.XPATH, '//button[text()="AGREE"]').click()


	dropdown = driver.find_element(By.XPATH, '//span[text()="Share & Export"]')

	actions = ActionChains(driver)

	actions.move_to_element(dropdown).click().perform()


	csv_button = driver.find_element(By.XPATH, '//button[text()="Get table as CSV (for Excel)"]')
	download_button = driver.find_element(By.XPATH, '//button[text()="Get as Excel Workbook"]')

	actions.move_to_element(csv_button).click().perform()

	page = driver.page_source

	driver.quit()

	soup = BeautifulSoup(page, "html.parser")


	raw_data = soup.find('pre').text

	raw_lines = raw_data.split('\n')

	clean_lines = filter(lambda x: x not in  ('', ' ') and x[0] not in ('-', ','), raw_lines)

	data = '\n'.join(clean_lines)

	with open(f'{start_year_abbrev}-{start_year_abbrev + 1}.csv', 'w') as f:
		f.write(data)

	print(f"Extracted for {start_year}-{end_year}")


get_data_for_year(20)