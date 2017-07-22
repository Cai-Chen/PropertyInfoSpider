# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rent = scrapy.Field()
    address = scrapy.Field()
    suburb = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    no_bedroom = scrapy.Field()
    no_bathroom = scrapy.Field()
    no_carspace = scrapy.Field()
    property_type = scrapy.Field()
    amenities = scrapy.Field()
