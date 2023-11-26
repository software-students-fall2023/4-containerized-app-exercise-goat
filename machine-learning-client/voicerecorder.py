import tkinter as tk
import threading
import pyaudio
#pip install pyaudio
import wave
class AudioRecorder:
    def __init__(me):
        me.audio = pyaudio.PyAudio()
        me.stream = None
        me.frames = []
        me.is_recording = False
    def start_recording(me):
        me.stream = me.audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
        me.is_recording = True
        threading.Thread(target=me.record).start()
    def stop_recording(me):
        me.is_recording = False
    def record(me):
        while me.is_recording:
            data = me.stream.read(1024)
            me.frames.append(data)
    def save_recording(me, filename):
        full_path = "C:\\Users\\YourUsername\\Documents\\" + filename
        #where to save the wavefiles.
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(2)
        waveFile.setsampwidth(me.audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)
        waveFile.writeframes(b''.join(me.frames))
        waveFile.close()
def record_audio():
    audio_recorder.start_recording()
    record_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
def stop_audio():
    audio_recorder.stop_recording()
    audio_recorder.save_recording("recorded_file.wav")
    record_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
audio_recorder = AudioRecorder()
window = tk.Tk()
window.title("Audio Recorder")
record_button = tk.Button(window, text="Record", command=record_audio)
record_button.pack()
stop_button = tk.Button(window, text="Stop", state=tk.DISABLED, command=stop_audio)
stop_button.pack()
window.mainloop()