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
tasks = {
    'Monday': ['Laundry', 'Entry Way and Laundry Room Cleaned', 'Github Commit', 'Sololearn Daily Learn Daily Lesson'],
    'Tuesday': [],
    'Wednesday': ['Clean Bathrooms', 'Laundry'],
    'Thursday': ['Order Groceries'],
    'Friday': ['Basement Straightened and Vacuumed', 'Floors Vacuumed and Mopped', 'Laundry'],
    'Saturday': [],
    'Sunday': ['Put out trash'],
}

#Get the current day of the week
day_of_week = datetime.datetime.now().strftime('%A')

# Loop over the tasks for the current day of the week
for task_name in tasks[day_of_week]:

    # The body of the API request. This includes the ID of the database you're adding the page to and the properties of the page
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
            'Analog': {
                'select': {
                    'name': 'Today'
                }
            },
            # Add more properties here
        }
    }

    # Send the API request
    response = requests.post(url, headers=headers, data=json.dumps(body))

    # Print the response
    print(response.json())






