import pymysql
import set_adsl
from urllib.request import urlopen
from redis import StrictRedis

host1 = '10.146.252.120'
# set_adsl.set_interface(sys.argv[1])
set_adsl.set_interface(host1)

s = urlopen('http://www.baidu.com')
print(s)

host2 = '106.39.246.223'
# host2 = '10.152.237.97'

# server = StrictRedis(host=host2, port=40111, decode_responses=True)
# server.sadd('aaaaa', 'aaaaa')
# v = server.spop('aaaaa')
# print(v)

etl_conf = {'host': host2, 'port': 40112, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
            'db': 'spider', 'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)
cur = etl.cursor()
sql = """CREATE TABLE `yd_oral_single_zh2ko` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `src` text COMMENT '源语言',
  `srcType` text COMMENT '源语言种类',
  `zh` text COMMENT '中文',
  `en` text COMMENT '英文',
  `ja` text COMMENT '日语',
  `ko` text COMMENT '韩语',
  `fr` text COMMENT '法语',
  `ru` text COMMENT '俄语',
  `es` text COMMENT '西班牙语',
  `pt` text COMMENT '葡萄牙语',
  `ara` text COMMENT '阿拉伯语',
  `de` text COMMENT '德语',
  `it` text COMMENT '意大利语',
  `url` text COMMENT 'url',
  `project` text COMMENT '工程名',
  `spider` text COMMENT '爬虫名',
  `server` text COMMENT 'ip',
  `load_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '落地时间',
  PRIMARY KEY (`id`),
  KEY `index_src` (`src`(255))
) ENGINE=InnoDB AUTO_INCREMENT=914975 DEFAULT CHARSET=utf8 COMMENT='有道api口语zh2ko';
"""
cur.execute(sql)
etl.commit()
print('create')
