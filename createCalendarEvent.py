from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
'''
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])
'''

# Creating an event
# Reference for creating events: https://developers.google.com/calendar/create-events#add_an_event
# Reference for event meta data: https://developers.google.com/calendar/v3/reference/events
startTime = datetime.datetime(2018, 7, 15, 23, 59).isoformat()
endTime = datetime.datetime(2018, 7, 16, 0, 30).isoformat()
eventData = {
  'summary': 'JARVIS AI Event',
  'description': 'An event created from the JARVIS AI project in the works by Scott Russell.',
  'start': {
    'dateTime': startTime,
    'timeZone': 'America/New_York'
  },
  'end': {
    'dateTime': endTime,
    'timeZone': 'America/New_York'
  },
  'reminders': {
    'useDefault': True
  }
}
newEvent = service.events().insert(calendarId='primary', body=eventData).execute()
print ('Event created: %s' % (newEvent.get('htmlLink')))

'''
if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
'''