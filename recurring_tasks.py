import os
import requests
import json
import datetime

# Get your Notion API tokens from environment variables
NOTION_TOKEN = os.environ['NOTION_SECRET_KEY']

# Replace this with your database IDs
DATABASE_ID = os.environ['NOTION_ZLTASKS_DATABASE']
RECURRING_TASKS_DATABASE_ID = os.environ['RECURRING_TASKS_DATABASE']
# The URL of the Notion API endpoint
url = 'https://api.notion.com/v1/pages'
query_url = f'https://api.notion.com/v1/databases/{RECURRING_TASKS_DATABASE_ID}/query'

# The headers for the API request. This includes your Notion API token and the version of the Notion API you're using
headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json'
}

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
    print(f"Response from Notion: {response.json()}")

current_date = datetime.date.today()

# Get the current day of the week
day_of_week = datetime.datetime.now().strftime('%A')

# Get current day of the month
day_of_month = current_date.day

# Get recurring tasks
response = requests.post(query_url, headers=headers)
response.raise_for_status()  # Will raise an exception for HTTP errors
recurring_tasks = response.json()['results']
print(f"Fetched {len(recurring_tasks)} tasks from the recurring tasks database.")

for task in recurring_tasks:
    # Continue to the next task if the 'Task Name' property is missing or has no title elements
    if 'Task Name' not in task['properties'] or not task['properties']['Task Name']['title']:
        continue

    task_name = task['properties']['Task Name']['title'][0]['plain_text']
    task_days_of_week = [option['name'] for option in task['properties'].get('Days of Week', {}).get('multi_select', [])]
    task_days_of_month = [int(option['name']) for option in task['properties'].get('Days of Month', {}).get('multi_select', [])]

    # Add task if it's due today (based on day of week)
    if day_of_week in task_days_of_week:
        print(f"Adding task '{task_name}' to the tasks database.")
        send_to_notion(task_name, due_date=current_date, analog_name='Today')


    # Add task if it's due today (based on day of month)
    if day_of_month in task_days_of_month:
        print(f"Adding task '{task_name}' to the tasks database.")
        send_to_notion(task_name, due_date=current_date)

