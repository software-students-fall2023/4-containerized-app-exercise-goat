'''import modules'''
import random
import os
import db
import requests
from flask import Flask, jsonify, request, render_template,  make_response


app=Flask(__name__, template_folder='templates')
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
@app.route('/cheat', methods=['GET'])
def show_answer():
    '''it will secretly tell you the answer'''
    message ='wow you have found me. I will give a hint'
    possible_answers = ['0','1','2','3','4','5','6','7','8','9']
    if (correct_answer!=''):
        if (correct_answer in possible_answers):
            hint = 'the answer is less than 10!'
        else:
            hint = 'the answer is more than 10!'
        response = make_response(jsonify({'message': message, 'hint':hint}))
    return response 
@app.route('/instruction', methods=['GET'])
def show_instruction():
    '''shows instructions'''
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>instructions</title>
    </head>
    <body>
        <h1>Hello!</h1>
        <br>
        <p>Thanks for using VoiceMath.</p>
        <p>This app is presented by the goat group.</p>
        <p>Voice Math is a web app which would 
        generate easy math questions 
        and gather your answer through microphone! 
        Upon starting, a math question 
        would show up on the screen. 
        You can click the 'start' button 
        to start recording your voice, 
        and click 'finish' to stop. 
        Once you click finish, the audio 
        will be uploaded to the server and check its correctness. 
        A message will be display to indicate your (transcribed) 
        answer and whether you get it right. You can also click 
        'next question' to get another question. 
        This app uses google cloud speech-to-text api. 
        This app is especially designed for kids who is not good at 
        addition or subtraction under ten but fluent with docker and git. </p>
        <p> if you run into an issue or need furthur help, feel 
        free to contact our team</p>
        <p>- [@AlvisYan2025](https://github.com/AlvisYan2025)
            - [@Jason-SL-Zhang](https://github.com/Jason-SL-Zhang)
            - [@SpencerWPak](https://github.com/SpencerWPak)
            - [@HenryGreene10](https://github.com/HenryGreene10)</p>
    </body>
    </html>
    """
    return html_content
@app.route('/test', methods=['GET'])
def test_connection():
    '''test connection'''
    response=make_response(jsonify({'message': 'hi'}))
    return response

def create_app():
    return app

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=4000)

