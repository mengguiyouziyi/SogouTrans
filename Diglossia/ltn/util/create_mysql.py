from info import etl


class CreateTable(object):
    def __init__(self, t_name):
        self.conn = etl
        self.cur = self.conn.cursor()
        self.t_name = t_name
        # if self._checkExists():
        #     print('This table is exist,Please check out!')
        #     exit(1)

    def create(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `{}` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
              `sours` longtext COMMENT '原文',
              `trans` longtext COMMENT '译文',
              `load_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '落地时间',
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='有道翻译';
		""".format(self.t_name)
        self.cur.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    # print(etl.get_host_info())
    # print(etl.get_proto_info())
    ct = CreateTable('yd_api')
    ct.create()
