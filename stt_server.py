from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from vosk import Model, KaldiRecognizer
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Load Vosk tiny model
model = Model("model/vosk-model-small-en-us-0.15") 

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('audio_chunk')
def handle_audio(data):
    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(data)
    result = json.loads(rec.Result())
    emit('transcript', result['text'])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
