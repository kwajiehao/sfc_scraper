import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# tutorial for scraping with selenium 
# http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python 

chrome_driver = '/Users/kwa/Documents/Code/Registered Licensees/chromedriver'

def open_up_files(time):
	chrome = webdriver.ChromeOptions()
	driver = webdriver.Chrome(executable_path='/Users/kwa/Documents/Code/Registered Licensees/chromedriver', options = chrome)
	page_url = 'https://www.sfc.hk/publicregWeb/searchByRa?locale=en'
	driver.get(page_url)
	time.sleep(time)

def init_driver(driver_path=chrome_driver, wait_time):
	driver = webdriver.Chrome(executable_path = driver_path, options = chrome)
	driver.wait = WebDriverWait(driver, wait_time)
    return driver


if __name__ == '__main__':
	driver = init_driver(10000)
	

