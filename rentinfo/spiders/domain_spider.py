# -*- coding: utf-8 -*-
import scrapy
from rentinfo.items import RentinfoItem

class DomainSpider(scrapy.Spider):
    name = 'domain_spider'

    def __init__(self, channel = 'rent', location = None, property_type = None,
            bedrooms = None, bathrooms = None, *args, **kwargs):
        super(DomainSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['domain.com.au']
        self.start_urls = ['https://www.domain.com.au']
        self.channel = channel
        self.location = location
        self.property_type = property_type.split(',') if property_type is not None else property_type
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms

    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
        "Referer": "https://www.domain.com.au",
    }

    def start_requests(self):
        reqs = []
        for url in self.start_urls:
            req = scrapy.Request(url, headers = self.post_headers)
            req.meta['Selenium'] = True
            reqs.append(req)
        return reqs

    def parse(self, response):
        #调试response
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # Get the proerty info url
        for sel in response.xpath("//li[@class='strap new-listing']"):
            pre = sel.xpath("div/div/div/h2|div/div/div/div/h2|div/div")
            url = pre.xpath("a/@href").extract_first(default = 'not found').strip()
            print (url)
            # yield scrapy.Request(url, callback = self.parse_info)

    def parse_info(self, response):
        items = RentinfoItem()
        items['rent'] = 0
        items['address'] = 1
        items['suburb'] = 2
        items['state'] = 3
        items['postcode'] = 4
        items['no_bedroom'] = 5
        items['no_bathroom'] = 6
        items['no_carspace'] = 7
        items['property_type'] = 8
        items['amenities'] = 9
        yield items
