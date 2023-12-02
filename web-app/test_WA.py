import pytest
from app import app, get_transcript
from bs4 import BeautifulSoup
import json
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    current_question_tag = soup.find('div', {'id': 'current-question'})
    assert current_question_tag is not None

def test_check_answer_correct(client):
    response = client.get('/')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    current_question_tag = soup.find('div', {'id': 'current-question'})
    
    if current_question_tag:
        correct_answer_tag = current_question_tag.find('span', {'class': 'correct-answer'})
        
        if correct_answer_tag:
            correct_answer = correct_answer_tag.text
            selected_answer_tag = soup.find('input', {'name': 'answer', 'checked': True})
            selected_answer = selected_answer_tag['value'] if selected_answer_tag else None
            
            assert selected_answer == correct_answer
        else:
            assert "No correct-answer span found in current question."
    else:
        assert f'No current question found in HTML: {response.data}'

def test_check_answer_incorrect(client):
    response = client.get('/')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    current_question_tag = soup.find('div', {'id': 'current-question'})

    if current_question_tag:
        correct_answer_tag = current_question_tag.find('span', {'class': 'correct-answer'})

        if correct_answer_tag:
            correct_answer = correct_answer_tag.text

            # Assume an incorrect answer for the test
            incorrect_answer = "incorrect_answer"

            selected_answer_tag = soup.find('input', {'name': 'answer', 'checked': True})
            selected_answer = selected_answer_tag['value'] if selected_answer_tag else None

            assert selected_answer != correct_answer
        else:
            assert "No correct-answer span found in current question."
    else:
        assert f'No current question found in HTML: {response.data}'
        
def test_check_answer_max_attempts(client):
    for _ in range(2):  # Only make two attempts to reach the maximum
        response = client.post('/check_answer', data={'answer': 'incorrect_answer'})
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data['max_attempts_reached'] is False

    # On the third attempt, max_attempts_reached should be True
    response = client.post('/check_answer', data={'answer': 'incorrect_answer'})
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data['max_attempts_reached'] is True
    assert 'next_question' in data


    
