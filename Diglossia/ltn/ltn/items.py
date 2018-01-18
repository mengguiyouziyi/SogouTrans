# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LtnItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()


class YdApiItem(scrapy.Item):
    src = scrapy.Field()
    srcType = scrapy.Field()
    zh = scrapy.Field()
    en = scrapy.Field()
    ja = scrapy.Field()
    ko = scrapy.Field()
    fr = scrapy.Field()
    ru = scrapy.Field()
    es = scrapy.Field()
    pt = scrapy.Field()
    ara = scrapy.Field()
    de = scrapy.Field()
    it = scrapy.Field()
