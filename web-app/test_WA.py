import pytest
from app import app, get_transcript

import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    
def test_upload_audio(client):
    response = client.get('/upload-audio')
    assert response

@pytest.fixture
def client(app):
    return app.test_client()
