# 张三给李四通过网银转账 100 极客币，现有数据库中三张表：
#   - 一张为用户表，包含用户 ID 和用户名字，
#   - 另一张为用户资产表，包含用户 ID 用户总资产，
#   - 第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。
# 请合理设计三张表的字段类型和表结构；
# 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
# import pymysql
import mysql.connector  # 替换 pymysql 解决 win10 环境中 pymysql 1366 报错问题
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from utils.logger_util import logger


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), nullable=False)
    asset = relationship("Asset", uselist=False, back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer(), primary_key=True)
    user_id = Column(
        Integer(),
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=True
    )
    user = relationship("User", back_populates="asset")
    total_asset = Column(Float(), nullable=False, default=0.0)

    def __repr__(self):
        return f"Asset(id={self.id}, total_asset={self.total_asset})"


class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer(), primary_key=True)
    trans_time = Column(DateTime(timezone=True), default=datetime.utcnow)
    from_id = Column(Integer())
    to_id = Column(Integer())
    amount = Column(Float(), nullable=False)

    def __repr__(self):
        return f"Record(id={self.id}, to_id={self.to_id},\
            from_id={self.from_id}, amount={self.amount})"


class AccountUtils:
    """
    账户操作工具类
    """    
    # dburl = "mysql+pymysql://testuser:tert1234@localhost:3306/geekbank?charset=utf8mb4"
    # 替换 pymysql 解决 win10 环境中 pymysql 1366 报错问题
    dburl = 'mysql+mysqlconnector://testuser:tert1234@localhost:3306/geekbank?charset=utf8mb4'
    engine = create_engine(dburl, echo=False, encoding="utf-8")
    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    
    def initialize_tables(self):
        """创建数据库表
        """        
        Base.metadata.create_all(self.engine)
        logger.info(f"初始化成功，创建了 3 张数据库表：user, asset, record。")
    
    def get_user_by_id(self, id):
        """通过用户id号获取user对象

        Args:
            id (int): 用户 id 号

        Returns:
            user(User): user 用户对象
        """        
        user = self.session.query(User).get(id)
        if user == None:
            logger.warning(f"id号 {id} 不存在")
            sys.exit(0)
        return user

    def is_enough(self, id, amount):
        """判断账户余额是否足够转账

        Args:
            id (int): 用户 id 号
            amount (float): 转出金额

        Returns:
            bool: 余额足够转账时返回True，否则返回False
        """        
        user = self.get_user_by_id(id)
        if user.asset != None:
            return user.asset.total_asset >= amount
        else:
            return False
       
    def add_user(self, name):
        """给user表中添加用户数据

        Args:
            name (字符串): 用户姓名
        """        
        user = User(name=name)
        try:
            self.session.add(user)
            self.session.commit()
            logger.info(f"创建用户 {name}， id号：{user.id} ")
        except SQLAlchemyError as e:
            logger.error("发生数据库错误，回滚")
            logger.error(e)
            self.session.rollback()
       
    def alter_asset(self, id, amount):
        """ 改变用户资产金额
            - 如果用户没有asset，则add添加记录
            - 如果已经有asset，则update更新记录

        Args:
            id (int): 用户id号
            amount (float): 账户变动金额，可正可负
        """        
        user = self.get_user_by_id(id)
        asset = user.asset
        try:
            if asset != None:
                new_amount = user.asset.total_asset + amount
                asset.total_asset = new_amount
            else:
                new_amount = amount
                asset = Asset(user_id=id, total_asset=amount)
                self.session.add(asset)
            self.session.commit()
            logger.info(f"账户 id 号：{id} ，变动金额：{amount} ，当前余额：{new_amount} 。")
        except SQLAlchemyError as e:
            logger.error("发生数据库错误, 回滚")
            logger.error(e)
            self.session.rollback()
    
    def transfer_money(self, from_id, to_id, amount):
        """转账

        Args:
            from_id (int): 被转账户 id 号
            to_id (int): 转账目标账户 id 号
            amount (float): 转账金额
        """        
        from_user = self.get_user_by_id(from_id)
        to_user = self.get_user_by_id(to_id)
        if self.is_enough(from_id, amount):
            try:
                self.alter_asset(from_id, -amount)
                self.alter_asset(to_id, amount)
                record = Record(from_id=from_id, to_id=to_id, amount=amount)
                self.session.add(record)
                self.session.commit()
                logger.info(f"从 {from_id} 到 {to_id} 转账 {amount} 极客币成功")
            except SQLAlchemyError as e:
                logger.error("发生数据库错误, 回滚")
                logger.error(e)
                self.session.rollback()
        else:
            logger.warning(f"被转账 id {from_id} 余额不足！")


if __name__ == "__main__":
    au = AccountUtils()
    # au.initialize_tables()
    # au.add_user("张三")
    # au.add_user("李四")
    # au.alter_asset(1, 10.0)
    # au.transfer_money(1,2,5)
    # au.transfer_money(1,2,500)
    au.alter_asset(1, 10000.0)
    au.transfer_money(1,2,500)
    