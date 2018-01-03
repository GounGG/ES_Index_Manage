# -*- coding:utf-8 -*-

import requests
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
import  re
from weixin import Send_Message
from mail import send_mail

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

    def get(self):
        r = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers)
        v=json.loads(r.text)
        return v
        

    def process(self):
        v = self.get()
        if v.get('status'):
            pass
        else:
            return (v['hits']['hits'])

# 获取日志
def get_data(index):
    date = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    url="http://172.20.10.16:9200/%s-%s/_search" %(index, date)
    headers={'Content-Type':'application/json'}
    # 添加监控关键字，多个关键字用|分割
    data={
         "query": {
             "match": {
                 "message": {
                    "query": "400007"
                }
            }
        }
    }
    C=ES_API(url, data, headers)
    return C.process()

# 应为我的索引都为xx-2017.xx.xx格式，所以indexs为我的索引名，并根据我的indexs，开启多线程
def data():
    indexs=['rapp', 'rweb']
    pool = ThreadPool(len(indexs))
    results = pool.map(get_data, indexs)
    pool.close()
    pool.join()
    return  results

# 对数据进行处理，只需要5分钟内的数据信息，当然也可以在API post提交数据时执行
def returnData():
    value = {}
    for i in data():
        if i:
            for x in i:
                ff = 0
                t = x['_source']['@timestamp']
                tt = re.search(r'^([0-9]{4}-[0-9]{2}-[0-9]{2})[a-zA-Z]+([0-9]{2}:[0-9]{2}:[0-9]{2}).*$', t)
                realtime = str(tt.group(1)) + str(tt.group(2))
                timeArray = time.strptime(realtime, "%Y-%m-%d%H:%M:%S")
                timeDiff = time.time() - time.mktime(timeArray) - 28800
                if int(timeDiff) < 300:
                    v = {}
                    v['time'] = str(tt.group(1)) + ' ' + str(tt.group(2))
                    v['message'] = x['_source']['message']
                    value[ff] = v
                    ff = ff + 1
    return value

# 报警的话，测了微信或者邮件，都是满足的
def if_null():
    if returnData():
        print "准备报警发送！"
        # 为了方便查看，输出json格式，replace主要是处理json为自动生产\符号，需要处理掉，不然无法输出中文
        send_mail(User, "ELK日志报警", json.dumps(returnData(), ensure_ascii=False,sort_keys=True, indent=2).replace('\\\\', '\\'))
        print "报警发送成功！"
        print "#################################分割线#######################################"
    else:
        pass
    time.sleep(300)

if __name__ == '__main__':
    while True:
       if_null()



