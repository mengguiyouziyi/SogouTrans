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
import socket
import random
import requests
import time
from collections import OrderedDict
from redis import StrictRedis
from scrapy import Request
from urllib.parse import urljoin
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from scrapy.item import Item, Field
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class YDLijuItem(Item):
    # Primary fields
    title = Field()
    job_cat1 = Field()
    city = Field()
    experience = Field()
    employ_way = Field()
    num = Field()
    item_title = Field()
    job_cat2 = Field()
    jd = Field()
    # Calculated fields
    # images = Field()
    # location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()


class YDLijuSpider(Spider):
    name = 'sg_job'
    items = []
    # DEBUG INFO WARNING ERROR CRITICAL
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "PHPSESSID=hn3o7vasspbu4qb0fitpmbk576; _pk_id.65.6b53=871115b67f1fed87.1518515241.1.1518515281.1518515241.",
            'host': "sogou.ourats.com",
            'referer': "http://sogou.ourats.com/internal-referral/reqdetails/?id=3544",
            'upgrade-insecure-requests': "1",
        },
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG'

    }

    def __init__(self, settings, *args, **kwargs):
        super(YDLijuSpider, self).__init__(*args, **kwargs)
        self.settings = settings
        self.uas = settings['USER_AGENT_CHOICES']
        self.col_comm = self.settings['SPIDER_CONF'][self.name]['col_comm']
        self.col_dict = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = self.settings['SPIDER_CONF'][self.name]['col_index_list']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = self.settings['SPIDER_CONF'][self.name]['tab_desc']  # 表格功能描述
        self.url = 'http://sogou.ourats.com/internal-referral/reqs/?page={}'
        self.ip = self._get_host_ip()
        # self.cookie = self._get_cookie()
        # self.request_key = '%(name)s:requests' % {'name': self.name}
        # self.error_key = '%(name)s:errors' % {'name': self.name}
        # self.redisparams = dict(
        #     host=settings['REDIS_HOST'],
        #     port=settings['REDIS_PORT'],
        #     decode_responses=True
        # )
        # self.server = self._get_redis()
        self.d = {}.fromkeys(self.col_dict.keys(), '')  # 用于item初始化

    # def _get_cookie(self):
    #     url = 'http://fanyi.youdao.com/'
    #     uas = self.settings.get('USER_AGENT_CHOICES', [])
    #     headers = {'User-Agent': random.choice(uas)}
    #     while 1:
    #         try:
    #             response = requests.get(url=url, headers=headers)
    #         except:
    #             time.sleep(3)
    #             continue
    #         break
    #     cookie_dict = dict(response.cookies.items())
    #     return cookie_dict

    # def _get_redis(self):
    #     return StrictRedis(**self.redisparams)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler.settings, *args, **kwargs)

    def start_requests(self):
        for page in range(1, 43):
            yield Request(self.url.format(page), callback=self.parse_httpbin,
                          headers={'User-Agent': random.choice(self.uas)},
                          errback=self.errback_httpbin)

    # def _lpush(self, key, l):
    #     if len(l) > 1:
    #         for line in l.split('\n'):
    #             self.server.lpush(key, line.strip())
    #     elif len(l) == 1:
    #         self.server.lpush(key, l.strip())
    #     else:
    #         self.logger.error('No provided line to push redis!')
    #         return

    def parse_httpbin(self, response):
        s = Selector(text=response.text)
        lis = s.xpath('//*[@class="job_list fix"]/ul/li[postion()>1]')
        for li in lis:
            title = li.xpath('./span/@title').extract_first()
            job_cat1 = li.xpath('./p/text()').extract_first()
            city = li.xpath('./i/text()').extract_first()
            experience = li.xpath('./em/text()').extract_first()
            employ_way = li.xpath('./b/text()').extract_first()
            num = li.xpath('./h1/text()').extract_first()
            url = urljoin(response.url, li.xpath('./a/@href').extract_first())
            item = YDLijuItem()
            item.update(self.d)
            item['title'] = title
            item['job_cat1'] = job_cat1
            item['city'] = city
            item['experience'] = experience
            item['employ_way'] = employ_way
            item['num'] = num
            yield Request(url, callback=self.parse_detail, meta={'item': item},
                          headers={'User-Agent': random.choice(self.uas)}, errback=self.errback_httpbin)

    def parse_detail(self, response):
        s = Selector(text=response.text)
        info = s.xpath('//*[@class="info"]')
        item_title = info.xpath('./span[1]/text()').extract_first()
        job_cat2 = info.xpath('./span[1]/text()').extract_first()
        jd = ''.join(s.xpath('//*[@id="req-jd"]//text()').extract()).strip()
        item = response.meta.get('item')
        item['item_title'] = item_title
        item['job_cat2'] = job_cat2
        item['jd'] = jd

        item['url'] = response.url
        item['project'] = self.settings.get('BOT_NAME')
        item['spider'] = self.name
        item['server'] = self.ip
        yield item

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
        else:
            request = failure.request
            self.logger.error('UnknowError on %s', request.url)

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
