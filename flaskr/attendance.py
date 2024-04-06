import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request,jsonify, session, url_for
)
import json
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from datetime import datetime
from flaskr.subject import get_subject_list_ddl
from flaskr.student import get_batch_list,get_course_list
bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/takeattendance', methods=('GET', 'POST'))
def takeattendance():
    subject_list= get_subject_list_ddl()
    batch_list = get_batch_list()
    course_list = get_course_list()
    today_date = datetime.today().date().strftime('%Y-%m-%d')
    return render_template('attendance/selectattendance.html',subject_list = subject_list,today_date=today_date,batch_list = batch_list,course_list=course_list)

@bp.route('/checkattendance', methods=['GET'])
def check_attendance():
    batch_id = request.args.get('batch_id', default='default_value', type=str)
    course_id = request.args.get('course_id', default='default_value', type=str)
    subject_id = request.args.get('subject_id', default='default_value', type=str)
    attendance_date = request.args.get('attendance_date', default='default_value', type=str)
    data = {}
    if check_exist(batch_id,course_id,subject_id,attendance_date):
        data = {'statuscode':2,'message': 'Attendance already exist do you want to update?'}
    else:
        data = {'statuscode':1,'message': 'No attendance found, do you want to take attendance?'}
    return jsonify(data)

def check_exist(batch_id,course_id,subject_id,attendance_date):
    flag = False
    attendance = get_db().execute(
        'SELECT id'
        ' FROM attendance '
        ' WHERE batch_id = ? AND course_id = ? AND subject_id = ? AND attendance_date = ?',
        (batch_id,course_id,subject_id,attendance_date)
    ).fetchone()

    if attendance is not None:
        flag = True
    return flag
@bp.route('/getstudents', methods=['GET'])
def getstudents():
    batch_id = request.args.get('batch_id', default='default_value', type=str)
    course_id = request.args.get('course_id', default='default_value', type=str)
    subject_id = request.args.get('subject_id', default='default_value', type=str)
    attendance_date = request.args.get('attendance_date', default='default_value', type=str)
    students = get_db().execute(
        'SELECT s.id,s.first_name,s.last_name,IFNULL(ast.status,"") status'
        ' FROM student s'
        ' JOIN batch b ON b.id = s.batch_id and b.id = ?'
        ' JOIN course c ON c.id = s.course_id and c.id = ?'
        ' JOIN course_subject cs on cs.course_id = c.id and cs.id= ?'
        ' JOIN subject sb ON sb.id = cs.subject_id '
        ' LEFT JOIN attendance a on a.batch_id = b.id AND a.course_id = c.id AND a.subject_id = sb.id and a.attendance_date = ?'
        ' LEFT JOIN attendance_student ast ON ast.attendance_id = a.id',
        (batch_id,course_id,subject_id,attendance_date)
    ).fetchall()

    student_ids = [{'id': student['id'],'first_name': student['first_name'],'last_name': student['last_name'],'status': student['status']} for student in students]
    return jsonify(student_ids)
