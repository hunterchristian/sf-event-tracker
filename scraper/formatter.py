from datetime import datetime, timedelta

paddedDay = {
  '1': '01',
  '2': '02',
  '3': '03',
  '4': '04',
  '5': '05',
  '6': '06',
  '7': '07',
  '8': '08',
  '9': '09',
}

def createUnformattedDateTime(date,time):
  parts = date.split(',')

  monthday = parts[1].split(' ')
  month = monthday[1].strip()
  day = monthday[2].strip()

  if int(day) < 10:
    day = paddedDay[day]

  year = parts[2].strip()
  time = ''.join(time.split(' ')).strip()

  return datetime.strptime(month + ' ' + day + ' ' + year + ' ' + time.upper(), '%B %d %Y %I:%M%p')

def formatDatetime(date, time):
  # TODO unit tests and better handling of unexpected formats 
  event_start = createUnformattedDateTime(date, time).strftime("%Y-%m-%dT%H:%M:%S")
  return str(event_start)

def createDefaultEndTime(date, time):
  event_start = createUnformattedDateTime(date, time)
  # TODO retrieve accurate end time
  event_end = (event_start + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
  return str(event_end)