# coding=utf-8
import json
import urllib

API_KEY = "390c6d3fbf9fdb070974872249d0e7fc"


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

        for li in j[u"list"]:
            if "12:00:00" in li["dt_txt"]:
                self.temp_max.append(li[u"main"][u'temp_max'])

    def get_temp_max(self):
        return self.temp_max[0]


if __name__ == '__main__':
    w = Weather(39.8, 141.1)
    print(w.get_temp_max())
