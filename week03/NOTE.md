# 学习笔记

1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。

 - 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
 - 将增加远程用户的 SQL 语句作为作业内容提交
mysql字符集配置文件my.cnf内容:
```ini
[client]
default_character_set = utf8mb4

[mysql]
default_character_set = utf8mb4
interactive_timeout= 28800		# 针对交互式连接超时时间
wait_timeout= 28800				# 针对非交互式连接超时时间
max_connections=1000			# MySQL的最大连接数
character_set_server = utf8mb4  # MySQL字符集设置
init_connect = 'SET NAMES utf8mb4'  # 服务器为每个连接的客户端执行的字符串
character_set_client_handshake = FALSE
collation_server = utf8mb4_unicode_ci
```
    验证字符集SQL语句：
```sql
mysql> SHOW VARIABLES LIKE 'character_set%';
mysql> SHOW VARIABLES LIKE 'collation_%';
```
    设定远程访问用户
```sql
mysql> create database testdb;
mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'38.97.3.4' IDENTIFIED BY '123456';
mysql> SHOW GRANTS FOR 'testuser';
```

2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
 - 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
 - 将 ORM、插入、查询语句作为作业内容提交

```sql
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 插入记录
user1 = User_table(username="姜子牙", age="99", birthday="1188-01-02", gender="男", education="道士")
user2 = User_table(username="申公豹", age="88", birthday="1158-01-02", gender="男", education="道士")
user3 = User_table(username="苏妲己", age="25", birthday="1118-01-02", gender="男", education="妃子")
session.add(user1)
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
```

3. 为以下 sql 语句标注执行顺序：
```sql
SELECT DISTINCT player_id, player_name, count(*) as num -- 5
FROM player JOIN team ON player.team_id = team.team_id  -- 1
WHERE height > 1.80                                     -- 2
GROUP BY player.team_id                                 -- 3
HAVING num > 2                                          -- 4
ORDER BY num DESC                                       -- 6
LIMIT 2                                                 -- 7
```

4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

Table1

| id | name |
|------|------|
| 1 | table1_table2 |
| 2 | table1 |

Table2

| id | name |
|------|------|
| 1 | table1_table2 |
| 3 | table2 |

结果是：
```sql
mysql> SELECT Table1.id, Table1.name, Table2.id, Table2.name
    -> FROM Table1
    -> INNER JOIN Table2
    -> ON Table1.id = Table2.id;
+----+---------------+----+---------------+
| id | name          | id | name          |
+----+---------------+----+---------------+
|  1 | table1_table2 |  1 | table1_table2 |
+----+---------------+----+---------------+
1 row in set (0.02 sec)

mysql> SELECT Table1.id, Table1.name, Table2.id, Table2.name
    -> FROM Table1
    -> LEFT JOIN Table2
    -> ON Table1.id = Table2.id;
+----+---------------+------+---------------+
| id | name          | id   | name          |
+----+---------------+------+---------------+
|  1 | table1_table2 |    1 | table1_table2 |
|  2 | table1        | NULL | NULL          |
+----+---------------+------+---------------+
2 rows in set (0.04 sec)

mysql> SELECT Table1.id, Table1.name, Table2.id, Table2.name
    -> FROM Table1
    -> RIGHT JOIN Table2
    -> ON Table1.id = Table2.id;
+------+---------------+----+---------------+
| id   | name          | id | name          |
+------+---------------+----+---------------+
|    1 | table1_table2 |  1 | table1_table2 |
| NULL | NULL          |  3 | table2        |
+------+---------------+----+---------------+
2 rows in set (0.06 sec)
```
5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。

  - 先开启执行时间统计功能，profile；
  - 执行一次内连接操作；
  - 添加索引；
  - 再执行一次内连接操作
  - 查看统计结果

```sql
mysql> show variables like "%pro%";
mysql> set profiling=1;             -- 开启执行时间统计功能
mysql> SELECT Table1.id, Table1.name, Table2.id, Table2.name
mysql> FROM Table1 INNER JOIN Table2 ON Table1.name = Table2.name;
mysql> create index table2_name_index on table2(name);
mysql> create index table1_name_index on table1(name);
mysql> show index from table2;
mysql> show index from table1;
mysql> SELECT Table1.id, Table1.name, Table2.id, Table2.name
mysql> FROM Table1 INNER JOIN Table2 ON Table1.name = Table2.name;
mysql> show profiles;
+----------+--------------+------------------------------------------------------------------------------------------------------------------------------+
| Query_ID | Duration     | Query                                                                                                                        |
+----------+--------------+------------------------------------------------------------------------------------------------------------------------------+
|        6 |   1.06267350 | SELECT Table1.id, Table1.name, Table2.id, Table2.name FROM Table1 INNER JOIN Table2 ON Table1.name = Table2.name |
|       13 | 127.40558225 | SELECT Table1.id, Table1.name, Table2.id, Table2.name FROM Table1 LEFT JOIN Table2 ON Table1.name = Table2.name  |
|       16 |   0.10757000 | SELECT Table1.id, Table1.name, Table2.id, Table2.name FROM Table1 LEFT JOIN Table2 ON Table1.name = Table2.name  |
+----------+--------------+------------------------------------------------------------------------------------------------------------------------------+
15 rows in set, 1 warning (0.00 sec)
mysql> select count(*) from table1;
+----------+
| count(*) |
+----------+
|     1992 |
+----------+
1 row in set (0.02 sec)

mysql> select count(*) from table2;
+----------+
| count(*) |
+----------+
|   999999 |
+----------+
1 row in set (0.18 sec)
```
发现在有无索引时，INNER JOIN的查询时间有大约10倍的差距，而LEFT JOIN大约有1000倍的差距。其中table1有大约2000条记录，table2大约有10万条数据。数据量在10000以内时查询时间差距很小。

  哪些情况适合建索引

  * 主键自动建立唯一索引
  * 频繁作为查询条件的字段应该创建索引
  * 查询中与其它表关联的字段，外键关系建立索引
  * 在高并发下倾向创建组合索引
  * 查询中排序、统计、分组的字段

  哪些情况不适合建索引

  * 表记录较少
  * 经常增删改的表
  * 数据重复且分布平均的表字段
  * where条件里用不到的字段

EXPLAIN可以检查SQL语句中是否使用了索引：
```sql
mysql> explain SELECT Table1.id, Table1.name, Table2.id, Table2.name
            FROM Table1 LEFT JOIN Table2 ON Table1.name = Table2.name;
```
