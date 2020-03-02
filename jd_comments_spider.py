# -*- coding: utf-8 -*-
# @Time    : 3/3/2020 12:10 AM
# @Author  : Romain 
# @FileName: jd_comments_spider.py
# @Software: PyCharm
# @Comment ：抓取jd商城的商品评论并存储进行分析


import requests
import json
import sqlite3

def get_comments(good_id):
    #good_url_template = 'https://item.jd.com/{}.html'.format(good_id)
    jsonurl='https://club.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(good_id)
    html=requests.get(jsonurl).text
    return html

def data_stored(html):
    conn = sqlite3.connect("comments.db")  # 建立连接，数据库存在时，直接连接；不存在时，创建相应数据库
    # 新建一张表
    conn.execute('''CREATE TABLE Comments_jd

          (ID text PRIMARY KEY     NOT NULL,
          comment text     );''')
    josntext=json.loads(html)
    comments= josntext['comments']
    #注意sql语句中使用了格式化输出的占位符%s和%d来表示将要插入的变量，其中%s需要加引号''
    for comment in comments:
        sql = "insert into Comments_jd(ID,comment) values('%s','%s')" % (comment['id'],comment['content'])
        conn.execute(sql)
        conn.commit()

    # 关闭数据库连接
    conn.close()

if __name__ == '__main__':
    html=get_comments(str(52297931949))
    data_stored(html)