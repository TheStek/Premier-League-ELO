from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time


# Hopefully a stable link to the current season
entry_point = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"


profile_path = r'C:\Users\User\Documents\5. Random Projects\Premier League ELO\Chrome Profile'

# Add option to run without opening a window
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("user-data-dir=" + profile_path)



# Start driver at the entry point
driver = webdriver.Chrome(executable_path = "chromedriver.exe", options = options)
driver.create_options()
driver.maximize_window()
driver.get(entry_point)

try:
# Agree to cookies
	driver.find_element(By.XPATH, '//button[text()="AGREE"]').click()
except:
	print("No cookies :(")

actor = ActionChains(driver)


def goToPreviousSeason():
	
	# Find previous button
	prev_button = driver.find_element(By.XPATH, '//a[text()="Previous Season"]')

	# Click previous button
	actor.move_to_element(prev_button).click().perform()



def scrapeData():
	dropdown = driver.find_element(By.XPATH, '//span[text()="Share & Export"]')

	actor.move_to_element(dropdown).click().perform()

	csv_button = driver.find_element(By.XPATH, '//button[text()="Get table as CSV (for Excel)"]')

	actor.move_to_element(csv_button).click().perform()

	generateCSVFromHTML(driver.page_source)


strip_season = lambda y: "".join(filter(lambda x: x in '1234567890-', y))

def generateCSVFromHTML(page):
	soup = BeautifulSoup(page, "html.parser")

	raw_data = soup.find('pre').text

	raw_lines = raw_data.split('\n')

	clean_lines = filter(lambda x: x not in  ('', ' ') and x[0] not in ('-', ','), raw_lines)

	data = '\n'.join(clean_lines).replace('–', '-').replace('´', "'")

	season = strip_season(soup.find('h1').text)

	with open(f'Data/{season}.csv', 'w') as f:
		f.write(data)

	print(f"Extracted data for {season}")


for i in range(30):
	try:
		scrapeData()
		goToPreviousSeason()
	except:
		break

driver.quit()
