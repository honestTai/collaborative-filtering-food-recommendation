import requests
from lxml import html
import csv
import os.path

etree = html.etree

# 切换工作目录到脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 打开CSV文件，如果不存在则创建并写入表头
csv_path = 'food1.csv'

if not os.path.exists(csv_path):
    fp = open(csv_path, 'a+', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(fp)
    csv_writer.writerow(['图片', '标题', '简介', '作者', '收藏数量', '评论数量', '类型'])
else:
    fp = open(csv_path, 'a+', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(fp)

for i in range(17):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }

    # 云南
    url1 = 'https://www.xiaochushuo.com/shicai/4032/?page={}'.format(i+1)

    page_text = requests.get(url=url1, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page_text)

    li_list = tree.xpath('//ul[@class="menu_list"][1]/li')

    for li in li_list:
        try:
            imgurl = li.xpath('.//a/div/img/@src')[0]
            title = li.xpath('.//div[@class="txt"]/a/h4/text()')[0]
            introduction = li.xpath('.//div[@class="txt"]/a/p/text()')[0]
            author = li.xpath('.//div[@class="writer"]/a/text()')[0]
            collect = li.xpath('.//div[@class="list_collect"]/span/text()')[0]
            praise = li.xpath('.//div[@class="praise"]/span/text()')[0]
            csv_writer.writerow([imgurl, title, introduction, author, collect, praise, '云南'])

        except Exception as e:
            print(f'本条爬取异常：{e}')

for i in range(100):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }

    # 川菜
    url2 = 'https://www.xiaochushuo.com/caipu/fenlei257352920/?page={}'.format(i+1)

    page_text = requests.get(url=url2, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page_text)

    li_list = tree.xpath('//ul[@class="menu_list"][1]/li')

    for li in li_list:
        try:
            imgurl = li.xpath('.//a/div/img/@src')[0]
            title = li.xpath('.//div[@class="txt"]/a/h4/text()')[0]
            introduction = li.xpath('.//div[@class="txt"]/a/p/text()')[0]
            author = li.xpath('.//div[@class="writer"]/a/text()')[0]
            collect = li.xpath('.//div[@class="list_collect"]/span/text()')[0]
            praise = li.xpath('.//div[@class="praise"]/span/text()')[0]
            csv_writer.writerow([imgurl, title, introduction, author, collect, praise, '四川'])

        except Exception as e:
            print(f'本条爬取异常：{e}')

for i in range(79):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }

    # 粤菜
    url3 = 'https://www.xiaochushuo.com/caipu/fenlei257352988/?page={}'.format(i+1)

    page_text = requests.get(url=url3, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page_text)

    li_list = tree.xpath('//ul[@class="menu_list"][1]/li')

    for li in li_list:
        try:
            imgurl = li.xpath('.//a/div/img/@src')[0]
            title = li.xpath('.//div[@class="txt"]/a/h4/text()')[0]
            introduction = li.xpath('.//div[@class="txt"]/a/p/text()')[0]
            author = li.xpath('.//div[@class="writer"]/a/text()')[0]
            collect = li.xpath('.//div[@class="list_collect"]/span/text()')[0]
            praise = li.xpath('.//div[@class="praise"]/span/text()')[0]
            csv_writer.writerow([imgurl, title, introduction, author, collect, praise, '粤菜'])

        except Exception as e:
            print(f'本条爬取异常：{e}')

for i in range(8):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }

    # 鲁菜
    url4 = 'https://www.xiaochushuo.com/shicai/12362/?page={}'.format(i+1)

    page_text = requests.get(url=url4, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page_text)

    li_list = tree.xpath('//ul[@class="menu_list"][1]/li')

    for li in li_list:
        try:
            imgurl = li.xpath('.//a/div/img/@src')[0]
            title = li.xpath('.//div[@class="txt"]/a/h4/text()')[0]
            introduction = li.xpath('.//div[@class="txt"]/a/p/text()')[0]
            author = li.xpath('.//div[@class="writer"]/a/text()')[0]
            collect = li.xpath('.//div[@class="list_collect"]/span/text()')[0]
            praise = li.xpath('.//div[@class="praise"]/span/text()')[0]
            csv_writer.writerow([imgurl, title, introduction, author, collect, praise, '鲁菜'])

        except Exception as e:
            print(f'本条爬取异常：{e}')

fp.close()