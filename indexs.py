# coding:utf-8

from elasticsearch import  Elasticsearch
import re
import time
import datetime

now = time.localtime()
data1 = datetime.datetime(now[0], now[1], now[2])

es=Elasticsearch("http://172.20.10.16:9200",http_auth=('Goun', r'fangjipu1314@'))


res = es.cat.indices()

l = res.split('\n')
def dindex(day=5):
    index = []
    for i in l:
        f = i.strip().split()
        if len(f) != 0:
            if str(f[0]) != 'close':
                if re.findall('^fund', f[2]):
                    pass
                elif re.findall('\d+\.\d+\.\d+$', f[2]):
                    time.strptime(re.findall('\d+\.\d+\.\d+$', f[2])[0], "%Y.%m.%d")
                    itime = time.strptime(re.findall('\d+\.\d+\.\d+$', f[2])[0], "%Y.%m.%d")
                    data2 = datetime.datetime(itime[0], itime[1], itime[2])
                    d = (data1-data2).days
                    if int(d) > int(day):
                        index.append(f[2])
    return index

g = res.split('\n')
def gindex():
    index = []
    for i in g:
        f = i.strip().split()
        if len(f) != 0:
            if str(f[0]) == 'close':
                index.append(f[1])
    return index
    

if __name__ == '__main__':
    print dindex()
    print gindex()
