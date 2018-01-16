import pymysql
import set_adsl

# set_adsl.set_interface(sys.argv[1])
set_adsl.set_interface('10.146.252.112')
etl_conf = {'host': '10.142.98.91', 'port': 3306, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)
etl.select_db('spider')
cur = etl.cursor()
sql = """select * from ltn limit 5"""
cur.execute(sql)
results = cur.fetchall()
print(results)
