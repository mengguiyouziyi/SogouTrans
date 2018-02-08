import requests
import string
import time
import hashlib
import json

# init
api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
my_appid = ''
cyber = ''
lower_case = list(string.ascii_lowercase)


def requests_for_dst(word):
    # init salt and final_sign
    salt = str(time.time())[:10]
    final_sign = str(my_appid) + word + salt + cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    # 区别en,zh构造请求参数
    if list(word)[0] in lower_case:
        paramas = {
            'q': word,
            'from': 'en',
            'to': 'zh',
            'appid': '%s' % my_appid,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }
        my_url = api_url + '?appid=' + str(
            my_appid) + '&q=' + word + '&from=' + 'en' + '&to=' + 'zh' + '&salt=' + salt + '&sign=' + final_sign
    else:
        paramas = {
            'q': word,
            'from': 'zh',
            'to': 'en',
            'appid': '%s' % my_appid,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }
        my_url = api_url + '?appid=' + str(
            my_appid) + '&q=' + word + '&from=' + 'zh' + '&to=' + 'en' + '&salt=' + salt + '&sign=' + final_sign
    response = requests.get(api_url, params=paramas).content
    content = str(response, encoding="utf-8")
    json_reads = json.loads(content)
    print(json_reads['trans_result'][0]['dst'])


while True:
    word = input("输入你想翻译的内容: ")
    requests_for_dst(word)


"""
# if targetText in ['Qwqwqwqwqwqwqwqw', 'qwqwqwqwqwqwqwqw', 'qwqwqwqwqwqwqwqw qwqwqwqwqw',
                #                   'wblankspace89w', 'Se tradurre vi appassiona e diverte, venite a tradurre con noi.',
                #                   'q.', 'w w w w w w w w w w w w w w w w w w', 'O que se passa?',
                #                   'Hayır, hayır, hayır, hayır.', '- Hạ sĩ Shaw. - Hạ sĩ Shaw.',
                #                   '= = = = = = = = = = = = = = = = = =', 'จัสติน จัสติน', 'Pulau Faraway Downs.',
                #                   'qwwwwwwwqwqw', '[原件:英文]', '-=YTET -伊甸园字幕组=- 翻译:', '(ququq', 'Ququequek', '页:1', '叩',
                #                   '武当行动', '(呻吟)', '轻声尖叫声尖叫声', 'GESCHÄFTSORDNUNG', 'qwqwqwqwqwqwqwqwqw',
                #                   'qwqwqwqwqwqwqw', 'Effect of the economy', 'qwqwqwqwqwqw',
                #                   'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw']:
                #     targetText = '\n'
"""