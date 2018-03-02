# ES_Index_Manage
## 简介 
本脚本可以通过提前指定日期，实现关闭，打开，删除索引的功能。

## 使用注意：
目前只支持index name以日期(2017.11.16)类似格式，如果需要修改，请修改indexs脚本参数。

## 关闭索引

```python
【ES_index_dispose.py】
close_index(10)     关闭10天前的所有索引,默认为5
```

## 删除索引

```shell
【ES_index_dispose.py】
delete_index('2018.02.01')    删除2018.02.01之前的所处于close状态的索引
delete_index()		删除所有处于关闭状态的索引
```

打开索引

```shell
open_index(10)    打开10天前的索引，默认为5{功能待优化}
```

