import sys
from os.path import dirname, abspath

from scrapy.cmdline import execute

base_path = abspath(dirname(__file__))
sys.path.append(base_path)
from scrapyProject.settings import SPIDER_CONF
from scrapyProject import settings

# file = os.path.basename(__file__).replace('cmd_', '').replace('.py', '')
if __name__ == '__main__':
    host = '10.142.97.80'
    settings.REDIS_HOST = settings.MYSQL_HOST = host
    spider_name = 'yd_liju_zh2es'
    args = SPIDER_CONF.get(spider_name).get('args')
    cmd_list = ['scrapy', 'crawl', spider_name]

    for k, v in args.items():
        cmd_list.extend(['-a', k + '=' + v])
    execute(cmd_list)
