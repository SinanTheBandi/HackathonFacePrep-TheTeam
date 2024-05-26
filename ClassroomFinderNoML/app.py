import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classroom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define database model for Schedule
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom = db.Column(db.String(50), nullable=False)
    day_of_week = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    is_empty = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Schedule {self.classroom} - {self.day_of_week} {self.time}>'

# Create database tables
with app.app_context():
    db.create_all()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Find classroom route
@app.route('/find', methods=['POST'])
def find():
    classroom = request.form['classroom']
    day_of_week = request.form['day_of_week']
    time = request.form['time']
    schedule = Schedule.query.filter_by(classroom=classroom, day_of_week=day_of_week, time=time).first()
    if schedule:
        result = "Empty" if schedule.is_empty else "Occupied"
    else:
        result = "No schedule found for the specified time."
    return render_template('result.html', result=result)

# Upload file route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            process_excel(filepath)
            return redirect(url_for('home'))
    return render_template('upload.html')

# Function to process uploaded Excel file
def process_excel(filepath):
    df = pd.read_excel(filepath)
    for index, row in df.iterrows():
        schedule = Schedule(
            classroom=row['Classroom'],
            day_of_week=row['Day_of_Week'],
            time=row['Time'],
            is_empty=row['Is_Empty']
        )
        db.session.add(schedule)
    db.session.commit()

# Add new schedule route
@app.route('/add', methods=['GET', 'POST'])
def add_schedule():
    if request.method == 'POST':
        classroom = request.form['classroom']
        day_of_week = request.form['day_of_week']
        time = request.form['time']
        is_empty = request.form['is_empty'].lower() == 'true'
        new_schedule = Schedule(classroom=classroom, day_of_week=day_of_week, time=time, is_empty=is_empty)
        db.session.add(new_schedule)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

# Start Flask application
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

