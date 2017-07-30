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
            # Get the address, suburb, state, postcode and put them into meta data of the request
            address = pre.xpath("a/div/div/div[1]/span/text()").extract_first(default = '').strip()
            suburb = pre.xpath("a/div/div/div[2]/span[1]/text()").extract_first(default = '').strip()
            state = pre.xpath("a/div/div/div[2]/span[2]/text()").extract_first(default = '').strip()
            postcode = pre.xpath("a/div/div/div[2]/span[3]/text()").extract_first(default = '').strip()
            req = scrapy.Request(url, callback = self.parse_info)
            req.meta['address'] = address
            req.meta['suburb'] = suburb
            req.meta['state'] = state
            req.meta['postcode'] = postcode
            yield req

    def parse_info(self, response):
        items = RentinfoItem()
        pre_rent = response.xpath('//*[@id="main"]/div/header/div/div[1]/span/text()').re('\$\d*,?\d*')
        items['rent'] = pre_rent[0][1:].replace(',', '') if len(pre_rent) > 0 else '0'
        items['address'] = response.meta['address']
        items['suburb'] = response.meta['suburb']
        items['state'] = response.meta['state']
        items['postcode'] = response.meta['postcode']
        items['no_bedroom'] = response.xpath('//span[@class="icon domain-icon-ic_beds"][1]/following-sibling::span/em/text()').extract_first(default = '0').strip()
        items['no_bedroom'] = 0 if items['no_bedroom'] == '-' else items['no_bedroom']
        items['no_bathroom'] = response.xpath('//span[@class="icon domain-icon-ic_baths"][1]/following-sibling::span/em/text()').extract_first(default = '0').strip()
        items['no_bathroom'] = 0 if items['no_bathroom'] == '-' else items['no_bathroom']
        items['no_carspace'] = response.xpath('//span[@class="icon domain-icon-ic_cars"][1]/following-sibling::span/em/text()').extract_first(default = '0').strip()
        items['no_carspace'] = 0 if items['no_carspace'] == '-' else items['no_carspace']
        items['property_type'] = response.xpath('//*[@id="description"]/ul/li/strong/text()|//*[@id="description"]/ul[2]/li/strong/text()').extract_first(default = '').strip()
        pre_amenities = response.xpath('//h4[text()="Features"]/following-sibling::ul[1]/li/text()').extract()
        items['amenities'] = ' '.join(pre_amenities)
        yield items
