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
from redis import StrictRedis
from urllib.parse import urlencode
from scrapy.spiders import Spider
from scrapy.exceptions import CloseSpider
from ltn.items import YdApiItem


class YdApiSpider(Spider):
    name = 'yd_api'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'referer': "http://fanyi.youdao.com/",
            # 'cookie': "OUTFOX_SEARCH_USER_ID_NCOO=1505415871.087814; OUTFOX_SEARCH_USER_ID=-1582931044@10.168.8.64; JSESSIONID=aaaqVIf9Ihfg97CoOXlcw; fanyi-ad-id=39535; fanyi-ad-closed=1; OUTFOX_SEARCH_USER_ID_NCOO=1505415871.087814; OUTFOX_SEARCH_USER_ID=-1582931044@10.168.8.64; ___rl__test__cookies=1514285803703",
            # 'cookie': "OUTFOX_SEARCH_USER_ID=104413480@10.168.8.63; JSESSIONID=aaaE_vQIwsIxP7ATeVhew",
        },
        'DOWNLOAD_DELAY': 2
    }

    def __init__(self, crawler, src='zh', tgt='ja', *args, **kwargs):
        super(YdApiSpider, self).__init__(*args, **kwargs)
        print(self.get_host_ip())
        self.settings = crawler.settings
        self.src = 'zh' if src == 'zh-CHS' else src
        self.tgt = 'zh' if tgt == 'zh-CHS' else tgt
        self.server = StrictRedis(host=self.settings.get('REDIS_HOST'), decode_responses=True)
        self.cookie_dict = self.get_cookie()
        self.cookie_key = '%(name)s:cookies' % {'name': self.name}
        self.request_key = '%(name)s:requests' % {'name': self.name}
        self.server.sadd(self.cookie_dict, json.dumps(self.cookie_dict, ensure_ascii=False))
        self.cookie = self.server.srandmember(self.cookie_dict)

    def get_cookie(self):
        url = 'http://fanyi.youdao.com/'
        uas = self.settings.get('USER_AGENT_CHOICES', [])
        headers = {'User-Agent': random.choice(uas)}
        response = requests.get(url=url, headers=headers)
        cookie_dict = dict(response.cookies.items())
        return cookie_dict

    def get_host_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler)

    def start_requests(self):
        while True:
            l = self.server.rpop(self.request_key)
            if not l:
                raise CloseSpider('no datas')
            url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
            salf = str(int(time.time() * 1000) + random.randint(1, 10))
            n = 'fanyideskweb' + l + salf + "aNPG!!u6sesA>hBAW1@(-"
            sign = hashlib.md5(n.encode('utf-8')).hexdigest()
            data = {
                'i': l,
                'from': 'zh-CHS' if self.src == 'zh' else self.src,
                'to': 'zh-CHS' if self.tgt == 'zh' else self.tgt,
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': salf,
                'sign': sign,
                'doctype': 'json',
                'version': "2.1",
                'keyfrom': "fanyi.web",
                # 'action': "FY_BY_DEFAULT",
                # 'action': "FY_BY_CLICKBUTTION",
                'action': "FY_BY_REALTIME",
                'typoResult': 'false'
            }
            yield scrapy.Request(url, method='POST', body=urlencode(data), cookies=json.loads(self.cookie))

    def parse(self, response):
        print(response.meta.items())
        try:
            resp = json.loads(response.text)
        except:
            return
        if resp.get('errorCode') != 0:
            print(response.text)
            return
        results = resp.get('translateResult', [])
        if not results:
            return
        for result in results:
            item = YdApiItem()
            trans = ''
            sours = ''
            for dict_rt in result:
                t = dict_rt.get('tgt', '')
                s = dict_rt.get('src', '')
                trans += t  # 此循环结束后，此行拼接完成
                sours += s
            d = {}.fromkeys(
                ['src', 'srcType', 'zh', 'en', 'ja', 'ko', 'fr', 'ru', 'es', 'pt', 'ara', 'de', 'it', 'url', 'project',
                 'spider', 'server'], '')
            item.update(d)
            item['src'] = sours
            item['srcType'] = self.src  # 源语言类型
            item[self.tgt] = trans
            item['url'] = response.url
            item['project'] = self.settings.get('BOT_NAME')
            item['spider'] = self.name
            item['server'] = socket.gethostname()

            yield item
