from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = 'AIzaSyC0r7lmGqzdfbzz6mcThfF0qrYE_yCrzkM'
GEMINI_API_URL = 'https://api.gemini.com/v1/your_endpoint'  # Use the actual Gemini API endpoint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = get_answer_from_gemini(question)
    return jsonify({'answer': answer})

def get_answer_from_gemini(question):
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'question': question,
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('answer')
    else:
        return 'Error retrieving answer from Gemini API'

if __name__ == '__main__':
    app.run(debug=True)
