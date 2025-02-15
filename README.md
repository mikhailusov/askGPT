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
http://127.0.0.1:5000
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
MIT License – Free for personal and commercial use.  
