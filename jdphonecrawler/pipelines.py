# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from jdphonecrawler.items import PhoneItem


class JdphonecrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class PhonePipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=settings['PHONE_SERVER'], port=settings['PHONE_PORT'])
        client.admin.authenticate(settings['PHONE_USER'], settings["PHONE_PWD"])
        db = client[settings['PHONE_DB']]
        self.phone_coll = db[settings['PHONE_COLLECTION']]

    def process_item(self, item, spider):
        if isinstance(item, PhoneItem):
            self.phone_coll.insert(dict(item))
        return item

