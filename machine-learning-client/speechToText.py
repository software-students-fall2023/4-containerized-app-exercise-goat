
# Imports the Google Cloud client library


from google.cloud import speech
from pydub import AudioSegment
import io
def convert_stereo_to_mono(input_wav, output_wav):
    # Load the stereo audio file
    audio = AudioSegment.from_wav(input_wav)

    # Convert stereo to mono
    audio = audio.set_channels(1)

    # Export the mono audio to a new WAV file
    audio.export(output_wav, format="wav")
def run_quickstart(local_file_path) -> speech.RecognizeResponse:
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    #gcs_uri = "machine-learning-client/77837^goodmrng.mp3"
    
    #gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
    #audio = speech.RecognitionAudio(uri=gcs_uri)
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    #print(content)
    audio = {"content": content}

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    print(response)
    output = ""
    for result in response.results:
        output += f"Transcript: {result.alternatives[0].transcript}"
    return output 
def get_transcript():
    input_wav = 'machine-learning-client/input.wav'
    output_wav = 'machine-learning-client/curr.wav'
    convert_stereo_to_mono(input_wav,output_wav)
    return run_quickstart(output_wav)

