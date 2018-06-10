import sys
# Include modules in parent directory (mainly for /database folder)
sys.path.append('/Users/hunterhodnett/PersonalProjects/sf-events-tracker')

from database.models import Event

from service import service

SF_FUNCHEAP_CAL_ID = '0ci8isapmul5hl42d1foie4pd8@group.calendar.google.com'

def createEvent(event):
    """
    Insert a new event into the SF Funcheap calendar
    """
    event = {
        'summary': event.description,
        'location': "",
        'description': "",
        'start': {
            'dateTime': event.datetime_start,
            'timeZone': "America/Los_Angeles"
        },
        'end': {
            'dateTime': event.datetime_end,
            'timeZone': "America/Los_Angeles"
        },
    }

    event = service.events().insert(calendarId=SF_FUNCHEAP_CAL_ID, body=event).execute()

def uploadEvents():
  events = Event.query.all()
  for event in events:
    createEvent(event)
