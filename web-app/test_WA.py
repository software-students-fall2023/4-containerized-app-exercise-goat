# pylint: disable=missing-module-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument
# pylint: disable=trailing-whitespace
# pylint: disable=invalid-name
# pylint: disable=singleton-comparison

import pytest
from app import create_app
from db import get_most_recent_transcript


@pytest.fixture
def app():
    app_instance = create_app()
    app_instance.config["TESTING"] = True
    return app_instance


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_upload_audio(client):
    response = client.get("/upload-audio")
    assert response


def test_connection(client):
    response = client.get("/test")
    assert response.status_code == 200


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"current_question" in response.data


def test_upload_audio_post(client, monkeypatch):
    monkeypatch.setattr("app.get_transcript", lambda: "transcript")
    response = client.post(
        "/upload-audio", data={"audio_data": (b"fake_audio_data", "audio.wav")}
    )
    assert response


# pylint: disable=trailing-whitespace
def test_cheat(client):
    response = client.get("/cheat")
    assert response.status_code == 200


def test_show_answer(client):
    response = client.get("/gimmeanswer")
    assert response.status_code == 200


def test_instruction(client):
    response = client.get("/instruction")
    assert response.status_code == 200


def test_db_error():
    message = get_most_recent_transcript()
    assert message is None
