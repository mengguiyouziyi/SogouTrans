# encoding:utf-8
from .sg_api import SgApiSpider


class YOSzh2jaSpider(SgApiSpider):
    name = 'sg_news_zh2jp'

    def __init__(self, *args, **kwargs):
        super(YOSzh2jaSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '搜狗api新闻zh2jp'
