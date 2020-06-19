import sqlite3
import time

fname = input("Enter the titles' file name: ")
if len(fname) < 1:
	fname = 'titles.txt'
try:
	fhandle = open(fname)
except:
	print('Invalid file name:', fname)
	quit() 

connection = sqlite3.connect('netflix.sqlite')
cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS Netflix_M')
cur.execute('DROP TABLE IF EXISTS Viewer_Ratings')

cur.execute('''CREATE TABLE Netflix_M 
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title TEXT,	
	year_release INTEGER)''')
cur.execute('''CREATE TABLE Viewer_Ratings 
	(movie_id INTEGER NOT NULL,
	avg_rating REAL, number_ratings INTEGER)''')

nmovies = 0
lsttitle = list()
lstyr = list()
for lines in fhandle:
	a = lines.strip()
	b = a.split(',')
	nmovies = nmovies + 1
	year = b[1]
	m_name = b[2]
	lsttitle.append(m_name)
	lstyr.append(year)

lstavg = list()
lstnr = list()
n = 0
test = 'mv_000000'
inttest = 0
testtype = '.txt'
while n<nmovies:
	inttest = inttest + 1
	if n<9:
		tname = test[:]
	elif n<99:
		tname = test[:-1]
	elif n<999:
		tname = test[:-2]
	elif n<9999:
		tname = test[:-3]
	else:
		tname = test[:-4]
	
	testname = tname + str(inttest) + testtype
	nratings = 0
	totrating = 0
	mhandle = open(testname)
	for eachline in mhandle:
		p = eachline.strip()
		q = p.split(',')
		try:
			rating = int(q[1])
		except:
			rating = 0
		
		totrating = totrating + rating
		nratings = nratings + 1
	avgrating = totrating/nratings
	lstnr.append(nratings)
	lstavg.append(avgrating)
	n = n + 1

count = 0
while count<nmovies:
	cur.execute('INSERT INTO Netflix_M (title,year_release) VALUES (?,?)',(lsttitle[count],lstyr[count]))
	cur.execute('SELECT id FROM Netflix_M WHERE title = ?',(lsttitle[count],))
	movie_id = cur.fetchone()[0]
	cur.execute('INSERT INTO Viewer_Ratings (movie_id,avg_rating,number_ratings) VALUES (?,?,?)',(movie_id,lstavg[count],lstnr[count]))
	count = count + 1
	
	if count%1400 == 0:
		print('Data of', count, 'movies retrieved')
		print('Pausing for a moment...')
		time.sleep(5)
connection.commit()

#cur.execute('''SELECT Netflix_M.title, Netflix_M.year_release, Viewer_Ratings.avg_rating, Viewer_Ratings.number_ratings 
#				FROM Netflix_M JOIN Viewer_Ratings 
#				ON Netflix_M.id = Viewer_Ratings.movie_id''')
print('Job Done!')
#connection.commit()
cur.close()