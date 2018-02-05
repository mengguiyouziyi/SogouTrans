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
import json
import hashlib
import time
import socket
import random
import requests
from collections import OrderedDict
from redis import StrictRedis
from urllib.parse import urlencode
from scrapy.spiders import Spider
from scrapy.exceptions import CloseSpider
# from scrapyProject.items import YdApiItem
from scrapy.item import Item, Field
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class YdApiItem(Item):
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


class YdApiSpider(Spider):
    # name = 'yd_oral_zh2ko'
    items = []
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'referer': "http://fanyi.youdao.com/",
        },
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self, settings, *args, **kwargs):
        super(YdApiSpider, self).__init__(*args, **kwargs)
        self.col_comm = settings['yd_oral_zh2ko']['col_comm']
        self.col_dict = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = settings['yd_oral_zh2ko']['col_index_list']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = settings['yd_oral_zh2ko']['tab_desc']  # 表格功能描述

        self.src = kwargs.get('src', 'zh')
        self.tgt = kwargs.get('tgt', 'ja')
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.ip = self._get_host_ip()
        self.cookie_dict = self._get_cookie()

        self.cookie_key = '%(name)s:cookies' % {'name': self.name}
        self.request_key = '%(name)s:requests' % {'name': self.name}
        self.error_key = '%(name)s:errors' % {'name': self.name}

        self.redisparams = dict(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            decode_responses=True
        )
        self.server = self._get_redis()
        self.server.sadd(self.cookie_key, json.dumps(self.cookie_dict, ensure_ascii=False))
        self.cookie = json.loads(self.server.srandmember(self.cookie_key))
        self.d = {}.fromkeys(self.col_dict.keys(), '')

    def _get_redis(self):
        return StrictRedis(**self.redisparams)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler.settings, *args, **kwargs)

    def start_requests(self):
        while 1:
            # try:
            #     line = self.server.rpop(self.request_key)
            # except:
            #     self.server = self._get_redis()
            #     continue
            line = self.server.rpop(self.request_key)
            if not line:
                raise CloseSpider('no datas')
            data = self._get_params(line)
            yield scrapy.Request(self.url, method='POST', body=urlencode(data), cookies=self.cookie,
                                 meta={'line': line}, callback=self.parse_httpbin, errback=self.errback_httpbin)

    def _get_params(self, line):
        salf = str(int(time.time() * 1000) + random.randint(1, 10))
        n = 'fanyideskweb' + line + salf + "aNPG!!u6sesA>hBAW1@(-"
        sign = hashlib.md5(n.encode('utf-8')).hexdigest()
        f = lambda x: 'zh-CHS' if x == 'zh' else x
        data = {
            'i': line,
            'from': f(self.src),
            'to': f(self.tgt),
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salf,
            'sign': sign,
            'doctype': 'json',
            'version': "2.1",
            'keyfrom': "fanyi.web",
            'action': "FY_BY_REALTIME",
            'typoResult': 'false'
        }
        return data

    # def _lpush(self, key, line):
    #     while 1:
    #         try:
    #             self.server.lpush(key, line.strip())
    #         except:
    #             self.server = self._get_redis()
    #             continue
    #         break

    def _lpush(self, key, line):
        self.server.lpush(key, line.strip())

    def parse_httpbin(self, response):
        line = response.meta.get('line')
        # -------------- 以下三种情况都会重新打入redis ---------------------
        try:
            resp = json.loads(response.text)
        except Exception as e:
            self.logger.error(repr(e))
            self.logger.error('JsonLoadsError on %s', line)
            self._lpush(self.error_key, line)
            return
        if resp.get('errorCode') != 0:
            self.logger.error(repr(response.text))
            self._lpush(self.request_key, line)
            return
        results = resp.get('translateResult', [])
        if not results:
            self.logger.error(repr(response.text))
            self._lpush(self.request_key, line)
            return
        for result in results:
            item = YdApiItem()
            trans = sours = ''
            for dict_rt in result:
                t = dict_rt.get('tgt', '')
                s = dict_rt.get('src', '')
                trans += t  # 此循环结束后，此行拼接完成
                sours += s
            item.update(self.d)
            item['src'] = sours
            item['srcType'] = self.src  # 源语言类型
            item[self.tgt] = trans
            # item['url'] = response.url
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


class YdNewsZhEsSpider(YdApiSpider):
    name = 'yd_news_zh2es'

    def __init__(self, *args, **kwargs):
        super(YdNewsZhEsSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api新闻zh2es'


class YdNewsZhFrSpider(YdApiSpider):
    name = 'yd_news_zh2fr'

    def __init__(self, *args, **kwargs):
        super(YdNewsZhFrSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api新闻zh2fr'


class YdNewsZhRuSpider(YdApiSpider):
    name = 'yd_news_zh2ru'

    def __init__(self, *args, **kwargs):
        super(YdNewsZhRuSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api新闻zh2ru'


class YdOralZhEsSpider(YdApiSpider):
    name = 'yd_oral_zh2es'

    def __init__(self, *args, **kwargs):
        super(YdOralZhEsSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api口语zh2es'


class YdOralZhFrSpider(YdApiSpider):
    name = 'yd_oral_zh2fr'

    def __init__(self, *args, **kwargs):
        super(YdOralZhFrSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api口语zh2fr'


class YdOralZhRuSpider(YdApiSpider):
    name = 'yd_oral_zh2ru'

    def __init__(self, *args, **kwargs):
        super(YdOralZhRuSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api口语zh2ru'


class YdOralZhJaSpider(YdApiSpider):
    name = 'yd_oral_zh2ja'

    def __init__(self, *args, **kwargs):
        super(YdOralZhJaSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api口语zh2ja'


class YdOralZhKoSpider(YdApiSpider):
    name = 'yd_oral_zh2ko'

    def __init__(self, *args, **kwargs):
        super(YdOralZhKoSpider, self).__init__(*args, **kwargs)
        # self.tab_desc = '有道api口语zh2ko'
