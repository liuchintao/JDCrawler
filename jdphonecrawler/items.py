# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class JdphonecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PhoneItem(scrapy.Item):
    p_id = Field()#京东商品id
    p_shop_url = Field()#商品所在商店地址
    p_shop = Field()#商品所在商店
    p_price = Field()#商品价格
    p_url = Field()#商品地址
    params = Field()#商品属性
    p_commit = Field()#商品评论总数


