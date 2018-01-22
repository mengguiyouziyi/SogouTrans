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
	name = 'yd_api_single'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
			'referer': "http://fanyi.youdao.com/",
		},
		'DOWNLOAD_DELAY': 2
	}

	def __init__(self, crawler, src, tgt, *args, **kwargs):
		super(YdApiSpider, self).__init__(*args, **kwargs)
		self.src = src
		self.tgt = tgt
		self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
		self.ip = self.get_host_ip()
		self.settings = crawler.settings
		self.server = StrictRedis(host=self.settings.get('REDIS_HOST'), decode_responses=True)
		self.cookie_dict = self.get_cookie()
		self.cookie_key = '%(name)s:cookies' % {'name': self.name}
		self.request_key = '%(name)s:requests' % {'name': 'yd_api'}
		self.error_key = '%(name)s:error' % {'name': 'yd_news_zh2ko'}
		self.server.sadd(self.cookie_key, json.dumps(self.cookie_dict, ensure_ascii=False))
		self.cookie = self.server.srandmember(self.cookie_key)
		self.item_keys = ['src', 'srcType', 'zh', 'en', 'ja', 'ko', 'fr', 'ru', 'es', 'pt', 'ara', 'de', 'it', 'url',
		                  'project', 'spider', 'server']
		self.d = {}.fromkeys(self.item_keys, '')

	def get_cookie(self):
		url = 'http://fanyi.youdao.com/'
		uas = self.settings.get('USER_AGENT_CHOICES', [])
		headers = {'User-Agent': random.choice(uas)}
		response = requests.get(url=url, headers=headers)
		cookie_dict = dict(response.cookies.items())
		return cookie_dict

	def get_host_ip(self):
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
		data = {
			'i': line,
			'from': 'zh-CHS' if self.src == 'zh' else self.src,
			'to': 'zh-CHS' if self.tgt == 'zh' else self.tgt,
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
		# -------------- 以下三种情况都会重新打入redis，但碰到的可能性不大 ----------------
		try:
			resp = json.loads(response.text)
		except Exception as e:
			self.logger.error(repr(e))
			# self.logger.error('JsonLoadsError on %s', aux)
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
			trans = ''
			sours = ''
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
		# log all failures
		self.logger.error(repr(failure))
		request = failure.request
		line = request.meta.get('line')
		# -------------------这种情况会经常遇到---------------------
		self.logger.error('TimeOutError')
		self.server.lpush(self.error_key, line.strip())
