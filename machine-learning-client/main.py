import voicerecorder
import db
import speechToText
import sys
def start_recording():
    voicerecorder.record_audio()
def stop_recording():
    voicerecorder.stop_audio()
def save(name):
    transcript = speechToText.get_transcript()
    print(transcript)
    db.save_current_audio(transcript,name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name.")
    else:
        function_name = sys.argv[1]
        if function_name in globals() and callable(globals()[function_name]):
            if (function_name=='save'):
                name = sys.argv[2]
                globals()[function_name](name)
            else: 
                globals()[function_name]()
        else:
            print(f"Function '{function_name}' not found.")