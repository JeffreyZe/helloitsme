import requests
import datetime
import time

print('At ', datetime.datetime.now(), ', We started the script.')

url = 'http://192.168.231.6/cgi-bin/login'

values = {'username': 'FAKE123A',
          'password': '00000000'}

while True:
    if requests.post(url, data=values).status_code != 200:
        req = requests.post(url, data=values)
        print('At ', datetime.datetime.now(), ', We are connected.')
        print('hi', req.status_code)
    time.sleep(30 * 60)