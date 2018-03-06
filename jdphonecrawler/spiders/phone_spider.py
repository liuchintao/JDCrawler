# -*- coding: utf-8 -*-

import scrapy
import re
from jdphonecrawler.items import PhoneItem
import json


class JdPhoneSpider(scrapy.Spider):
    name = 'jdphone'
    rotate_use_agent = True
    search_iPhone = r'https://search.jd.com/Search?keyword=iphone&enc=utf-8'
    start_urls = [search_iPhone, ]

    # def parse_comment(self, response):
    #     comment_item = PhoneCommentItem()
    #     summary_item = CommitSummaryItem()
    #     comment_item['pc_p_id'] = response.meta['p_id']
    #     content = response.text
    #     if content:
    #         content = json.loads(re.sub(r'fetchJSON_comment98vv52582\(', '', content)[:-2])
    #         for comment in content['comments']:
    #             comment_item['id'] = comment['id']
    #             comment_item['content'] = comment['content']

    #
    # def count_page_num(self, amount):
    #     ptn1 = re.compile('\d+\+')
    #     if not ptn1.match(amount):
    #         return 10
    #     else:
    #         n = int(re.search(r'\d+', amount).group())
    #         n = n / 10 + 10
    #         return n if n <= 100 else 100

    def parse_detail(self, response):
        item = response.meta['item']
        parameter_list = response.xpath('//div[@class="p-parameter"]//ul//text()').extract()
        ptn = re.compile(r'\S+\s*：*\S+')
        params = ""
        for param in parameter_list:
            if ptn.match(param):
                params = params + ptn.match(param).group() + ';'
        item['params'] = params
        return item
        # comment_url = r"https://club.jd.com/comment/productPageComments.action?" \
        #               r"callback=fetchJSON_comment98vv52582&productId=%d&score=0&sortType=5&" \
        #               r"page=%d&pageSize=10&isShadowSku=0&rid=0&fold=1"
        # page_num = int(self.count_page_num(item['p_commit'][0])) + 1
        # for i in range(page_num):
        #     yield scrapy.Request(comment_url % (int(item['p_id']), i), callback=self.parse_comment,
        #                          meta={'p_id': item['p_id']})
        #

    def parse(self, response):
        phones = response.xpath('//li[@class="gl-item"]')
        for phone in phones:
            pitem = PhoneItem()
            pitem['p_id'] = str(phone.xpath('./@data-sku').extract()[0])
            pitem['p_shop_url'] = phone.xpath('./div[@class="gl-i-wrap"]/div[@class="p-shop"]'
                                              '/span[@class="J_im_icon"]/a/@href').extract()
            pitem['p_shop'] = phone.xpath('./div[@class="gl-i-wrap"]/div[@class="p-shop"]/span[@class="J_im_icon"]'
                                          '/a/text()').extract()
            pitem['p_price'] = phone.xpath('./div[@class="gl-i-wrap"]/div[@class="p-price"]'
                                           '/strong/i/text()').extract()
            pitem['p_commit'] = phone.xpath('./div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong'
                                            '/a[contains(@id, "J_comment_")]/text()').extract()
            pitem['p_url'] = r"https://item.jd.com/" + pitem['p_id'] + r".html"
            yield scrapy.Request(pitem['p_url'], self.parse_detail, meta={'item': pitem})
