import app
from flask import Blueprint, render_template, request, redirect

bp = Blueprint('form', __name__, static_folder="static", template_folder='templates')


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            "f_name": request.form['f_name'],
            "l_name": request.form['l_name'],
            "email": request.form['email'],
            "resume": request.form['resume'],
            "job": request.form['job']
        }
        print(data)
        return redirect('/')
    return render_template('index.html')
