from flask import Blueprint, render_template, request, redirect
from app.googleapi import DriveService, get_creds

bp = Blueprint('form', __name__, static_folder="static", template_folder='templates')
SECRETS = './secrets.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = get_creds(SECRETS, SCOPES)
drive = DriveService(creds)
print("drive creds: ", drive.creds)


@bp.route("/", methods=['GET', 'POST'])
def index():
    drive.list_files(10, True)
    if request.method == 'POST':
        data = {
            "f_name": request.form['f_name'],
            "l_name": request.form['l_name'],
            "email": request.form['email'],
            "resume": request.form['resume'],
            "job": request.form['job']
        }
        print(data)

        for key in data:
            drive.create_file(data[key], 'spreadsheet')
        return redirect('/')
    return render_template('index.html')


@bp.route("/list", methods=['GET'])
def list():
    files = drive.list_files(10)
    return files

