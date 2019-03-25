import html
import pandas as pd
import selenium.common.exceptions
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# list of words to strip from name
blacklist = ['co.,', 'co', 'limited', 'HK', 'Hong Kong']

def init_driver(wait_time, headless=False, driver_path=chrome_driver):
	"""function to initialize a chrome driver with a specified wait time to keep
	the browser open"""
	chrome = webdriver.ChromeOptions()
	if headless:
		chrome.add_argument("headless")
	driver = webdriver.Chrome(executable_path = driver_path, options = chrome)
	driver.wait = WebDriverWait(driver, wait_time)
	return driver



def write_logs(driver, error_message, stack_trace):
	"""function to write logs"""
	# print the error message and stack and see if that's what you want to log
	print (error_message + '\n' + stack_trace)

	# if it is, add it to your outfile how you want to record it
	with open('selenium_browser.log', 'w') as outfile:
		outfile.write(error_message + '\n' + stack_trace)

if __name__ == '__main__':
	# initiate google driver so we can do search results
	google_search = init_driver(10000)
	google_search.get('https://www.google.com/search?q=random&oq=random&aqs=chrome..69i57j0l5.2637j0j7&sourceid=chrome&ie=UTF-8')








anything inside brackets - split by ' ('