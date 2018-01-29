import codecs
import pymysql
from redis import StrictRedis
import sys
from os.path import dirname, abspath

fpath = abspath(dirname(__file__))
ffpath = dirname(fpath)
sys.path.append(fpath)
sys.path.append(ffpath)

from scrapyProject.settings import (REDIS_HOST, REDIS_PORT, MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD,
                                    MYSQL_PORT, SPIDER_CONF)
from .set_adsl import set_interface


class Send(object):

    def __init__(self, file, spider_name, redis_host=REDIS_HOST, redis_port=REDIS_PORT, mysql_host=MYSQL_HOST,
                 mysql_dbname=MYSQL_DBNAME, mysql_user=MYSQL_USER, mysql_passwd=MYSQL_PASSWD, mysql_port=MYSQL_PORT):
        etl_conf1 = {'host': mysql_host, 'port': mysql_port, 'user': mysql_user, 'password': mysql_passwd,
                    'charset': 'utf8', 'db': mysql_dbname, 'cursorclass': pymysql.cursors.DictCursor}
        print(etl_conf1)
        host = '106.39.246.223'
        etl_conf = {'host': host, 'port': 50112, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
                    'db': 'spider', 'cursorclass': pymysql.cursors.DictCursor}
        print(etl_conf)
        self.conn = pymysql.connect(**etl_conf)
        self.cursor = self.conn.cursor()
        self.server = StrictRedis(host=host, port=50111, decode_responses=True)
        self.request_key = spider_name + ':requests'
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


def main(file, spider_name):
    send = Send(file=file, spider_name=spider_name)
    send.send_redis()
    send.close_file()


if __name__ == '__main__':
    set_interface('10.146.253.44')
    spider_name = sys.argv[1]
    file = SPIDER_CONF.get(spider_name).get('in_file')
    file = '/search/chenguang/meng/documents/SogouTrans/' + file
    main(file=file, spider_name=spider_name)
