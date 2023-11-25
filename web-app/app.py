from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Generate a random addition or subtraction problem
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    operation = random.choice(['+', '-'])
    correct_answer = str(eval(f"{num1} {operation} {num2}"))

    # Generate three random wrong answers
    wrong_answers = [str(random.randint(1, 18)) for _ in range(3)]

    # Combine correct and wrong answers and shuffle them
    answers = [correct_answer] + wrong_answers
    random.shuffle(answers)

    # Convert answers to dictionary format for easier JSON serialization
    choices = {chr(65 + i): answers[i] for i in range(4)}

    return render_template('index.html', num1=num1, num2=num2, operation=operation, choices=choices)

if __name__ == '__main__':
    app.run(debug=True)
