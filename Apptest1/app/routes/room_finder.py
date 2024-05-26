from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.models import db, Classroom, Timetable
from datetime import datetime

room_finder_bp = Blueprint('room_finder', __name__)

@room_finder_bp.route('/')
def room_finder():
    return render_template('index.html')

@room_finder_bp.route('/find', methods=['POST'])
def find():
    classroom = request.form.get('classroom')
    day_of_week = request.form.get('day_of_week')
    time = request.form.get('time')

    # Logic to find if classroom is empty
    result = f"Classroom {classroom} is empty on {day_of_week} at {time}"

    return render_template('result.html', result=result)

@room_finder_bp.route('/upload')
def upload():
    return render_template('upload.html')

@room_finder_bp.route('/upload', methods=['POST'])
def upload_post():
    file = request.files['file']
    # Logic to handle file upload
    return redirect(url_for('room_finder.room_finder'))

@room_finder_bp.route('/add')
def add():
    return render_template('add.html')

@room_finder_bp.route('/add', methods=['POST'])
def add_post():
    classroom = request.form.get('classroom')
    day_of_week = request.form.get('day_of_week')
    time = request.form.get('time')
    is_empty = request.form.get('is_empty')
    
    # Logic to add new schedule
    return redirect(url_for('room_finder.room_finder'))
