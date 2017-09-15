#!/usr/bin/env python
#Autor: Erick Duffis
#Email:erickduffis@gmail.com
#This is a machine learning code that search for queries that delay the mysql process and kill them
#good for system administrators
#this example only shows a delay method but you can add any amount and train the machine to detect them, 
#such as detecting attacks by injection
import time,os
import MySQLdb
from sklearn import tree

feauters = [[1,1,1,1,1,0],[0,1,0,0,0,1],[0,1,1,1,0,0],[1,1,1,1,1,0],[0,0,0,0,0,1]]
labels = [0,1,0,0,1]
text = ['Bad query','Good query','Bad query','Bad query','Good query']

#Learning proccess
clf = tree.DecisionTreeClassifier()
clf = clf.fit(feauters,labels)

#Database information
DB = MySQLdb.connect(host="192.168.200.100",user="user",passwd="password",db="database")
cur = DB.cursor() #cursor for database

#reurns the data from the query
def searchQuery(mquery):
	table23=0
	auxiliar=0
	ceros=0
	nines=0
	not_in=0
	if mquery.find('table23')>0: #this is a critical table that uses thousands of data
		table23=1
	if mquery.find('auxiliar')>0: #this is a command field that the users uses daily
		auxiliar=1
	if mquery.find('000000000000')>0: #Custom error that user insert int fields
		ceros=1
	if mquery.find('999999999999')>0: #Custom error that user insert int fields
		nines=1
	if mquery.find('not in')>0:	#Critical mysql command used  in big data tables
		not_in=1
	
	return table23,auxiliar,ceros,nines,not_in

while True:
	os.system("clear") #clear Screen
	cur.execute("show full processlist;") #Get process in use
	for row in cur.fetchall():
		table23,auxiliar,ceros,nines,not_in = searchQuery(str(row[7]))
		result  = clf.predict([[table23,auxiliar,ceros,nines,not_in,1]])
		print "[Id]:",row[0]
		print "[Query]:",row[7]
		print "[INFO Prediction]: " + str(text[int(result)])
		
		if str(text[int(result)])=='Bad query' :
			cur.execute("kill " + str(row[0]) + ";")
			DB.commit()
			print "[OK] Process wos killed!!"
	time.sleep(25)	#Sleep for 25 seconds	
