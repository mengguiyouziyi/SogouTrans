# encoding:utf-8
from .yd_api import YdApiSpider


class YOSzh2koSpider(YdApiSpider):
    name = 'yd_oral_single_zh2ko'

    def __init__(self, *args, **kwargs):
        super(YOSzh2koSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api口语zh2ko'
