import io
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from datetime import datetime

bp = Blueprint('form', __name__, static_folder="static", template_folder='templates')
SECRETS = './secrets.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

gc = gspread.service_account(filename=SECRETS)
internships = gc.open('Resumes').worksheet("Internship")
fulltime = gc.open('Resumes').worksheet("Full-Time")

gauth = GoogleAuth()
gauth.auth_method = 'service'
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS, SCOPES)
drive = GoogleDrive(gauth)

ALLOWED_EXTENSIONS = {'pdf'}

PARENT_FOLDER_ID = '1hwLdGhQ8gt36TrLMMbkZ0kUXX_3Qkfd5'
INTERNSHIP_FOLDER_ID = '1cKXq0Tya5iP2UHG2WbUN8eivq0g8IwCn'
FULLTIME_FOLDER_ID = '1D4HTAiu1Csxn952q-U8_-VCp6o5K_u-F'


def allowed_file(filename: str):
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
    # flash(f'Email {entry["email"]} was found on record, replaced with new info')
    return worksheet.update_cells(updated_cells)


def create_file(file, parent_id: str, mime_type: str):
    try:
        new_file = drive.CreateFile({
            'title': secure_filename(file.filename),
            'mimeType': mime_type,
            'parents': [{'id': parent_id}]
        })
        file.seek(0)
        buffer = io.BytesIO(file.read())
        new_file.content = buffer
        return new_file.Upload()
    except Exception as e:
        return print(e)


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
        if request.form['job'] == 'internship':
            add_entry(entry, internships)
            create_file(resume, INTERNSHIP_FOLDER_ID, 'application/pdf')
        if request.form['job'] == 'full-time':
            add_entry(entry, fulltime)
            create_file(resume, FULLTIME_FOLDER_ID, 'application/pdf')
        print(entry)
        return redirect('/')
    return render_template('index.html')
