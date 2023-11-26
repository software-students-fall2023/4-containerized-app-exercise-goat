import voicerecorder
import db
import speechToText
import io
def start_recording():
    voicerecorder.record_audio()
def stop_recording():
    voicerecorder.stop_audio()
def save(name):
    transcript = speechToText.get_transcript()
    db.save_current_audio(transcript,name)
    
