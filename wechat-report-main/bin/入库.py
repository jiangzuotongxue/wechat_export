# coding=utf-8
import pymysql
import re
from pymysql.converters import escape_string
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='jiangzuo',
    db='nnn',
    charset='utf8mb4',
    port=3306)

cur = conn.cursor()

with open(r"/Users/jiangzuo/Desktop/毕业设计/f/江左/诺诺.txt", encoding='utf-8') as f:
    lines = f.readlines()
    filter_lines = []
    reg = "^.*\s\(.+\):"

    for line in lines:
        # 去除转发的聊天记录 简单过滤
        if (line.startswith('江左') or line.startswith('诺诺')) and re.match(reg, line):
            filter_lines.append(line.strip())

for line in filter_lines:
    s1 = line.find(" ")
    s2 = line.find("):")
    name = line[:s1]
    time = line[s1 + 2:s2]
    content = line[s2 + 2:]
    print(line)
    insert_sql = f"insert into log(user,datetime,content) values ('{name}','{time}' ,'{escape_string(content)}')"
    cur.execute(insert_sql)
conn.commit()
