

def main():
    secrets = '../../secrets.json'
    drive = DriveService(secrets)
    drive.list_files(10, True)


if __name__ == '__main__':
    main()
