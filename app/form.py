from flask import Blueprint, render_template, request, redirect
from app.googleapi import DriveService, get_creds
import gspread
from datetime import datetime

bp = Blueprint('form', __name__, static_folder="static", template_folder='templates')
SECRETS = './secrets.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = get_creds(SECRETS, SCOPES)
drive = DriveService(creds)
print("drive creds: ", drive.creds)

gc = gspread.service_account(filename=SECRETS)
internships = gc.open('Resumes').worksheet("Internship")
fulltime = gc.open('Resumes').worksheet("Full-Time")


@bp.route("/", methods=['GET', 'POST'])
def index():
    #drive.list_files(10, True)
    if request.method == 'POST':
        form = request.form
        data = [form['f_name'], form['l_name'], form['email'], datetime.now().isoformat(), form['resume']]
        print(form['job'])
        if form['job'] == 'internship':
            internships.append_row(data)
        if form['job'] == 'full-time':
            fulltime.append_row(data)
        print(data)

        return redirect('/')
    return render_template('index.html')


@bp.route("/list", methods=['GET'])
def list():
    files = drive.list_files(10)
    return files

