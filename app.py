import pyaudio
import wave
import whisper
import numpy as np
import tempfile
import os
import threading
import requests
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import warnings
import json

warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for local testing

OLLAMA_API = "http://localhost:11434/api/tags"
OLLAMA_GENERATE = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "codellama"  # Default model

# Fetch available models from Ollama
@app.route("/get_models", methods=["GET"])
def get_models():
    try:
        response = requests.get(OLLAMA_API)
        models = response.json().get("models", [])
        model_names = [model["name"] for model in models]
        return jsonify({"models": model_names})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set_model", methods=["POST"])
def set_model():
    global OLLAMA_MODEL
    data = request.get_json()
    if "model" in data:
        OLLAMA_MODEL = data["model"]
        return jsonify({"status": "success", "model": OLLAMA_MODEL})
    return jsonify({"error": "Invalid model selection"}), 400

# Initialize Whisper model
model = whisper.load_model("base", device="cpu")

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
RECORD_SECONDS = 5  # Keep fixed-length chunks
OVERLAP_SECONDS = 3  # Overlap to prevent missing words
BLACKHOLE_INDEX = 4  # Change this to your BlackHole index

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, input_device_index=BLACKHOLE_INDEX,
                frames_per_buffer=CHUNK)

@app.route("/")
def index():
    return render_template("index.html")

# Default context message (can be changed in UI)
current_context = (
    "You are a software engineer candidate in a technical interview for a Java developer role. "
    "You will be asked technical questions by the interviewer. "
    "Answer in a structured way: **first, provide the shortest possible correct answer** to directly answer the question, "
    "then briefly elaborate with an explanation or example. "
    "Keep your responses concise but informative, demonstrating expertise."
)

@app.route("/get_context", methods=["GET"])
def get_context():
    return json.dumps({"context": current_context})

@app.route("/set_context", methods=["POST"])
def set_context():
    global current_context
    data = json.loads(request.data)
    current_context = data["context"]
    return json.dumps({"status": "success"})

def transcribe_audio(filename):
    with app.app_context():
        result = model.transcribe(filename, language="ru")
        text = result["text"]
        os.remove(filename)
        if text.strip():
            socketio.emit("new_transcription", {"text": text})

def listen_for_audio():
    with app.app_context():
        while True:
            frames = []
            for _ in range(int(RATE / CHUNK * (RECORD_SECONDS + OVERLAP_SECONDS))):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                filename = tmp_wav.name

            wf = wave.open(filename, "wb")
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            threading.Thread(target=transcribe_audio, args=(filename,)).start()

@socketio.on("ask_gpt")
def handle_ask_gpt(data):
    user_text = data["text"]
    response_id = data["id"]

    socketio.emit("gpt_response", {"response": "", "id": response_id})

    def stream_ollama():
        try:
            response = requests.post(
                OLLAMA_GENERATE,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": f"{current_context}\n\nQuestion: {user_text}\nAnswer:",
                    "stream": True
                },
                stream=True
            )

            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line.decode("utf-8"))
                        token = json_data.get("response", "")
                        socketio.emit("gpt_response", {"response": token, "id": response_id})
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            socketio.emit("gpt_response", {"response": f"Error: {str(e)}", "id": response_id})

    threading.Thread(target=stream_ollama).start()

threading.Thread(target=listen_for_audio, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8080, debug=True)
