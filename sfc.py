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



# tutorial for scraping with selenium 
# http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python 

# other references for scraping
# https://code.tutsplus.com/tutorials/modern-web-scraping-with-beautifulsoup-and-selenium--cms-30486

chrome_driver = '/Users/kwa/Documents/Code/Registered Licensees/chromedriver'
letters = list(range(1,27)) # since there are 26 letters
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
table_header = ['CE Reference', 'Name', 'Chinese Name', 'Main Business Address', 'Active License Record']

def init_driver(wait_time, headless=False, driver_path=chrome_driver):
	"""function to initialize a chrome driver with a specified wait time to keep
	the browser open"""
	chrome = webdriver.ChromeOptions()
	if headless:
		chrome.add_argument("headless")
	driver = webdriver.Chrome(executable_path = driver_path, options = chrome)
	driver.wait = WebDriverWait(driver, wait_time)
	return driver

# note that a type 1 license has a button id of 1019, and each subsequent type is an 
# increment of 1. Therefore, we can include what type license as an input

def sfc_lookup(driver, type):
	"""lookup the license type on the SFC website"""
	driver.get('https://www.sfc.hk/publicregWeb/searchByRa?locale=en')
	try:
		# choose type of license
		type_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radiofield-' + str(1018 + type) + '-inputEl"]')))
		type_button.click()

		# select corporation type
		biz_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="roleTypeCorporation-inputEl"]')))
		biz_button.click()

	except Exception as e:
		error_message = str(e)
		stack_trace = str(traceback.format_exc())
		write_logs(driver, error_message, stack_trace)
		# driver.close()
		# exit("Exception occurred")

def sfc_per_letter(driver, letter_no):
	"""Collect all the pages of data for a given letter"""
	try:
		# choose letter to search
		dropdown_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ext-gen1069"]')))
		dropdown_button.click()
		driver.find_element_by_xpath('//*[@id="boundlist-1064-listEl"]/ul/li[' + str(letter_no) + ']').click()

		# click the search button
		search_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="button-1011-btnInnerEl"]')))
		search_button.click()

		# check the number of pages and items
		pages = driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbtext-1053"]')))
		items = driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbtext-1060"]')))
		
		# we need an explicit wait since the value of the element changes as the webpage loads
		time.sleep(2.5) 
		num_pages = int(pages.get_attribute("innerHTML").split(' ')[1])
		num_items = int(items.get_attribute("innerHTML").split(' - ')[1].split(' ')[2])
		# print(num_pages, num_items)
		return num_pages, num_items

	except Exception as e:
		error_message = str(e)
		stack_trace = str(traceback.format_exc())
		write_logs(driver, error_message, stack_trace)

def sfc_all_pages_per_letter(driver, page_no, item_lim):
	"""Scrape all data on the page"""
	try: 
		# input page number into box
		box = driver.find_element_by_xpath('//*[@id="numberfield-1052-inputEl"]')
		box.clear()
		box.send_keys(page_no)
		box.send_keys(Keys.ENTER)

		# explicit wait for page to load
		time.sleep(2.5)

		# count the total number of items on the page
		total_items = item_lim - (20 * (page_no - 1))
		if total_items >= 20:
			num_objects = 20
		else:
			num_objects = total_items

		# initialize list to store results
		results = [None] * num_objects

		# find table by xpath
		table1 = '//*[@id="gridview-1046"]/table/tbody/tr['
		table2 = ']/td['
		table3 = ']/div'

		# first row number is 2 since row number 1 is header
		# store results in list as tuples
		for row in range(2, num_objects+2):
			field1 = driver.find_element_by_xpath(table1 + str(row) + table2 + str(1) + table3).get_attribute("innerHTML")
			field2 = html.unescape(driver.find_element_by_xpath(table1 + str(row) + table2 + str(2) + table3 + '/a').get_attribute("innerHTML"))
			field3 = driver.find_element_by_xpath(table1 + str(row) + table2 + str(3) + table3).get_attribute("innerHTML")
			field4 = html.unescape(driver.find_element_by_xpath(table1 + str(row) + table2 + str(6) + table3).get_attribute("innerHTML"))
			field5 = driver.find_element_by_xpath(table1 + str(row) + table2 + str(7) + table3).get_attribute("innerHTML")
			
			# store data in results 
			results[row-2] = (field1, field2, field3, field4, field5)
		
		# print(results[0])
		return results

	except Exception as e:
		error_message = str(e)
		stack_trace = str(traceback.format_exc())
		write_logs(driver, error_message, stack_trace)
	

def write_logs(driver, error_message, stack_trace):
	"""function to write logs"""
	# print the error message and stack and see if that's what you want to log
	print (error_message + '\n' + stack_trace)

	# if it is, add it to your outfile how you want to record it
	with open('selenium_browser.log', 'w') as outfile:
		outfile.write(error_message + '\n' + stack_trace)

if __name__ == '__main__':
	driver = init_driver(10000)
	sfc_lookup(driver, 9)
	for letter in letters:
		results = []
		page_lim, item_lim = sfc_per_letter(driver, letter)
		for page in list(range(1, page_lim+1)):
			results += sfc_all_pages_per_letter(driver, page, item_lim)
	
		# store results as pandas df
		df = pd.DataFrame(results, columns=table_header)
		print(df.head())
		df.to_csv('data/' + alphabet[letter-1] + 'license9_firms.csv')



