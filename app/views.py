import app
from flask import Blueprint, render_template

bp = Blueprint('views', __name__, static_folder="static", template_folder='templates')

@bp.route("/")
def index():
    return render_template('index.html')
