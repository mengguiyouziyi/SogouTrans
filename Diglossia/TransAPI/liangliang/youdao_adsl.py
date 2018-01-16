import sys
import time
import youdao


def translate_file(fin, fout, flog, api, src, tgt, divisor, remainder, threshold=5):
    with open(fin) as fin, open(fout, 'w') as fout, open(flog, 'w') as flog:
        for index, l in enumerate(fin):
            if remainder != (index % divisor):
                continue

            error_num = 0
            while error_num < threshold:
                res, flag = api(l.strip(), src, tgt)
                if flag:
                    fout.write(
                        str(index) + '\t' + l.strip().replace('\t', ' ') + '\t' + res.replace('\n', ' ').replace('\t',
                                                                                                                 ' ').strip().encode(
                            'utf8') + '\n')
                    fout.flush()
                    print(res.encode('utf8'))
                    time.sleep(1.0)
                    break
                else:
                    error_num += 1
                    time.sleep(5.0)
            if error_num == threshold:
                flog.write(str(index) + '\t' + l.strip().replace('\t', ' ') + '\n')
                flog.flush()
                print(index, l.strip())
    return


if __name__ == '__main__':
    import set_adsl

    set_adsl.set_interface(sys.argv[1])

    api = youdao.youdao
    fin, fout, flog, src, tgt = sys.argv[2:7]
    divisor, remainder = int(sys.argv[7]), int(sys.argv[8])
    translate_file(fin, fout, flog, api, src, tgt, divisor, remainder, threshold=1)
