import os
import requests
import json
import datetime
from datetime import date, datetime

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



#Get current date information
current_date = date.today()
current_week_number = current_date.isocalendar()[1]
current_month = current_date.month
current_year = current_date.year
day_of_week = datetime.now().strftime('%A')
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
    task_frequency = task['properties'].get('Frequency', {}).get('select', {}).get('name')
    task_start_date = task['properties'].get('Start Date', {}).get('date', {}).get('start')
    print(f"Adding {task_name} to Next Actions database") 



    if task_frequency == 'Daily':
        send_to_notion(task_name, due_date=current_date, analog_name='Today')

    elif task_frequency == 'Weekly' and day_of_week in task_days_of_week:
        send_to_notion(task_name, due_date=current_date, analog_name='Today')

    elif task_frequency == 'Every Other Week' and day_of_week in task_days_of_week:
        # Parse the start date into a datetime object
        start_date = datetime.strptime(task_start_date, '%Y-%m-%d')
        start_week_number = start_date.isocalendar()[1]
        # Check if the difference between the current week number and the start week number is even
        if (current_week_number - start_week_number) % 2 == 0:
            send_to_notion(task_name, due_date=current_date, analog_name='Today')



    # For monthly tasks
    elif task_frequency == 'Monthly' and day_of_month == 1:
        task_due_days = [int(option['name']) for option in task['properties'].get('Days of Month', {}).get('multi_select', [])]
        for due_day in task_due_days:
            print(f"Adding monthly task '{task_name}' to the tasks database for the date: {current_year}-{current_month}-{due_day}.")
            due_date = date(current_year, current_month, due_day)
            send_to_notion(task_name, due_date=due_date)


    elif task_frequency == 'Every Other Month' and day_of_month in task_days_of_month and current_month % 2 == 0:
        send_to_notion(task_name, due_date=current_date)


    # For yearly tasks
    elif 'Months' in task['properties']:
        task_months = [int(option['name']) for option in task['properties']['Months']['multi_select']]
        task_due_days = [int(option['name']) for option in task['properties'].get('Days of Month', {}).get('multi_select', [])]
        if current_month in task_months and day_of_month == 1:
            for due_day in task_due_days:
                print(f"Adding yearly task '{task_name}' to the tasks database for the date: {current_year}-{current_month}-{due_day}.")
                due_date = date(current_year, current_month, due_day)
                send_to_notion(task_name, due_date=due_date)
 
