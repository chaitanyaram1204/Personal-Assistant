from Google import Create_Service,convert_to_RFC_datetime
import pandas as pd


SecretFile='client_secret_file.json' # add your file
ApiName = 'tasks'
ApiVersion='v1'
scopes = ['https://www.googleapis.com/auth/tasks']
service = Create_Service(SecretFile,ApiName,ApiVersion,scopes)

'''tasklistRestaurants = service.tasklists().insert(
    body = {'title':'Restaurants to try'}
).execute()

for i in range(1):
    
    service.tasklists().insert(body={'title':'Tasklst #{0}'.format(i+1)}).execute()'''
response = service.tasklists().list().execute()
lstItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.tasklists().list(
        maxResults=30,
        pageToken=nextPageToken
    ).execute()
    lstItems.extend(response.get('items'))
    nextPageToken = response.get('nextPageToken')

print()
temp=pd.DataFrame(lstItems).head()['id'][0]
mainTasklistId = temp
"""title = 'San Francisco'
notes = ''
due = ''
status = 'needsAction'
deleted = False
"""
data = ["Water plants","2023-10-28"]
title = data[0]
print(data[0])
notes = ''
date = data[1]
print(date)
due = date+'T00:00:00.000Z'
status = 'needsAction'
deleted = False

request_body = {
    'title': title,
    'notes': notes,
    'due': due,
    'deleted': deleted,
    'status': status
}

response = service.tasks().insert(
    tasklist=mainTasklistId,
    body=request_body
).execute()


'''pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)
pd.set_option('display.min_rows', 500)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 120)
pd.set_option('expand_frame_repr', True)'''
