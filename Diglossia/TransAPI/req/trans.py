# -*- coding: UTF-8 -*-
import hashlib
import requests
import time
import random
import re
import traceback
import codecs
import execjs

s = requests.Session()
uas = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


class Trans(object):
    src_index = tgt_index = 0

    def __init__(self, api, langf, langt, inf, outf, st=3, lnum=30):
        global src_index
        global tgt_index
        self.headers = {}
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'w', 'utf-8')
        # self.rlines = self.inf.readlines()
        lang = {'youdao': {'zh': 'zh-CHS', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru'},
                'bing': {'zh': 'zh-CHS', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru',
                         'de': 'de'},
                'sogou': {'zh': 'zh-CHS', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru',
                          'de': 'de'},
                'tencent': {'zh': 'zh', 'en': 'en', 'jp': 'jp', 'ko': 'kr', 'fr': 'fr', 'es': 'es', 'ru': 'ru',
                            'de': 'de'},
                'baidu': {'zh': 'zh', 'en': 'en', 'jp': 'jp', 'ko': 'kor', 'fr': 'fra', 'es': 'spa', 'ru': 'ru',
                          'de': 'de'},
                'google': {'zh': 'zh-CN', 'en': 'en', 'jp': 'ja', 'ko': 'ko', 'fr': 'fr', 'es': 'es', 'ru': 'ru',
                           'de': 'de'}}
        try:
            self.langf, self.langt = lang[api][langf], lang[api][langt]
        except:
            traceback.print_exc()
            print('This api dont support this language! Please retry!')
            exit(1)
        self.st = st  # request sleep time
        self.lnum = lnum  # translate line-number once
        # self.ttype = ttype  # translate type(multiple and single)
        self.rmethod = 'POST'  # request method
        self.s = requests.Session()
        self.api = api
        if self.api == 'youdao':
            self.headers = {
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'referer': "http://fanyi.youdao.com/",
            }
            self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
            self.s.get('http://fanyi.youdao.com/')
        elif self.api == 'bing':
            self.headers = {
                'content-type': "application/json; charset=UTF-8",
            }
            self.url = 'http://www.bing.com/translator/api/Translate/TranslateArray?from={f}&to={t}'.format(
                f=self.langf, t=self.langt)
            self.s.get('https://www.bing.com/translator/')
        elif self.api == 'sogou':
            self.headers = {
                'content-type': "application/x-www-form-urlencoded",
                'Accept': "application/json",
            }
            self.url = 'http://fanyi.sogou.com/reventondc/multiLangTranslate'
        elif self.api == 'tencent':
            """10 lines"""
            self.url = 'http://fanyi.qq.com/api/translate'
            if self.lnum > 10:
                print('Dont exceed 10!')
                self.lnum = 10
        elif self.api == 'baidu':
            self.headers = {
                'cookie': "BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1468_25810_13551_21126_17001_20928; BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517819636; PSINO=2; H_PS_PSSID=1468_25810_13551_21126_17001_20928; locale=zh; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636,1517904654; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517904654",
            }
            self.url = 'http://fanyi.baidu.com/v2transapi'
            # self.token, self.gtk = self.get_some()
            self.token, self.gtk = '0e78aac73442f34955d5d1681d701403', '320305.131321201'
        elif self.api == 'google':
            self.url = 'https://translate.google.cn/translate_a/single'
            self.rmethod = 'GET'
        else:
            print('You have to provide a api!<youdao bing sogou tencent baidu google>')
            exit(1)

    def get_some(self):
        """
            for baidu
        :return:
        """
        resp = self.s.get(url='http://fanyi.baidu.com/translate', headers=self.headers)
        token = re.search(r"token: '(\w+)?',", resp.text).group(1)
        gtk = re.search(r"gtk = '([.\d]+)?';", resp.text).group(1)
        return token, gtk

    def get_data(self, lines):
        if self.api == 'youdao':
            salf = str(int(time.time() * 1000) + random.randint(1, 10))
            n = 'fanyideskweb' + lines + salf + "aNPG!!u6sesA>hBAW1@(-"
            sign = hashlib.md5(n.encode('utf-8')).hexdigest()
            data = {
                'i': lines,
                'from': self.langf,
                'to': self.langt,
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': salf,
                'sign': sign,
                'doctype': 'json',
                'version': "2.1",
                'keyfrom': "fanyi.web",
                'action': "FY_BY_REALTIME",
                'typoResult': 'false'
            }
        elif self.api == 'bing':
            data = "[{\"id\":652829,\"text\":\"%s\"}]" % lines
            data = data.encode('utf-8')
        elif self.api == 'sogou':
            data = {
                'text': lines,
                'from': self.langf,
                'to': self.langt
            }
        elif self.api == 'tencent':
            data = {
                'sourceText': lines,
                'source': self.langf,
                'target': self.langt,
                'sessionUuid': 'translate_uuid' + str(int(time.time()) * 1000),
            }
        elif self.api == 'baidu':
            sign = Py4Js().getSign(lines, self.gtk)
            data = {
                'query': lines,
                'from': self.langf,
                'to': self.langt,
                'transtype': 'translang',
                'simple_means_flag': '3',
                'sign': sign,
                'token': self.token
            }
        elif self.api == 'google':
            data = {"client": "t", "sl": self.langf, "tl": self.langt, "hl": "zh-CN",
                    "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"], "ie": "UTF-8", "oe": "UTF-8",
                    "source": "btn", "ssel": "4", "tsel": "3", "kc": "0", "tk": Py4Js().getTk(lines), "q": lines}
        else:
            return

        return data

    def translate(self, lines):
        data = self.get_data(lines)
        self.headers['user-agent'] = random.choice(uas)
        kw = dict(method=self.rmethod, url=self.url, headers=self.headers)
        if self.rmethod == 'GET':
            kw.update(dict(params=data))
        else:
            kw.update(dict(data=data))
        try:
            resp = self.s.request(**kw).json()
        except:
            traceback.print_exc()
            return
        # if self.ttype == 'multi':
        return self.get_multi(resp)
        # else:
        #     return self.get_single(resp)

    def get_multi(self, resp):
        if self.api == 'youdao':
            if resp.get('errorCode') != 0:
                return
            results = resp.get('translateResult', [])
            if not results:
                return
            trans = ''
            for result in results:
                for dict_rt in result:
                    tgt = dict_rt.get('tgt', '')
                    # if 'qwqwqwqwqwqwqwqw' in tgt.lower():
                    #     tgt = '\n'
                    trans += tgt  # 此循环结束后，此行拼接完成
                trans += '\n'  # 结尾添加换行符。空行返回的也是一个dict，不用特别关注
        elif self.api == 'bing':
            items = resp.get('items', [])
            if not items:
                return
            trans = ''
            for item in items:
                tgt = item.get('text', '')
                # if 'qwqwqwqwqwqwqwqw' in tgt.lower:
                #     tgt = '\n'
                trans += (tgt.strip() + '\n')
        elif self.api == 'sogou':
            if resp.get('errorCode') != '0':
                return
            trans = resp.get('dit', '')
            # dit = resp.get('dit', '').split('\n')
            # trans = ''
            # for tgt in dit:
            #     # if 'qwqwqwqwqwqwqwqw' in tgt.lower():
            #     #     tgt = '\n'
            #     trans += (tgt.strip() + '\n')
        elif self.api == 'tencent':
            translate = resp.get('translate')
            if not translate:
                return
            records = translate.get('records', [])
            if not records:
                return
            trans = ''
            for record in records:
                targetText = record['targetText']
                trans += targetText
        elif self.api == 'baidu':
            trans_result = resp.get('trans_result')
            if not trans_result:
                return
            data_baidu = trans_result.get('data', [])
            if not data_baidu:
                return
            trans = ''
            for dbd in data_baidu:
                dst = dbd.get('dst', '')
                # if 'qwqwqwqwqwqwqwqw' in dst.lower():
                #     dst = '\n'
                trans += (dst.strip() + '\n')
        elif self.api == 'google':
            trans = ''
            for record in resp[0][:-1]:
                trans += record[0]
            # ditstr = ''
            # for record in resp[0][:-1]:
            #     ditstr += record[0]
            # dit = ditstr.split('\n')
            # trans = ''
            # for tgt in dit:
            #     # if 'qwqwqwqwqwqwqwqw' in tgt.lower():
            #     #     tgt = '\n'
            #     trans += (tgt.strip() + '\n')
        else:
            trans = ''
        for line in trans.split('\n'):
            self.tgt_index += 1
            print(self.tgt_index, line)
        return trans

    # def get_single(self, resp):
    #     if self.api == 'youdao':
    #         trans = ''
    #     elif self.api == 'bing':
    #         trans = ''
    #     elif self.api == 'sogou':
    #         trans = ''
    #     elif self.api == 'tencent':
    #         translate = resp.get('translate')
    #         if not translate:
    #             return
    #         records = translate.get('records', [])
    #         if not records:
    #             return
    #         trans = ''
    #         for record in records:
    #             targetText = record['targetText']
    #             trans += targetText
    #     elif self.api == 'baidu':
    #         trans = ''
    #     elif self.api == 'google':
    #         trans = ''
    #     else:
    #         trans = ''
    #
    #     return trans

    def write(self, text):
        if text in ['\n', '\r', '\r\n', '\n\r']:
            self.tgt_index += 1
            print(self.tgt_index)
            self.outf.write('\n')
            return
        ttext = self.translate(text.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 5:
                print('exit...')
                exit(1)
            ttext = self.translate(text.strip())
            print('again...')
        self.outf.write(ttext.strip() + '\n')

    # def read_single(self):
    #     for i, line in enumerate(self.rlines):
    #         print(str(i + 1), line)
    #         line = line.replace('"', '\'').replace('\t', '')
    #         yield line

    def read(self):
        lines = ''
        for line in self.inf:
            self.src_index += 1
            print(self.src_index, line.strip())
            if line in ['\n', '\r', '\r\n', '\n\r']:
                if len(lines) > 1:
                    yield lines
                    lines = ''
                yield line
                continue
                # line = 'qwqwqwqwqwqwqwqw' + '\n'
            line = line.replace('"', '\'').replace('\t', '')
            lines += line
            if self.src_index % self.lnum == 0:
                yield lines
                lines = ''
            else:
                continue
        yield lines

    def main(self):
        for text in self.read():
            self.write(text)
            if self.st != 0:
                time.sleep(self.st)


class Bing(object):

    def __init__(self, inf, outf, langf, langt, st=1, session=s, lnum=1, ttype='multi'):
        self.headers = {
            'content-type': "application/json; charset=UTF-8",
        }
        self.url = 'http://www.bing.com/translator/api/Translate/TranslateArray?from={f}&to={t}'.format(f=langf,
                                                                                                        t=langt)
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'a', 'utf-8')
        self.rlines = self.inf.readlines()
        self.st = st
        self.lnum = lnum
        self.ttype = ttype
        self.s = session
        self.s.get('https://www.bing.com/translator/')

    def get_data(self, lines):
        data = '[{"id":877480416,"text":"%s"}]' % lines
        data = data.encode('utf-8')
        return data

    def translate(self, lines):
        data = self.get_data(lines)
        self.headers['user-agent'] = random.choice(uas)
        try:
            resp = self.s.post(self.url, headers=self.headers, data=data).json()
        except:
            traceback.print_exc()
            return
        if self.ttype == 'multi':
            return self.get_multi(resp)
        else:
            return self.get_single(resp)

    def get_single(self, resp):
        items = resp.get('items', [])
        if not items or len(items) == 0:
            return
        trans = items[0].get('text', '')
        return trans

    def get_multi(self, resp):
        items = resp.get('items', [])
        if not items:
            return
        trans = ''
        for item in items:
            tgt = item.get('text', '')
            if tgt in ['mengguiyouziyi']:
                tgt = '\n'
            trans += (tgt.strip() + '\n')
        return trans

    def write(self, lines):
        if lines == '\n' or lines == '\r\n' or lines == '\r':
            self.outf.write('\n')
            return
        ttext = self.translate(lines.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 10:
                print('exit...')
                exit(1)
            self.s.get('https://www.bing.com/translator/')
            ttext = self.translate(lines.strip())
            print('again...')
        self.outf.write(ttext.strip() + '\n')

    def read(self):
        for i, line in enumerate(self.rlines):
            # if (i + 1) < 1393:
            #     continue
            print(str(i + 1), line)
            line = line.replace('"', '\'').replace('﻿', '').replace('\t', '')
            yield line

    def main(self):
        for lines in self.read():
            self.write(lines)
            if self.st != 0:
                time.sleep(self.st)


class Sogou(object):

    def __init__(self, inf, outf, f, t, st=1):
        self.headers = {
            'content-type': "application/x-www-form-urlencoded",
            'Accept': "application/json",
        }
        self.url = 'http://fanyi.sogou.com/reventondc/multiLangTranslate'
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'a', 'utf-8')
        self.rlines = self.inf.readlines()
        self.f, self.t = f, t
        self.st = st

    def translate(self, lines):
        data = {
            'text': lines,
            'from': self.f,
            'to': self.t
        }
        try:
            resp = s.post(self.url, headers=self.headers, data=data).json()
        except:
            traceback.print_exc()
            return
        if resp.get('errorCode') != '0':
            return
        trans = resp.get('dit')
        return trans

    def write(self, lines):
        if lines == '\n' or lines == '\r\n' or lines == '\r':
            self.outf.write('\n')
            return
        ttext = self.translate(lines.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 10:
                print('exit...')
                exit(1)
            ttext = self.translate(lines)
            print('again...')
        self.outf.write(ttext.strip() + '\n')

    def read(self):
        for i, line in enumerate(self.rlines):
            # if (i + 1) < 1393:
            #     continue
            print(str(i + 1), line)
            line = line.replace('"', '\'').replace('﻿', '').replace('\t', '')
            yield line

    def main(self):
        for lines in self.read():
            self.write(lines)
            time.sleep(self.st)


class Tencent(object):

    def __init__(self, inf, outf, f, t, st=1):
        self.headers = {
            # 'accept': "application/json, text/javascript, */*; q=0.01",
            # 'accept-encoding': "gzip, deflate",
            # 'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            # 'connection': "keep-alive",
            # 'content-length': "241",
            # 'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            # 'host': "fanyi.qq.com",
            # 'origin': "http://fanyi.qq.com",
            # 'referer': "http://fanyi.qq.com/",
            # 'x-requested-with': "XMLHttpRequest",
            # 'cache-control': "no-cache",
            # 'postman-token': "9ea73ee4-8bd7-793f-174e-88b890062ac0"
        }
        self.url = 'http://fanyi.qq.com/api/translate'
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'a', 'utf-8')
        self.rlines = self.inf.readlines()
        self.f, self.t = f, t
        self.st = st
        # s.get('http://fanyi.qq.com/')

    def translate(self, lines):
        data = {
            'sourceText': lines,
            'source': self.f,
            'target': self.t,
            'sessionUuid': 'translate_uuid' + str(int(time.time()) * 1000),
        }
        self.headers['user-agent'] = random.choice(uas)
        try:
            resp = s.post(self.url, headers=self.headers, data=data).json()
            print(resp)
        except:
            traceback.print_exc()
            return
        trans = ''
        for records in resp.get('translate').get('records'):
            trans += records['targetText']
        print(trans)
        return trans

    def write(self, lines):
        if lines == '\n' or lines == '\r\n' or lines == '\r':
            self.outf.write('\n')
            return
        ttext = self.translate(lines.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 5:
                print('exit...')
                exit(1)
            ttext = self.translate(lines)
            print('again...')
        self.outf.write(ttext.strip() + '\n')

    def read(self):
        for i, line in enumerate(self.rlines):
            # if (i + 1) < 1393:
            #     continue
            print(str(i + 1), line)
            line = line.replace('"', '\'').replace('﻿', '').replace('\t', '')
            yield line

    def main(self):
        for lines in self.read():
            if lines == '\r\n':
                self.outf.write('\n')
                continue
            self.write(lines)
            time.sleep(self.st)


class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
            var k = "";
            var b = 406644;
            var b1 = 3293161072;
    
            var jd = ".";
            var $b = "+-a^+6";
            var Zb = "+-3^+b+-f";
    
            for (var e = [], f = 0, g = 0; g < a.length; g++) {
                var m = a.charCodeAt(g);
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                e[f++] = m >> 18 | 240,
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                e[f++] = m >> 6 & 63 | 128),
                e[f++] = m & 63 | 128)
            }
            a = b;
            for (f = 0; f < e.length; f++) a += e[f],
            a = RL(a, $b);
            a = RL(a, Zb);
            a ^= b1 || 0;
            0 > a && (a = (a & 2147483647) + 2147483648);
            a %= 1E6;
            return a.toString() + jd + (a ^ b)
        };
    
        function RL(a, b) {
            var t = "a";
            var Yb = "+";
            for (var c = 0; c < b.length - 2; c += 3) {
                var d = b.charAt(c + 2),
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
            }
            return a
        }
    """)

        self.bd_js = execjs.compile("""
            function a(r) {
    if (Array.isArray(r)) {
        for (var o = 0, t = Array(r.length); o < r.length; o++)
            t[o] = r[o];
        return t
    }
    return Array.from(r)
}

function n(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}

function hash(r, _gtk) {
    var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === o) {
        var t = r.length;
        t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substring(r.length,r.length - 10))
    } else {
        for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
            "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
            C !== h - 1 && f.push(o[C]);
        var g = f.length;
        g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
    }
    var u = void 0
        , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
    u = null !== i ? i : (i = _gtk || "") || "";
    for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
        var A = r.charCodeAt(v);
        128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
    }
    for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
        p += S[b],
            p = n(p, F);
    return p = n(p, D),
        p ^= s,
    0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
    p.toString() + "." + (p ^ m)
}

var i = null;
        """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

    def getSign(self, text, gtk):
        return self.bd_js.call('hash', text, gtk)


class Baidu(object):

    def __init__(self, inf, outf, f, t, st=1):
        self.headers = {
            # 'accept': "*/*",
            # 'accept-encoding': "gzip, deflate",
            # 'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            # 'connection': "keep-alive",
            # 'content-length': "171",
            # 'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            # 'cookie': "BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1468_25810_13551_21126_17001_20928; BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517819636; PSINO=2; H_PS_PSSID=1468_25810_13551_21126_17001_20928; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636,1517883650; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517883650; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D",
            'cookie': "BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1468_25810_13551_21126_17001_20928; BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517819636; PSINO=2; H_PS_PSSID=1468_25810_13551_21126_17001_20928; locale=zh; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636,1517904654; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517904654",

            # 'host': "fanyi.baidu.com",
            # 'origin': "http://fanyi.baidu.com",
            # 'referer': "http://fanyi.baidu.com/?aldtype=16047",
            # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            # 'x-requested-with': "XMLHttpRequest",
            # 'cache-control': "no-cache",
            # 'postman-token': "819fa12c-d409-7508-e2b0-d39104c90c39"
        }
        self.url = 'http://fanyi.baidu.com/v2transapi'
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'a', 'utf-8')
        self.rlines = self.inf.readlines()
        self.f, self.t = f, t
        self.st = st
        self.s = s
        self.token, self.gtk, self.cookies = self.get_some()

    def get_some(self):
        headers = {
            # 'accept': "image/webp,image/apng,image/*,*/*;q=0.8",
            # 'accept-encoding': "gzip, deflate",
            # 'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            # 'connection': "keep-alive",
            # 'cookie': "BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1468_25810_13551_21126_17001_20928; BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517819636; PSINO=2; H_PS_PSSID=1468_25810_13551_21126_17001_20928; locale=zh; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636,1517904654; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517904654",
            'cookie': "BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1468_25810_13551_21126_17001_20928; BIDUPSID=9A8AE2183BD3E9117DB522396BDAC93E; PSTM=1513771771; BAIDUID=64CB201E7C2EF5C1B639D5C128CBDC51:FG=1; BDUSS=VIwMFhXaldkT1p0OEpmOX5ZSjNFRWtodW1xNGtBd0JwRmJyd3Nsa01yOGtiWTVhQVFBQUFBJCQAAAAAAAAAAAEAAADQbm4Gc3VuMDEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTgZlok4GZaO; MCITY=-%3A; BDSFRCVID=AI_sJeC62CmwrTbAtIgkKwc89gAgB9OTH6aooTttO34J-bmLO2hXEG0PqU8g0Ku-_vjDogKK0mOTHvbP; H_BDCLCKID_SF=tb4f_I82fIvbfP0kej7Kq4tHenAD0nJZ5mAqoDbGJpOhHljeyxv1yn-Searbq45aQncnaIQqa-3osnRjWfJK3TtwhMrT3tQ43bRT0tPy5KJvfj6e-Ur1hP-UyN3LWh37bDrTVD8MJD--hIDr2-r_h-Fh22T22-uXKK_s3bcg-hcqEIL4LtcKK-70LtOZWpOibKAOVluayDJvDxbSj4Qoh-IjWbtqLqcJaCvf5l6Y5p5nhMJeXj7JDMP0qtOkqTOy523ion6vQpn-HxtuDju5jTvyDHDsb-IX2I3EX4I8Kb7VKROkenjCyntpbt-qJtFL-nr3_hj_5POaOP3ne5rF2MKSDR5nBT5KWCb4oPjXJDJYDJ5bytua-60kQN3T0UuO5bRi5RoH0RQFDn3oyT3VXp0n5x5Tqj_ffRAJVIIQb-3bK4b4MJ3HbbKtKUnHetJXqKD_oCLKtKDtf-bn-tc2-tFshGcL-ncjK-cJLn3-a-52-tbY5-vqeTFrMpbZKxJmMgkeK-opJlj8oJbpXMD5eqoWhbjKQ5OZLJcuLIOFfD_5MCL9e58ben-W5gTXa4J-aIOysJOOaCvC8qTRy4oTj6Dwyf7HB6QC5RrRVpv5KKPBJCOPhq8-3MvB-tr9J4cgaGT82PnGQMt2bMI4Qft20M0IeMtjBbQaJRTXKn7jWhk2Dq72ybjD05TXDaAeJjtDJR3fL-08-bnhfbjkKn3oKR3H-UnLqh-qb67Z0l8Ktt36jfOhjUQ1LqDeM-jzqpR-tK5l_pcmWIQHDITkWMOv-J0z3N7yqx3lbgo4KKJx-RLWeIJo5t5M0J3DhUJiB5OLBan7LJoxfD_2hK0mD5t32--OMmT22-uXKK_s5lT7-hcqEIL4LPcbKl0VLqOAK-nibKAOVR3p5h_B8UbSj4Qohp035-PetUILKDjr2KoSyp5nhMJl3j7JDMP0qJnqaf3y523ion6vQpn-Hxtu-n5jHjj3DGJP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517819636; PSINO=2; H_PS_PSSID=1468_25810_13551_21126_17001_20928; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1516242485,1517382007,1517819636,1517883650; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517883650; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D",

            # 'host': "fanyi.baidu.com",
            # 'referer': "http://fanyi.baidu.com/translate",
            # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            # 'cache-control': "no-cache",
            # 'postman-token': "67313f4f-651a-414a-68f4-e15f98f14c38"
        }
        resp = self.s.get(url='http://fanyi.baidu.com/translate', headers=self.headers)
        token = re.search(r"token: '(\w+)?',", resp.text).group(1)
        gtk = re.search(r"gtk = '([.\d]+)?';", resp.text).group(1)
        cookies = dict(resp.cookies.items())
        return token, gtk, cookies

    def translate(self, lines):
        sign = Py4Js().getSign(lines, self.gtk)
        print(sign)
        """514617.211208
        320305.131321201
        0e78aac73442f34955d5d1681d701403"""
        data = {
            'query': lines,
            'from': self.f,
            'to': self.t,
            'transtype': 'translang',
            'simple_means_flag': '3',
            'sign': sign,
            'token': self.token
        }
        try:
            resp = self.s.post(self.url, headers=self.headers, data=data, timeout=4).json()
            print(resp)
        except:
            traceback.print_exc()
            return
        trans_result = resp.get('trans_result')
        if not trans_result:
            return
        data = trans_result.get('data')
        if not data:
            return
        trans = data[0].get('dst')
        print(trans)
        return trans

    def write(self, lines):
        if lines == '\n' or lines == '\r\n' or lines == '\r':
            self.outf.write('\n')
            return
        ttext = self.translate(lines.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 7:
                print('exit...')
                exit(1)
            ttext = self.translate(lines)
            print('again...')
        self.outf.write(ttext.strip() + '\n')

    def read(self):
        for i, line in enumerate(self.rlines):
            # if (i + 1) < 200:
            #     continue
            print(str(i + 1), line)
            line = line.replace('"', '\'').replace('﻿', '').replace('\t', '')
            yield line

    def main(self):
        for lines in self.read():
            self.write(lines)
            time.sleep(self.st)


class Google(object):

    def __init__(self, inf, outf, f, t, st=1):
        self.headers = {
            # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            # 'x-chrome-uma-enabled': "1",
            # 'x-client-data': "CKa1yQEIkrbJAQijtskBCMG2yQEI+pzKAQipncoBCKijygE=",
            # 'accept': "*/*",
            # 'referer': "https://translate.google.cn/",
            # 'accept-encoding': "gzip, deflate, br",
            # 'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            # # 'cookie': "_ga=GA1.3.1749489104.1517825006; _gid=GA1.3.2065408570.1517825006; 1P_JAR=2018-2-5-10; NID=123=H-vtaHh-UVg2uXSokviy_f3KWgBn8gRb0ORgE1Y8mEBcw1OHEjXlDb1JaguSOrJFqNl6E58WXg2hzUMaFauJVdZPcCyx-bKloqTI-qXQpxULy9HaDWQ0QD-oRrCqKb2x",
            # 'cache-control': "no-cache",
            # 'postman-token': "17adc4e1-ab77-a171-cd71-9e7d343fa275"
        }
        self.url = 'https://translate.google.cn/translate_a/single'
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'w', 'utf-8')
        self.rlines = self.inf.readlines()
        self.f, self.t = f, t
        self.st = st
        # s.get('https://translate.google.cn/')

    def translate(self, lines):
        querystring = {"client": "t", "sl": self.f, "tl": "zh-CN", "hl": "zh-CN",
                       "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"], "ie": "UTF-8", "oe": "UTF-8",
                       "source": "btn", "ssel": "4", "tsel": "3", "kc": "0", "tk": Py4Js().getTk(lines), "q": lines}
        try:
            resp = requests.get(self.url, headers=self.headers, params=querystring).json()
            print(resp)
        except:
            traceback.print_exc()
            return
        trans = ''
        for records in resp[0][:-1]:
            trans += records[0]
        print(trans)
        return trans

    def write(self, lines):
        if lines == '\n' or lines == '\r\n' or lines == '\r':
            self.outf.write('\n')
            return
        ttext = self.translate(lines.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 5:
                print('exit...')
                exit(1)
            ttext = self.translate(lines)
            print('again...')
        self.outf.write(ttext.strip() + '\n')

    def read(self):
        for i, line in enumerate(self.rlines):
            # if (i + 1) < 1393:
            #     continue
            print(str(i + 1), line)
            line = line.replace('"', '\'').replace('﻿', '').replace('\t', '')
            yield line

    def main(self):
        for lines in self.read():
            self.write(lines)
            time.sleep(self.st)


class Niutrans(object):

    def __init__(self, inf, outf, f, t, st=1):
        self.headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'connection': "keep-alive",
            'content-length': "131",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'host': "183.129.153.70:8080",
            'origin': "http://fanyi.niutrans.com",
            'referer': "http://fanyi.niutrans.com/",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "2fae939d-3246-ac0b-f2ea-d9c3806d4444"
        }
        self.url = 'http://183.129.153.70:8080/NiuTransServer/translation?from={f}&to={t}'.format(f=f, t=t)
        self.inf, self.outf = codecs.open(inf, 'r', 'utf-8'), codecs.open(outf, 'w', 'utf-8')
        self.rlines = self.inf.readlines()
        self.st = st

    def translate(self, lines):
        payload = "src_text=%s&url=5" % lines
        try:
            resp = s.post(self.url, headers=self.headers, data=payload).json()
        except:
            traceback.print_exc()
            return
        trans = resp.get('tgt_text').strip()
        return trans

    def write(self, lines):
        if lines == '\n':
            self.outf.write(lines)
        ttext = self.translate(lines.strip())
        n = 0
        while not ttext:
            time.sleep(5)
            n += 1
            if n > 3:
                print('exit...')
                exit(1)
            ttext = self.translate(lines)
            print('again...')
        self.outf.write(ttext + '\n')

    def read(self):
        for i, line in enumerate(self.rlines):
            print(str(i + 1), line)
            line = line.replace('"', '\'').replace('﻿', '').replace('\t', '')
            yield line

    def main(self):
        for lines in self.read():
            self.write(lines)
            time.sleep(self.st)


if __name__ == '__main__':
    """<youdao bing sogou tencent baidu google>"""
    api = 'google'
    langf = 'es'
    langt = 'zh'
    kwargs = dict(api=api, langf=langf, langt=langt, inf='./source/{1}{0}.{0}'.format(langf, langt),
                  outf='./result/{2}{0}_{1}.{0}2{2}'.format(langf, api, langt), st=2, lnum=10)
    Trans(**kwargs).main()
