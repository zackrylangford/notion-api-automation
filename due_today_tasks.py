import os
import requests
import json
import datetime

# Get your Notion API token from environment variables
NOTION_TOKEN = os.environ['NOTION_SECRET_KEY']

# Replace this with your database ID
DATABASE_ID = os.environ['NOTION_ZLTASKS_DATABASE']

# The URL of the Notion API endpoint
list_url = 'https://api.notion.com/v1/databases/' + DATABASE_ID + '/query'
update_url = 'https://api.notion.com/v1/pages/'

# The headers for the API request. This includes your Notion API token and the version of the Notion API you're using
headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json'
}

# Get current date
current_date = datetime.date.today().strftime('%Y-%m-%d')

# List pages in the database
response = requests.post(list_url, headers=headers)

if response.status_code == 200:
    results = response.json().get('results')
    for page in results:
        properties = page.get('properties')

        # Make sure the 'Due Date' property exists
        due_date_property = properties.get('Due Date')
        if due_date_property is not None:
            # Compare 'Due Date' with current date
            due_date = due_date_property.get('date', {}).get('start')

            if due_date == current_date:
                # If 'Due Date' is today, update 'Analog' to 'Today'
                page_id = page.get('id')

                body = {
                    'properties': {
                        'Analog': {
                            'select': {
                                'name': 'Today'
                            }
                        }
                    }
                }

                response = requests.patch(update_url + page_id, headers=headers, data=json.dumps(body))

                if response.status_code == 200:
                    print(f"Successfully updated task: {page_id}")
                else:
                    print(f"Error updating task: {response.text}")

