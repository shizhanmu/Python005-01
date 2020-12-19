#!/usr/bin/env python
from random import randint
import pymysql
from dbconfig import read_db_config
from faker import Faker

dbserver = read_db_config()
db = pymysql.connect(**dbserver)
faker = Faker()

try:
    
    # 使用 cursor() 方法创建一个游标对象
    with db.cursor() as cursor:
        datas = []
        for i in range(100000, 1000000):
            datas.append((i, faker.name()))
        sql = '''INSERT IGNORE INTO table2 (id, name) VALUES (%s, %s)'''
        values = tuple(datas)
        cursor.executemany(sql, values)
    db.commit()

except Exception as e:
    print(f"insert error {e}")

finally:
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)