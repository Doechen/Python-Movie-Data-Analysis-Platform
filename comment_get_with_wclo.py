import requests
from urllib.parse import urlencode
from lxml import etree
from requests.exceptions import RequestException
import langconv
import re
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba

# 排行页面
def get_top_page(start):
    params = {
        'start': start,
        'filter': '',
    }
    url = 'https://movie.douban.com/top250?' + urlencode(params)
    print(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_text = response.text
            return response_text
        return None
    except RequestException:
        print('获取源代码失败')
        return None
# 评论链接
def get_comment_link(top_page):
    html = etree.HTML(str(top_page))
    result = html.xpath('//div[@class="hd"]//a/@href')
    return result
# 评论页面
def get_comment_page(comment_link, start):
    params = {
        'start': start,
        'limit': '20',
        'sort': 'new_score',
        'status': 'P'
    }
    url = comment_link + 'comments?' + urlencode(params)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_text = response.text
            return response_text
        return 'Error'
    except RequestException:
        print('get_comment_page() Error')
        return None



# 获取评论
def get_comment(comment_page):
    html = etree.HTML(comment_page)
    result = html.xpath('//div[@class="mod-bd"]//div/div[@class="comment"]/p/span/text()')
    return result

# 繁体字转简体字
def Traditional2Simplified(sentence):
    sentence = langconv.Converter('zh-hans').convert(sentence)
    return sentence

# 清理，相应的可能出现的清理内容是上网查的
def clear(string):
    string = string.strip()
    string = re.sub(r"[！!？｡。，&;＂★＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃「」『』【】"
                    r"〔〕〖〗〘〙#〚〛〜〝〞/?=~〟,〰–—‘’‛“”„‟…‧﹏.]", " ", string)
    string = re.sub(r"[!\'\"#。$%&()*+,-.←→/:~;<=>?@[\\]^_`_{|}~", " ", string)
    return Traditional2Simplified(string).lower()


def save_to_txt(results):
    for result in results:
        result = clear(result)
        with open('BigProjectHW\pachong\comment.txt', 'a', encoding='utf-8') as file:
            file.write(result)


#拆分
def cut_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    stop_words=set(line.strip() for line in open('BigProjectHW\cn_stopwords.txt', encoding='utf-8'))
    wordList = []
    for content in lines:
        if "=" in content:
            continue
        contentString = str(content).replace("'","")
        words = jieba.lcut(contentString)
        wordList.extend(words)
    wordDict = {}
    for word in wordList:
        if word in stop_words:
            continue
        if len(word) > 1:
            if word not in wordDict.keys():
                wordDict[word] = 1
            else:
                wordDict[word] = wordDict[word] + 1
    return wordDict




#运行，记录进程
print("爬取开始...")
for start in range(0, 250, 25):
    print("正在爬取第" + str(int(start / 25 + 1)) + "页！！！")
    top_page = get_top_page(start)
    comment_links = get_comment_link(top_page)
    for i, comment_link in enumerate(comment_links):
        for j in range(0, 100, 20):   #设置每个电影的前100评论
            comment_page = get_comment_page(comment_link, j)
            results = get_comment(comment_page)
            save_to_txt(results)
print("Top250电影中每个电影对应的100条评论已保存在本地")


cut_results = cut_text('BigProjectHW\pachong\comment.txt')

img = Image.open(r"static\assets\img\tree.jpg") # 打开遮罩图片
mask = np.array(img) #将图片转换为数组
wc = WordCloud(font_path="msyh.ttc",
               mask=mask,
               width = 1000,
               height = 700,
               background_color='white',
               max_words=200,
               ).generate(str(cut_results))

# 显示词云
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")  # 不显示坐标轴
plt.show() # 显示图片

# 保存到文件
wc.to_file(r"static\assets\img\wCom.png")
print('词云图已保存至本地')

