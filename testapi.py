import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Kelhou"
REPO_NAME = "privdata"
FILE_PATH = "1stsem.xlsx"
BRANCH = "main"

def fetch_github_file():
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        file_info = response.json()

        print("File metadata:", file_info)
        
        file_content = base64.b64decode(file_info['content'])
        with open(FILE_PATH, 'wb') as file:
            file.write(file_content)

        print(f"File '{FILE_PATH}' successfully fetched and saved locally.")
    except Exception as e:
        print(f"Error fetching file: {e}")

if __name__ == "__main__":
    fetch_github_file()
