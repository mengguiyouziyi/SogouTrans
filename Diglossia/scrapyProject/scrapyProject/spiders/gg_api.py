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
import execjs
import socket
from collections import OrderedDict
from redis import StrictRedis
from urllib.parse import urlencode
from scrapy.spiders import Spider
from scrapy.exceptions import CloseSpider
from scrapy.item import Item, Field
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class GGApiItem(Item):
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


class GGApiSpider(Spider):
    items = []
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self, settings, *args, **kwargs):
        super(GGApiSpider, self).__init__(*args, **kwargs)
        self.js = Py4Js()
        self.settings = settings
        self.col_comm = self.settings['SPIDER_CONF'][self.name]['col_comm']
        self.col_dict = OrderedDict(self.col_comm)  # 为创建mysql表格的column而设置的属性
        self.col_index_list = self.settings['SPIDER_CONF'][self.name]['col_index_list']  # 为创建mysql表格的index而设置的属性
        self.tab_desc = self.settings['SPIDER_CONF'][self.name]['tab_desc']  # 表格功能描述
        lang_dict = settings['LANG'][self.name[:2]]
        self.lsrc = kwargs.get('src', 'zh')  # 标准语言简称
        self.ltgt = kwargs.get('tgt', 'jp')
        self.src = lang_dict[kwargs.get('src', 'zh')]  # 各网站自己的语言标识
        self.tgt = lang_dict[kwargs.get('tgt', 'jp')]
        self.url = 'https://translate.google.cn/translate_a/single'
        self.ip = self._get_host_ip()
        self.request_key = '%(name)s:requests' % {'name': self.name}
        self.error_key = '%(name)s:errors' % {'name': self.name}

        self.redisparams = dict(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            decode_responses=True
        )
        self.server = self._get_redis()
        self.d = {}.fromkeys(self.col_dict.keys(), '')  # 用于item初始化

    def _get_redis(self):
        return StrictRedis(**self.redisparams)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler.settings, *args, **kwargs)

    def start_requests(self):
        request = scrapy.Request(self.url, method='GET', callback=self.parse_httpbin, errback=self.errback_httpbin)
        while 1:
            lines = ''
            for i in range(30):
                line = self.server.rpop(self.request_key)
                if not line:
                    data = self._get_params(lines)
                    request.body = data
                    request.meta['lines'] = lines
                    yield request
                    raise CloseSpider('No datas, close spider...')
                lines += (line + '\n')
                lines = lines.strip()
            data = self._get_params(lines)
            request.body = data
            request.meta['lines'] = lines
            yield request

    def _get_params(self, lines):
        data = {"client": "t", "sl": self.src, "tl": self.tgt, "hl": "zh-CN",
                "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"], "ie": "UTF-8", "oe": "UTF-8",
                "source": "btn", "ssel": "4", "tsel": "3", "kc": "0", "tk": self.js.getTk(lines), "q": lines}
        return urlencode(data)

    def _lpush(self, key, lines):
        for line in lines.split('\n'):
            self.server.lpush(key, line.strip())

    def parse_httpbin(self, response):
        lines = response.meta.get('lines')
        try:
            resp = json.loads(response.text)
        except Exception as e:
            self.logger.error(repr(e))
            self.logger.error('JsonLoadsError on %s', lines[0])
            self._lpush(self.error_key, lines)
            return
        try:
            results = resp[0][:-1]
        except Exception as e:
            self.logger.error(repr(response.text))
            self.logger.error('IndexError on %s', lines[0])
            self._lpush(self.request_key, lines)
            return
        trans = sours = ''
        for result in results:
            trans += result[0]
            sours += result[1]
        trans_list = trans.split('\n')
        sours_list = sours.split('\n')
        if len(trans_list) != len(sours_list):
            self.logger.error('Source not equal translation on %s', lines[0])
            self._lpush(self.request_key, lines)
            return 
        for tran, sour in zip(trans_list, sours_list):
            item = GGApiItem()
            item.update(self.d)
            item['src'] = sour
            item['srcType'] = self.lsrc  # 源语言类型
            item[self.ltgt] = tran
            item['url'] = response.url
            item['project'] = self.settings.get('BOT_NAME')
            item['spider'] = self.name
            item['server'] = self.ip
            yield item

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        lines = failure.request.meta.get('lines')
        self._lpush(self.request_key, lines)
        # log all failures
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            # response = failure.value.response
            self.logger.error('HttpError on %s', lines[0])
        elif failure.check(DNSLookupError):
            # this is the original request
            # request = failure.request
            self.logger.error('DNSLookupError on %s', lines[0])
        elif failure.check(TimeoutError, TCPTimedOutError):
            # request = failure.request
            self.logger.error('TimeoutError on %s', lines[0])
        else:
            self.logger.error('UnknowError on %s', lines[0])

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


class GGNewsZhEsSpider(GGApiSpider):
    name = 'gg_news_zh2es'

    def __init__(self, *args, **kwargs):
        super(GGNewsZhEsSpider, self).__init__(*args, **kwargs)


class GGNewsZhFrSpider(GGApiSpider):
    name = 'gg_news_zh2fr'

    def __init__(self, *args, **kwargs):
        super(GGNewsZhFrSpider, self).__init__(*args, **kwargs)


class GGNewsZhRuSpider(GGApiSpider):
    name = 'gg_news_zh2ru'

    def __init__(self, *args, **kwargs):
        super(GGNewsZhRuSpider, self).__init__(*args, **kwargs)


class GGOralZhEsSpider(GGApiSpider):
    name = 'gg_oral_zh2es'

    def __init__(self, *args, **kwargs):
        super(GGOralZhEsSpider, self).__init__(*args, **kwargs)


class GGOralZhFrSpider(GGApiSpider):
    name = 'gg_oral_zh2fr'

    def __init__(self, *args, **kwargs):
        super(GGOralZhFrSpider, self).__init__(*args, **kwargs)


class GGOralZhRuSpider(GGApiSpider):
    name = 'gg_oral_zh2ru'

    def __init__(self, *args, **kwargs):
        super(GGOralZhRuSpider, self).__init__(*args, **kwargs)


class GGOralZhJpSpider(GGApiSpider):
    name = 'gg_oral_zh2jp'

    def __init__(self, *args, **kwargs):
        super(GGOralZhJpSpider, self).__init__(*args, **kwargs)


class GGOralZhKoSpider(GGApiSpider):
    name = 'gg_oral_zh2ko'

    def __init__(self, *args, **kwargs):
        super(GGOralZhKoSpider, self).__init__(*args, **kwargs)


class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
            var k = "";
            var b = 406644;
            var b1 = 3293161072;

            var jd = ".";
            var $b = "+-a^+6";
            var Zb = "+-3^+b+-f";

            for (var e = [], f = 0, g = 0; g < a.length; g++) {
                var m = a.charCodeAt(g);
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                e[f++] = m >> 18 | 240,
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                e[f++] = m >> 6 & 63 | 128),
                e[f++] = m & 63 | 128)
            }
            a = b;
            for (f = 0; f < e.length; f++) a += e[f],
            a = RL(a, $b);
            a = RL(a, Zb);
            a ^= b1 || 0;
            0 > a && (a = (a & 2147483647) + 2147483648);
            a %= 1E6;
            return a.toString() + jd + (a ^ b)
        };

        function RL(a, b) {
            var t = "a";
            var Yb = "+";
            for (var c = 0; c < b.length - 2; c += 3) {
                var d = b.charAt(c + 2),
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
            }
            return a
        }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)
