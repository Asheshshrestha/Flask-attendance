import functools
import os
from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for,Response,jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import admin_login_required
app = Flask(__name__)
bp = Blueprint('automatic_attendance', __name__, url_prefix='/automatic_attendance')
from flaskr.db import get_db
from werkzeug.exceptions import abort

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#=====================================================================================
import cv2
import csv
import pandas as pd
import face_recognition
import numpy as np
import requests
from datetime import datetime
import glob
#=====================================================================================
BATCH_ID = 0
COURSE_ID = 0
SUBJECT_ID = 0
ATTENDANCE_LOG = os.path.join(PROJECT_ROOT, 'ml\\attendance_log\\')
ATTENDANCE_SNAPSHOT = os.path.join(PROJECT_ROOT, 'ml\\snapshots\\')
ATTENDANCE_LOG_PATH = ''
FIELD_NAMES = ['id','status','confidence']
#=====================================================================================
camera = None
saved_df = pd.read_csv(
    os.path.join(PROJECT_ROOT, 'ml\encoding\encodings.csv'))
en = saved_df["Encodings"]
n = saved_df["Persons"]

e = []
for i in en:
    e.append(np.fromstring(i[1:-1], dtype=float, sep=' '))

def detect_known_faces(img, image_encodings=e, persons=n):
    height, width = img.shape[:2]
    resized_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    fc = []
    fn = []
    confidences = []
    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(
        rgb_img, face_locations, model="small")
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(
            image_encodings, face_encoding)
        face_distances = face_recognition.face_distance(image_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        confidence = 1 - face_distances[best_match_index]
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = persons[first_match_index]
            y1, x2, y2, x1 = [coord * 4 for coord in face_location]
            # Crop and save face image
            face_img = img[y1:y2, x1:x2]
            face_file_path = os.path.join(ATTENDANCE_SNAPSHOT, f'temp_{name}_{round(confidence, 2)}.jpg')
            print(face_file_path)
            cv2.imwrite(face_file_path, face_img)
        fc.append(face_location)
        fn.append(name)
        confidences.append(round(confidence, 2))
    return fc, fn, confidences
#=====================================================================================
def generate_frames():
    camera = cv2.VideoCapture(0)  # Use 0 for webcam, or a video file path
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame,1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        face_locations, face_names, match_confidences = detect_known_faces(frame)
        if face_names:
            for face_loc, name, confidence in zip(face_locations, face_names, match_confidences):
                y1, x2, y2, x1 = face_loc
                cv2.putText(frame, str(name)+' '+ str(confidence)+'%', (x1*4, y1*4 - 40),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1*4, y1*4), (x2*4, y2*4), (0, 0, 200), 4)
                if name != 'Unknown':
                    present_student= {'id':name,'status':'present','confidence':confidence}
                    with open(ATTENDANCE_LOG_PATH, 'a') as csv_file:
                        dict_object = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
                        dict_object.writerow(present_student)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@bp.route('/video_feed')
def video_feed():
    global ATTENDANCE_LOG_PATH
    attendance_log_file_name = str(BATCH_ID)+'_'+str(COURSE_ID)+'_'+str(SUBJECT_ID)+'.csv'
    ATTENDANCE_LOG_PATH = os.path.join(ATTENDANCE_LOG, attendance_log_file_name)
    with open(ATTENDANCE_LOG_PATH, mode='w', newline='') as file:
        pass  
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/<int:bid>/<int:cid>/<int:sid>/take_attendance', methods=['GET'])
def index(bid,cid,sid):
    global BATCH_ID,COURSE_ID,SUBJECT_ID
    BATCH_ID = bid
    COURSE_ID = cid
    SUBJECT_ID = sid
    return render_template('automatic_attendance/preview.html')


@bp.route('/stop_taking_attendance',methods=['GET'])
def stop_taking_attendance():
    global camera
    batch_id = BATCH_ID
    course_id = COURSE_ID
    subject_id = SUBJECT_ID
    attendance_date = datetime.today().date().strftime('%Y-%m-%d')
    student_list = get_student_list(batch_id,course_id,subject_id)
    if camera is not None:
        camera.release()
        camera = None
    return jsonify(student_list)

def get_student_list(batch_id,course_id,subject_id):
    students = get_db().execute(
                '''SELECT DISTINCT s.id, s.first_name, s.last_name
                    FROM student s
                    JOIN batch b ON b.id = s.batch_id 
                    JOIN course c ON c.id = s.course_id 
                    JOIN course_subject cs ON cs.course_id = c.id 
                    JOIN subject sb ON sb.id = cs.subject_id 
                    JOIN teacher t ON t.id = sb.teacher_id
                    WHERE s.batch_id = ?  AND cs.course_id = ? AND cs.subject_id = ? AND t.user_id = ? ORDER BY s.id''',
                (batch_id,course_id,subject_id,g.user['id'])
            ).fetchall()
    student_list = [{'id': student['id'],'first_name': student['first_name'],'last_name': student['last_name']} for student in students]
    columns = ['id', 'first_name', 'last_name']
    students_df = pd.DataFrame(student_list, columns=columns)
    students_df.set_index('id', inplace=True)
    print(ATTENDANCE_LOG_PATH,'attendane')
    field_names = ['id', 'status', 'confidence']
    pre_df = pd.read_csv(ATTENDANCE_LOG_PATH, names=field_names)
    df = pre_df.loc[pre_df.groupby('id')['confidence'].idxmax()]
    merged_df = pd.merge(students_df, df, on='id', how='left')
    merged_df['confidence'] = merged_df['confidence'].fillna(0)
    merged_df['status'] = merged_df['status'].fillna('absent')
    result = merged_df.to_dict(orient='records')
    return result