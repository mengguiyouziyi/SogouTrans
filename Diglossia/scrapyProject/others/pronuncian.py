try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve
from scrapy.selector import Selector
import time
import requests


def down(url='https://pronuncian.com/introduction-to-linking/'):
    headers = {
        'accept': "*/*",
        'accept-encoding': "identity;q=1, *;q=0",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'range': "bytes=0-",
        'referer': "https://pronuncian.com/introduction-to-linking/",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        'cache-control': "no-cache",
    }
    res = requests.get(url, headers=headers)
    s = Selector(text=res.text)
    audio_urls = s.xpath('//div[@class="sqs-audio-embed"]/@data-url').extract()

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

    for audio in audio_urls:
        print('Download %s' % audio)
        file = audio.split('/')[-1]
        urlretrieve(audio, file, cbk)
        time.sleep(2)


if __name__ == '__main__':
    down()
