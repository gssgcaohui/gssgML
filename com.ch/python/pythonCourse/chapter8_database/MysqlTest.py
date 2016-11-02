import time, MySQLdb


conn = MySQLdb.connect(host='localhost', user='root', passwd='123', db='test', port=3306)
cur = conn.cursor()
# 删除表
sql = "drop table if exists test1"
cur.execute(sql)
# 创建表
sql = "create table if not exists test1(name  varchar(128) primary key,created int(10))"
cur.execute(sql)

# 写入单行
sql = "insert into test1(name,created) values (%s,%s)"
param = ("zs", int(time.time()))
n = cur.execute(sql, param)
print "insert", n

# 写入多行
sql = "insert into test1(name,created) values (%s,%s)"
param = ("ls", int(time.time()), ("ww", 11), ("zl", 22))
n = cur.execute(sql, param)
print "insertthree", n

# 更新
sql = "update test1 set name=%s where name ='zs'"
param = ("zsagain",)
n = cur.execute(sql, param)
print "update", n

# 查询
n = cur.execute("select * from test1")
for row in cur.fetchall():
    print row
    for r in row:
        print r

# 删除 mysql的占位符是%s
sql = "delete from test1 where name = %s"
param = ("ls",)
n = cur.execute(sql, param)
print 'delete', n

# 查询
n = cur.execute("select * from test1")
print cur.fetchall()

cur.close

# 提交
conn.commit()
# 关闭
conn.close()
