from googleapiclient.errors import HttpError
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_creds(secrets, scopes):
    print('secrets: ', secrets)
    if os.path.exists(secrets):
        print('secrets.json found')
        return service_account.Credentials.from_service_account_file(secrets, scopes=scopes)
    return None


class GoogleService:

    def __init__(self, creds, api_name, api_version):
        self.creds = creds
        self.api_name = api_name
        self.api_version = api_version

    def get_service(self):
        try:
            return build(self.api_name, self.api_version, credentials=self.creds)
        except Exception as e:
            print('error, make sure you have secrets.json in the project root: ', e)


class DriveService(GoogleService):

    API_NAME = 'drive'
    API_VERSION = 'v3'

    def __init__(self, creds):
        self.creds = creds
        super().__init__(self.creds, self.API_NAME, self.API_VERSION)

    def list_files(self, page_size: int, log=False):
        print('creds: ', self.creds)
        results = super().get_service().files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if log:
            if not items:
                print('No files found. You probably need to give the service account access to your drive')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        return items

    def create_file(self, name: str, mimeType: str):
        file_metadata = {
            'name': name,
            'mimeType': F'application/vnd.google-apps.{mimeType}',
            'parents': ['1hwLdGhQ8gt36TrLMMbkZ0kUXX_3Qkfd5']
        }
        file = super().get_service().files().create(body=file_metadata, fields='id').execute()
        print(F'File has created with ID: "{file.get("id")}".')
        return file

    def delete_file(self, file_id):
        file = super().get_service().files().delete(fileId=file_id).execute()

    def get_file(self, file_id):
        file = super().get_service().files().get(fileId=file_id).execute()
        print(file)

    """
    def delete_all(self):
        # will error on files not created by service
        items = list_files(1000)
        for item in items:
            try:
                delete_file(item['id'])
            except HttpError as e:
                print('error, you\'re probably trying to delete a file created by somebody else: ', e)
    """


def main():
    secrets = '../../secrets.json'
    drive = DriveService(secrets)
    drive.list_files(10, True)


if __name__ == '__main__':
    main()
