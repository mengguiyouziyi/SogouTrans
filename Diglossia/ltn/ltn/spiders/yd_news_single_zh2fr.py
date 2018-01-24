# encoding:utf-8
from .yd_api import YdApiSpider


class YOSzh2jaSpider(YdApiSpider):
    name = 'yd_news_single_zh2fr'

    def __init__(self, *args, **kwargs):
        super(YOSzh2jaSpider, self).__init__(*args, **kwargs)
        self.col_list = {'src': '源语言', 'srcType': '源语言种类', 'zh': '中文', 'en': '英文', 'ja': '日语', 'ko': '韩语', 'fr': '法语',
                         'ru': '俄语', 'es': '西班牙语', 'pt': '葡萄牙语', 'ara': '阿拉伯语', 'de': '德语', 'it': '意大利语', 'url': 'url',
                         'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
        self.col_index_list = ['src']
        self.tab_desc = '有道api新闻zh2fr'
