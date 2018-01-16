# -*- coding: utf8 -*-
'''
for every system: get a translation result by (src line, src_lang, tgt_lang)
return the (tgt, flag). flag represents whether the translation is OK.
'''
import requests
import time
import hashlib
import sys


def youdao(src, src_lang, tgt_lang):
    if 'zh' in tgt_lang:
        tgt_lang = 'zh-CHS'
    if 'zh' in src_lang:
        src_lang = 'zh-CHS'
    if 'jp' in src_lang:
        src_lang = 'ja'
    if 'jp' in tgt_lang:
        tgt_lang = 'ja'

    m = hashlib.md5()
    u = 'fanyideskweb'
    f = str(int(time.time() * 1000))
    c = "rY0D^0'nM0}g5Mm1z%1G4"
    m.update((u + src + f + c))
    data = {
        'i': src,
        'from': src_lang,
        'to': tgt_lang,
        'smartresult': 'dict',
        'client': u,
        'salt': f,
        'sign': m.hexdigest(),
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
        'typoResult': 'false'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Origin': 'http://fanyi.youdao.com/',
        'Referer': 'http://fanyi.youdao.com/',
    }
    post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=null'
    post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    try:
        youdaojson = requests.post(post_url, headers=headers, data=data, timeout=5).json()
        # tgt = youdaojson['translateResult'][0][1]['tgt']
        tgt = ''
        respond = youdaojson['translateResult'][0]
        for result in respond:
            tgt += result['tgt'].replace('\n', ' ')
        flag = True
        return tgt, flag
    except Exception as e:
        tgt = ''
        flag = False
        return tgt, flag


def test_youdao():
    src = 'He also said "the US" would seek a stronger partnership with India. I love you.'
    print("[the src:]", src)
    res, flag = youdao(src, 'en', 'zh')
    print(res.encode('utf8'), flag)

    print("the zh2en result, src is translted just now")
    res, flag = youdao(res.encode('utf8'), 'zh', 'en')
    print(res.encode('utf8'), flag)


if __name__ == "__main__":
    test_youdao()
