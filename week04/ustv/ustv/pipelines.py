# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class UstvPipeline:
    
    def __init__(self, host, database, user, password, port):
      self.host = host
      self.database = database
      self.user = user
      self.password = password
      self.port = port
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password,
                                  self.database, charset='utf8mb4', port=self.port)
   
    def process_item(self, item, spider):
        try:
            with self.db.cursor() as self.cursor:
                sql = '''INSERT INTO shortcomment_short (subject_id, title, category, nickname, rating, posttime, shorttext) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
                value = tuple(item.values())
                self.cursor.execute(sql, value)
            self.db.commit()
        except Exception as e:
            print(f"数据库错误 {e}")
        return item

    def close_spider(self, spider):
        if self.db is not None:
            self.db.close()
    