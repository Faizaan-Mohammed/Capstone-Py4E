from matplotlib import pyplot as plt
import sqlite3

connection = sqlite3.connect('netflix.sqlite')
cur = connection.cursor()
cur.execute('''SELECT Netflix_M.title, Viewer_Ratings.number_ratings 
			FROM Netflix_M JOIN Viewer_Ratings ON Netflix_M.id = Viewer_Ratings.movie_id''')

test = dict()
for rows in cur:
	mtitle = rows[0]
	nratings = rows[1]
	test[nratings] = mtitle
cur.close()

testnewname = list()
testnewnumber = list()
for (v,k) in sorted(test.items(),reverse=True):
	testnewname.append(k)
	testnewnumber.append(v)	

plt.style.use('fivethirtyeight')
testnewname = testnewname[:10]
testnewnumber = testnewnumber[:10]

plt.barh(testnewname,testnewnumber)
plt.xlabel('Number of ratings')
plt.title('Top 10 movies with most number of ratings')
plt.show()