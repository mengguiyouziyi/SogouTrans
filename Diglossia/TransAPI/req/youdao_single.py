# coding: utf-8
import time
import random
import hashlib
import requests
import traceback
import codecs


def translate(line):
	url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='

	content = line

	s = "AUTO",
	l = "ko"
	u = 'fanyideskweb'
	c = 'aNPG!!u6sesA>hBAW1@(-'
	d = content
	f = str(int(time.time() * 1000) + random.randint(1, 10))
	sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()

	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
		'Connection': 'keep-alive',
		'Content-Length': '205',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie': 'JSESSIONID=aaalHNVSigPD8-hsnhf3v; SESSION_FROM_COOKIE=fanyiweb; OUTFOX_SEARCH_USER_ID=526401539@113.16.65.153; _ntes_nnid=1892114ba72ae7f868a29a4db02914a0,1502250589343; _dict_cpm_show=1502250589350; _dict_cpm_close=1; OUTFOX_SEARCH_USER_ID_NCOO=1688640113.572293; ___rl__test__cookies=1502251640921',
		'Host': 'fanyi.youdao.com',
		'Origin': 'http://fanyi.youdao.com',
		'Referer': 'http://fanyi.youdao.com/',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
	}

	data = {}
	data['i'] = content
	data['from'] = s
	data['to'] = l
	data['smartresult'] = 'dict'
	data['client'] = 'fanyideskweb'
	data['salt'] = f
	data['sign'] = sign
	data['doctype'] = 'json'
	data['version'] = '2.1'
	data['keyfrom'] = 'fanyi.web'
	data['action'] = 'FY_BY_CLlCKBUTTON'
	data['typoResult'] = 'true'

	try:
		resp = requests.post(url, data, headers=headers).json()
		if resp.get('errorCode') != 0:
			return
		trans = resp.get('translateResult', [])[0][0].get('tgt')
		return trans
	except:
		traceback.print_exc()
		return None


if __name__ == '__main__':
	trans = translate('虽然我是外国人，但是我还是很喜欢中国文化。')
	print(trans)
# 	with codecs.open('./source/oral1600.zh', 'r', 'utf-8') as f:
# 		with codecs.open('./result/oral1600-youdao-2.ko', 'a', 'utf-8') as f1:
# 			for i, line in enumerate(f.readlines()):
# 				if i + 1 < 810:
# 					continue
# 				if line == '\n':
# 					f1.write(line)
# 					continue
# 				print(str(i + 1), line)
#
# 				line = line.replace('\n', '').replace('\r', '').replace('"', '\"')
# 				t_line = translate(line)
# 				n = 0
# 				while not t_line:
# 					time.sleep(5)
# 					n += 1
# 					if n > 6:
# 						print('exit...')
# 						exit(1)
# 					t_line = translate(line)
# 					print('again...')
# 				f1.write(t_line + '\n')
# 				time.sleep(2.5)
