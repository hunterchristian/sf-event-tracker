from bs4 import BeautifulSoup

from browser import getPageSource

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from hashlib import sha256

engine = create_engine('sqlite:///events.db', echo=False)
Base = declarative_base()

class Event(Base):
  """
  A table to store data on events that are happening in San Francisco
  """

  __tablename__ = 'events'
  id          = Column(String, primary_key=True)
  #link        = Column(String, unique=True)
  date        = Column(String)
  time        = Column(String)
  description = Column(String)
  price       = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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
      id = sha256((event_date + time + desc + price).encode('utf-8')).hexdigest()

      event = session.query(Event).filter_by(id=id).first()

      # Only add event to the DB if it doesn't already exist
      if event is None:
        event = Event(
          id=id,
          date=event_date,
          time=time,
          price=price
        )

        session.add(event)
        session.commit()

scrape_events()