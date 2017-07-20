# -*- coding: utf-8 -*-
import scrapy
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# Chrome Driver config
chromeDriver = "D:\setup\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromeDriver
browser = webdriver.Chrome(executable_path = chromeDriver)

# Firefox Driver config
# firefoxDriver = "D:\setup\geckodriver.exe"
# browser = webdriver.Firefox(executable_path = firefoxDriver)

browser.get("https://www.realestate.com.au/")
time.sleep(0.3) #sleep 0.3s
# browser.maximize_window() # Maximize the browser
# Click the channel list
search_channel = browser.find_element_by_xpath("//div[@class='rui-select-wrapper']")
search_channel.click()
# Click the channel list again (The class name changed)
# search_channel_1 = browser.find_element_by_css_selector(".rui-select-wrapper.rui-select-open")
# search_channel_1.click()
# Choose the channel (Here is 'rent')
time.sleep(0.3) #sleep 0.3s
channel = browser.find_element_by_css_selector(".rui-select-wrapper.rui-select-open").find_element_by_xpath("ul/li[@data-value='rent']")
channel.click()
# Input the location
where = browser.find_element_by_id("where")
where.send_keys("Box Hill, VIC 3128")
# Find the property type list
property_list = browser.find_elements_by_xpath("//div[@class='rui-select-wrapper rui-default-selected']")[0]
property_list.click()
# Choose the property type (Here assume a list)
property_type_list = ['House', 'unit apartment', 'Townhouse']
# The class value changes after the first click
cnt = 1
for property_type in property_type_list:
    if cnt == 1:
        property = browser.find_element_by_css_selector(".rui-select-wrapper.rui-default-selected.rui-select-open").find_element_by_xpath("ul/li/input[@value='" + property_type + "']/parent::li")
    else:
        property = browser.find_element_by_css_selector(".rui-select-wrapper.rui-select-open").find_element_by_xpath("ul/li/input[@value='" + property_type + "']/parent::li")
    property.click()
    cnt += 1
# Min beds
minbeds_list = browser.find_elements_by_xpath("//div[@class='rui-select-wrapper rui-default-selected']")[1]
minbeds_list.click()
# Choose the min beds (Studio)
minbeds = browser.find_element_by_css_selector(".rui-select-wrapper.rui-default-selected.rui-select-open").find_element_by_xpath("ul/li[@data-value='Studio']")
minbeds.click()
# Max beds
maxbeds_list = browser.find_elements_by_xpath("//div[@class='rui-select-wrapper rui-default-selected']")[1]
maxbeds_list.click()
# Choose the max beds (2 beds)
maxbeds = browser.find_element_by_css_selector(".rui-select-wrapper.rui-default-selected.rui-select-open").find_element_by_xpath("ul/li[@data-value='2']")
maxbeds.click()

# Click the search button
# search_button = browser.find_element_by_xpath("//button[@class='rui-search-button']")
# search_button.click()


time.sleep(3)
# Print the title
print (browser.title)
#browser.quit()


# class RentinfoSpiderSpider(scrapy.Spider):
#     name = 'rentinfo_spider'
#     allowed_domains = ['']
#     start_urls = ['http:///']
#
#     def parse(self, response):
#         pass
