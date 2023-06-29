import os
import requests

token = os.environ['NOTION_SECRET_KEY']

# Your task database ID
database_id = os.environ['NOTION_ZLTASKS_DATABASE']

# Notion API base URL
base_url = 'https://api.notion.com/v1'

# Headers for the API requests
headers = {
    'Authorization': f'Bearer {token}',
    'Notion-Version': '2021-08-16'
}

# Get all tasks from the database
def get_tasks():
    # Body for the database query
    body = {
        'filter': {
            'property': 'v[_E',  # Replace with the ID of your checkbox property
            'checkbox': {
                'equals': True
            }
        }
    }

    response = requests.post(f'{base_url}/databases/{database_id}/query', headers=headers, json=body)
    return response.json()

# Delete a task (block) by ID
def delete_task(block_id):
    requests.delete(f'{base_url}/blocks/{block_id}', headers=headers)

# Main script
def main():
    # Get all tasks
    tasks = get_tasks()
    
    # Print tasks
    print(tasks)

    # Iterate over tasks
    for task in tasks['results']:
        # Delete the task
        delete_task(task['id'])

# Run the script
if __name__ == "__main__":
    main()





