import random
import os
from flask import Flask, jsonify, request, render_template
from pydub import AudioSegment
import wave 

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

current_question = None
attempts = 0

def generate_question():
    global current_question
    # Generate a random addition or subtraction problem
    num1 = random.randint(1, 9)
    num2 = random.randint(1, num1)
    operation = random.choice(['+', '-'])
    correct_answer = str(eval(f"{num1} {operation} {num2}"))

    # Generate three random wrong answers
    wrong_answers = [str(random.randint(1, 18)) for _ in range(3)]

    # Combine correct and wrong answers and shuffle them
    answers = [correct_answer] + wrong_answers
    random.shuffle(answers)

    # Convert answers to dictionary format for easier JSON serialization
    choices = {chr(65 + i): answers[i] for i in range(4)}

    current_question = {
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'correct_answer': correct_answer,
        'choices': choices
    }

@app.route('/')
def index():
    generate_question()
    return render_template('LetterMath.html', current_question=current_question)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global attempts
    user_answer = request.form.get('answer')
    correct_answer = current_question['correct_answer']

    is_correct = user_answer == correct_answer

    attempts += 1

    if is_correct:
        attempts = 0  # Reset attempts on correct answer
        generate_question()  # Move to the next question
        return jsonify({'is_correct': True, 'next_question': current_question})
    elif attempts >= 3:
        attempts = 0
        generate_question()  # Move to the next question
        return jsonify({'is_correct': False, 'next_question': current_question, 'max_attempts_reached': True})
    else:
        return jsonify({'is_correct': False, 'max_attempts_reached': False})

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if request.method == "POST":
        f= request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('LetterMath.html')
    else:
        return render_template("LetterMath.html")
    '''if audio_file:
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
        audio_file.save(save_path)

        return jsonify({'message': 'Audio file uploaded successfully', 'transcription': 'transcription_result'})'''
def check_file():
    audio = AudioSegment.from_file("uploads/blob")
    print("Channels:", audio.channels)
    print("Sample Width (bytes):", audio.sample_width)
    print("Sample Rate (Hz):", audio.frame_rate)

if __name__ == '__main__':
    check_file()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    #convert_blob_file_to_wav()
    app.run(host='0.0.0.0', port=3000, debug=True)

