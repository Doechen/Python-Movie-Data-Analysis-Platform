from flask import Flask, render_template
import pymysql


app = Flask(__name__,template_folder='templates',static_folder="static")


@app.route('/')
def index():
    return render_template("index.html")   #主页面时


@app.route('/index')     #分发路由
def home():
    return index()


@app.route('/movie')
def movie():
    datalist = []
    con = pymysql.connect(   #连接
        host='localhost',
        port=3306,
        user='root',
        passwd='111111',
        db='movie',
        charset='utf8'
    )
    cur = con.cursor()   #新建光标
    sql = "select * from movies"
    data = cur.execute(sql)
    result = cur.fetchall()  #每执行一次退后一行，取到一行
    for item in result:
        datalist.append(item)
    cur.close()
    con.close()
    print(datalist)
    return render_template("movie.html", movies=datalist)  #传给movies


@app.route('/score')
def score():
    score = []
    num = []
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='111111',
        db='movie',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from movie_score_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        score.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("score.html", score=score, num=num)


@app.route('/country')
def country():
    country = []
    num = []
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='111111',
        db='movie',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from movie_country_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        country.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("country.html", country=country, num=num)





@app.route('/year')
def year():
    year = []
    num = []
    s = []
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='111111',
        db='movie',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from movie_year_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        s.append(item)
        year.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("year.html", year=year, num=num)




@app.route('/type')
def type():
    type = []
    num = []
    dataset=[]
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='111111',
        db='movie',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from movie_type_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        type.append(str(item[0]))
        num.append(item[1])
    for i in range(len(type)):
        dataset.append({'name':type[i],'value':num[i]})

    cur.close()
    conn.close()
    return render_template("type.html", dataset=dataset,type=type,num=num)



@app.route('/comment')    #词云图
def word():
    return render_template("comment.html")


@app.route('/performance')  #展示界面
def other():
    return render_template("performance.html")




if __name__ == '__main__':
    app.run()
    app.debug=True