Python:Movie Data Analysis Platform
1. Introduction:
Users can access the URL to find the movie title, country, director and lead actor, year of release, rating, quotes and movie genre of Douban Top 250 movies. When clicking on a movie title, you can also jump to the movie's detail page. In this page, users can also search among the 250 movies according to their needs.

Users can also go to the country distribution page and visualize the percentage of Top 250 movies by country through the bar chart, and understand the relationship between quality movies and countries through the analysis below. The same goes for ratings and year of release, which can also be concluded by the following analysis.

If users click on the word cloud interface, they can see the tree graph formed by the reviews of the top250 movies, and click on 'About the movie' on the right side to get a quick preview animation of the movie quotes, so that they can actually experience the movie's impact.


2. Run description:
2.1 Data preparation:
First run the 'pachong and wash.py' file to get the basic movie information saved in the 'movie.csv' file in the pachong directory. Then run 'type_wash.py' and 'country_wash.py' to get the two processed data, which are stored in 'type_wash.csv' and 'country_wash.csv ' files. Because each movie may contain more than one data in the data crawled down directly. In fact in the total list we are in need of this kind of situation where one movie contains corresponding multiple data. But when making a movie data analysis platform, what we need to give users is relatively accurate results, specifically which genre is the most attractive? Which country produced the most popular movies? This requires us to make some new specific quantity tables after splitting. For example, if the country has multi-country cooperation, but the statistics can not be so directly when it is not the same element. Finally, run the 'comment_get_with_wclo.py' file to get the comments of each movie and the resulting word cloud, which are saved in 'comment.txt' and static\assets\img\Wcom.png' (the py file will call zh_wiki.py and langconv.py files by itself). Then connect mysql and import 'movie.csv', 'type_wash.csv', 'country_wash.csv' Import the data into navicat to generate country,type,year,score and the corresponding database for movie.

You need to save the data in your own mysql, so that the 'app.py' file can call out the data and pass it to the html.In fact, I found that in addition to python's statistical aggregate data, navicat for mysql can also be implemented with its code, so I took this opportunity to learn part of the code.So you need to configure Navicat and mysql according to the Navicat installation tutorial mentioned in the reference below, and the specific storage method is described in the mysqlcode.txt document. First, use the mysql code to build the corresponding packets, then use the code to fill in the data of movie_year_num and movie_score_num, and manually import the movie.csv, country_wash.csv, and type_wash.csv into movie, movie_num, and movie_type_num in the pachong document. country_num and movie_type_num packets.

After doing the above, remember to change 'passwd' to your own mysql password in "conn = pymysql.Connect" under each function in the app.py file.


2.2 Run the website
Click directly on the 'app.py' file again to run the file and enter the URL.


2.3 Using the website
The home page consists of four clickable buttons, which correspond to the basic movie information (click on the movie name to enter the detailed page), movie rating statistics, genre statistics, and the review word cloud (click on 'About Movie' to enter the display page). You can also access the corresponding pages through the navigation bar on the top right.There also exit the data analizes, the corresponding data analysis is also presented at the bottom of the displayed web chart.


3.Libraries to be installed
flask
pymysql
urllib.parse
lxml
requests.exceptions
re
wordcloud
numpy
matplotlib.pyplot
jieba
csv
collections
copy
time
os
pandas


Software/Configuration to be installed
navicat
mysql


