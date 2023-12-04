# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=singleton-comparison
# pylint: disable=no-member
# pylint: disable=no-name-in-module

"""import modules"""
import pytest
from app import create_app
from db import get_most_recent_transcript


@pytest.fixture
def app():
    """create app"""
    app_instance = create_app()
    app_instance.config["TESTING"] = True
    return app_instance


@pytest.fixture
def client(app):
    """create client"""
    return app.test_client()


def test_index(client):
    """test index page"""
    response = client.get("/")
    assert response.status_code == 200


def test_upload_audio(client):
    """test upload audio function"""
    response = client.get("/upload-audio")
    assert response


def test_connection(client):
    """test connection to app"""
    response = client.get("/test")
    assert response.status_code == 200


def test_index_route(client):
    """test index route"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"current_question" in response.data


def test_upload_audio_post(client, monkeypatch):
    """test upload audio route"""
    monkeypatch.setattr("app.get_transcript", lambda: "transcript")
    response = client.post(
        "/upload-audio", data={"audio_data": (b"fake_audio_data", "audio.wav")}
    )
    assert response


def test_cheat(client):
    """test cheat route"""
    response = client.get("/cheat")
    assert response.status_code == 200


def test_show_answer(client):
    """test show answer route"""
    response = client.get("/gimmeanswer")
    assert response.status_code == 200


def test_instruction(client):
    """test instruction route"""
    response = client.get("/instruction")
    assert response.status_code == 200


def test_db_error():
    """test behavior if db error"""
    message = get_most_recent_transcript()
    assert message is None
