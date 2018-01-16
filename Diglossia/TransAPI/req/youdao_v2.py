# -*- coding: UTF-8 -*-
import hashlib
import requests
import time
import random
import traceback
import codecs


def translate(line):
	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
		'Connection': 'keep-alive',
		'Content-Length': '205',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie': 'DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; OUTFOX_SEARCH_USER_ID=-387641640@111.202.103.204; JSESSIONID=abcycARi1YlJ3dwyg1Zbw; OUTFOX_SEARCH_USER_ID_NCOO=1989515012.5791845; fanyi-ad-id=39535; fanyi-ad-closed=1; ___rl__test__cookies=1514269650057',
		'Host': 'fanyi.youdao.com',
		'Origin': 'http://fanyi.youdao.com',
		'Referer': 'http://fanyi.youdao.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
	}
	url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
	salf = str(int(time.time() * 1000) + random.randint(1, 10))
	n = 'fanyideskweb' + line + salf + "aNPG!!u6sesA>hBAW1@(-"
	sign = hashlib.md5(n.encode('utf-8')).hexdigest()
	data = {
		'i': line,
		'from': 'zh-CHS',
		'to': 'ja',
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
		'typoResult': 'true'
	}
	try:
		resp = requests.post(url, headers=headers, data=data).json()
		if resp.get('errorCode') != 0:
			return
		trans = resp.get('translateResult', [])[0][0].get('tgt')
		return trans
	except:
		traceback.print_exc()
		return None


if __name__ == '__main__':
	with codecs.open('./source/tourism1600.zh', 'r', 'utf-8') as f:
		with codecs.open('./result/tourism1600-youdao.jp', 'a', 'utf-8') as f1:
			for i, line in enumerate(f.readlines()):
				if i + 1 < 745:
					continue
				if line == '\n':
					f1.write(line)
					continue
				print(str(i + 1), line)
				line = line.replace('\n', '').replace('\r', '').replace('"', '\"').replace('﻿', '')
				t_line = translate(line)
				n = 0
				while not t_line:
					time.sleep(5)
					n += 1
					if n > 5:
						print('exit...')
						exit(1)
					t_line = translate(line)
					print('again...')
				f1.write(t_line + '\n')
				time.sleep(3)
