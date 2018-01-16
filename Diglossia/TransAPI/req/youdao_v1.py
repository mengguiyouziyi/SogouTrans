# -*- coding: UTF-8 -*-
import hashlib
import requests
import time
import random
import traceback
import codecs


class Dict:
	def __init__(self):
		self.s = requests.Session()
		self.m = hashlib.md5()
		self.headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
			'Referer': 'http://fanyi.youdao.com/',
			'contentType': 'application/x-www-form-urlencoded; charset=UTF-8'
		}
		self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
		self.base_config()

	def base_config(self):
		self.s.get('http://fanyi.youdao.com/', headers=self.headers)

	def translate(self, line):
		salf = str(int(time.time() * 1000) + random.randint(1, 10))
		n = 'fanyideskweb' + line + salf + "aNPG!!u6sesA>hBAW1@(-"
		sign = hashlib.md5(n.encode('utf-8')).hexdigest()
		data = {
			'i': line,
			'from': 'AUTO',
			'to': 'ko',
			'smartresult': 'dict',
			'client': 'fanyideskweb',
			'salt': salf,
			'sign': sign,
			'doctype': 'json',
			'version': "2.1",
			'keyfrom': "fanyi.web",
			# 'action': "FY_BY_DEFAULT",
			'action': "FY_BY_CLICKBUTTION",
			# 'action': "FY_BY_REALTIME",
			'typoResult': 'false'
		}
		try:
			resp = self.s.post(self.url, headers=self.headers, data=data).json()
			if resp.get('errorCode') != 0:
				return
			trans = resp.get('translateResult', [])[0][0].get('tgt')
			return trans
		except:
			traceback.print_exc()
			return None


if __name__ == '__main__':
	dic = Dict()
	with codecs.open('./source/oral1600.zh', 'r', 'utf-8') as f:
		with codecs.open('./result/oral1600-youdao.ko', 'a', 'utf-8') as f1:
			for i, line in enumerate(f.readlines()):
				if i + 1 < 962:
					continue
				if line == '\n':
					f1.write(line)
					continue
				print(str(i + 1), line)
				line = line.replace('\n', '').replace('\r', '').replace('"', '\"').replace('﻿', '')
				t_line = dic.translate(line)
				n = 0
				while not t_line:
					time.sleep(5)
					n += 1
					if n > 6:
						print('exit...')
						exit(1)
					t_line = dic.translate(line)
					print('again...')
				f1.write(t_line + '\n')
				time.sleep(3)
