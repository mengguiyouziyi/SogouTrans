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
    col_list = {'src': '源语言', 'srcType': '源语言种类', 'zh': '中文', 'en': '英文', 'ja': '日语', 'ko': '韩语', 'fr': '法语',
                'ru': '俄语', 'es': '西班牙语', 'pt': '葡萄牙语', 'ara': '阿拉伯语', 'de': '德语', 'it': '意大利语', 'url': 'url',
                'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
    col_index_list = ['src']
    tab_desc = '有道翻译'
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
    # images = Field()
    # location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
