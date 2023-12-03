import random
import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from pydub import AudioSegment
import db 
import requests

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

current_question = None
attempts = 0
correct_answer = "1"

def generate_question():
    global current_question
    # Generate a random addition or subtraction problem
    num1 = random.randint(1, 9)
    num2 = random.randint(1, num1)
    operation = random.choice(['+', '-'])
    global correct_answer
    correct_answer = str(eval(f"{num1} {operation} {num2}"))

    current_question = {
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'correct_answer': correct_answer,
    }
def get_transcript():
    target_url = 'http://mlc:3000/transcript'
    response = requests.get(target_url)
    if (response):
        transcript = db.get_most_recent_transcript()
        return transcript
    return "there is an error fetching a transcript"
@app.route('/')
def index():
    generate_question()
    return render_template('LetterMath.html', current_question=current_question)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if request.method == "POST":
        f= request.files['audio_data']
        with open('uploads/audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        transcript= get_transcript() or "no transcript"
        print(transcript)
        print(correct_answer)
        transcript = str(transcript.strip())
        if transcript == correct_answer:
            isRight = "True"
        else:
            isRight = "False"
        response = make_response(jsonify({'transcript': transcript, 'isRight': isRight, 'correct_answer': correct_answer}))
        return response
    else:
        return render_template("LetterMath.html",current_question=current_question)
    
def check_file():
    audio = AudioSegment.from_file("uploads/blob")
    print("Channels:", audio.channels)
    print("Sample Width (bytes):", audio.sample_width)
    print("Sample Rate (Hz):", audio.frame_rate)

if __name__ == '__main__':
    #check_file()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    #convert_blob_file_to_wav()
    app.run(host='0.0.0.0', port=4000)
