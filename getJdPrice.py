#!/usr/bin/pyhton3
#-*- coding: utf-8 -*-
import urllib.request
import json
import pymysql
import time

db = pymysql.connect("localhost","root","","jd_crawler" )

cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

sql_select = "select * from t_commodity where status=1"

try:
  # 执行sql语句
  cursor.execute(sql_select)
  # 执行sql语句
  postData = cursor.fetchall()
except:
  # 发生错误时回滚
  db.rollback()

for item in postData:

  # 获取skuId对应价格
  url='http://p.3.cn/prices/mgets?skuIds=J_'+item['skuId']

  request=urllib.request.Request(url)
  response=urllib.request.urlopen(request)
  content=response.read()

  result=json.loads(content.decode('utf-8'))

  price=result[0]

  now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

  sql_insert = "INSERT INTO t_price(commodityId, price, updateTime) VALUES (%s, %s, str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))" % (item['id'], price['p'], now)

  try:
    # 执行sql语句
    cursor.execute(sql_insert)
    db.commit()
  except:
    print('insert error')
    # 发生错误时回滚
    db.rollback()

else: 
  print('Success Save Price')


# 关闭数据库连接
db.close()
