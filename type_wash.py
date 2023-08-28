import csv
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#数据处理，拆分以及统计
def read_csv_column(filename, column_name):
    data = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row[column_name])

    return data



typen=[]
filename = 'D:\本人学习\BigProjectHW\pachong\movie.csv'
column_name = '类型'
type = read_csv_column(filename, column_name)
print(type)


for i in range(len(type)):
    if(type[i]=='纪录片'):
        typen.append('纪录片')
    elif (len(type[i]))%2==0:
        typen=typen+[type[i][j:j + 2] for j in range(0, len(type[i]), 2)]

print(typen)
counter = Counter(typen)
typeset=list(counter.keys())
num=list(counter.values())
print(typeset)


rows = zip(typeset, num)

with open(r'D:\本人学习\BigProjectHW\pachong\type_wash.csv', 'w', newline='',encoding='utf_8_sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Type', 'Num'])

    for row in rows:
        writer.writerow(row)

print('处理过的类型信息已保存至本地')


img = Image.open(r"static\assets\img\tree.jpg")
mask = np.array(img)
wc = WordCloud(font_path="msyh.ttc",
               mask=mask,
               width = 1000,
               height = 700,
               background_color='white',
               max_words=200,
               ).generate(str(typeset))

# 显示词云与保存
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
wc.to_file(r"static\assets\img\word.png")
print('类型词云图已保存至本地')

