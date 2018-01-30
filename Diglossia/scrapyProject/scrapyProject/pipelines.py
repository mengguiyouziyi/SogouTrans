# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)
import pymysql
import logging

logger = logging.getLogger(__name__)


class MysqlPipeline(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.spider = self.crawler.spider
        self.tab = self.spider.name
        settings = self.crawler.settings
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            # use_unicode=False,
        )
        self.conn = self._conn_mysql(dbparams)
        self.conn.ping(True)
        # while not self.conn:
        #     logger.warning('Reconnect mysql~~~')
        #     self.conn = self._conn_mysql(dbparams)
        self.cursor = self.conn.cursor()
        if not self.create():
            self.crawler.engine.close_spider(self.spider, 'CreateTableError on {}'.format(self.tab))

        self.col_list = self._get_column()[1:-1]
        self.col_str = ','.join(self.col_list)
        self.val_str = self._handle_str(len(self.col_list))

    def _conn_mysql(self, p):
        try:
            conn = pymysql.connect(**p)
            return conn
        except:
            return

    def create(self):
        sql = """CREATE TABLE IF NOT EXISTS `"""
        sql += self.tab
        sql += """` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',"""
        for col, desc in self.spider.col_list.items():
            sql += """`{col}` text COMMENT '{desc}',""".format(col=col, desc=desc)
        sql += """`load_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '落地时间', PRIMARY KEY (`id`),"""
        for col in self.spider.col_index_list:
            sql += """KEY `index_{0}` (`{0}`(255))""".format(col)
        sql += """) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='{tab_desc}';""".format(tab_desc=self.spider.tab_desc)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(e)
            return

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _get_column(self):
        """
        获取mysql表 字段字符串
        :return: 全部字段
        """
        sql = """select group_concat(column_name) from information_schema.columns WHERE table_name = '{tab}' and table_schema = 'spider'""".format(
            tab=self.tab)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            logger.error(e)
            logger.error('获取数据表字段错误....')
            self.crawler.engine.close_spider(self.spider, 'mysql error')
        results = self.cursor.fetchall()
        col_str = results[0]['group_concat(column_name)']
        col_list = col_str.split(',')
        return col_list

    def _handle_str(self, num):
        """
        根据插入字段数量来构造sql语句
        :param num: 插入字段数量
        :return: sql的value字符串
        """
        x = "%s"
        y = ", %s"
        for i in range(num - 1):
            x += y
        return x

    def process_item(self, item, spider):
        in_sql = """insert into {tab} ({col}) VALUES ({val})""".format(tab=self.tab, col=self.col_str, val=self.val_str)
        in_args = [item[i] for i in self.col_list]
        self.conn.ping(True)
        try:
            self.cursor.execute(in_sql, in_args)
            self.conn.commit()
            logger.info(item[self.col_list[0]])
        except Exception as e:
            logger.error(e)
            logger.error('mysql error，源为：{}'.format(item[self.col_list[0]]))
            self.crawler.engine.close_spider(spider, 'mysql error')
