# -*- coding: UTF-8 -*-
import hashlib
import requests
import time
import random
import traceback
import codecs


def translate(lines):
    headers = {
        'host': "fanyi.youdao.com",
        'connection': "keep-alive",
        'content-length': "40576",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "http://fanyi.youdao.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "http://fanyi.youdao.com/",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': "OUTFOX_SEARCH_USER_ID_NCOO=1505415871.087814; OUTFOX_SEARCH_USER_ID=-1582931044@10.168.8.64; JSESSIONID=aaaqVIf9Ihfg97CoOXlcw; fanyi-ad-id=39535; fanyi-ad-closed=1; OUTFOX_SEARCH_USER_ID_NCOO=1505415871.087814; OUTFOX_SEARCH_USER_ID=-1582931044@10.168.8.64; ___rl__test__cookies=1514285803703",
        'cache-control': "no-cache",
    }
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    salf = str(int(time.time() * 1000) + random.randint(1, 10))
    n = 'fanyideskweb' + lines + salf + "aNPG!!u6sesA>hBAW1@(-"
    sign = hashlib.md5(n.encode('utf-8')).hexdigest()
    data = {
        'i': lines,
        'from': 'ko',
        'to': 'zh-CHS',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salf,
        'sign': sign,
        'doctype': 'json',
        'version': "2.1",
        'keyfrom': "fanyi.web",
        # 'action': "FY_BY_DEFAULT",
        # 'action': "FY_BY_CLICKBUTTION",
        'action': "FY_BY_REALTIME",
        'typoResult': 'false'
    }
    try:
        resp = requests.post(url, headers=headers, data=data).json()
        # print(resp)
        if resp.get('errorCode') != 0:
            return
        results = resp.get('translateResult', [])
        if not results:
            return
        trans = ''
        for result in results:
            for dict_rt in result:
                tgt = dict_rt.get('tgt', '')
                trans += tgt  # 此循环结束后，此行拼接完成
            trans += '\n'  # 结尾添加换行符。空行返回的也是一个dict，不用特别关注
        return trans
    except:
        traceback.print_exc()
        return None


def main(f1, lines):
    # print(lines)
    trans_lines = translate(lines)
    n = 0
    while not trans_lines:
        time.sleep(5)
        n += 1
        if n > 3:
            print('exit...')
            exit(1)
        trans_lines = translate(lines)
        print('again...')
    f1.write(trans_lines)


if __name__ == '__main__':
    # source_lines = '''학생회 관계자 는 " 처음 만난 그, 알 그 는 확실히 좋아 보 인 다.'''
    # lines = ''
    # for line in source_lines.split('\n'):
    #     # line = line.replace('"', '\"').replace('﻿', '') + '\n'
    #     lines += line
    # trans_lines = translate(lines)
    # print(trans_lines)
    with codecs.open('./source/news1k.zh', 'r', 'utf-8') as f:
        with codecs.open('./result/news1k-youdao.ko', 'a', 'utf-8') as f1:
            lines = ''
            for i, line in enumerate(f.readlines()):
                j = i + 1
                print(str(j), line)
                line = line.replace('"', '\"').replace('﻿', '')
                lines += line
                if line != '\n' and j % 51 == 0:  # 不为空，且51倍数时，写操作
                    main(f1, lines)
                    lines = ''
                    time.sleep(3)
                else:  # 还剩三种情况：空=51，空！=51，不空！=51
                    if line == '\n':
                        continue
                if line != '\n' and j % 53 == 0:  # 不空=51时，写
                    main(f1, lines)
                    lines = ''
                    time.sleep(3)
                else:  # 空=51，空！=51，不空且除了53之外的所有情况都过
                    continue
                main(f1, lines)
