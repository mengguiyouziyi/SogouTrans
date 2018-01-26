import os
import sys

from scrapy.cmdline import execute

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

file = os.path.basename(__file__).replace('cmd_', '').replace('.py', '')
execute(['scrapy', 'crawl', file])
