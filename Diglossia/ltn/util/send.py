import codecs
import pymysql
from redis import StrictRedis
import sys
from os.path import dirname, abspath

fpath = abspath(dirname(__file__))
ffpath = dirname(fpath)
sys.path.append(fpath)
sys.path.append(ffpath)

from ltn.ltn.settings import REDIS_HOST, MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PORT


class SendMysql(object):

    def __init__(self, file, request_key, redis_host=REDIS_HOST, mysql_host=MYSQL_HOST, mysql_dbname=MYSQL_DBNAME,
                 mysql_user=MYSQL_USER, mysql_passwd=MYSQL_PASSWD, mysql_port=MYSQL_PORT):
        etl_conf = {'host': mysql_host, 'port': mysql_port, 'user': mysql_user, 'password': mysql_passwd,
                    'charset': 'utf8', 'db': mysql_dbname, 'cursorclass': pymysql.cursors.DictCursor}
        self.conn = pymysql.connect(**etl_conf)
        self.cursor = self.conn.cursor()
        self.server = StrictRedis(host=redis_host, decode_responses=True)
        self.request_key = request_key
        self.file = codecs.open(file, 'r', 'utf-8')

    def send_mysql(self):
        sql = """insert into yd_news(zh) VALUES (%s)"""
        temp = []
        num = 0
        for line in self.file:
            num += 1
            if num % 10000 == 0:
                print(num)
            if not line:
                continue
            if len(temp) > 5000:
                self.cursor.executemany(sql, temp)
                self.conn.commit()
                temp.clear()
            else:
                temp.append(line.strip())
        self.cursor.executemany(sql, temp)
        self.conn.commit()

    def send_redis(self):
        num = 0
        for line in self.file:
            num += 1
            if num % 10000 == 0:
                print(num)
            if not line:
                continue
            self.server.lpush(self.request_key, line.strip().replace('\t', ''))

    def close_file(self):
        self.file.close()


def main(file, request_key):
    send = SendMysql(file=file, request_key=request_key)
    send.send_redis()
    send.close_file()


if __name__ == '__main__':
    file = sys.argv[1]
    request_key = sys.argv[2]
    main(file=file, request_key=request_key)
