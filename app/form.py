from flask import Blueprint, render_template, request, redirect, flash, current_app
import os
from werkzeug.utils import secure_filename
from app.googleapi import DriveService, get_creds
import gspread
from gspread import Cell
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

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename: str):
    print('filename? ', filename)
    print('period? ', '.' in filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_entry(entry: dict, worksheet):
    email_cell = worksheet.find(entry['email'])
    entry_values = [entry[key] for key in entry]
    print("entry values: ", entry_values)
    if email_cell is None:
        return worksheet.append_row(entry_values)
    updated_cells = []
    for i in range(0, len(entry_values)):
        # Cell(row, col, value), creates new cell objects with updated values
        updated_cells.append(Cell(email_cell.row, i+1, entry_values[i]))
    print("updated cells: ", updated_cells)
    flash(f'Email {entry["email"]} was found on record, replaced with new info')
    return worksheet.update_cells(updated_cells)


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entry = {
            "f_name": request.form['f_name'],
            "l_name": request.form['l_name'],
            "email": request.form['email'],
            "last_modified": datetime.now().ctime(),
            "resume": request.files['resume'].filename
        }
        resume = request.files['resume']
        print('resume exists', resume)
        print('allowed', allowed_file(resume.filename))
        if resume and allowed_file(resume.filename):

            filename = secure_filename(resume.filename)
            resume.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        if request.form['job'] == 'internship':
           add_entry(entry, internships)
        if request.form['job'] == 'full-time':
           add_entry(entry, fulltime)
        print(entry)

        return redirect('/')
    return render_template('index.html')


@bp.route("/list", methods=['GET'])
def list():
    files = drive.list_files(10)
    return files

