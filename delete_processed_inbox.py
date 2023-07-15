import os
import requests

token = os.environ['NOTION_SECRET_KEY']

# Your task database ID
database_id = os.environ['NOTION_INBOX_DATABASE']

# Notion API base URL
base_url = 'https://api.notion.com/v1'

# Headers for the API requests
headers = {
    'Authorization': f'Bearer {token}',
    'Notion-Version': '2021-08-16'
}

def get_tasks():
    # Body for the database query
    body = {
        'filter': {
            'property': 'Processed',  # Replace with the ID of your checkbox property
            'checkbox': {
                'equals': True
            }
        }
    }

    response = requests.post(f'{base_url}/databases/{database_id}/query', headers=headers, json=body)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error with status code {response.status_code}: {response.text}")
        return None

# Delete a task (block) by ID
def delete_task(block_id):
    requests.delete(f'{base_url}/blocks/{block_id}', headers=headers)

def main():
    # Get all tasks
    tasks = get_tasks()
    
    # Print tasks
    print(tasks)

    # If tasks is None, an error occurred
    if tasks is None:
        print("Failed to fetch tasks")
        return

    # Iterate over tasks
    for task in tasks['results']:
        # Delete the task
        delete_task(task['id'])

# Run the script
if __name__ == "__main__":
    main()






