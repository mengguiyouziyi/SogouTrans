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
from scrapyProject.items import YdApiItem


class YdApiSpider(Spider):
    # name = 'yd_oral_zh2ko'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'referer': "http://fanyi.youdao.com/",
        },
        'DOWNLOAD_DELAY': 1.7
    }

    def __init__(self, crawler, src, tgt, *args, **kwargs):
        super(YdApiSpider, self).__init__(*args, **kwargs)
        self.col_comm = {'src': '源语言', 'srcType': '源语言种类', 'zh': '中文', 'en': '英文', 'ja': '日语', 'ko': '韩语', 'fr': '法语',
                         'ru': '俄语', 'es': '西班牙语', 'pt': '葡萄牙语', 'ara': '阿拉伯语', 'de': '德语', 'it': '意大利语', 'url': 'url',
                         'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
        self.col_list = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = ['src']  # 为创建mysql表格的index而设置的属性
        self.src = src
        self.tgt = tgt
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.ip = self._get_host_ip()
        self.settings = crawler.settings
        self.server = StrictRedis(host=self.settings.get('REDIS_HOST'), decode_responses=True)
        self.cookie_dict = self._get_cookie()
        self.cookie_key = '%(name)s:cookies' % {'name': self.name}
        self.request_key = '%(name)s:requests' % {'name': self.name}
        self.error_key = '%(name)s:errors' % {'name': self.name}
        self.server.sadd(self.cookie_key, json.dumps(self.cookie_dict, ensure_ascii=False))
        self.cookie = self.server.srandmember(self.cookie_key)
        # self.item_keys = ['src', 'srcType', 'zh', 'en', 'ja', 'ko', 'fr', 'ru', 'es', 'pt', 'ara', 'de', 'it', 'url',
        #                   'project', 'spider', 'server']
        self.d = {}.fromkeys(self.col_list.keys(), '')

    def _get_cookie(self):
        url = 'http://fanyi.youdao.com/'
        uas = self.settings.get('USER_AGENT_CHOICES', [])
        headers = {'User-Agent': random.choice(uas)}
        response = requests.get(url=url, headers=headers)
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

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler, *args, **kwargs)

    def start_requests(self):
        while 1:
            line = self.server.rpop(self.request_key)
            if not line:
                raise CloseSpider('no datas')
            salf, n, sign, data = self._get_params(line)
            yield scrapy.Request(self.url, method='POST', body=urlencode(data), cookies=json.loads(self.cookie),
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
        return salf, n, sign, data

    def parse_httpbin(self, response):
        line = response.meta.get('line')
        # -------------- 以下三种情况都会重新打入redis ---------------------
        try:
            resp = json.loads(response.text)
        except Exception as e:
            self.logger.error(repr(e))
            self.logger.error('JsonLoadsError on %s', line)
            self.server.lpush(self.error_key, line.strip())
            return
        if resp.get('errorCode') != 0:
            self.logger.error(repr(response.text))
            self.server.lpush(self.error_key, line.strip())
            return
        results = resp.get('translateResult', [])
        if not results:
            self.logger.error(repr(response.text))
            self.server.lpush(self.error_key, line.strip())
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
        self.logger.error('TimeOutError on %s', line)
        self.server.lpush(self.request_key, line.strip())


class YdNewsZhEsSpider(YdApiSpider):
    name = 'yd_news_zh2es'

    def __init__(self, *args, **kwargs):
        super(YdNewsZhEsSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api新闻zh2es'


class YdNewsZhFrSpider(YdApiSpider):
    name = 'yd_news_zh2fr'

    def __init__(self, *args, **kwargs):
        super(YdNewsZhFrSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api新闻zh2fr'


class YdNewsZhRuSpider(YdApiSpider):
    name = 'yd_news_zh2ru'

    def __init__(self, *args, **kwargs):
        super(YdNewsZhRuSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api新闻zh2ru'


class YdOralZhEsSpider(YdApiSpider):
    name = 'yd_oral_zh2es'

    def __init__(self, *args, **kwargs):
        super(YdOralZhEsSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api口语zh2es'


class YdOralZhFrSpider(YdApiSpider):
    name = 'yd_oral_zh2fr'

    def __init__(self, *args, **kwargs):
        super(YdOralZhFrSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api口语zh2fr'


class YdOralZhRuSpider(YdApiSpider):
    name = 'yd_oral_zh2ru'

    def __init__(self, *args, **kwargs):
        super(YdOralZhRuSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api口语zh2ru'


class YdOralZhJaSpider(YdApiSpider):
    name = 'yd_oral_zh2ja'

    def __init__(self, *args, **kwargs):
        super(YdOralZhJaSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api口语zh2ja'


class YdOralZhKoSpider(YdApiSpider):
    name = 'yd_oral_zh2ko'

    def __init__(self, *args, **kwargs):
        super(YdOralZhKoSpider, self).__init__(*args, **kwargs)
        self.tab_desc = '有道api口语zh2ko'
