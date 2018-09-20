#!/usr/bin/python3
# coding:utf-8

import requests
from datetime import datetime
from datetime import timedelta
import time

def get_date(days=2):
    old_time = datetime.now() - timedelta(days=days)
    date = time.strftime('%Y.%m.%d', time.strptime(str(old_time), "%Y-%m-%d %H:%M:%S.%f"))
    return date

def merge_segments(index_name):
    r = requests.get(url="http://10.105.71.144:9200/_cat/indices/{}".format(index_name))
    if int(r.status_code) == 200:
        x = requests.post("http://10.105.71.144:9200/{}/_forcemerge?max_num_segments=1".format(index_name))
        print(x.url, x.text)

index_list = ['web', 'developer', 'device']

for name in  index_list:
   index_name = "{}-{}".format(name, get_date())
   merge_segments(index_name)
