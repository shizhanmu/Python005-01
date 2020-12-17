#!/usr/bin/env python
# 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
# 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
# 将 ORM、插入、查询语句作为作业内容提交

import pymysql
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User_table(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    age = Column(Integer())
    birthday = Column(Date())
    gender = Column(String(2))
    education = Column(Enum("小学", "初中", "高中", "专科", "本科", "硕士", "博士"))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"User_table(id={self.id}, username={self.username}, gender={self.gender})"

dburl = "mysql+pymysql://testuser:123456@localhost:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")
# Base.metadata.create_all(engine)

SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 插入记录
user1 = User_table(username="姜子牙", age="99", birthday="1188-01-02", gender="男", education="博士")
user2 = User_table(username="申公豹", age="88", birthday="1158-01-02", gender="男", education="硕士")
user3 = User_table(username="苏妲己", age="25", birthday="1118-01-02", gender="男", education="本科")
# session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

# 查询记录
result = session.query(User_table).all()
for r in result:
    print(result)
session.commit()

# 更新记录
query = session.query(User_table)
query = query.filter(User_table.id == 3)
query.update({User_table.gender: '女'})
new_user = query.first()
print(new_user.gender)
session.commit()

# 删除记录
query = session.query(User_table)
query = query.filter(User_table.username == '申公豹')
# session.delete(query.one())
query.delete()      # 就地删除方式
print(query.first())
session.commit()
