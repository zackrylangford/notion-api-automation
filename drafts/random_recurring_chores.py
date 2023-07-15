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



#Quarterly Tasks
quarterly_tasks = {
    1: ['Call to set up oil changes for vehicles', 'Pay Q4 taxes', 'Descale Keurig'],
    2: ['Change Roomba Air filter'],
    3: ['Change air filter in AC'],
    4: ['Call to set up oil changes for vehicles', 'Pay Q1 taxes'],
    5: ['Change Roomba Air filter'],
    6: ['Pay Q2 taxes', 'Change Air Filter in AC'],
    7: ['Call to set up oil changes for vehicles'],
    8: ['Change Roomba air filter'],
    9: ['Pay Q3 taxes', 'Change Air Filter in AC'],
    10: ['Call to set up oil changes for vehicles'],
    11: ['Change Roomba air filter'],
    12: ['Change Air Filter in AC']   
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


# Get current day of the month
day_of_month = current_date.day

#Get current month
current_month = current_date.month

for task_name in quarterly_tasks.get(current_month, []):
    send_to_notion(task_name, due_date=current_date)







