import redis, hashlib
from info import etl


class Send(object):
    def __init__(self, conn=etl, redis_key='cnn_uncrawl:myrequests'):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.r = redis.StrictRedis(host='10.142.97.92', decode_responses=True)
        self.key = redis_key
        self.sha = hashlib.sha1()

    def send(self):
        # tech = ['https://search.api.cnn.io/content?size=100&q=technology&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #         for i in range(1, 300)]
        # for url in tech:
        #     self.r.sadd(self.key, url)
        # poli = ['https://search.api.cnn.io/content?size=100&q=politics&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #         for i in range(1, 781)]
        # for url in poli:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=us&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 1567)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=china&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 207)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=money&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 319)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=health&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 425)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=Business&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 750)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=Markets&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 115)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        # us = ['https://search.api.cnn.io/content?size=100&q=Culture&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
        #       for i in range(1, 135)]
        # for url in us:
        #     self.r.sadd(self.key, url)
        us = ['https://search.api.cnn.io/content?size=100&q=Gadgets&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 13)]
        for url in us:
            self.r.sadd(self.key, url)
        us = ['https://search.api.cnn.io/content?size=100&q=Future&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 297)]
        for url in us:
            self.r.sadd(self.key, url)
        us = ['https://search.api.cnn.io/content?size=100&q=Startups&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 14)]
        for url in us:
            self.r.sadd(self.key, url)
        us = ['https://search.api.cnn.io/content?size=100&q=Autos&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 15)]
        for url in us:
            self.r.sadd(self.key, url)
        us = ['https://search.api.cnn.io/content?size=100&q=Security&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 551)]
        for url in us:
            self.r.sadd(self.key, url)
        us = ['https://search.api.cnn.io/content?size=100&q=State&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 742)]
        for url in us:
            self.r.sadd(self.key, url)


if __name__ == '__main__':
    send = Send()
    send.send()
