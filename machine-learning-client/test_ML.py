import sys
import pytest
from unittest.mock import patch, Mock
from google.cloud import speech
from pydub import AudioSegment
import io


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

def convert_stereo_to_mono(input_wav, output_wav):
    audio = AudioSegment.from_wav(input_wav)
    audio = audio.set_channels(1)
    audio.export(output_wav, format="wav")

def run_quickstart(local_file_path) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    with io.open(local_file_path, "rb") as f:
        content = f.read()

    audio = {"content": content}

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    output = ""
    for result in response.results:
        output += f"{result.alternatives[0].transcript}"
    return output 

def get_transcript():
    input_wav = 'uploads/audio.wav'
    output_wav = 'curr.wav'
    convert_stereo_to_mono(input_wav, output_wav)
    return run_quickstart(output_wav)

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
