# 🚀 AskGPT: Your AI-Powered Live Call Assistant 🎙️💬  

**AskGPT** is a **real-time AI assistant** that enhances your **calls, interviews, meetings, and lectures** by providing **instant AI-generated insights**.  
It captures live audio, transcribes speech into text, and generates **context-aware responses**—all in real-time!  

## ✨ Features  
- 🎤 **Live Transcription** – Converts speech into text instantly using **Whisper AI**.  
- 🤖 **Instant AI Responses** – Get **context-aware** AI-generated answers on the fly.  
- ⚙️ **Customizable AI Context** – Adapt AskGPT for **customer service, interviews, or important calls**.  
- 🔒 **Local & Private** – Runs **entirely on your machine** using **Ollama**, keeping data secure.  
- ⚡ **Fast & Seamless** – Streams **AI responses token-by-token** for real-time assistance.  

---

## 🔍 How It Works  
1. **Start AskGPT** – It listens to your call or meeting.  
2. **Transcribes Speech** – Converts spoken words into editable text.  
3. **Modify & Ask AI** – Adjust the text before sending it to AI.  
4. **Instant AI Assistance** – AI generates **short, precise answers** with brief explanations.  

💡 **Use it for:**  
✅ **Providing Context for Customer Service** – Quickly retrieve relevant information to assist customers efficiently.  
✅ **Getting Context on Important Calls** – Summarize key points and remember critical details.  
✅ **Help During Interviews** – Get AI assistance in answering behavioral, technical, or case study questions.  

---

## 🎧 Setting Up BlackHole on macOS for Audio Routing

AskGPT uses **BlackHole** to capture system audio for transcription. Follow these steps to install and configure it properly.

---

### 1️⃣ Install BlackHole
BlackHole is a **virtual audio driver** that allows applications to send and receive audio between different apps.

1. Download BlackHole from the official [BlackHole GitHub](https://github.com/ExistentialAudio/BlackHole).
2. Install it by following the instructions in the `.pkg` installer.

---

### 2️⃣ Create a Multi-Output Device (Route Audio to Both Speakers & BlackHole)
To hear the system audio while also sending it to BlackHole:

1. Open **Audio MIDI Setup** (`Command + Space` → search for "Audio MIDI Setup").
2. Click **`+`** in the bottom-left corner and select **"Create Multi-Output Device"**.
3. In the right panel, enable:
   - ✅ **Built-in Output** (Your Mac’s speakers or external device)
   - ✅ **BlackHole 16ch** (or the version you installed)
4. Set **BlackHole as the Master Device**.
5. Check **Drift Correction** for your built-in speakers.
6. Rename it (optional) to something like **"BlackHole + Speakers"** for easy identification.

---

### 3️⃣ Find & Set `BLACKHOLE_INDEX` in `app.py`
AskGPT needs the correct **input device index** to listen to **BlackHole**.  

#### ✅ **Find the BlackHole Device Index**
Run the following script to list available audio devices:

```sh
python devs.py
```

This will output something like:

```
Index 0: Built-in Microphone
Index 1: BlackHole 16ch
Index 2: Built-in Output
```

Look for the **BlackHole device** and note its **index number**.

#### ✅ **Update `AUDIO_DEVICE_INDEX` in `app.py`**
Open `app.py` and update this line:
```python
AUDIO_DEVICE_INDEX = X  # Change this to your BlackHole device index
```
For example, if `BlackHole 16ch` is at index `1`, update:
```python
AUDIO_DEVICE_INDEX = 1  # Change this to your BlackHole device index
```

Save the file and restart **AskGPT**.

---

### 4️⃣ Set Your Mac’s Audio Output to the Multi-Output Device
1. Open **System Settings** → **Sound**.
2. Under **Output**, select your **Multi-Output Device**.
3. Now, all system audio will be played **through both your speakers and BlackHole**.

---

### 5️⃣ Use BlackHole as an Input in AskGPT
1. Open **AskGPT** and ensure it is set to listen to **BlackHole**.
2. Now, the system audio will be transcribed while still being audible through your speakers.

💪 **You’re all set!** Now, AskGPT will capture system audio while you can still hear it! 🎧🔥

---

### 🛠️ Troubleshooting
- If you **don’t hear sound**, check that **Built-in Output** is enabled in your **Multi-Output Device**.
- If **AskGPT doesn’t capture audio**, ensure **BlackHole is selected as the input device** in your app.
- Run `devs.py` again if **BlackHole's index changes** after reconnecting devices.
- Restart your Mac if changes don’t apply immediately.



## 🛠 Installation & Setup  

### **1️⃣ Install Dependencies**  

Make sure you have **Python 3.9+** installed. Then, install required libraries:  

```sh
pip install flask flask-socketio pyaudio whisper flask-cors requests
```

### **2️⃣ Install & Run Ollama**  

Download **Ollama** and install the best AI model for your use case:  

```sh
curl -fsSL https://ollama.ai/install.sh | sh
```

Then, install the AI models:  

```sh
ollama pull codellama  # Best for coding-related queries
ollama pull mistral    # Fast & balanced responses
ollama pull gemma      # General-purpose AI model
```

Now, start the Ollama server:  

```sh
ollama serve
```

### **3️⃣ Run AskGPT**  

```sh
python app.py
```

Then open:  

```
http://127.0.0.1:8080
```

---

## ⚙️ Customizing the AI Context  

Click **"Set Context"** in the UI to modify the AI’s behavior. You can:  
- 🏆 **Support customer service interactions** (e.g., "Summarize key customer concerns and suggest appropriate responses.")  
- 📝 **Assist in important calls** (e.g., "Extract important details and action points from business meetings.")  
- 🎤 **Help during interviews** (e.g., "Provide structured responses to behavioral and technical interview questions.")  

---

## 🎯 Who Should Use AskGPT?  
🚀 **Customer Service Representatives** – Get **real-time AI-generated insights** to improve responses.  
📞 **Professionals & Business Users** – **Take live notes** and gain context during important calls.  
🎙️ **Job Seekers & Interviewees** – **Receive AI-assisted responses** in interviews beyond technical roles.  

No more struggling to keep up—**AskGPT is your personal AI assistant for live conversations!** 🚀🔥  

---

## 🤝 Contributing  
Got an idea for improvement?  
Feel free to submit a **pull request** or open an **issue** on GitHub!  

---

## 📜 License  
CC0 1.0 Universal – Free for personal and commercial use.  
