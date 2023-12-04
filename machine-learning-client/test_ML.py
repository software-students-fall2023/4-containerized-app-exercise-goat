# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

import sys
from unittest.mock import patch, Mock
import io
from speechToText import run_quickstart, convert_stereo_to_mono


sys.modules["voicerecorder"] = Mock()
sys.modules["db"] = Mock()
sys.modules["speechToText"] = Mock()


def test_convert_stereo_to_mono():
    input_wav = "test_input.wav"
    output_wav = "test_output.wav"
    with patch("pydub.AudioSegment.from_wav") as mock_from_wav:
        mock_audio_segment = mock_from_wav.return_value
        mock_audio_segment.set_channels.return_value = mock_audio_segment
        convert_stereo_to_mono(input_wav, output_wav)
        mock_audio_segment.set_channels.assert_called_once_with(1)
        mock_audio_segment.export.assert_called_once_with(output_wav, format="wav")


def test_run_quickstart():
    local_file_path = "test.wav"
    with patch("google.cloud.speech.SpeechClient") as mock_speech_client:
        mock_client_instance = Mock()
        mock_speech_client.return_value = mock_client_instance
        with patch.object(mock_client_instance, "recognize"):
            with patch("builtins.open", return_value=io.StringIO()):
                run_quickstart(local_file_path)
