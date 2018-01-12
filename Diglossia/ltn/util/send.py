import redis, hashlib
from info import etl


class Send(object):
    def __init__(self, conn=etl, redis_key='cnn_uncrawl:dupefilter'):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.r = redis.StrictRedis(host='10.142.97.92', decode_responses=True)
        self.key = redis_key
        self.sha = hashlib.sha1()

    def send(self):
        sql = """select url from meishij"""
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for i, result in enumerate(results):
            if (i + 1) % 5000 == 0:
                print(i)
            url = result.get('url', '')
            if not url:
                continue
            self.sha.update(url.encode('utf-8'))
            self.r.sadd(self.key, self.sha.hexdigest())


if __name__ == '__main__':
    send = Send()
    send.send()
