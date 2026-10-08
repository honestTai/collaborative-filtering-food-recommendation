import pandas as pd
import pymysql
import os
import nltk
import re
import jieba
from collections import Counter

# 切换工作目录到脚本所在的路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 连接到数据库
def connect_to_database():
    return pymysql.connect(
        host='127.0.0.1',
        user='foodFlask',
        password='CHANGE_ME_BEFORE_RUNNING',
        db='food_flask',
        charset='utf8mb4'
    )

# 下载停用词列表（如果没有下载过）
stop_words = {'的', '是', '在', '和', '了', '有', '这', '个', '我', '也', '不', '人', '都', '说', '要', '去'}

# 处理简介文本，分词并去除停用词
def process_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # 去除标点符号
    text = re.sub(r'\s+', ' ', text)  # 去除多余空格
    text = text.strip()
    words = jieba.cut(text)
    return [word for word in words if word not in stop_words and len(word) > 1]

# 清空指定表的数据
def clear_table(cursor, table_name):
    try:
        sql = f"DELETE FROM {table_name};"
        cursor.execute(sql)
        cursor.connection.commit()

        sql = f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;"
        cursor.execute(sql)
        cursor.connection.commit()

    except Exception as e:
        print(f"清空表 {table_name} 失败: {e}")
        cursor.connection.rollback()

# 执行数据分析并插入数据库
def run_sql(cursor):
    df = pd.read_csv('food1.csv', encoding='utf-8')

    grouped = df.groupby('类型')['简介'].apply(' '.join).reset_index()

    for idx, row in grouped.iterrows():
        foodtype = row['类型']
        description = row['简介']
        words = process_text(description)
        word_count = Counter(words)

        for word, count in word_count.items():
            if count > 5:
                data = (count, word, foodtype)
                sql = "INSERT INTO wordanalysis(value, name, foodtype) VALUES (%s, %s, %s);"
                try:
                    cursor.execute(sql, data)
                    cursor.connection.commit()
                except Exception as e:
                    print(f"插入数据失败: {e}")
                    cursor.connection.rollback()

    # 统计分析
    analyze_data(cursor, df)

# 分析数据并插入相应表中
def analyze_data(cursor, df):
    # 美食类型
    cate_num = list(df['类型'].value_counts())
    cate_list = list(df['类型'].value_counts().index)

    # 评论
    comment_num = list(df.sort_values(by='评论数量', ascending=False)['评论数量'])[:20]
    comment_list = list(df.sort_values(by='评论数量', ascending=False)['标题'])[:20]

    # 收藏
    collect_num = list(df.sort_values(by='收藏数量', ascending=False)['收藏数量'])[:20]
    collect_list = list(df.sort_values(by='收藏数量', ascending=False)['标题'])[:20]

    insert_analysis_data(cursor, cate_num, cate_list, "cateanalysis", "cate_num", "cate_list")
    insert_analysis_data(cursor, comment_num, comment_list, "commentanalysis", "comment_num", "comment_list")
    insert_analysis_data(cursor, collect_num, collect_list, "collectanalysis", "collect_num", "collect_list")

# 插入分析数据
def insert_analysis_data(cursor, num_list, list_items, table_name, num_col, item_col):
    for i in range(len(num_list)):
        data1 = (num_list[i], list_items[i])
        sql = f"INSERT INTO {table_name}({num_col}, {item_col}) VALUES (%s, %s);"
        try:
            cursor.execute(sql, data1)
            cursor.connection.commit()
        except Exception as e:
            print(f"插入数据到 {table_name} 失败: {e}")
            cursor.connection.rollback()

def main():
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        clear_table(cursor, "cateanalysis")
        clear_table(cursor, "commentanalysis")
        clear_table(cursor, "collectanalysis")
        clear_table(cursor, "wordanalysis")
        run_sql(cursor)
        print("分析数据成功插入数据库！")
    except Exception as e:
        print("出现错误！" + str(e))
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
