import pytest
from app import create_app
import json

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_upload_audio(client):
    response = client.get('/upload-audio')
    assert response

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'current_question' in response.data

def test_upload_audio_post(client, monkeypatch):
    monkeypatch.setattr("app.get_transcript", lambda: "transcript")
    response = client.post('/upload-audio', data={'audio_data': (b'fake_audio_data', 'audio.wav')})
    assert response
