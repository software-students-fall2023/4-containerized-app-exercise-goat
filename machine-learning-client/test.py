import wave

def check_wav_file(file_path):
    try:
        with wave.open(file_path, 'rb') as wav_file:
            # Check audio file format
            if wav_file.getnchannels() not in [1, 2]:
                return False, "Invalid number of channels (must be 1 or 2)"

            if wav_file.getsampwidth() not in [1, 2, 3, 4]:
                return False, "Invalid sample width"

            if wav_file.getframerate() <= 0:
                return False, "Invalid frame rate"

            return True, "WAV file is correctly formatted"

    except Exception as e:
        return False, f"Error: {str(e)}"
print(check_wav_file('audio.wav'))