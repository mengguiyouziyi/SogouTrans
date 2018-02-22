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
from scrapy.spiders import Spider
from scrapy.selector import Selector
# from scrapy.exceptions import CloseSpider
from scrapy.item import Item, Field
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class YDLijuItem(Item):
    # Primary fields
    src = Field()
    srcType = Field()
    zh = Field()
    en = Field()
    jp = Field()
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


class YDLijuSpider(Spider):
    # name = 'yd_liju_zh2fr'
    items = []
    # DEBUG INFO WARNING ERROR CRITICAL
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'connection': "keep-alive",
            'cookie': "JSESSIONID=abc8QNqnIEudc54rXVogw; _ntes_nnid=37654b69fb8068815e62ac8efce10e81,1518518343349; OUTFOX_SEARCH_USER_ID_NCOO=1581663191.8012152; OUTFOX_SEARCH_USER_ID=-1027152539@10.168.11.12",
            'host': "dict.youdao.com",
            'referer': "http://dict.youdao.com/w/fr/lj%3A%E6%88%91%E4%BB%AC/",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "b5e3aaf6-e291-55db-5c0e-01c0d36c3a2a"
        },
        'DOWNLOAD_DELAY': 3,
        'LOG_LEVEL': 'INFO'

    }

    def __init__(self, settings, *args, **kwargs):
        super(YDLijuSpider, self).__init__(*args, **kwargs)
        self.settings = settings
        self.uas = settings['USER_AGENT_CHOICES']
        self.col_comm = self.settings['SPIDER_CONF'][self.name]['col_comm']
        self.col_dict = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = self.settings['SPIDER_CONF'][self.name]['col_index_list']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = self.settings['SPIDER_CONF'][self.name]['tab_desc']  # 表格功能描述
        lang_dict = settings['LANG'][self.name[:2]]
        self.lsrc = kwargs.get('src', '')  # 标准语言简称
        self.ltgt = kwargs.get('tgt', '')
        self.src = lang_dict[self.lsrc]  # 各网站自己的语言标识
        self.tgt = lang_dict[self.ltgt]
        self.url = 'http://dict.youdao.com/w/{tgt}/lj%3A{word}/'
        self.ip = self._get_host_ip()
        self.cookie = self._get_cookie()
        self.request_key = '%(name)s:requests' % {'name': self.name}
        self.error_key = '%(name)s:errors' % {'name': self.name}

        self.redisparams = dict(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            decode_responses=True
        )
        self.server = self._get_redis()
        self.d = {}.fromkeys(self.col_dict.keys(), '')  # 用于item初始化

    def _get_cookie(self):
        url = 'http://fanyi.youdao.com/'
        uas = self.settings.get('USER_AGENT_CHOICES', [])
        headers = {'User-Agent': random.choice(uas)}
        while 1:
            try:
                response = requests.get(url=url, headers=headers)
            except:
                time.sleep(3)
                continue
            break
        cookie_dict = dict(response.cookies.items())
        return cookie_dict

    def _get_redis(self):
        return StrictRedis(**self.redisparams)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler.settings, *args, **kwargs)

    def start_requests(self):
        while 1:
            line = self.server.rpop(self.request_key)
            if not line:
                self.logger.info('No datas, close spider...')
                return
                # raise CloseSpider('No datas, close spider...')
            else:
                yield Request(self.url.format(tgt=self.tgt, word=line), callback=self.parse_httpbin,
                              headers={'User-Agent': random.choice(self.uas)}, meta={'line': line}, cookies=self.cookie,
                              errback=self.errback_httpbin)

    def _lpush(self, key, l):
        if len(l) > 1:
            for line in l.split('\n'):
                self.server.lpush(key, line.strip())
        elif len(l) == 1:
            self.server.lpush(key, l.strip())
        else:
            self.logger.error('No provided line to push redis!')
            return

    def parse_httpbin(self, response):
        line = response.meta.get('line')
        s = Selector(text=response.text)
        lis = s.xpath('//*[@class="ol"]/li')
        if '当前分类下找不到' in response.text:
            self.logger.info('No example sentence on %s', line)
            return
        # if len(lis.extract()) < 1:
        #     self.logger.error('Error cause no example sentence on %s', line)
        #     self._lpush(self.request_key, line)
        #     return
        for li in lis:
            sour = li.xpath('./p[1]//text()').extract()
            sour = ''.join(sour).strip()
            tran = li.xpath('./p[2]//text()').extract()
            tran = ''.join(tran).strip()
            if tran == '':
                self.logger.error('empty on %s', line)
                self._lpush(self.request_key, line)
                return
            item = YDLijuItem()
            item.update(self.d)
            item['src'] = sour
            item['srcType'] = self.lsrc  # 源语言类型
            item[self.ltgt] = tran
            item['url'] = response.url
            # item['project'] = self.settings.get('BOT_NAME')
            # item['spider'] = self.name
            item['server'] = self.ip
            yield item

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        line = failure.request.meta.get('line')
        self._lpush(self.request_key, line)
        # log all failures
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            # response = failure.value.response
            self.logger.error('HttpError on %s', line)
        elif failure.check(DNSLookupError):
            # this is the original request
            # request = failure.request
            self.logger.error('DNSLookupError on %s', line)
        elif failure.check(TimeoutError, TCPTimedOutError):
            # request = failure.request
            self.logger.error('TimeoutError on %s', line)
        else:
            self.logger.error('UnknowError on %s', line)

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


class YDLijuZhFrSpider(YDLijuSpider):
    name = 'yd_liju_zh2fr'

    def __init__(self, *args, **kwargs):
        super(YDLijuZhFrSpider, self).__init__(*args, **kwargs)


class YDLijuZhKoSpider(YDLijuSpider):
    name = 'yd_liju_zh2ko'

    def __init__(self, *args, **kwargs):
        super(YDLijuZhKoSpider, self).__init__(*args, **kwargs)


class YDLijuZhJpSpider(YDLijuSpider):
    name = 'yd_liju_zh2jp'

    def __init__(self, *args, **kwargs):
        super(YDLijuZhJpSpider, self).__init__(*args, **kwargs)
