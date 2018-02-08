#!/bin/env python
# -*- coding: utf8 -*-
'''
for every system: get a translation result by (src line, src_lang, tgt_lang)
return the (tgt, flag). flag represents whether the translation is OK.
'''
import os
import sys
import time
import hashlib
import requests


def baidu(src, src_lang, tgt_lang):
    data = {
        'query': src,
        'from': src_lang,
        'to': tgt_lang,
        'transtype': 'translang',
        'simple_means_flag': '3'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Origin': 'http://fanyi.baidu.com/',
        'Referer': 'http://fanyi.baidu.com/',
    }
    url = 'http://fanyi.baidu.com/v2transapi'
    try:
        tgt = requests.post(url, headers=headers, data=data, timeout=4).json()
        print(tgt)
        tgt = tgt['trans_result']['data'][0]['dst'].replace('\n', ' ')
        return tgt, True
    except Exception as e:
        return '', False


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
    # post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=null'
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


def tencent(src, src_lang, tgt_lang):
    data = {
        'sourceText': src,
        'source': src_lang,
        'target': tgt_lang,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    url = 'http://dong.qq.com/api/translate'
    try:
        # tgt = requests.post(url,headers = headers,data=data).json()['records'][0]['targetText']
        tgt = ''
        respond = requests.post(url, headers=headers, data=data, timeout=4).json()['records']
        for result in respond:
            tgt += result['targetText'].replace('\n', ' ')
        return tgt, True
    except Exception as e:
        return '', False


def xunfei(src, src_lang, tgt_lang):
    if 'zh' in src_lang:
        src_lang = 'cn'
    if 'zh' in tgt_lang:
        tgt_lang = 'cn'
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}
    url = "http://www.xfyun.cn/services/mtranslate/tryTranslat?from_lang=%s&to_lang=%s&origin_text=" % (
        src_lang, tgt_lang)
    try:
        html = requests.post(url + src, headers=head, timeout=20)
        html.encoding = html.apparent_encoding
        tgt = html.json()['data']['result'].replace('\n', ' ')
        return tgt, True
    except:
        return '', False


def sogou_search(src, src_lang, tgt_lang):
    if 'zh' in tgt_lang:
        tgt_lang = 'zh-CHS'
    if 'zh' in src_lang:
        src_lang = 'zh-CHS'
    data = {
        'text': src,
        'from': src_lang,
        'to': tgt_lang,
        'useDetect': 'off'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Origin': 'http://fanyi.sogou.com/',
        'Referer': 'http://fanyi.sogou.com/',
    }
    url = 'http://fanyi.sogou.com/reventondc/translate'
    try:
        tgt = requests.post(url, headers=headers, data=data, timeout=4).json()
        tgt = tgt['translate']['dit'].replace('\n', ' ')
        return tgt, True
    except Exception as e:
        return '', False


def sogou_pc(src, src_lang, tgt_lang):
    data = {
        'content': src,
        'from': src_lang,
        'to': tgt_lang,
        'type': 1,
        'domain': 0
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = "http://translator.speech.sogou.com/index.mt"
    try:
        tgt = requests.post(url, headers=headers, data=data, timeout=10)
        print(tgt)
        return tgt, True
    except Exception as e:
        print(e)
        return '', False


mtapi = {'baidu': baidu, 'youdao': youdao, 'tencent': tencent, 'xunfei': xunfei, 'sogou_search': sogou_search,
         'sogou_pc': sogou_pc}

if __name__ == "__main__":
    # parse arguments
    if len(sys.argv) != 4:
        print >> sys.stderr, "%s [baidu|youdao|tencent|xunfei|sogou_search] srclang tgtlang < in > out" % (__file__)
        sys.exit(1)
    com, sl, tl = sys.argv[1:4]
    index = 0
    # load cache
    # read lines from stdin
    for line in sys.stdin:
        index += 1
        print >> sys.stderr, "count=%s" % (index)
        line = line.strip()
        # skip empty lines
        if line == "":
            print("")

        # try 10 times
        for i in range(1, 50):
            result, flag = mtapi[com](line, sl, tl)
            if flag:
                result = result.replace('\n', ' ')
                print >> sys.stdout, result.encode("utf-8")
                break
            else:
                print >> sys.stderr, "Error at line, index=%s, text=%s" % (index, line)
        time.sleep(4)
    # x, y = baidu("Maintenant, j'ai déjà trouvé cet article-là.", 'fra', 'zh')
    # print(x, y)
