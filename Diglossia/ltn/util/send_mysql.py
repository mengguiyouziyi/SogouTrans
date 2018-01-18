import codecs
from info import etl


class SendMysql(object):
    def __init__(self, conn=etl):
        self.conn = conn
        self.cursor = etl.cursor()
        self.file = codecs.open('news.liang.10g.txt.half.1kw.filter.uniq', 'r', 'utf-8')

    def send(self):
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
                self.cursor.executemany(sql)
                self.conn.commit()
                temp.clear()
            else:
                temp.append(line.strip())
        self.cursor.executemany(sql)
        self.conn.commit()

    def close_file(self):
        self.file.close()


if __name__ == '__main__':
    send = SendMysql()
    send.send()
    send.close_file()
