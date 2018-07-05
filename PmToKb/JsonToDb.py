import MySQLdb
import json

datalist = []  　　　　　　　　　　　　　　　　　　　　# python 列表
with open('/data/scripts/logdb/json.txt','r') as f:
    for line in f:　　　　　　　　　　　　　　　　　　　 # 读取json文件中的行（也就是json的object）　　　
        datalist.append(json.loads(line))　　　　　　　 # 将json的object转成 Python的dict，追加到Python 列表中, 结果都是unicode格式：[{},{},{},{},{}] 
for dict in datalist:
    print dict　　　　　　　　　　　　　　　　　　　　 # 打印显示 转换后的结果

for dict in datalist:
    dict[u'LOCAL'] = dict[u'LOCAL'].replace('\r\n','\\r\\n').replace("'s","\\'s")  # 将字段中的特殊：回车换行以及's 转换，方便形成sql语句
    sql = "insert into db1.s1 (mobile,NAME,LOCAL,CreateTime,id) values('%s','%s','%s','%s','%s');" % (dict[u'mobile'],dict[u'NAME'],dict[u'LOCAL'],str(dict[u'CreateTime']),dict[u'id'])
    print sql