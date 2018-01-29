import sys
from os.path import dirname, abspath

from scrapy.cmdline import execute

base_path = abspath(dirname(__file__))
sys.path.append(base_path)
from .util import set_adsl
from .scrapyProject.settings import SPIDER_CONF

# file = os.path.basename(__file__).replace('cmd_', '').replace('.py', '')
if __name__ == '__main__':
    """yd_news_zh2es"""
    if len(sys.argv) == 3:
        ip = sys.argv[2]
        set_adsl.set_interface(ip)

    spider_name = sys.argv[1]
    args = SPIDER_CONF.get(spider_name).get('args')
    cmd_list = ['scrapy', 'crawl', spider_name]

    for k, v in args.items():
        cmd_list.extend(['-a', k + '=' + v])
    execute(cmd_list)
