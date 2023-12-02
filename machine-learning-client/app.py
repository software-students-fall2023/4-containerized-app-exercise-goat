from flask import Flask, jsonify, request, make_response
import db
import speechToText
import wave 

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def recognize_and_save(Id=1):
    Id = request.args.get('Id')
    #print(Id)
    transcript = speechToText.get_transcript()
    #print(transcript)
    db.save_transcript(transcript,Id)
    response = make_response(jsonify({'message': 'transcript saved!'}))
    return response

def save_wav_file(audio_data, output_file_path='input.wav'):
    with wave.open(output_file_path, 'wb') as wav_file:
        wav_file.setnchannels(1)  
        wav_file.setsampwidth(2) 
        wav_file.setframerate(44100)  
        wav_file.writeframes(audio_data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)