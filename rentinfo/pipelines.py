# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class RentinfoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into rental_data(rent, address, suburb, state, postcode, no_bedroom, no_bathroom, no_carspace, property_type, amenities) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['rent'], item['address'], item['suburb'], item['state'], item['postcode'], item['no_bedroom'], item['no_bathroom'], item['no_carspace'], item['property_type'], item['amenities'])
        tx.execute(sql, params)

    def _handle_error(self, failure, item, spider):
        print (failure)
