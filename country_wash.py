import csv
from collections import Counter

#数据处理，拆分以及统计
def read_csv_column(filename, column_name):
    data = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row[column_name])

    return data



countryn=[]
filename = 'BigProjectHW\pachong\movie.csv'  # 替换为你的CSV文件路径
column_name = '国家'
country = read_csv_column(filename, column_name)


for i in range(len(country)):
    country[i]=country[i].replace('\xa0',' ').split(' ')
    countryn=countryn+country[i]
print(countryn)
counter = Counter(countryn)
countryset=list(counter.keys())
num=list(counter.values())
print(countryset)

rows = zip(countryset, num)

with open('BigProjectHW\pachong\country_wash.csv', 'w', newline='',encoding='utf_8_sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Country', 'Num'])

    for row in rows:
        writer.writerow(row)

print('处理过的国家信息已保存至本地')
