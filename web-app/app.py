import random
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='templates')

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
    is_correct = user_answer == 'A'  # For simplicity, assuming 'A' is always correct
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
