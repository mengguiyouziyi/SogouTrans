import pymysql
from redis import StrictRedis
from rediscluster import StrictRedisCluster

############################ redis info ############################
startup_nodes = [{"host": "10.142.97.92", "port": "7000"},
                 {"host": "10.142.97.92", "port": "7001"},
                 {"host": "10.142.97.92", "port": "7002"},
                 {"host": "10.142.97.92", "port": "7003"},
                 {"host": "10.142.97.92", "port": "7004"},
                 {"host": "10.142.97.92", "port": "7005"}]
# rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
server = StrictRedis(host='10.142.97.92', decode_responses=True)
############################ mysql info ############################
# etl
etl_conf = {'host': '10.142.98.91', 'port': 3306, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)
etl.select_db('spider')
# print(etl.get_host_info())
