# stt_server.py

import os
import zipfile
import urllib.request
import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from vosk import Model, KaldiRecognizer

# ------------------------------
# 1. Download Vosk tiny model automatically if not present
# ------------------------------
model_folder = "model/vosk-model-small-en-us-0.15"
zip_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
zip_path = "vosk-model-small-en-us-0.15.zip"

if not os.path.exists(model_folder):
    print("Downloading Vosk tiny model...")
    urllib.request.urlretrieve(zip_url, zip_path)
    print("Extracting model...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("model")
    os.remove(zip_path)
    print("Vosk model ready!")

# ------------------------------
# 2. Initialize Flask and SocketIO
# ------------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Load Vosk model
model = Model(model_folder)
print("Vosk model loaded successfully.")

# ------------------------------
# 3. Flask routes
# ------------------------------
@app.route('/')
def index():
    return render_template("index.html")  # frontend HTML for captions

# ------------------------------
# 4. Handle incoming audio via WebSocket
# ------------------------------
@socketio.on('audio_chunk')
def handle_audio(data):
    """
    data: raw PCM 16-bit audio bytes from browser
    """
    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(data)
    result = json.loads(rec.Result())
    emit('transcript', result['text'])

# ------------------------------
# 5. Start server
# ------------------------------
if __name__ == "__main__":
    print("Starting STT server on port 5000...")
    socketio.run(app, host="0.0.0.0", port=5000)
