from bs4 import BeautifulSoup
from selenium import webdriver

SF_EVENTS_URL = 'http://sf.funcheap.com/events/san-francisco/'

def scrape_events():
  browser = webdriver.Chrome()
  browser.get(SF_EVENTS_URL)
  soup = BeautifulSoup(browser.page_source, 'html.parser')
  
  rows = soup.find('table').find_all('tr')
  for row in rows:
    columns = row.find_all('td')
      
    if len(columns) == 1:
      print(columns[0].get_text(strip=True))
    elif len(columns) == 3:
      time = columns[0].get_text(strip=True)
      desc = columns[1].get_text(strip=True)
      price = columns[2].get_text(strip=True)

      print('time: ' + time)
      print('desc: ' + desc)
      print('price: ' + price)
      print('\n')

scrape_events()