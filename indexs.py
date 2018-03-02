# coding:utf-8

from elasticsearch import  Elasticsearch
import re
import time
import datetime

now = time.localtime()
date1 = datetime.datetime(now[0], now[1], now[2])

es=Elasticsearch("http://172.20.10.16:9200",http_auth=('Goun', r'fangjipu1314@'))


res = es.cat.indices()

# 获取制定日期的indexs
l = res.split('\n')
def dindex(day=5):
    index = []
    for i in l:
        f = i.strip().split()
        if len(f) != 0:
            if str(f[0]) != 'close':
                # 不进行处理的关键字
                if re.findall('^fund|^hf', f[2]):
                    pass
                elif re.findall('\d+\.\d+\.\d+$', f[2]):
                    time.strptime(re.findall('\d+\.\d+\.\d+$', f[2])[0], "%Y.%m.%d")
                    itime = time.strptime(re.findall('\d+\.\d+\.\d+$', f[2])[0], "%Y.%m.%d")
                    date2 = datetime.datetime(itime[0], itime[1], itime[2])
                    d = (date1-date2).days
                    if int(d) > int(day):
                        index.append(f[2])
    return index

# 获取处于close status的index
g = res.split('\n')
def gindex(date=None):
    index = []
    for i in g:
        f = i.strip().split()
        if len(f) != 0:
            if str(f[0]) == 'close':
                Date = re.search(r'[a-zA-Z]+\-([0-9]+\.[0-9]+\.[0-9]+)', str(f[1])).group(1)
                if date != None:
                    itime = time.strptime(Date, "%Y.%m.%d")
                    date1 = datetime.datetime(itime[0], itime[1], itime[2])
                    otime = time.strptime(date, "%Y.%m.%d")
                    date2 = datetime.datetime(otime[0], otime[1], otime[2])
                    if date2 > date1:
                        index.append(f[1]) 
                else:    
                    index.append(f[1])                
    return index
    

if __name__ == '__main__':
    #print dindex()
    print gindex()
