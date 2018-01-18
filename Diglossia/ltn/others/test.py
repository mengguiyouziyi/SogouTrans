import pymysql
import set_adsl
from urllib.request import urlopen
from redis import StrictRedis

# set_adsl.set_interface(sys.argv[1])
# set_adsl.set_interface('10.146.252.112')
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

a = {"translateResult": [[{"tgt": "証券新聞社の記者統計によると、2015年4四半期末のデータによると、第4四半期末の株式ファンドの平均化は6割となっている。",
                           "src": "《证券日报》基金新闻部记者统计发现，2015年四季度末数据显示，四季度末偏股基金平均仓位六成。"},
                          {"tgt": "こんにちは。",
                           "src": "你好。"}],
                         [{"tgt": "みなさん、こんにちは。", "src": "大家好，我号。"},
                          {"tgt": "みなさんこんにちは。", "src": "大家好。"}]],
     "errorCode": 0, "type": "zh-CHS2ja"}
