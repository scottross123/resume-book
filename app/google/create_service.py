import os
from google.oauth2 import service_account
from googleapiclient.discovery import build


def create_service(SECRETS_FILE, API_NAME, API_VERSION, SCOPES):

    creds = None
    if os.path.exists(SECRETS_FILE):
        print('secrets.json found')
        creds = service_account.Credentials.from_service_account_file(SECRETS_FILE, scopes=SCOPES)
    try:
        return build(API_NAME, API_VERSION , credentials=creds)
    except Exception as e:
        print('error, make sure you have secrets.json in the project root: ', e)