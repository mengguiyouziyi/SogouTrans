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
# from scrapyProject.items import PaiziItem
from scrapy.item import Item, Field
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ChinaEfItem(Item):
    # Primary fields
    brand_zh = Field()
    brand_en = Field()
    style = Field()
    comp_link = Field()
    addr = Field()
    brand_url = Field()
    categary = Field()
    company = Field()

    # Calculated fields
    # images = Field()
    # location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()


class PaiziSpider(Spider):
    name = 'china_ef'
    items = []
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            # 'cookie': "__cfduid=d47b541d128fbc6add11ea7f8e87f2e9d1517381654; Hm_lvt_d1ee41a7bd599b11abed3a7121f69480=1517381656; ctrl_time=1; yjs_id=56a61b15fdeb81013d0ea10be1803bf5; Hm_lpvt_d1ee41a7bd599b11abed3a7121f69480=1517489631",
            'host': "www.china-ef.com",
            'upgrade-insecure-requests': "1",
        },
        'DOWNLOAD_DELAY': 1.5,
        'COOKIES_ENABLED': False,
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'RETRY_TIMES': 5,
        'DOWNLOAD_TIMEOUT': 300
    }

    def __init__(self, *args, **kwargs):
        super(PaiziSpider, self).__init__(*args, **kwargs)
        self.col_comm = {'brand_zh': '中文品牌名', 'brand_en': '英文品牌名', 'style': '品牌风格', 'comp_link': '公司官网', 'addr': '地址',
                         'brand_url': '品牌详情页url', 'categary': '行业类别', 'company': '公司', 'url': 'url', 'project': '工程名',
                         'spider': '爬虫名', 'server': 'ip'}
        self.col_dict = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = ['brand_zh']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = 'china-ef品牌名称'
        self.ip = self._get_host_ip()
        # self.settings = self.crawler.settings
        self.d = {}.fromkeys(self.col_dict.keys(), '')

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
        burl = 'http://www.china-ef.com/brand/list-0-0-0-0-0-0-{}.html'
        urls = [burl.format(x) for x in range(1, 3827)]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_httpbin,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    def parse_httpbin(self, response):
        s = Selector(text=response.text)
        urls = s.xpath('//div[@class="pic-tit"]/a/@href').extract()
        for url in urls:
            brand_url = urljoin(response.url, url)
            yield scrapy.Request(brand_url, callback=self.parse_detail)

    def parse_detail(self, response):
        s = Selector(text=response.text)
        tbody = s.xpath('//*[@class="contact-left"]/table/tbody')
        brand_zh = tbody.xpath('./tr[1]/td[2]/text()').extract()
        brand_en = tbody.xpath('./tr[2]/td[2]/text()').extract()
        categary = tbody.xpath('./tr[3]/td[2]/text()').extract()
        style = tbody.xpath('./tr[4]/td[2]/text()').extract()
        company = tbody.xpath('./tr[5]/td[2]/text()').extract()
        comp_link = tbody.xpath('./tr[6]/td[2]/text()').extract()
        addr = tbody.xpath('./tr[7]/td[2]/text()').extract()

        item = ChinaEfItem()
        item.update(self.d)

        item['brand_zh'] = ''.join(brand_zh).strip()
        item['brand_en'] = ''.join(brand_en).strip()
        item['categary'] = ''.join(categary).strip()
        item['style'] = ''.join(style).strip()
        item['company'] = ''.join(company).strip()
        item['comp_link'] = ''.join(comp_link).strip()
        item['addr'] = ''.join(addr).strip()

        item['brand_url'] = response.url  # 源语言类型
        # item['url'] = response.url
        item['project'] = self.settings.get('BOT_NAME')
        item['spider'] = self.name
        item['server'] = self.ip
        yield item

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
