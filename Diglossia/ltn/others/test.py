import pymysql
import set_adsl
from urllib.request import urlopen
from redis import StrictRedis

# set_adsl.set_interface(sys.argv[1])
set_adsl.set_interface('10.146.252.112')
# server = StrictRedis(host='10.152.97.92', decode_responses=True)
# server.sadd('aaaaa', 'aaaaa')
# v = server.spop('aaaaa')
# print(v)

s = urlopen('http://www.baidu.com')
print(s)
etl_conf = {'host': '10.146.252.112', 'port': 3306, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)
etl.select_db('spider')
cur = etl.cursor()
sql = """select * from yd_api_ja limit 1"""
cur.execute(sql)
results = cur.fetchall()
print(results)
