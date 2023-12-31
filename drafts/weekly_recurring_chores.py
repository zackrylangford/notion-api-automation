import os
import requests
import json
import datetime

# Get your Notion API token from environment variables
NOTION_TOKEN = os.environ['NOTION_SECRET_KEY']

# Replace this with your database ID
DATABASE_ID = os.environ['NOTION_ZLTASKS_DATABASE']

# The URL of the Notion API endpoint
url = 'https://api.notion.com/v1/pages'

# The headers for the API request. This includes your Notion API token and the version of the Notion API you're using
headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json'
}

# Map each day of the week to a list of tasks that need to be done on that day
weekly_tasks = {
    'Monday': ['Walk or Play with Maisy', 'Laundry', 'Entry Way and Laundry Room Cleaned', 'Maisy Ear Drops (till July 12)'],
    'Tuesday': ['Walk or Play with Maisy', 'Make sure bills are paid', 'Maisy Ear Drops (till July 12)'],
    'Wednesday': ['Walk or Play with Maisy', 'Clean Bathrooms', 'Laundry', 'Maisy Ear Drops (till July 12)'],
    'Thursday': ['Walk or Play with Maisy', 'Order Groceries','Maisy Ear Drops (till July 12)'],
    'Friday': ['Walk or Play with Maisy', 'Basement Straightened and Vacuumed', 'Floors Vacuumed and Mopped', 'Laundry', 'Maisy Ear Drops (till July 12)'],
    'Saturday': ['Walk or Play with Maisy', 'Maisy Ear Drops (till July 12)'],
    'Sunday': ['Walk or Play with Maisy', 'Put out trash', 'Maisy Ear Drops (till July 12)'],
}

#Monthly Tasks
monthly_tasks = {
    1: [], 
    2: ['Skip Hello Fresh'],
    3: ['Monthly Income and Expenses up to date'],
    24: ['Heart and flea meds for pets'],
    28: ['Income and expenses prepped for the month']
}

#Get the current day of the week
day_of_week = datetime.datetime.now().strftime('%A')

#Get current day of the month
day_of_month = datetime.datetime.now().strftime('%A')


def send_to_notion(task_name, due_date, analog_name=None):
    body = {
        'parent': { 'database_id': DATABASE_ID },
        'properties': {
            'Name': {
                'title': [
                    {
                        'text': {
                            'content': task_name
                        }
                    }
                ]
            },
            'Due Date': {
                'date': {
                    'start': due_date.strftime('%Y-%m-%d'),
                }
            }
        }
    }

    if analog_name is not None:
        body['properties']['Analog'] = {
            'select': {
                'name': analog_name
            }
        }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()  # Will raise an exception for HTTP errors

    except requests.exceptions.RequestException as e:
        print(f"Error sending task to Notion: {e}")
        return  # Exit the function

    print(response.json())

current_date = datetime.date.today()

# Loop over the tasks for the current day of the week
for task_name in weekly_tasks.get(day_of_week, []):
    send_to_notion(task_name, due_date=current_date, analog_name='Today')

# Get current day of the month
day_of_month = current_date.day

#Get current month
current_month = current_date.month

# Loop over the tasks for the current day of the month if it's the first day of the month
if day_of_month == 1:
    for day, task_list in monthly_tasks.items():
        for task_name in task_list:
            due_date = current_date.replace(day=day)
            send_to_notion(task_name, due_date=due_date)








