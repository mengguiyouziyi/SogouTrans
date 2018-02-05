import pymysql
import set_adsl
import socket
from redis import StrictRedis


def test_redis(host, port):
    server = StrictRedis(host=host, port=port, decode_responses=True)
    server.sadd('aaaaa', 'aaaaa')
    v = server.spop('aaaaa')
    print(v)


def test_mysql(host, port):
    etl_conf = {'host': host, 'port': port, 'user': 'spider', 'password': 'chenguang', 'charset': 'utf8',
                'db': 'spider', 'cursorclass': pymysql.cursors.DictCursor}
    etl = pymysql.connect(**etl_conf)
    cursor = etl.cursor()
    sql = """select host from information_schema.processlist WHERE ID=connection_id();"""
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result.get('host'))


def _get_host_ip():
    """
    获取当前网络环境的ip地址
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    set_adsl.set_interface('10.146.252.113')
    r = {'host': '10.146.252.112', 'port': 50111}
    # m = {'host': '10.146.252.112', 'port': 50112}
    test_redis(**r)
    # test_mysql(**m)
