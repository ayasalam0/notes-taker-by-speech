import os
from flask import Flask, render_template, request
import speech_recognition as sr
from pydub import AudioSegment


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recorder', methods=['POST'])
def transcribe():
    audio_file = request.files['audio_data']
    file_path = "audio.webm"
    audio_file.save(file_path)

    audio = AudioSegment.from_file(file_path)
    audio.export("audio.wav", format="wav")
    recognizer = sr.Recognizer()

    with sr.AudioFile("audio.wav") as source:
        audio_data = recognizer.record(source)

    os.remove(file_path)
    os.remove("audio.wav")

    try:
        text = recognizer.recognize_google(audio_data)
    except (sr.RequestError, sr.UnknownValueError):
        text = "Speech recognition failed."
    return text


if __name__ == '__main__':
    app.run(debug=True)
