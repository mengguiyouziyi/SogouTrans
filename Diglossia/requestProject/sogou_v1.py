# -*- coding: UTF-8 -*-
import hashlib
import requests
import time
import random
import traceback
import codecs


def translate(lines, fr, t):
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'Accept': "application/json",
    }
    url = 'http://fanyi.sogou.com/reventondc/multiLangTranslate'
    data = {
        'text': lines,
        'from': fr,
        'to': t
    }
    try:
        resp = requests.post(url, headers=headers, data=data).json()
        if resp.get('errorCode') != '0':
            return
        trans = resp.get('dit')
        return trans
    except:
        traceback.print_exc()
        return None


def main(f1, lines):
    fr = 'zh-CHS'
    t = 'ko'
    # t = 'zh-CHS'
    # fr = 'ko'
    trans = translate(lines, fr, t)
    f1.write(trans + '\n')


if __name__ == '__main__':
    with codecs.open('./source/zh2ko/oral1600.zh', 'r', 'utf-8') as f, codecs.open('./result/zh2ko/oral1600.zh.ko', 'w',
                                                                                   'utf-8') as f1:
        for line in f:
            print(line)
            if line == '\n':
                print('no line')
                f1.write('\n')
                continue
            main(f1, line)
