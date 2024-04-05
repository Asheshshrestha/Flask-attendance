import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from datetime import datetime
from flaskr.subject import get_subject_list_ddl
bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/takeattendance', methods=('GET', 'POST'))
def takeattendance():
    subjects= get_subject_list_ddl()
    today_date = datetime.today().date().strftime('%Y-%m-%d')
    return render_template('attendance/selectattendance.html',subjects = subjects,today_date=today_date)