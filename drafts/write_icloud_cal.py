import os
import requests
from calendar_integrate import get_icloud_events
import time

notion_api_key = os.environ['NOTION_SECRET_KEY']
database_id = os.environ['NOTION_CALENDAR_DATABASE']
max_retries = 5
delay_seconds = 5

headers = {
    'Authorization': f'Bearer {notion_api_key}',
    'Notion-Version': '2021-08-16',
    'Content-Type': 'application/json',
}

events = get_icloud_events()

for event in events:
    event_data = event.instance.vevent

    # Generate a unique identifier for the event
    event_id = f'{event_data.summary.value}-{event_data.dtstart.value}'

    for attempt in range(max_retries):
        try:
            # Check if a page with this event ID already exists
            response = requests.post(
                'https://api.notion.com/v1/databases/cf1d0614701c463892649d12807f1adc/query',
                headers=headers,
                json={}
            )
            response.raise_for_status()  # Raise an exception if the response indicates an error
            pages = response.json()['results']

            # Check if a page with this event ID already exists
            existing_page = next((page for page in pages if 'text' in page['properties']['EventID'] and page['properties']['EventID']['text'][0]['plain_text'] == event_id), None)
            
            if existing_page:
                print(f'Page for event "{event_data.summary.value}" already exists, skipping...')
                break

            # Prepare the request data
            data = {
                'parent': {'database_id': database_id},
                'properties': {
                    'Name': {
                        'title': [
                            {
                                'text': {
                                    'content': str(event_data.summary.value)
                                }
                            }
                        ]
                    },
                    'Date': {
                        'date': {
                            'start': str(event_data.dtstart.value),
                            'end': str(event_data.dtend.value)
                        }
                    },
                    'EventID': {  # Adjust to match your Notion database
                        'text': [
                            {
                                'content': event_id
                            }
                        ]
                    }
                }
            }

            # Send the request to the Notion API
            response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)

            # Check the response
            if response.status_code != 200:
                print(f'Error creating page for event "{event_data.summary.value}": {response.content}')
            else:
                print(f'Successfully created page for event "{event_data.summary.value}"')
                break  # Break the loop if the request was successful

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:  # If this isn't the last attempt
                print(f'Error on attempt {attempt + 1} of {max_retries}. Retrying in {delay_seconds} seconds...')
                time.sleep(delay_seconds)  # Wait for the specified delay
            else:  # If this is the last attempt, re-raise the exception
                raise e

