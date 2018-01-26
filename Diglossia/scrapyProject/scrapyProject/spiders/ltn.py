# encoding:utf-8
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)
import scrapy
import codecs
import re
from urllib.parse import urljoin
from scrapy.spiders import Spider
from scrapyProject.items import LtnItem
from scrapy.selector import Selector


class MeishijieSpider(Spider):
    name = 'ltn'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'host': "iservice.ltn.com.tw",
            'connection': "keep-alive",
            'cache-control': "no-cache",
            'upgrade-insecure-requests': "1",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'referer': "http://iservice.ltn.com.tw/Service/english/",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            # 'cookie': "__auc=a367f560160dda384d6d0098895; _ga=GA1.3.241169643.1515546969; _gid=GA1.3.1837033544.1515546969; __gads=ID=93267f5838361c0b:T=1515546969:S=ALNI_MZOB93YbcJ_j97UPG5umrXxWuTyHA",
        },
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        url = 'http://iservice.ltn.com.tw/Service/english/index.php?page='
        for p in range(1, 344):  # 344
            yield scrapy.Request(url + str(p))

    def parse(self, response):
        s = Selector(text=response.text)
        urls = s.xpath(
            '//*[@id="content_english"]//tr/td/a/@href').extract()  # //*[@id="content_english"]/table/tr/td/a
        for url in urls:
            url = urljoin(response.url, url)
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        s = Selector(text=response.text)
        title = s.xpath('//h2[@class="title"]/text()').extract_first().replace('《中英對照讀新聞》', '').replace('中英對照讀新聞》', '')
        ps = s.xpath('//div[@id="newsContent"]/p[not(contains(@class, "boldtitle"))]')
        # with codecs.open('zh_tw.txt', 'a', 'utf-8') as zhf:
        #     zhf.write(title + '\n')
        texts = ''
        for i, p in enumerate(ps):
            text = p.xpath('.//text()').extract()
            text = ''.join(text).replace('\n', '').replace('\r', '').strip()
            if not text or '\n' == text:
                continue
            if '例句：' in text or '◎' in text or '新聞辭典' in text or '動詞' in text or '副詞' in text or '慣用語' in text or '名詞' in text or '形容詞' in text or '動詞片語' in text or '片語' in text:
                continue
            if re.search(r'\.（.*。）$', text, re.M):
                continue
            if re.search(r'^[-_A-Za-z0-9]+：', text, re.M):
                continue
            text = text.replace('\n', '').replace('\r', '').strip()
            texts += (text + '\n')
            # zhf.write(text + '\n')
            # zhf.write('\n')
        item = LtnItem()
        item['url'] = response.url
        item['title'] = title
        item['text'] = texts
        yield item
