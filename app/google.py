import os
from google.oauth2 import service_account
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = None
    print(os.path.exists('../secrets.json'))
    if os.path.exists('../secrets.json'):
        creds = service_account.Credentials.from_service_account_file('../secrets.json', scopes=SCOPES)
    try:
        service = build('drive', 'v3', credentials=creds)
        print('succ')
    except Exception as e:
        print('credentials not found', e)

if __name__ == '__main__':
    main()