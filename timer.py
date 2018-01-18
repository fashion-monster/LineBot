import threading, time
import datetime, time
from time import sleep
import requests


def timerun():
    while True:
        if datetime.datetime.now().hour == 0 + 15 and datetime.datetime.now().minute == 22 and datetime.datetime.now().second == 0:
            while requests.post(url='https://127.0.0.1:5000/push_message'):
                print('b')
            print (datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            time.sleep(10)


thread_obj = threading.Thread(target=timerun)
thread_obj.start()
