# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import selenium
import time
from scrapy.http import HtmlResponse

class RentinfoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# Middleware for realestate website
class RealestateMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "rentinfo_spider" and 'Selenium' in request.meta:
            # Chrome Driver config
            chromeDriver = "D:\setup\chromedriver.exe"
            browser = webdriver.Chrome(executable_path = chromeDriver)

            # Firefox Driver config
            # firefoxDriver = "D:\setup\geckodriver.exe"
            # browser = webdriver.Firefox(executable_path = firefoxDriver)

            browser.get(request.url)
            time.sleep(0.3) #sleep 0.3s
            # # browser.maximize_window() # Maximize the browser
            # Click the channel list
            search_channel = browser.find_element_by_xpath("//div[@class='rui-select-wrapper search-channel-container']")
            search_channel.click()
            # Choose the channel
            channel = browser.find_element_by_xpath("//div[@class='rui-select-wrapper search-channel-container']/div/ul/li[@data-value='"+ spider.channel +"']")
            channel.click()
            # Input the location
            if spider.location is not None:
                where = browser.find_element_by_id("where")
                where.send_keys(spider.location)
                # Click the property type twice to remove the auto-filled context
                browser.find_element_by_xpath("//div[@class='condition property-select-holder']").click()
                browser.find_element_by_xpath("//div[@class='condition property-select-holder']").click()
            # Find the property type list
            if spider.property_type is not None:
                property_list = browser.find_element_by_xpath("//div[@class='condition property-select-holder']")
                property_list.click()
                # Choose the property type
                for property_type in spider.property_type:
                    property = browser.find_element_by_xpath("//div[@class='condition property-select-holder']/div/div/ul/li/input[@value='" + property_type + "']/parent::li")
                    property.click()
            # Min beds
            if spider.minbeds is not None:
                minbeds_list = browser.find_element_by_xpath("//div[@class='min beds select-holder']")
                minbeds_list.click()
                # Choose the min beds
                minbeds = browser.find_element_by_xpath("//div[@class='min beds select-holder']/div/ul/li[@data-value='"+ spider.minbeds +"']")
                minbeds.click()
            # Max beds
            if spider.maxbeds is not None:
                maxbeds_list = browser.find_element_by_xpath("//div[@class='max beds select-holder']")
                maxbeds_list.click()
                # Choose the max beds
                maxbeds = browser.find_element_by_xpath("//div[@class='max beds select-holder']/div/ul/li[@data-value='"+ spider.maxbeds +"']")
                maxbeds.click()

            # Click the search button
            search_button = browser.find_element_by_xpath("//button[@class='rui-search-button']")
            search_button.click()
            time.sleep(1)
            # Put first page into body
            body = browser.page_source
            while True:
                try:
                    # Click next page button
                    browser.find_element_by_link_text('Next').click()
                    time.sleep(1)
                    # Add next page into body
                    body += browser.page_source
                except selenium.common.exceptions.NoSuchElementException as e:
                    print ('Page crawling completed.')
                    break
            return HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
        else:
            return None
