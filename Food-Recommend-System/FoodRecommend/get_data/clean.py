import pandas as pd
import os

# 切换工作目录到脚本所在的路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

data = pd.read_csv('food1.csv', encoding='utf-8-sig')

data.dropna(inplace=True)
data.drop_duplicates(subset=['标题'], keep='first', inplace=True)
data['简介'] = data['简介'].str.replace(r'[\\]', '', regex=True)
data['简介'] = data['简介'].str.strip()

data.to_csv('food.csv', encoding='utf-8-sig', index=False)  # 修正为 utf-8-sig