import pandas as pd
import re
import selenium.common.exceptions
import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# one way to circumvent google scraper rate limits and restrictions is to open and close a new browser for each search term

chrome_driver = '/Users/kwa/Documents/Code/Registered Licensees/chromedriver'

# fields to import
fields = ['CE Reference', 'Name']

# import data
license_no = sys.argv[1]
data = pd.read_csv('data/license' + str(license_no) + '.csv', usecols=fields)


# list of words to strip from name
blacklist = [' AG', ' co.,', ' co', ' Limited', ' LIMITED', ' HK', ' Hong Kong']

def init_driver(wait_time, headless=False, driver_path=chrome_driver):
	"""function to initialize a chrome driver with a specified wait time to keep
	the browser open"""
	chrome = webdriver.ChromeOptions()
	if headless:
		chrome.add_argument("headless")
	driver = webdriver.Chrome(executable_path = driver_path, options = chrome)
	driver.wait = WebDriverWait(driver, wait_time)
	return driver

def search(string):
    """get a the number of search results for a given string"""
    try: 
        driver = init_driver(100, headless=False)
        driver.get('https://www.google.com/search?q=random+site&oq=random+site&aqs=chrome..69i57j69i59l2.4076j0j7&sourceid=chrome&ie=UTF-8')
        
        # box = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tsf"]/div[2]/div[1]/div[2]/div/div[1]/input')))
        # box = driver.find_element(By.XPATH, '//*[@id="tsf"]/div[2]/div[1]/div[2]/div/div[1]/input')
        box = driver.find_element(By.NAME, 'q')

        # submit search in google 
        box.clear()
        box.send_keys(name_strip(string))
        box.send_keys(Keys.ENTER)
        results = driver.find_element_by_xpath('//*[@id="resultStats"]').get_attribute("innerHTML")
        print(results)
        driver.quit() 
        try:
            return(int(''.join(results.split('<')[0].split(' ')[1].split(','))))
        except:
            return(int(''.join(results.split('<')[0].split(' ')[0])))
    
    except:
        print('Unknown error')

def name_strip(name, blacklist=blacklist):
    """Strip names of blacklisted words and other unwanted characters"""
    result = re.sub(' \(.*?\)','', name)
    result = remove_multiple_strings(result, blacklist)
    result = result.split(',')[0]
    result = '"' + result + '"' + ' hong kong'
    return result

def remove_multiple_strings(string, replace_list):
  for word in replace_list:
    string = string.replace(word, '')
  return string

def write_logs(driver, error_message, stack_trace):
	"""function to write logs"""
	# print the error message and stack and see if that's what you want to log
	print (error_message + '\n' + stack_trace)

	# if it is, add it to your outfile how you want to record it
	with open('selenium_browser.log', 'w') as outfile:
		outfile.write(error_message + '\n' + stack_trace)

if __name__ == '__main__':
    data['results'] = data.Name.apply(search)
    data.head()
    data.to_csv('data/license' + str(license_no) + '_search.csv')
