from twisted.enterprise import adbapi
import datetime
import pymysql.cursors
import logging

log = logging.getLogger(__name__)


class SQLStorePipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='mydb', user='myuser', passwd='mypass',
                                            cursorclass=pymysql.cursors.DictCursor, charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        tx.execute("select * from websites where link = %s", (item['link'][0],))
        result = tx.fetchone()
        if result:
            log.debug("Item already stored in db: %s" % item)
        else:
            tx.execute(
                "insert into websites (link, created) values (%s, %s)",
                (item['link'][0], datetime.datetime.now())
            )
            log.debug("Item stored in db: %s" % item)

    def handle_error(self, e):
        log.error(e)
