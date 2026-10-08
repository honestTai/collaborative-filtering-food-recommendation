import random
import pandas as pd
import os
import pymysql

# 切换工作目录到脚本所在的路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_sql():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='foodFlask',
        password='CHANGE_ME_BEFORE_RUNNING',
        db='food_flask',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    df = pd.read_csv('food.csv',encoding='utf-8-sig')

    for i in range(df.shape[0]):
        data = df.iloc[i]

        price_rand = random.uniform(30, 120)

        data1 = (data['标题'], data['类型'], data['简介'], data['图片'], price_rand)

        sql = "insert into foods(foodname,foodtype,recommend,imgurl,price) values" + str(data1)

        try:
            cursor.execute(sql)
            connection.commit()
        except:
            connection.rollback()
        
    cursor.close()
    connection.close()

run_sql()