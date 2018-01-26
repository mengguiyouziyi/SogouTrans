import os
import sys

from scrapy.cmdline import execute

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)
from util import set_adsl
from .scrapyProject.settings import SPIDER_CONF

# file = os.path.basename(__file__).replace('cmd_', '').replace('.py', '')
if __name__ == '__main__':
    """yd_news_zh2es"""
    spider_name = sys.argv[1]
    if len(sys.argv) == 3:
        ip = sys.argv[2]
        set_adsl.set_interface(ip)
    name_split = spider_name.split('2')
    for_name_split = name_split[0].split('_')
    src = for_name_split[2]
    tgt = name_split[1]
    execute(['scrapy', 'crawl', spider_name, '-a', 'src=%s' % src, '-a', 'tgt=%s' % tgt])
