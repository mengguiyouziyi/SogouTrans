# encoding:utf-8
from .yd_api import YdApiSpider


class YOSzh2jaSpider(YdApiSpider):
    name = 'yd_news_single_zh2ru'

    def __init__(self, *args, **kwargs):
        super(YOSzh2jaSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api新闻zh2ru'
