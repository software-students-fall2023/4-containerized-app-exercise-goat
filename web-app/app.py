'''import modules'''
import random
import os
import db
import requests
from flask import Flask, jsonify, request, render_template,  make_response


def create_app():
    '''Create a Flask web application instance'''
    return Flask(__name__, template_folder='templates')
app= create_app()
# Set up the upload folder for audio files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
current_question = None # pylint: disable=invalid-name
correct_answer = "" # pylint: disable=invalid-name

def generate_question():
    '''Function to generate a random addition 
    or subtraction problem and set it as the current question'''
    global current_question # pylint: disable=global-statement
    num1 = random.randint(1, 9)
    num2 = random.randint(1, num1)
    operation = random.choice(['+', '-'])
    global correct_answer # pylint: disable=global-statement
    correct_answer = str(eval(f"{num1} {operation} {num2}"))# pylint: disable=eval-used
    current_question = {
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'correct_answer': correct_answer,
    }

def get_transcript():
    '''Function to get the most recent transcript from an external service'''
    target_url = 'http://mlc:3000/transcript'
    response = requests.get(target_url)# pylint: disable=missing-timeout
    if response:
        transcript = db.get_most_recent_transcript()
        return transcript
    return "There is an error fetching a transcript"

@app.route('/')
def index():
    '''Define a route for the home page'''
    generate_question()
    return render_template('VoiceMath.html', current_question=current_question)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    '''route for handling audio file uploads'''
    # Save the uploaded audio file and print a success message
    f = request.files['audio_data']
    with open('uploads/audio.wav', 'wb') as audio:
        f.save(audio)
    print('File uploaded successfully')

    # Get the transcript and compare it with the correct answer
    transcript = get_transcript() or "Please say again"
    transcript = str(transcript.strip())
    if transcript == correct_answer:
        isRight = "Correct!" # pylint: disable=invalid-name
    else:
        isRight = "Wrong!" # pylint: disable=invalid-name
    # Create a JSON response with the transcript,
    # correctness, and correct answer
    # pylint: disable=line-too-long
    response = make_response(jsonify({'transcript': transcript, 'isRight': isRight, 'correct_answer': correct_answer}))
    return response
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=4000)
