# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class LtnItem(Item):
    url = Field()
    title = Field()
    text = Field()


class YdApiItem(Item):
    # Primary fields
    src = Field()
    srcType = Field()
    zh = Field()
    en = Field()
    ja = Field()
    ko = Field()
    fr = Field()
    ru = Field()
    es = Field()
    pt = Field()
    ara = Field()
    de = Field()
    it = Field()

    # Calculated fields
    images = Field()
    location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
