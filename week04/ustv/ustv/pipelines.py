# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from utils.dbconfig import read_db_config


class UstvPipeline:
    
    def __init__(self):
        dbserver = read_db_config()
        self.db = pymysql.connect(**dbserver)
    
    def process_item(self, item, spider):
        try:
            with self.db.cursor() as self.cursor:
                sql = '''INSERT INTO shortcomment_short (subject_id, title, category, nickname, rating, posttime, shorttext) VALUES (%s,%s,%s,%s,%s,%s,%s,)'''
                self.cursor.execute(sql, tuple(item.values()))
            self.db.commit()

        except Exception as e:
            print(f"数据库错误 {e}")
        return item

    def close_spider(self, spider):
        if self.db is not None:
            self.db.close()
            print(self.cursor.rowcount)
    