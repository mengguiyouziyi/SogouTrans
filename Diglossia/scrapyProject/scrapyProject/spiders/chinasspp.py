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
from collections import OrderedDict
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapyProject.items import ChinassppItem


class ChinassppSpider(Spider):
    name = 'chinasspp'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            # 'cookie': "__cfduid=d379e46a2529cc430e2f04ecfcae937351517381359; ASP.NET_SessionId=l3fqyt45yo2ukd550ztfp0bs; UM_distinctid=1614afa1a24483-06b9cb63892e6f-3c604504-1fa400-1614afa1a259cf; CNZZDATA538723=cnzz_eid%3D1536902815-1517381038-%26ntime%3D1517381038; yjs_id=7e80921c93ac6993642327ccd659e1eb; ctrl_time=1; CNZZDATA3858846=cnzz_eid%3D1652662703-1517377065-%26ntime%3D1517382465",
            'host': "www.chinasspp.com",
            'referer': "http://www.chinasspp.com/brand/brands-3.html",
            'upgrade-insecure-requests': "1",
        },
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': False,
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    }

    def __init__(self, crawler, *args, **kwargs):
        super(ChinassppSpider, self).__init__(*args, **kwargs)
        self.col_comm = {'brand': '品牌名', 'brand_url': '品牌详情页url', 'categary': '行业类别', 'company': '公司', 'url': 'url',
                         'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
        self.col_list = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = ['brand']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = 'chinasspp品牌名称'
        self.ip = self._get_host_ip()
        self.settings = crawler.settings
        self.d = {}.fromkeys(self.col_list.keys(), '')

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
        burl = 'http://www.chinasspp.com/brand/brands-'
        for i in range(1, 1593):
            url = burl + str(i) + '.html'
            yield scrapy.Request(url, callback=self.parse_httpbin, errback=self.errback_httpbin)

    def parse_httpbin(self, response):
        s = Selector(text=response.text)
        firsts = s.xpath('//*[@class="first"]')
        for first in firsts:
            brand = first.xpath('./a/text()').extract_first()
            brand_url = first.xpath('./a/@href').extract_first()
            categary = first.xpath('./span/text()').extract_first()
            company = first.xpath('./text()').extract()
            company = ''.join(company).strip()
            item = ChinassppItem()
            item.update(self.d)
            item['brand'] = brand
            item['brand_url'] = brand_url  # 源语言类型
            item['categary'] = categary.replace('行业类别：', '')
            item['company'] = company.strip()
            # item['url'] = response.url
            item['project'] = self.settings.get('BOT_NAME')
            item['spider'] = self.name
            item['server'] = self.ip
            yield item

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
