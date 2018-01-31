try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve
import time
import xlrd
import os
from traceback import print_exc
from os.path import exists, join


def down(audio, out_dir='./audios/'):
    if not exists(out_dir):
        os.mkdir(out_dir)

    def cbk(a, b, c):
        '''回调函数
        @a: 已经下载的数据块
        @b: 数据块的大小
        @c: 远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('%.2f%%' % per)

    print('Download %s' % audio)
    file = join(out_dir, audio.split('/')[-1])
    try:
        urlretrieve(audio, file, cbk)
        return True
    except:
        print_exc()
        return
        # time.sleep(1)


def read_xml(file):
    workbook = xlrd.open_workbook(file)
    table = workbook.sheet_by_index(0)
    aacs = table.col_values(3)
    mp3s = table.col_values(13)
    return list(set(aacs[1:] + mp3s[1:]))


if __name__ == '__main__':
    # audio = 'http://6tiantian.oss-cn-beijing.aliyuncs.com/mp3_YTY4MzY2YzUtYmU0Yy00ZjAyLWIwNDktM2YyYmVhMGQ4NjRi.mp3'
    # down(audio)
    cols = read_xml(file='./student_question.xlsx')
    for col in cols:
        is_ok = down(col)
        if not is_ok:
            continue
