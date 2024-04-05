import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)

app = Flask(__name__)
bp = Blueprint('teacher', __name__, url_prefix='/teacher')
from flaskr.db import get_db
from werkzeug.exceptions import abort


@bp.route('/list', methods=['GET'])
def index():
    db = get_db()
    teachers  = db.execute(
        'SELECT * FROM teacher'
    ).fetchall()
    return render_template('teacher/list.html', teachers=teachers)

@bp.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        first_name = request.form['txtFirstName']
        last_name = request.form['txtLastName']
        email = request.form['txtEmail']
        error = None

        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        if not email:
            error = 'Email is required.'

        if error is not None:
            flash(error,"danger")
        else:
            db = get_db()
            db.execute(
                'Insert into teacher(first_name,last_name,email)'
                ' VALUES (?, ?, ?)',
                (first_name, last_name, email)
            )
            db.commit()
            flash("Successfully added new teacher","success")
            return redirect(url_for('teacher.index'))
    return render_template('teacher/add.html')

def get_teacher(id):
    post = get_db().execute(
        'SELECT first_name, last_name, email'
        ' FROM teacher '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    teacher = get_teacher(id)

    if request.method == 'POST':
        first_name = request.form['txtFirstName']
        last_name = request.form['txtLastName']
        email = request.form['txtEmail']
        error = None

        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        if not email:
            error = 'Email is required.'

        if error is not None:
            flash(error,'danger')
        else:
            db = get_db()
            db.execute(
                'UPDATE teacher SET first_name = ?, last_name = ?, email = ?'
                ' WHERE id = ?',
                (first_name, last_name,email, id)
            )
            db.commit()
            flash("Successfully updated teacher","success")
            return redirect(url_for('teacher.index'))

    return render_template('teacher/update.html', teacher=teacher)
@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_teacher(id)
    db = get_db()
    db.execute('DELETE FROM teacher WHERE id = ?', (id,))
    db.commit()
    flash("Successfully deleted teacher","success")
    return redirect(url_for('teacher.index'))