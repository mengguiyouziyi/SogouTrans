import os
import sys

from scrapy.cmdline import execute

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

file = os.path.basename(__file__).replace('cmd_', '').replace('.py', '')
if __name__ == '__main__':
    import set_adsl

    set_adsl.set_interface(sys.argv[3])
    # set_adsl.set_interface('10.146.252.112')
    execute(['scrapy', 'crawl', file, '-a', 'src=%s' % sys.argv[1], '-a', 'tgt=%s' % sys.argv[2]])