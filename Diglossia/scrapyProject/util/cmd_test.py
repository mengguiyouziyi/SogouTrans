import sys
from os.path import dirname, abspath

from scrapy.cmdline import execute

base_path = abspath(dirname(__file__))
sys.path.append(base_path)

# file = os.path.basename(__file__).replace('cmd_', '').replace('.py', '')
if __name__ == '__main__':
    cmd_list = ['scrapy', 'crawl', 'paizi']
    execute(cmd_list)
