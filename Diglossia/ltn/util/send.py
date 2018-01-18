import codecs
import json
from info import etl, server


class SendMysql(object):
    def __init__(self, conn=etl, server=server):
        self.conn = conn
        self.cursor = etl.cursor()
        self.server = server
        self.request_key = '%(name)s:requests' % {'name': 'yd_api'}
        self.file = codecs.open('news1617.zh', 'r', 'utf-8')

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
            self.server.lpush(self.request_key, line.strip())

    def close_file(self):
        self.file.close()


if __name__ == '__main__':
    send = SendMysql()
    send.send_redis()
    send.close_file()
