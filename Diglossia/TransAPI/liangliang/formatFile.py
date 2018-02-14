import codecs
import logging

logger = logging.getLogger(__name__)
handle = logging.FileHandler('log.txt')
logger.addHandler(handle)
# logger.setLevel(logging.INFO)

with codecs.open('vocab.src1', 'r', 'utf-8') as f, codecs.open('vocab.src', 'w', 'utf-8') as f1:
    for i, l in enumerate(f):
        print(i)
        ls = l.split('	')
        if not len(ls) == 2:
            print('over')
            exit(1)
        logger.info(str((i + 1)) + repr(l))
        f1.write(ls[1].strip() + '\n')
