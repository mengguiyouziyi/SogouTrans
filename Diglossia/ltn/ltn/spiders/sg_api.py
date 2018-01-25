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
import socket
from collections import OrderedDict
from redis import StrictRedis
from urllib.parse import urlencode
from scrapy.spiders import Spider
from scrapy.exceptions import CloseSpider
from ltn.items import YdApiItem


class SgApiSpider(Spider):
    # name = 'yd_oral_single_zh2ko'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'content-type': "application/x-www-form-urlencoded",
            'Accept': "application/json",
        },
        'DOWNLOAD_DELAY': 2
    }

    def __init__(self, crawler, src, tgt, *args, **kwargs):
        super(SgApiSpider, self).__init__(*args, **kwargs)
        self.col_comm = {'src': '源语言', 'srcType': '源语言种类', 'zh': '中文', 'en': '英文', 'ja': '日语', 'ko': '韩语', 'fr': '法语',
                         'ru': '俄语', 'es': '西班牙语', 'pt': '葡萄牙语', 'ara': '阿拉伯语', 'de': '德语', 'it': '意大利语', 'url': 'url',
                         'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
        self.col_list = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = ['src']  # 为创建mysql表格的index而设置的属性
        self.src = src
        self.tgt = tgt
        self.url = 'http://fanyi.sogou.com/reventondc/multiLangTranslate'
        self.ip = self._get_host_ip()
        self.settings = crawler.settings
        self.server = StrictRedis(host=self.settings.get('REDIS_HOST'), decode_responses=True)
        self.request_key = '%(name)s:requests' % {'name': self.name}
        self.error_key = '%(name)s:errors' % {'name': self.name}
        self.cookie = self.server.srandmember(self.cookie_key)
        self.d = {}.fromkeys(self.col_list.keys(), '')

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
            data = self._get_params(line)
            yield scrapy.Request(self.url, method='POST', body=urlencode(data), meta={'line': line},
                                 callback=self.parse_httpbin, errback=self.errback_httpbin)

    def _get_params(self, line):
        f = lambda x: 'zh-CHS' if x == 'zh' else x
        data = {
            'from': f(self.src),
            'to': f(self.tgt),
            'text': line,
        }
        return data

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
        sours = resp.get('text')
        trans = resp.get('dit')
        item = YdApiItem()
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
