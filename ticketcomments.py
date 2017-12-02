from urllib.parse import urlencode
import json
import requests
import pyodbc


user = 'youruserid/email' + '/token'
pwd = 'yourpassword' #api key obtained from Zendesk Admin website

x = 1

while x != '':
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=yourserver;DATABASE=yourdatabasename;UID=youruserid;PWD=yourpassword') #for test usage
	cursor = cnxn.cursor()
	cursor.execute("SELECT TOP 1 TicketId FROM dbo.Tickets WHERE CommentsRetrieved = 0")
	for row in cursor.fetchall():
		x = row.TicketId
	cnxn.close()
	print(x)
	if x == 1:
		exit()
	url = 'https://yourzendeskwebsitename.zendesk.com/api/v2/tickets/' + str(x) + '/comments.json' #replace yourzendeskwebsitename with yours
	response = requests.get(url, auth=(user, pwd))# Do the HTTP get request
		
	# Check for HTTP codes other than 200
	if response.status_code != 200:
		print(response.status_code)
		exit()
	
	data = response.json() #take response from API, use JSON module to parse it
	comments = data['comments']
	for comment in comments:
		ticket = x
		id = comment['id']
		body = str(comment['body'])
		commentcreated = comment['created_at']
		cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=yourserver;DATABASE=yourdatabasename;UID=youruserid;PWD=yourpassword') #for test usage
		cursor = cnxn.cursor()
		cursor.execute("INSERT INTO dbo.TicketComments (TicketId,CommentId,Comment,CommentCreate) VALUES (?,?,?,?)",ticket,id,body,commentcreated)
		cnxn.commit()
		cnxn.close()
		
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=yourserver;DATABASE=yourdatabasename;UID=youruserid;PWD=yourpassword') #for test usage
	cursor = cnxn.cursor()
	cursor.execute("UPDATE dbo.Tickets SET CommentsRetrieved = 1 FROM Zendesk.Tickets WHERE TicketId = ?",x)
	cnxn.commit()
	cnxn.close()