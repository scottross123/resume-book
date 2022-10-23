from create_service import create_service

SECRETS_FILE = '../../secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(SECRETS_FILE, API_NAME, API_VERSION, SCOPES)

def list_files():
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found. You probably need to give the service account access to your drive')
        return
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

def create_folder(name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['1hwLdGhQ8gt36TrLMMbkZ0kUXX_3Qkfd5']
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print(F'Folder has created with ID: "{file.get("id")}".')
    return file.get('id')


def delete_folder(fileId):
    #fileId = '1xFMGIFNtzgrB_g-HavWQFJcWudXHd-rc'
    file = service.files().delete(fileId=fileId).execute()

def create_spreadsheet(name, parent_id):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [parent_id]
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print(F'Folder has created with ID: "{file.get("id")}".')
    return file

def main():
    list_files()
    folder = create_folder('internship')
    list_files()
    create_spreadsheet('bruh', folder)
    list_files()

if __name__ == '__main__':
    main()