import pyaudio
import wave
import whisper
import numpy as np
import tempfile
import os
import warnings
import threading

warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

# Initialize Whisper model
model = whisper.load_model("base", device="cpu")  # Use "small" for better accuracy in Russian

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1  # BlackHole usually works in mono
RATE = 16000  # Whisper prefers 16kHz for speech
CHUNK = 4096  # Increase buffer size for better accuracy
RECORD_SECONDS = 5  # Keep fixed-length chunks
OVERLAP_SECONDS = 2  # Overlap to prevent missing words
BLACKHOLE_INDEX = 3  # Change this to your BlackHole index

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream from BlackHole
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, input_device_index=BLACKHOLE_INDEX,
                frames_per_buffer=CHUNK)

print("Listening...")

def transcribe_audio(filename):
    """Transcribes audio using Whisper"""
    result = model.transcribe(filename, language="ru")
    text = result["text"]
    os.remove(filename)  # Cleanup temp file
    print("Recognized:", text)

while True:
    frames = []

    # Capture audio for RECORD_SECONDS + OVERLAP_SECONDS
    for _ in range(int(RATE / CHUNK * (RECORD_SECONDS + OVERLAP_SECONDS))):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    # Save to a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        filename = tmp_wav.name

    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Transcribe in a separate thread (to reduce lag)
    threading.Thread(target=transcribe_audio, args=(filename,)).start()
