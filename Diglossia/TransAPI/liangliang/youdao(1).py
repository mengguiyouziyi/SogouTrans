import requests
import sys
import os
import time


def get_html_by_word(word, out):
    url = 'http://dict.youdao.com/example/blng/ko/%s/#keyfrom=dict.main.moreblng' % word.decode('utf8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    with open(out, 'w') as f:
        try:
            f.write(requests.get(url, headers=headers).content)
        except:
            print('ERROR', word)
    return


def get_htmls(fvocab, out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    with open(fvocab, 'r') as f:
        for l in f:
            index, word = l.split()
            path = os.path.join(out_dir, '%09d.html' % (int(index)))
            if not os.path.exists(path):
                get_html_by_word(word, path)
                time.sleep(1.2)
            print(index)
    return


def ishan(text):
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)


def filter_vocab(fin, fout, flog):
    with open(fin) as fin, open(fout, 'w') as fout, open(flog, 'w') as flog:
        for i, l in enumerate(fin):
            l1 = l.strip().decode('utf8')
            if ishan(l1):
                fout.write(str(i) + '\t' + l)
            else:
                flog.write(str(i) + '\t' + l)
    return


if __name__ == '__main__':
    # filter_vocab(*sys.argv[1:4])
    get_htmls(*sys.argv[1:3])
