# encoding:utf-8
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)
import scrapy
import socket
from urllib.parse import urljoin
from collections import OrderedDict
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapyProject.items import PaiziItem


class PaiziSpider(Spider):
    name = 'paizi'
    items = []
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            # 'cookie': "__cfduid=d1596eb7074094ff50d4bb83d90198cf41517381642; Hm_lvt_026db5c3c3a31c50553b1821c989f465=1517381643; UM_distinctid=1614afe6a90a5-043ab32cc16937-3c604504-1fa400-1614afe6a917c0; amvid=469a0cb6eaf5e2fa88ce502c624ffefc; CNZZDATA1261571158=2111473164-1517378720-%7C1517467442; Hm_lpvt_026db5c3c3a31c50553b1821c989f465=1517468664",
            'host': "i.paizi.com",
            'referer': "https://i.paizi.com/",
            'upgrade-insecure-requests': "1",
        },
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': False,
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    }

    def __init__(self, crawler, *args, **kwargs):
        super(PaiziSpider, self).__init__(*args, **kwargs)
        self.col_comm = {'brand': '品牌名', 'brand_url': '品牌详情页url', 'categary': '行业类别', 'company': '公司', 'url': 'url',
                         'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
        self.col_dict = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = ['brand']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = 'pazi品牌名称'
        self.ip = self._get_host_ip()
        self.settings = crawler.settings
        self.d = {}.fromkeys(self.col_dict.keys(), '')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler, *args, **kwargs)

    def _get_host_ip(self):
        """
        获取当前网络环境的ip地址
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def start_requests(self):
        burl = 'https://i.paizi.com/dp-{xx}-{yy}'
        urls = [[burl.format(xx=chr(xx), yy=yy) for xx in range(97, 123)] for yy in range(1, 12)]
        urls.append('https://i.paizi.com/dp-shu')
        for url in urls:
            yield scrapy.Request(url)

    def parse(self, response):
        s = Selector(text=response.text)
        lis = s.xpath('//*[@class="c03-3-1"]/ul/li')
        if len(lis.extract()) == 0:
            return
        for li in lis:
            # brand = li.xpath('./a/text()').extract_first()
            brand_url = li.xpath('./a/@href').extract_first()
            brand_url = urljoin(response.url, brand_url)
            yield scrapy.Request(brand_url, callback=self.parse_detail)

    def parse_detail(self, response):
        s = Selector(text=response.text)
        brand = s.xpath('//*[@class="c02-1-2-1 sty-l"]/p[2]/text()')
        item = PaiziItem()
        item.update(self.d)
        item['brand'] = brand
        item['brand_url'] = response.url  # 源语言类型
        # item['url'] = response.url
        item['project'] = self.settings.get('BOT_NAME')
        item['spider'] = self.name
        item['server'] = self.ip
        yield item
