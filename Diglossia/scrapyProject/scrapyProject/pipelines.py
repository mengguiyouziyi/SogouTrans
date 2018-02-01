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
    def __init__(self, dbparams, redisparams, spider):
        self.dbparams = dbparams
        self.redisparams = redisparams

    @classmethod
    def from_crawler(cls, crawler):
        dbparams = dict(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            db=crawler.settings['MYSQL_DBNAME'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            # use_unicode=False,
        )
        redisparams = dict(
            host=crawler.settings['REDIS_HOST'],
            port=crawler.settings['REDIS_HOST'],
            decode_responses=True
        )
        return cls(dbparams, redisparams, crawler.spider)

    def open_spider(self, spider):
        create(spider, self.dbparams)
        col_list = get_column(spider, self.dbparams)
        spider.col_list = col_list

    def close_spider(self, spider):
        self._in_func(spider)

    def _in_func(self, spider):
        col_list = spider.col_list[1:-1]
        col_str = ','.join(col_list)
        val_str = handle_str(len(col_list))
        in_sql = """insert into {tab} ({col}) VALUES ({val})""".format(tab=spider.name, col=col_str, val=val_str)
        while 1:
            try:
                conn = pymysql.connect(**self.dbparams)
                cursor = conn.cursor()
                cursor.executemany(in_sql, spider.items)
                conn.commit()
            except Exception as e:
                logger.error(e)
                continue
            finally:
                cursor.close()
                conn.close()
            break

    def process_item(self, item, spider):
        col_list = spider.col_list[1:-1]
        in_args = [item[i] for i in col_list]
        logger.info(item[col_list[0]])
        if len(spider.items) > 1000:
            self._in_func(spider)
            logger.info('Insert 1000')
            spider.items.clear()
        else:
            spider.items.append(in_args)
        yield item


def handle_str(num):
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


def get_column(spider, dbparams):
    """
    获取mysql表 字段字符串
    :return: 全部字段
    """
    sql = """select group_concat(column_name) from information_schema.columns WHERE table_name = '{tab}' and table_schema = 'spider'""".format(
        tab=spider.name)
    try:
        conn = pymysql.connect(**dbparams)
    except Exception as e:
        logger.error(e)
        logger.error('获取数据表字段错误....')
        # self.crawler.engine.close_spider(self.spider, 'mysql error')
    else:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        col_str = results[0]['group_concat(column_name)']
        col_list = col_str.split(',')
    finally:
        conn.close()
        return col_list


def create(spider, dbparams):
    sql = """CREATE TABLE IF NOT EXISTS `"""
    sql += spider.name
    sql += """` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',"""
    for col, desc in spider.col_dict.items():
        sql += """`{col}` text COMMENT '{desc}',""".format(col=col, desc=desc)
    sql += """`load_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '落地时间', PRIMARY KEY (`id`),"""
    for col in spider.col_index_list:
        sql += """KEY `index_{0}` (`{0}`(255))""".format(col)
    sql += """) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='{tab_desc}';""".format(tab_desc=spider.tab_desc)
    try:
        conn = pymysql.connect(**dbparams)
    except Exception as e:
        logger.error(e)
    else:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
