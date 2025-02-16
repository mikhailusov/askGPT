import os
import json
import wave
import threading
import tempfile
import warnings
import requests
import logging
import pyaudio
import whisper
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

# ========== Logging Setup ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to file
        logging.StreamHandler()  # Output logs to console
    ]
)

# Suppress Whisper warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

# Flask App Setup
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration Constants
OLLAMA_API = "http://localhost:11434/api/tags"
OLLAMA_GENERATE = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "codellama"
AUDIO_DEVICE_INDEX = 4  # Change this to your BlackHole device index
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
RECORD_SECONDS = 5
OVERLAP_SECONDS = 3

# Global Variables
ollama_model = DEFAULT_MODEL
current_context = (
    "You are a software engineer candidate in a technical interview for a Java developer role. "
    "You will be asked technical questions by the interviewer. "
    "Provide a concise answer first, then briefly elaborate with an explanation or example."
)

# Initialize Whisper Model
logging.info("Loading Whisper model...")
whisper_model = whisper.load_model("base", device="cpu")
logging.info("Whisper model loaded successfully.")

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
    input_device_index=AUDIO_DEVICE_INDEX, frames_per_buffer=CHUNK
)
logging.info("Audio stream initialized.")


# ========== API ROUTES ==========
@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/get_models", methods=["GET"])
def get_models():
    """Fetch available models from Ollama."""
    logging.info("Fetching available models from Ollama...")
    try:
        response = requests.get(OLLAMA_API)
        response.raise_for_status()
        models = response.json().get("models", [])
        model_names = [model["name"] for model in models]
        logging.info(f"Available models: {model_names}")
        return jsonify({"models": model_names})
    except requests.RequestException as e:
        logging.error(f"Error fetching models: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/set_model", methods=["POST"])
def set_model():
    """Set the AI model to use."""
    global ollama_model
    data = request.get_json()
    if "model" in data:
        ollama_model = data["model"]
        logging.info(f"Model changed to: {ollama_model}")
        return jsonify({"status": "success", "model": ollama_model})
    logging.warning("Invalid model selection attempt.")
    return jsonify({"error": "Invalid model selection"}), 400


@app.route("/get_context", methods=["GET"])
def get_context():
    """Retrieve the current AI context."""
    return jsonify({"context": current_context})


@app.route("/set_context", methods=["POST"])
def set_context():
    """Update the AI conversation context."""
    global current_context
    data = request.get_json()
    if "context" in data:
        current_context = data["context"]
        logging.info("Context updated.")
        return jsonify({"status": "success"})
    logging.warning("Invalid context update attempt.")
    return jsonify({"error": "Invalid context"}), 400


# ========== AUDIO PROCESSING ==========
def save_audio(frames):
    """Save recorded audio to a temporary WAV file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        filename = tmp_wav.name

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    logging.info(f"Audio saved to: {filename}")
    return filename


def transcribe_audio(filename):
    """Transcribe audio using Whisper and emit results via SocketIO."""
    try:
        logging.info(f"Transcribing audio: {filename}")
        result = whisper_model.transcribe(filename, language="ru")
        text = result.get("text", "").strip()
        os.remove(filename)
        logging.info(f"Transcription result: {text[:50]}...")  # Show first 50 chars

        if text:
            socketio.emit("new_transcription", {"text": text})
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        socketio.emit("new_transcription", {"error": str(e)})


def listen_for_audio():
    """Continuously record and process audio in background."""
    logging.info("Starting audio recording thread...")
    while True:
        frames = [stream.read(CHUNK, exception_on_overflow=False)
                  for _ in range(int(RATE / CHUNK * (RECORD_SECONDS + OVERLAP_SECONDS)))]

        filename = save_audio(frames)
        threading.Thread(target=transcribe_audio, args=(filename,)).start()


# ========== AI RESPONSE HANDLING ==========
@socketio.on("ask_gpt")
def handle_ask_gpt(data):
    """Handle AI query and stream response."""
    user_text = data.get("text", "")
    response_id = data.get("id", "")

    if not user_text or not response_id:
        logging.warning("Invalid AI request received.")
        socketio.emit("gpt_response", {"response": "Invalid input", "id": response_id})
        return

    logging.info(f"Received AI request: {user_text[:50]}...")  # Show first 50 chars

    def stream_ollama():
        """Stream AI-generated response token by token."""
        try:
            response = requests.post(
                OLLAMA_GENERATE,
                json={"model": ollama_model, "prompt": f"{current_context}\n\nQ: {user_text}\nA:", "stream": True},
                stream=True
            )
            logging.info("Streaming AI response...")

            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line.decode("utf-8"))
                        token = json_data.get("response", "")
                        socketio.emit("gpt_response", {"response": token, "id": response_id})
                    except json.JSONDecodeError:
                        continue
        except requests.RequestException as e:
            logging.error(f"Error during AI response streaming: {e}")
            socketio.emit("gpt_response", {"response": f"Error: {str(e)}", "id": response_id})

    threading.Thread(target=stream_ollama).start()


# Start audio recording in the background
threading.Thread(target=listen_for_audio, daemon=True).start()

if __name__ == "__main__":
    logging.info("Starting Flask server...")
    socketio.run(app, host="127.0.0.1", port=8080, debug=True)
