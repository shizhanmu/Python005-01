#!/usr/bin/env python
import time
from random import randint
import pymysql
from dbconfig import read_db_config

dbserver = read_db_config()
db = pymysql.connect(**dbserver)

start = time.time()
try:
    # 使用 cursor() 方法创建一个游标对象
    with db.cursor() as cursor:
        for i in range(1):
            # id = randint(4, 999)
            # sql = f'''SELECT name FROM table1 WHERE id="{id}"'''
            # cursor.execute(sql)
            # name = cursor.fetchone()[0]
            # print(f"Result1: {name}")
        
            # sql = f'''SELECT * FROM table1 WHERE name="{name}"'''
            # cursor.execute(sql)
            # result2 = cursor.fetchone()
            # print(f"Result2: {result2}")
        
            sql = '''SELECT Table1.id, Table1.name, Table2.id, Table2.name
            FROM Table1 INNER JOIN Table2 ON Table1.name = Table2.name'''
            cursor.execute(sql)
            result3 = cursor.fetchall()
            print(f"Result2: {result3}")
    db.commit()

except Exception as e:
    print(f"fetch error {e}")

finally:
    # 关闭数据库连接
    db.close()


period = time.time() - start
print(f"It takes {period} seconds. ")