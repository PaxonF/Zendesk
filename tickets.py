from urllib.parse import urlencode
import json
import requests
import pyodbc
from datetime import timedelta
from datetime import datetime

today = ''
a = 0
while a < 31:	#change for number of days you want to get
	#date functions to get first day of last month
	today = datetime.strptime('2013-09-14' , '%Y-%m-%d') - timedelta(days=a)
		
	year = today.strftime('%Y')
	month = today.strftime('%m').lstrip('0')
	day = today.strftime('%d').lstrip('0')

	fulldatetime = str(year) + '-' + str(month) + '-' + str(day)
	print(fulldatetime)
		
	user = '<your user id>' + '/token' #your user id/email
	pwd = 'xxxxx' #api key obtained from Zendesk Admin website

		
		#add modified tickets to the same list.	
	params = {
			'query': 'type:ticket created:'+ fulldatetime
		}

	url = 'https://yourzendeskwebsite.zendesk.com/api/v2/search.json?' + urlencode(params) #replace yourzendeskwebsite with yours
	#response = session.get(url)	
	while url:	
		response = requests.get(url, auth=(user, pwd))# Do the HTTP get request
		
	# Check for HTTP codes other than 200
		if response.status_code != 200:
			print(response.status_code)
			exit()
			
		data = response.json() #take response from API, use JSON module to parse it
		ticket_list = data['results'] #get first level JSON data and put into object
		
		for ticket in ticket_list:
			cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=YourServerName;DATABASE=YourDatabaseName;UID=UserId;PWD=PasswordHere') #replace as needed
			cursor = cnxn.cursor()
			cursor.execute("INSERT INTO dbo.Tickets (TicketId) VALUES (?)",ticket['id']) ##see ReadMe.txt for SQL DDL
			cnxn.commit()
			cnxn.close()
		url = data['next_page']
	a = a + 1
		