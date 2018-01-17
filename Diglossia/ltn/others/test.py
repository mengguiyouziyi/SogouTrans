import pymysql
import set_adsl
from redis import StrictRedis

# server = StrictRedis(host='10.134.9.106', decode_responses=True)
# server.sadd('aaaaa', 'aaaaa')
# v = server.spop('aaaaa')
# print(v)
# set_adsl.set_interface(sys.argv[1])
set_adsl.set_interface('10.142.97.80')
etl_conf = {'host': '10.142.98.91', 'port': 3306, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)
etl.select_db('spider')
cur = etl.cursor()
sql = """select * from ltn limit 5"""
cur.execute(sql)
results = cur.fetchall()
print(results)
