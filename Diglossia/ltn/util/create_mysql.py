import pymysql

etl_conf = {'host': '10.142.97.80', 'port': 3306, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
            'db': 'spider', 'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)


class CreateTable(object):
    def __init__(self, t_name, conn=etl):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.t_name = t_name

    def create(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `{}` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
              `src` longtext COMMENT '源语言',
              `srcType` VARCHAR(20) DEFAULT '' COMMENT '源语言种类',
              `zh` longtext COMMENT '中文',
              `en` longtext COMMENT '英语',
              `ja` longtext COMMENT '日语',
              `ko` longtext COMMENT '韩语',
              `fr` longtext COMMENT '法语',
              `ru` longtext COMMENT '俄语',
              `es` longtext COMMENT '西班牙语',
              `pt` longtext COMMENT '葡萄牙语',
              `ara` longtext COMMENT '阿拉伯语',
              `de` longtext COMMENT '德语',
              `it` longtext COMMENT '意大利语',
              `load_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '落地时间',
              PRIMARY KEY (`id`),
              KEY `index_src` (`src`(255))
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='有道翻译';
		""".format(self.t_name)
        self.cur.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    # print(etl.get_host_info())
    # print(etl.get_proto_info())
    ct = CreateTable('yd_news')
    ct.create()
