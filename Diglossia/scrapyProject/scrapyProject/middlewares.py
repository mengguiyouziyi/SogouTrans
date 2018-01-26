# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)

import base64
from random import choice
from redis import StrictRedis
from scrapy.exceptions import IgnoreRequest, CloseSpider


# from jianjie.utils.bloomfilter import PyBloomFilter, rc


# class BloomfilterMiddleware(object):
# 	def __init__(self):
# 		self.bf = PyBloomFilter(conn=rc)
#
# 	def process_request(self, request, spider):
# 		url = request.url
# 		if self.bf.is_exist(url):
# 			raise IgnoreRequest
# 		else:
# 			self.bf.add(url)

# class CloseMiddleware(object):
# 	def process_response(self, request, response, spider):
# 		if response.status == 402:
# 			raise CloseSpider('402 proxy no use')
# 		else:
# 			return response


class ProxyMiddleware(object):
    def __init__(self):
        self.proxyServer = "http://http-dyn.abuyun.com:9020"
        pl = [
            "H1XX369E3AGF7AQD:F2F5005CDF302D89",
            "HOKRYM10F5AHIW4D:DCF22DAF1A9040F5",
        ]
        self.proxyAuths = ["Basic " + base64.urlsafe_b64encode(bytes(p, "ascii")).decode("utf8") for p in pl]

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Proxy-Authorization"] = choice(self.proxyAuths)


class RetryMiddleware(object):
    def __init__(self, settings):
        host = settings.get('REDIS_HOST')
        port = settings.get('REDIS_PORT')
        self.server = StrictRedis(host=host, port=port, db=0, decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        """
        猜想：
            request复制改属性，指纹不同，返回重新申请；
            原request也会在重试机制中重新申请
        :param request:
        :param response:
        :param spider:
        :return:
        """
        retries = request.meta.get('retry_times', 0)
        if retries >= 5 and response.status in [429, 503] and 'index.html' in request.url:
            self.server.sadd('cnn:wrong', request.url)
            # print('wrong status: %s, retrying~~' % response.status, request.url)
            # retryreq = request.copy()
            # retryreq.dont_filter = True  # 告诉scrapy，此request不去重
            # return retryreq
            return request
        else:
            return response


class RotateUserAgentMiddleware(object):
    """Middleware used for rotating user-agent for each request"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('USER_AGENT_CHOICES', []))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', choice(self.agents))
