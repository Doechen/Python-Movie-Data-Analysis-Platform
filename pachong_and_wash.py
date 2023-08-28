#编写代码
import requests
from lxml import etree
from time import sleep
import pandas as pd
import os

MOVIES = []
IMGURLS = []


# 获取网页源代码
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    try:
        html = requests.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        # 判断
        if html.status_code == 200:
            print('成功获取源代码')
            # print(html.text)
    except Exception as e:
        print('获取源代码失败：%s' % e)
    return html.text


# 解析网页源代码,数据爬取和清洗
def parse_html(html):
    html = etree.HTML(html)
    tables = html.xpath("//ol[@class='grid_view']//li")
    movies = []
    imgUrls = []


    # 因为要获取标题文本，所以xpath表达式要追加 /text(), t.xpath返回的是一个列表，且列表中只有一个元素所以追加一个[0]
    for t in tables:

        # 电影名
        title = t.xpath(".//div[@class='hd']//span/text()")[0]


        #获取链接
        link=t.xpath(".//div[@class='item']//a")[0]
        link=str(link.attrib).split("'href': ")
        link=link[1].strip("'").strip("'}")

        #参演
        maker=t.xpath(".//div[@class='bd']//p/text()")[0]
        maker = maker.replace(' ','')
        maker = maker.replace('\n','')

        #标签
        pl = t.xpath(".//div[@class='bd']//br")[0]
        pl = pl.tail.replace('\xa0','')
        pl = pl.replace('\n','')


        #评分
        score=t.xpath(".//div[@class='star']//span[2]//text()")[0]


        #摘句
        try:
            quote = t.xpath(".//p[@class='quote']//span/text()")[0]
        except:
            quote=''


        # 截取国家
        pl=pl.split('/')
        country=pl[1]
        if '中' in country:   #数据处理
            country='中国'
        #截取年份
        year=pl[0].strip('\xa0')
        if '中国大陆' in year:
            year=year.replace('(中国大陆)','')   #数据清理
        #截取类型
        tag=pl[2].replace(' ','')
        if '1978' in tag:
            tag='\xa0剧情动画奇幻古装'



        # 截取导演与主演1
        zong=maker



        movie = {
            '电影名': title,
            '国家': country,
            '导演及主演': zong,
            '年份': year,
            '评分': score,
            '引言': quote,
            '链接': link,
            '类型': tag
        }

        # 图片
        imgUrl = t.xpath(".//a/img/@src")[0]

        movies.append(movie)
        imgUrls.append(imgUrl)

    return movies, imgUrls


# 下载图片保存文件
def downloadimg(url, movie):
    if 'img' in os.listdir(r'pachong'):
        pass
    else:
        os.mkdir(r'pachong/img')
    os.chdir(r'pachong/img')
    img = requests.request('GET', url).content

    with open(movie['电影名'] + '.jpg', 'wb') as f:
        print('正在下载: %s' % url)
        f.write(img)




if __name__ == '__main__':
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}'.format(i * 25)
        html = get_html(url)
        sleep(1)
        movies = parse_html(html)[0]
        imgUrls = parse_html(html)[1]

        MOVIES.extend(movies)
        IMGURLS.extend(imgUrls)

    # 下载图片保存文件
    for i in range(250):
        sleep(1)
        downloadimg(IMGURLS[i], MOVIES[i])

    os.chdir(r'BigProjectHW\pachong\img')

    # 以csv格式写入本地
    moviedata = pd.DataFrame(MOVIES)
    moviedata.to_csv(r'pachong\movie.csv', index=False, encoding='utf_8_sig')
    print("电影信息已保存至本地")


