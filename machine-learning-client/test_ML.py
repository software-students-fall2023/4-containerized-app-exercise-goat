import sys
import pytest
from unittest.mock import patch, Mock
from speechToText import run_quickstart, convert_stereo_to_mono
import io
import json
from app import app, save_wav_file


# Mocking external dependencies
sys.modules['voicerecorder'] = Mock()
sys.modules['db'] = Mock()
sys.modules['speechToText'] = Mock()

import main
import voicerecorder

@pytest.fixture
def audio_recorder():
    return voicerecorder.AudioRecorder()

def test_start_recording_in_main():
    with patch('voicerecorder.record_audio') as mock_record_audio:
        main.start_recording()
        mock_record_audio.assert_called_once()

def test_stop_recording_in_main():
    with patch('voicerecorder.stop_audio') as mock_stop_audio:
        main.stop_recording()
        mock_stop_audio.assert_called_once()

def test_save_in_main():
    with patch('speechToText.get_transcript', return_value='Test transcript'):
        with patch('db.save_current_audio') as mock_save_current_audio:
            name = 'test_name'
            main.save(name)
            mock_save_current_audio.assert_called_once_with('Test transcript', name)

def test_convert_stereo_to_mono():
    input_wav = 'test_input.wav'
    output_wav = 'test_output.wav'
    with patch('pydub.AudioSegment.from_wav') as mock_from_wav:
        mock_audio_segment = mock_from_wav.return_value
        mock_audio_segment.set_channels.return_value = mock_audio_segment
        convert_stereo_to_mono(input_wav, output_wav)
        mock_audio_segment.set_channels.assert_called_once_with(1)
        mock_audio_segment.export.assert_called_once_with(output_wav, format="wav")

def test_run_quickstart():
    local_file_path = 'input.wav'
    with patch('google.cloud.speech.SpeechClient') as mock_speech_client:
        mock_client_instance = Mock()
        mock_speech_client.return_value = mock_client_instance
        with patch.object(mock_client_instance, 'recognize') as mock_recognize:
            with patch('builtins.open', return_value=io.StringIO()) as mock_open:
                run_quickstart(local_file_path)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_get_transcript(monkeypatch):
    def mock_get_transcript_function():
        return "Mocked transcript"
    
    monkeypatch.setattr("app.speechToText.get_transcript", mock_get_transcript_function)

@pytest.fixture
def mock_save_transcript(monkeypatch):
    def mock_save_transcript_function(transcript, Id):
        return None  # Mock the save_transcript function
    
    monkeypatch.setattr("app.db.save_transcript", mock_save_transcript_function)

def test_recognize_and_save(client, mock_get_transcript, mock_save_transcript):
    response = client.get('/transcript?Id=1')

    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == {'message': 'transcript saved!'}


