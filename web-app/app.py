"""
This module contains a Flask web application for a math question game with audio input handling.
"""

import os
import random
from flask import Flask, jsonify, request, render_template, make_response
import requests
from pydub import AudioSegment
import db

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CURRENT_QUESTION = None
ATTEMPTS = 0
CORRECT_ANSWER = "1"

def generate_question():
    """Generate a random addition or subtraction problem."""
    global CURRENT_QUESTION, CORRECT_ANSWER
    num1 = random.randint(1, 9)
    num2 = random.randint(1, num1)
    operation = random.choice(['+', '-'])
    CORRECT_ANSWER = str(num1 + num2 if operation == '+' else num1 - num2)

    CURRENT_QUESTION = {
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'correct_answer': CORRECT_ANSWER,
    }

def get_transcript():
    """Fetch the most recent transcript from a specified URL."""
    target_url = 'http://mlc:3000/transcript'
    response = requests.get(target_url)
    if response:
        return db.get_most_recent_transcript()
    return "Error fetching transcript"

@app.route('/')
def index():
    """Render the main page with a new question."""
    generate_question()
    return render_template('LetterMath.html', current_question=CURRENT_QUESTION)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    """Handle audio file upload and validate the answer."""
    if request.method == "POST":
        audio_file = request.files['audio_data']
        audio_file.save(os.path.join(UPLOAD_FOLDER, 'audio.wav'))
        print('File uploaded successfully')
        transcript = get_transcript() or "No transcript"
        print(transcript)
        print(CORRECT_ANSWER)
        transcript = transcript.strip()
        is_right = "True" if transcript == CORRECT_ANSWER else "False"
        response = make_response(jsonify({'transcript': transcript, 'isRight': is_right, 'correct_answer': CORRECT_ANSWER}))
        return response
    return render_template("LetterMath.html", current_question=CURRENT_QUESTION)

def check_file():
    """Check the properties of the uploaded audio file."""
    audio = AudioSegment.from_file(os.path.join(UPLOAD_FOLDER, 'blob'))
    print("Channels:", audio.channels)
    print("Sample Width (bytes):", audio.sample_width)
    print("Sample Rate (Hz):", audio.frame_rate)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=4000)
