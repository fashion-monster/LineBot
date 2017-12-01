# coding=utf-8
import json
import requests
import urllib
import time
from datetime import datetime
import math

API_KEY = "390c6d3fbf9fdb070974872249d0e7fc"


def datetime_to_epoch(d):
    return int(time.mktime(d.timetuple()))


def calc_disconfort_index(H, T):
    return 0.81 * T + 0.01 * H * (0.99 * T - 14.3) + 46.3


class Weather(object):
    """docstring for Weather"""

    def __init__(self, lat, lon):
        super(Weather, self).__init__()

        self.LAT = lat
        self.LON = lon
        self.temp_max = []

        url = "http://api.openweathermap.org/data/2.5/forecast?lat={0:}&lon={1:}&units=metric&mode=json&appid={2:}".format(
            self.LAT, self.LON, API_KEY)
        response = urllib.urlopen(url)
        res = response.read()
        j = json.loads(res)
        print(j)

        now = datetime.now()
        print(now)
        epoch = datetime_to_epoch(now)
        print(epoch)
        # 現在時刻から３時間後のEpochを計算する
        now = (math.ceil(epoch / 10800)) * 10800

        for li in j[u"list"]:
            if "12:00:00" in li["dt_txt"]:
                self.temp_max.append(li[u"main"][u'temp_max'])

    def get_temp_max(self):
        return self.temp_max[0]


if __name__ == '__main__':
    w = Weather(39.8, 141.1)
    print(w.get_temp_max())
