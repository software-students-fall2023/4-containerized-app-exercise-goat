from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Generate a random addition or subtraction problem
    operator = random.choice(['+', '-'])
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    problem = f"{num1} {operator} {num2} = ?"

    # Generate 3 incorrect options and 1 correct option
    options = [chr(ord('A') + i) for i in range(4)]
    correct_option = random.choice(options)
    options.remove(correct_option)
    random.shuffle(options)
    answers = {
        'A': num1 + num2 if correct_option == 'A' else random.randint(1, 18),
        'B': num1 + num2 if correct_option == 'B' else random.randint(1, 18),
        'C': num1 + num2 if correct_option == 'C' else random.randint(1, 18),
        'D': num1 + num2 if correct_option == 'D' else random.randint(1, 18),
    }

    return render_template('index.html', problem=problem, options=options, answers=answers)

if __name__ == '__main__':
    app.run(debug=True)
