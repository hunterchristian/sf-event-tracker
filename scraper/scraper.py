import sys
# Include modules in parent directory (mainly for /database folder)
sys.path.append('/Users/hunterhodnett/PersonalProjects/sf-events-tracker')

from bs4 import BeautifulSoup

from browser import getPageSource
from formatter import formatDatetime, createDefaultEndTime

from database.createDatabase import db
from database.models import Event

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from hashlib import sha256

db.create_all()

SF_EVENTS_URL = 'http://sf.funcheap.com/events/san-francisco/'
EMPTY_DATE = '<not found>'

def scrape_events():
  soup = BeautifulSoup(getPageSource(SF_EVENTS_URL), 'html.parser')
  
  rows = soup.find('table').find_all('tr')
  event_date = EMPTY_DATE
  for row in rows:
    maybe_date = row.find('h2')
    if maybe_date:
      event_date = maybe_date.get_text(strip=True)

    columns = row.find_all('td')
    if len(columns) == 3:
      time = columns[0].get_text(strip=True)
      desc = columns[1].get_text(strip=True)
      price = columns[2].get_text(strip=True)

      if event_date == EMPTY_DATE:
        raise Exception('Date not found for event: ' + desc)

      # Create hash of all info about this event
      # to detect duplicates in DB
      id = int(sha256((event_date + time + desc + price).encode('utf-8')).hexdigest(), 16) % sys.maxsize

      event = db.session.query(Event).filter_by(id=id).first()

      # TODO handle creation of 'all day' events
      if time == 'All Day':
        continue

      datetime_start = formatDatetime(event_date, time)
      datetime_end = createDefaultEndTime(event_date, time)

      # Only add event to the DB if it doesn't already exist
      if event is None:
        event = Event(
          id=id,
          date=event_date,
          datetime_end=datetime_end,
          datetime_start=datetime_start,
          description=desc,
          price=price,
          time=time
        )

        db.session.add(event)
        db.session.commit()

scrape_events()