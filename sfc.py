import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



# tutorial for scraping with selenium 
# http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python 

chrome_driver = '/Users/kwa/Documents/Code/Registered Licensees/chromedriver'
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def init_driver(wait_time, driver_path=chrome_driver):
	"""function to initialize a chrome driver with a specified wait time to keep
	the browser open"""
	chrome = webdriver.ChromeOptions()
	driver = webdriver.Chrome(executable_path = driver_path, options = chrome)
	driver.wait = WebDriverWait(driver, wait_time)
	return driver

# note that a type 1 license has a button id of 1019, and each subsequent type is an 
# increment of 1. Therefore, we can include what type license as an input

def sfc_lookup(driver, type, letter_no):
	"""lookup the license type on the SFC website"""
	driver.get('https://www.sfc.hk/publicregWeb/searchByRa?locale=en')
	try:
		# choose type of license
		type_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radiofield-' + str(1018 + type) + '-inputEl"]')))
		type_button.click()

		# select corporation type
		biz_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="roleTypeCorporation-inputEl"]')))
		biz_button.click()
		
		# choose letter to search
		dropdown_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ext-gen1069"]')))
		dropdown_button.click()
		driver.find_element_by_xpath('//*[@id="boundlist-1064-listEl"]/ul/li[' + str(letter_no) + ']').click()

		# click the search button
		search_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="button-1011-btnInnerEl"]')))
		search_button.click()

	except Exception as e:
		error_message = str(e)
		stack_trace = str(traceback.format_exc())
		write_logs(driver, error_message, stack_trace)
		# driver.close()
		# exit("Exception occurred")

def write_logs(driver, error_message, stack_trace):
	"""function to write logs"""
	# print the error message and stack and see if that's what you want to log
	print (error_message + '\n' + stack_trace)

	# if it is, add it to your outfile how you want to record it
	with open('selenium_browser.log', 'w') as outfile:
		outfile.write(error_message + '\n' + stack_trace)

if __name__ == '__main__':
	driver = init_driver(10000)
	sfc_lookup(driver, 9, 3)


