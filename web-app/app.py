import random
import os
from flask import Flask, jsonify, request, render_template
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
    return render_template('voicerecord.html', current_question=current_question)

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
    print('receive audio uploads')
    audio_file = request.files.get('audio')
    #audio_file = request.files.get('audioFile')
    print(audio_file)
    if audio_file:
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(save_path)
        # Store the file path or other relevant information in your database
    #convert_blob_file_to_wav()
    print('done')
    return jsonify({'message': 'Audio file uploaded successfully'})
def convert_blob_file_to_wav(input_file_path='uploads/blob', output_file_path='output.wav'):
    with open(input_file_path, 'rb') as blob_file:
        blob_data = blob_file.read()

    with wave.open(output_file_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(blob_data)
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    #convert_blob_file_to_wav()
    app.run(host='0.0.0.0', port=3000, debug=True)
