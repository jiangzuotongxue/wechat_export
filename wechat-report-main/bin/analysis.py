import functools

import pymysql
import jieba
import json

#读取停用词
def get_stopword_list(file):
    with open(file,'r',encoding='utf-8')as f:
        stopword_list=[word.strip('\n') for word in f.readlines()]
        return stopword_list

#分词 然后清楚清楚停用词
def clean_stopword(str,stopwprd_list):
    result=[]
    word_list=jieba.lcut(str)
    for w in word_list:
        result.append(w)
    return result
stopword_file=r'/Users/jiangzuo/Downloads/git下载文件/wechat-report-main/bin/stop_works'
stopword_list=get_stopword_list(stopword_file)


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='jiangzuo',
    db='nnn',
    charset='utf8mb4',
    port=3306)

cur = conn.cursor()

cur.execute("select * from log")

r = cur.fetchall()
result = {}

# 获得最长的一句话
max_item = None
for item in r:
    content = item[3]
    if (max_item is None or len(content) > len(max_item[3])) and content.find('http') == -1:
        max_item = item
print(max_item)

# # 进行分词
word_arr = []
for item in r:
    content = item[3]
    word_arr = word_arr+clean_stopword(content,stopword_list)
word_count_map = {}
for word in word_arr:
    if word in word_count_map:
        word_count_map[word] = word_count_map[word] + 1
    else:
        word_count_map[word] = 1
word_count_arr = []
for word in word_count_map:
    o = {
        'word': word,
        'count': word_count_map[word]
    }
    word_count_arr.append(o)
    with open("result.txt","a+",encoding="utf-8") as f2:
        f2.write(f"{word}\t{word_count_map[word]}\n")


def custom_sort(x, y):
    if x['count'] > y['count']:
        return -1
    if x['count'] < y['count']:
        return 1
    return 0


result['word'] = sorted(word_count_arr, key=functools.cmp_to_key(custom_sort))

with open("result.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(result, ensure_ascii=False)
    )
