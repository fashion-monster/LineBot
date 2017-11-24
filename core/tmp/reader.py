import os, sys


def none_detector(obj):
    if obj == "":
        return "NaN"
    else:
        return obj


def reader():
    """
    return: pattern, popular
    """
    f = open('./2016_6scraping.csv', 'r')
    cnt = 1
    pattern = {}
    popular = {}

    for line in f:
        line = line.rstrip()
        l = line.split(',')

        l5 = none_detector(l[5])
        l6 = none_detector(l[6])
        l7 = none_detector(l[7])
        l8 = none_detector(l[8])
        if (l5 != "NaN") and (l8 != "NaN"):
            patt = 'top1: ' + l5 + ' top2: ' + l6 + ' top3: ' + l7 + ' bottom: ' + l8
        else:
            continue

        for i in range(cnt):
            try:
                if pattern[i] == patt:
                    popular[i] += 1
            except KeyError:
                pattern[cnt] = patt
                popular[cnt] = 1
                cnt += 1
    return pattern, popular


if __name__ == '__main__':
    reader()
