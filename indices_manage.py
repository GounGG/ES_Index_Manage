#!/usr/bin/python3
# coding:utf-8

from elasticsearch import Elasticsearch
import curator

'''
;; 删除以filebeat开头的索引
'''
# ES 连接信息，默认为本机的9200端口
client = Elasticsearch()

def Delete_action(index_name, day):
  try:
    ilo = curator.IndexList(client)
    # 筛选以什么开头的，进行删除
    ilo.filter_by_regex(kind='prefix', value=index_name)
    # 按创建时间赛选 older|younger 老的| 新的 timestring 匹配datestamp中的时间(当source为name的时候需)
    ilo.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=day)
    # 进行删除操作
    delete_indices = curator.DeleteIndices(ilo, master_timeout=30)
    # 操作记录，不会执行操作
    msg = delete_indices.do_dry_run()
    # 确定操作
    delete_indices.do_action()
    return msg
  except Exception as e:
    return e

class Remove_alias():
  def __init__(self, name, ilo):
    self.name = name
    self.ilo = ilo
  def run(self):
    remove_alias02 = curator.Alias(name=self.name)
    remove_alias02.remove(self.ilo)
    remove_alias02.do_action()
    return True

def Close_action(index_name, alias_name, day):
  try:
    ilo = curator.IndexList(client)
    # 筛选以什么开头的，进行删除
    ilo.filter_by_regex(kind='prefix', value=index_name)
    # 按创建时间赛选 older|younger 老的| 新的 timestring 匹配datestamp中的时间(当source为name的时候需)
    ilo.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=day)
    # 进行移除别名操作
    try:
      # 在使用alias做查询时，会应为关闭的索引还有别名，导致返回403，所以我们需要移除别名
      Remove_alias(name = alias_name, ilo = ilo).run()
    except Exception as e:
      raise "移除名别失败"
    finally:
      # 进行关闭操作
      close_indices = curator.Close(ilo)
      # 操作记录，不会执行操作
      msg = close_indices.do_dry_run()
      # 执行关闭操作
      close_indices.do_action()
      return msg
  except Exception as e:
    return e

if __name__ == '__main__':
  # Active01
  index_list = ['device', 'web-']
  del_day_list = [5, 15]
  close_day_list = [3, 7]
  alias_list = ['device', 'web']
  for i in map(Delete_action, index_list, del_day_list):
    print(i)
  for i in map(Close_action, index_list, alias_list, close_day_list):
    print(i)
  # Active02
  index_list_02 = ['flow_']
  del_day_list_02 = [45]
  for i in map(Delete_action, index_list_02, del_day_list_02):
    print(i)
