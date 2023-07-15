import os
import caldav
from datetime import datetime
from caldav import DAVClient, Calendar
import datetime

def get_icloud_events():
    # Your iCloud username (Apple ID) and password
    username = os.environ['APPLE_ID_USERNAME'] 
    password = os.environ['ICLOUD_APP_PASS']

    # Your CalDAV URL
    url = os.environ['ICLOUD_CAL_URL']

    # Create a client instance
    client = caldav.DAVClient(
        url=url,
        username=username,
        password=password,
    )

    # Get the calendar
    my_calendars = client.principal().calendars()
    for calendar in my_calendars:
        if calendar.name == 'Home':
            my_calendar = calendar
            break

    print('Fetching events...')
    start_date = datetime.date.today() - datetime.timedelta(days=30)  # 30 days ago
    end_date = datetime.date.today() + datetime.timedelta(days=30)  # 30 days in the future
    events = my_calendar.date_search(start=start_date, end=end_date)

    return events

