# -*- coding: utf-8 -*-
import scrapy
from rentinfo.items import RentinfoItem

class RealestateSpider(scrapy.Spider):
    name = 'realestate_spider'

    def __init__(self, channel = 'rent', location = None, property_type = None,
            minbeds = None, maxbeds = None, *args, **kwargs):
        super(RealestateSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['realestate.com.au']
        self.start_urls = ['https://www.realestate.com.au']
        self.channel = channel
        self.location = location
        self.property_type = property_type.split(',') if property_type is not None else property_type
        self.minbeds = minbeds
        self.maxbeds = maxbeds

    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
        "Referer": "https://www.realestate.com.au",
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
        for property in response.xpath('//article'):
            # 3 xpath to extract url
            pre = property.xpath("div[@class='listingInfo rui-clearfix']|aside/div[@class='listingInfo rui-clearfix']|div[@class='listing-content resultBodyWrapper']/div[@class='listingInfo rui-clearfix']")
            url = pre.xpath("div[@class='vcard']/h2/a/@href").extract_first(default = 'not found').strip()
            full_url = self.start_urls[0] + url
            print (full_url)
            yield scrapy.Request(full_url, callback = self.parse_info)

    def parse_info(self, response):
        items = RentinfoItem()
        pre_rent = response.xpath('//*[@id="listing_info"]/ul/li[2]/p/text()').re('\$\d*')
        items['rent'] = pre_rent[0][1:] if len(pre_rent) > 0 else '0'
        items['address'] = response.xpath('//*[@id="listing_address"]/h1/span[1]/text()').extract_first(default = '').strip()
        items['suburb'] = response.xpath('//*[@id="listing_address"]/h1/span[2]/text()').extract_first(default = '').strip()
        items['state'] = response.xpath('//*[@id="listing_address"]/h1/span[3]/text()').extract_first(default = '').strip()
        items['postcode'] = response.xpath('//*[@id="listing_address"]/h1/span[4]/text()').extract_first(default = '').strip()
        items['no_bedroom'] = response.xpath('//dt[@class="rui-icon rui-icon-bed"]/following-sibling::dd[1]/text()').extract_first(default = '0').strip()
        items['no_bathroom'] = response.xpath('//dt[@class="rui-icon rui-icon-bath"]/following-sibling::dd[1]/text()').extract_first(default = '0').strip()
        items['no_carspace'] = response.xpath('//dt[@class="rui-icon rui-icon-car"]/following-sibling::dd[1]/text()').extract_first(default = '0').strip()
        items['property_type'] = response.xpath('//*[@id="listing_info"]/ul/li[1]/span/text()').extract_first(default = '').strip()
        items['amenities'] = response.xpath('//*[@id="features"]/div[2]/div/ul[2]/li[2]/text()').extract_first(default = '').strip()
        yield items
