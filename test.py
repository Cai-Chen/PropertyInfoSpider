# -*- coding: utf-8 -*-
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium
import time
import PIL.Image
import io
from scrapy.http import HtmlResponse


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
dcap["phantomjs.page.settings.loadImages"] = False
browser = webdriver.PhantomJS(desired_capabilities=dcap)
browser.set_window_size(1024, 768)

browser.get("https://www.domain.com.au/")

channel = browser.find_element_by_name("Terms.Mode")
browser.execute_script("arguments[0].setAttribute('value', 'rent');", channel)

location = browser.find_element_by_xpath("//*[@id='react-select-3--value']/div[2]/input")
location.clear()
location.send_keys('box hill')
time.sleep(1)

more_options = browser.find_element_by_xpath("//span[text()='More options']")
more_options.click()
property_type = browser.find_element_by_xpath("//span[text()='House']")
browser.execute_script("arguments[0].click();", property_type)
property_type = browser.find_element_by_xpath("//span[text()='Apartment']")
browser.execute_script("arguments[0].click();", property_type)

bedrooms = browser.find_element_by_name("Terms.Bedrooms")
browser.execute_script("arguments[0].setAttribute('value', '>2');", bedrooms)

bathrooms = browser.find_element_by_name("Terms.Bathrooms")
browser.execute_script("arguments[0].setAttribute('value', '>2');", bathrooms)

search_button = browser.find_element_by_xpath("//*[@id='domain-home-content']/div[1]/form/div[1]/button")
search_button.click()
time.sleep(2)

PIL.Image.open(io.BytesIO(browser.get_screenshot_as_png())).show()
