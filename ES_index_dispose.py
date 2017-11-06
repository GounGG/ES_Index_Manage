# coding:utf-8

import requests
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
import  re
import indexs

'''
delect index    url:"http://192.168.30.135:9200/app-2017.05.16"  headers:'Content-Type: application/json' data:{"query": {"match_all":{}}}'
select log  curl： "http://192.168.30.135:9200/_search"  headers：'Content-Type: application/json' data：{"query": {"match": {"message": {"query": "ERROR|77" }}}'
'''

# request API
class ES_API:
    def __init__(self, url, data, headers):
        self.url=url
        self.data=data
        self.headers=headers

    def delete(self):
        r = requests.delete(url=self.url, data=json.dumps(self.data), headers=self.headers, auth=('Goun', r'fangjipu1314@'))
        v=r.text
        print(v)

    def post(self):
        r = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers, auth=('Goun', r'fangjipu1314@'))
        v=r.text
        print(v)

# 删除索引,删除当前已经关闭的
def delete_index():
    try:
        for i in indexs.gindex(day):
            url = r"http://172.20.10.16:9200/%s" %(i)
            headers = {'Content-Type':'application/json'}
            data = {"query": {"match_all":{}}}
            C=ES_API(url, data, headers)
            C.delete()
            time.sleep(3)
        return "Delete indexs OK!"
    except Exception as e:
        return e

# 关闭索引，day保留多少天，当索引处于关闭状态，资源占用比较少
def close_index(day):
    for i in indexs.dindex(day):
        url = r"http://172.20.10.16:9200/%s/_close?pretty" %(i)
        headers = {'Content-Type':'application/json'}
        data = {}
        C=ES_API(url, data, headers)
        C.post()
        time.sleep(10)
    return "index status close ok!"

def open_index(day):
    for i in indexs.dindex(day):
        url = r"http://172.20.10.16:9200/%s/_close?pretty" %(i)
        headers = {'Content-Type':'application/json'}
        data = {}
        C=ES_API(url, data, headers)
        C.post()
        time.sleep(10)
    return "index status close ok!"

start_time=time.time()
close_index(10)
#delete_index()
stop_time=time.time()
print(u'删除总耗时:',int(stop_time)-int(start_time),'s')









