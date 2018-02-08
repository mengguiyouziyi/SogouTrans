# -*- coding: utf-8 -*-

import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)
from collections import OrderedDict

BOT_NAME = 'scrapyProject'

SPIDER_MODULES = ['scrapyProject.spiders']
NEWSPIDER_MODULE = 'scrapyProject.spiders'

##~~~~~~~~~~~~~~~~ scrapy-redis ~~~~~~~~~~~~~~~~~~~
# Enables scheduling storing requests queue in redis.
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '10.146.252.112'
# REDIS_HOST = '106.39.246.223'
# REDIS_HOST = '10.142.237.97'
# REDIS_HOST = '10.146.254.57'
REDIS_PORT = 50111

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False
# COOKIES_DEBUG = True

# DEBUG INFO WARNING ERROR CRITICAL
LOG_LEVEL = 'INFO'
LOG_STDOUT = True

RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
# REDIRECT_ENABLED = False

DOWNLOAD_TIMEOUT = 30

USER_AGENT_CHOICES = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'baidu.middlewares.BaiduSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapyProject.middlewares.ProxyMiddleware': 1,
    # 'scrapyProject.middlewares.RetryMiddleware': 110,
    'scrapyProject.middlewares.RotateUserAgentMiddleware': 3,
    # 'cnn_scrapy.middlewares.BloomfilterMiddleware': 2,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapyProject.pipelines.MysqlPipeline': 999,
    # 'scrapyProject.pipelines.DuplicatesPipeline': 111,
}

# Mysql数据库的配置信息
MYSQL_HOST = '10.146.252.112'
MYSQL_PORT = 3306  # 数据库端口，在dbhelper中使用

# MYSQL_HOST = '10.146.254.57'
# MYSQL_HOST = '10.142.237.97'
# MYSQL_HOST = '106.39.246.223'
MYSQL_DBNAME = 'spider'  # 数据库名字，请修改
MYSQL_USER = 'spider'  # 数据库账号，请修改
MYSQL_PASSWD = 'chenguang'  # 数据库密码，请修改
# MYSQL_PORT = 50112  # 数据库端口，在dbhelper中使用

REDIS_CLUSTER_NODES = [
    {"host": "10.142.97.92", "port": "7000"},
    {"host": "10.142.97.92", "port": "7001"},
    {"host": "10.142.97.92", "port": "7002"},
    {"host": "10.142.97.92", "port": "7003"},
    {"host": "10.142.97.92", "port": "7004"},
    {"host": "10.142.97.92", "port": "7005"}
]

TELNETCONSOLE_ENABLED = False

# ------------------------------------ mysql 字段与描述 ---------------------------------------------------------
trans_api_col_comm = {'src': '源语言', 'srcType': '源语言种类', 'zh': '中文', 'en': '英文', 'jp': '日语', 'ko': '韩语',
                      'fr': '法语', 'ru': '俄语', 'es': '西班牙语', 'pt': '葡萄牙语', 'ara': '阿拉伯语', 'de': '德语',
                      'it': '意大利语', 'url': 'url', 'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
brand_col_comm = {'brand_zh': '中文品牌名', 'brand_en': '英文品牌名', 'style': '品牌风格', 'comp_link': '公司官网',
                  'addr': '地址', 'brand_url': '品牌详情页url', 'categary': '行业类别', 'company': '公司', 'url': 'url',
                  'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
# brand_col_comm = {'brand': '品牌名', 'brand_url': '品牌详情页url', 'categary': '行业类别',
#                   'company': '公司', 'url': 'url', 'project': '工程名', 'spider': '爬虫名', 'server': 'ip'}
col_d = {'col_comm': trans_api_col_comm, 'col_index_list': ['src']}
news1617 = oral800w = col_d.copy()
news1617.update({'in_file': 'news1617.zh'})
oral800w.update({'in_file': 'oral800w.zh'})
SPIDER_CONF = {
    # ----------------------------------------- yd ---------------------------------------------
    'yd_news_zh2es': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'es'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api新闻zh2es'},
    'yd_news_zh2fr': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'fr'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api新闻zh2fr'},
    'yd_news_zh2ru': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ru'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api新闻zh2ru'},
    'yd_news_zh2ko': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ko'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api新闻zh2ko'},
    'yd_news_zh2jp': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'jp'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api新闻zh2jp'},
    'yd_oral_zh2es': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'es'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api口语zh2es'},
    'yd_oral_zh2fr': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'fr'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api口语zh2fr'},
    'yd_oral_zh2ru': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ru'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api口语zh2ru'},
    'yd_oral_zh2ko': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ko'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api口语zh2ko'},
    'yd_oral_zh2jp': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'jp'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '有道api口语zh2jp'},
    # ----------------------------------------- gg ---------------------------------------------
    'gg_news_zh2es': news1617.update({'args': {'src': 'zh', 'tgt': 'es'}, 'tab_desc': '谷歌api新闻zh2es'}) or news1617,
    'gg_news_zh2fr': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'fr'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api新闻zh2fr'},
    'gg_news_zh2ru': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ru'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api新闻zh2ru'},
    'gg_news_zh2de': news1617.update({'args': {'src': 'zh', 'tgt': 'de'}, 'tab_desc': '谷歌api新闻zh2de'}) or news1617,
    'gg_news_zh2ko': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ko'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api新闻zh2ko'},
    'gg_news_zh2jp': {'in_file': 'news1617.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'jp'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api新闻zh2jp'},

    'gg_oral_zh2es': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'es'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api口语zh2es'},
    'gg_oral_zh2fr': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'fr'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api口语zh2fr'},
    'gg_oral_zh2ru': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ru'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api口语zh2ru'},
    'gg_oral_zh2de': oral800w.update({'args': {'src': 'zh', 'tgt': 'de'}, 'tab_desc': '谷歌api口语zh2de'}) or oral800w,
    'gg_oral_zh2ko': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'ko'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api口语zh2ko'},
    'gg_oral_zh2jp': {'in_file': 'oral800w.zh', 'args': OrderedDict({'src': 'zh', 'tgt': 'jp'}),
                      'col_comm': trans_api_col_comm,
                      'col_index_list': ['src'], 'tab_desc': '谷歌api口语zh2jp'},
    # ----------------------------------------- brand ---------------------------------------------
    'chinasspp': {'in_file': '', 'args': {},
                  'col_comm': brand_col_comm,
                  'col_index_list': ['src'], 'tab_desc': 'chinasspp品牌名称'},
    'paizi': {'in_file': '', 'args': {},
              'col_comm': brand_col_comm,
              'col_index_list': ['src'], 'tab_desc': 'pazi品牌名称'},
    'china_ef': {'in_file': '', 'args': {},
                 'col_comm': brand_col_comm,
                 'col_index_list': ['src'], 'tab_desc': 'china_ef品牌名称'},
}
LANG = {'yd': {'zh': 'zh-CHS', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru'},
        'bi': {'zh': 'zh-CHS', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru', 'de': 'de'},
        'sg': {'zh': 'zh-CHS', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru', 'de': 'de'},
        'tx': {'zh': 'zh', 'en': 'en', 'jp': 'jp', 'ko': 'kr', 'fr': 'fr', 'es': 'es', 'ru': 'ru', 'de': 'de'},
        'bd': {'zh': 'zh', 'en': 'en', 'jp': 'jp', 'ko': 'kor', 'fr': 'fra', 'es': 'spa', 'ru': 'ru', 'de': 'de'},
        'gg': {'zh': 'zh-CN', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru', 'de': 'de'}}
