import random
import os
import db
import requests
from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from pydub import AudioSegment

# Create a Flask web application instance
app = Flask(__name__, template_folder='templates')

# Set up the upload folder for audio files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize global variables
current_question = None
correct_answer = ""

# Function to generate a random addition or subtraction problem and set it as the current question
def generate_question():
    global current_question
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

# Function to get the most recent transcript from an external service
def get_transcript():
    target_url = 'http://mlc:3000/transcript'
    response = requests.get(target_url)
    if response:
        transcript = db.get_most_recent_transcript()  # Assuming this function retrieves the transcript from the database
        return transcript
    return "There is an error fetching a transcript"

# Define a route for the home page
@app.route('/')
def index():
    generate_question()
    return render_template('VoiceMath.html', current_question=current_question)

# Define a route for handling audio file uploads
@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if request.method == "POST":
        # Save the uploaded audio file and print a success message
        f = request.files['audio_data']
        with open('uploads/audio.wav', 'wb') as audio:
            f.save(audio)
        print('File uploaded successfully')

        # Get the transcript and compare it with the correct answer
        transcript = get_transcript() or "no transcript"
        print(transcript)
        print(correct_answer)
        transcript = str(transcript.strip())
        if transcript == correct_answer:
            isRight = "Correct!"
        else:
            isRight = "Wrong!"

        # Create a JSON response with the transcript, correctness, and correct answer
        response = make_response(jsonify({'transcript': transcript, 'isRight': isRight, 'correct_answer': correct_answer}))
        return response
    else:
        return render_template("VoiceMath.html", current_question=current_question)

# Function to check the properties of an audio file
def check_file():
    audio = AudioSegment.from_file("uploads/blob")
    print("Channels:", audio.channels)
    print("Sample Width (bytes):", audio.sample_width)
    print("Sample Rate (Hz):", audio.frame_rate)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=4000)
