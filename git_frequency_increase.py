import requests
from datetime import datetime
from base64 import b64encode, b64decode

# User credentials and repository details
GITHUB_USERNAME = "USER_NAME"
GITHUB_TOKEN = "GITHUB_TOKEN"  # Use a personal access token instead of a password
REPO_NAME = "REPO_NAME"
FILE_PATH = "FILE_NAME"

# Base API URL
BASE_URL = "https://api.github.com"

def update_file():
    # Get the current file's SHA and content
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
        # Decode the content from base64
        current_content = b64decode(file_data["content"]).decode()

        # Append the current date and time to the content
        new_content = current_content + f"\n# Update on {datetime.now()}\n"
        encoded_content = b64encode(new_content.encode()).decode()

        # Update the file with the new content
        payload = {
            "message": "Daily update",
            "content": encoded_content,
            "sha": sha,
        }
        response = requests.put(url, json=payload, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

        if response.status_code == 200:
            print("File updated successfully.")
        else:
            print(f"Error updating file: {response.json()}")
    else:
        print(f"Error fetching file: {response.json()}")

# Run the function
if __name__ == "__main__":
    update_file()
