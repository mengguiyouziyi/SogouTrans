mark = {"en": 1, "zh": 2}

#  [\u4e00-\u9fa5]
def split_zh_en(zh_en_str):
    zh_en_group = []
    zh_gather = ""
    en_gather = ""
    zh_status = False

    for c in zh_en_str:
        if not zh_status and is_zh(c):
            zh_status = True
            if en_gather != "":
                zh_en_group.append([mark["en"], en_gather.strip()])
                en_gather = ""
        elif not is_zh(c) and zh_status:
            zh_status = False
            if zh_gather != "":
                zh_en_group.append([mark["zh"], zh_gather.strip()])
        if zh_status:
            zh_gather += c
        else:
            en_gather += c
            zh_gather = ""

    if en_gather != "":
        zh_en_group.append([mark["en"], en_gather.strip()])
    elif zh_gather != "":
        zh_en_group.append([mark["zh"], zh_gather.strip()])

    return zh_en_group


def is_zh(c):
    x = ord(c)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True

        # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True

        # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
        # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True

        # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True

        # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True

    else:
        return False


if __name__ == '__main__':
    zh_en_group = split_zh_en('India tops global pollution deaths of 9 million a year 全球污染一年致900萬人死亡，印度居冠')
    print(zh_en_group)
