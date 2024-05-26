from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from werkzeug.utils import secure_filename
import os
#import pickle
import joblib
from joblib import load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classrooms.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}
db = SQLAlchemy(app)

#with open('classroom_model.pkl', 'rb') as f:
#   model = pickle.load(f)

#with open('classroom_model.joblib', 'rb') as f:
#    model = joblib.load(f)

with open('classroom_model.pkl', 'rb') as f:
    model = joblib.load(f)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    is_empty = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Schedule {self.classroom} - {self.date} {self.time}>'

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find', methods=['POST'])
def find():
    classroom = request.form['classroom']
    date = request.form['date']
    time = request.form['time']
    day_of_week = pd.to_datetime(date).dayofweek
    input_data = pd.get_dummies(pd.DataFrame([[classroom, day_of_week, time]], columns=['classroom', 'day_of_week', 'time']))
    prediction = model.predict(input_data)[0]
    result = "Empty" if prediction == 1 else "Occupied"
    return render_template('result.html', result=result)

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

def process_excel(filepath):
    df = pd.read_excel(filepath)
    for index, row in df.iterrows():
        schedule = Schedule(
            classroom=row['Classroom'],
            date=row['Date'],
            time=row['Time'],
            is_empty=row['Is_Empty']
        )
        db.session.add(schedule)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
