# ❄️ Elsa AI Chatbot

**Talk to Elsa from Frozen in real-time!**  
This project brings the magic of Arendelle to life using **AI + Web technologies**.  
It includes:
- 🧊 A **Flask backend** with a fine-tuned TinyLLaMA model (via [Unsloth](https://unsloth.ai/))  
- 🌐 A **React frontend** with a magical snowflake-themed UI  
- 🤖 A **trained dialogue system** that captures Elsa's regal yet kind personality  

---

## ✨ Features
- Engage in **real-time conversations** with Elsa  
- Switch response length dynamically with commands:
  - `/long` → Longer responses  
  - `/short` → Shorter responses  
  - `/auto` → Smart auto mode  
- Cleaned, structured responses with natural sentence endings  
- Memory-friendly **model offloading** (runs on GPU if available, falls back to CPU)  
- Frozen-inspired **UI with animations**  

---

## 🛠️ Tech Stack
- **Backend:** Flask, Hugging Face Transformers, PEFT, Torch  
- **Model:** Fine-tuned [TinyLLaMA-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama)  
- **Frontend:** React.js, CSS animations  
- **Dataset:** 800+ synthetic Elsa dialogues & Frozen-inspired Q&A pairs  

---

## 📂 Project Structure without Training Model File Structure
```

elsa_App/
├── backend/
│   ├── venv/                   # Python virtual environment (auto-generated)
│   │   ├── Scripts/
│   │   │   ├── activate
│   │   │   ├── python.exe
│   │   │   └── pip.exe
│   │   └── Lib/
│   │       └── site-packages/  # Python packages
│   ├── offload/                # Model offload directory (created by you)
│   ├── trained_model/          # Your trained model files
│   │   ├── adapter_config.json
│   │   ├── adapter_model.safetensors
│   │   ├── chat_template.jinja
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer.json
│   │   ├── tokenizer.model
│   │   └── tokenizer_config.json
│   ├── app.py                  # Flask server (main backend file)
│   ├── requirements.txt        # Python dependencies
│   └── start.bat               # Optional Windows start script
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── SnowflakeAnimation.jsx
    │   │   ├── SnowflakeAnimation.css
    │   │   ├── ElsaVideoPlayer.jsx
    │   │   ├── ElsaVideoPlayer.css
    │   │   ├── IntroPage.jsx
    │   │   ├── IntroPage.css
    │   │   ├── ChatInterface.jsx
    │   │   ├── ChatInterface.css
    │   │   ├── DeveloperPage.jsx
    │   │   ├── DeveloperPage.css
    │   │   ├── MoviesPage.jsx
    │   │   └── MoviesPage.css
    │   ├── services/
    │   │   └── api.js          # API service functions
    │   ├── App.jsx
    │   ├── App.css
    │   ├── main.jsx
    │   └── index.css
    ├── public/
    │   ├── vite.svg
    │   └── favicon.ico
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    └── node_modules/           # Auto-generated (don't commit to git)


````

---

# 🚀 Elsa AI Chatbot - Complete Setup Guide

## 📋 Two Ways to Use This Project:

### Option 1: 🏃‍♂️ **Just Run the App** (Quick Start)
If you want to use the pre-trained chatbot:

1. **Navigate to the app folder:**
   ```bash
   cd elsaApp
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run Flask backend
   python app.py
   ```

3. **Set up the frontend** (in a NEW terminal):
   ```bash
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start React app
   npm run dev
   ```

4. **Access the app:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Option 2: 🎓 **Train Your Own Model** (Advanced)
If you want to train your own Elsa model:

1. **Prepare your data:**
   - Create a CSV file with question-answer pairs
   - Format: `Question,Answer` columns
   - You can use TinyLlama (as I did) or any other model

2. **Run the training scripts in order:**

3. **After training, run the app** (as in Option 1)

## 🛠️ **Requirements:**
- Python 3.8+ with virtual environment
- Node.js and npm for React frontend
- CSV dataset (if training your own model)
- GPU recommended for training (but works on CPU too)

## ⚡ **Quick Notes:**
- Backend runs on port 5000 (Flask API)
- Frontend runs on port 5173 (React app)
- No additional files needed to run - everything works automatically
- Training can take several hours depending on your hardware

Choose Option 1 if you just want to use the chatbot, or Option 2 if you want to train your own custom model! 🚀❄️
---

## 🌍 Deployment (Free Hosting Options)

* **Backend (Flask + Model)** → Deploy on [Render](https://render.com/), [Railway](https://railway.app/), or [Hugging Face Spaces](https://huggingface.co/spaces).
* **Frontend (React)** → Deploy on [Vercel](https://vercel.com/) or [Netlify](https://www.netlify.com/).

⚡ **Tip:** For Hugging Face Spaces, just upload your backend folder and select `Flask` as the runtime.

---

## 💡 Training Your Own Elsa

When building this project, one of the **biggest challenges** was the **lack of existing Elsa datasets**.
At first, I tried searching everywhere—scripts, transcripts, dialogue datasets but none really fit. I had no idea how to train a model just based on a few movie clips.

So instead, I decided to **create a synthetic dataset myself**.

* Wrote **800+ lines of Elsa-inspired dialogues**
* Added Frozen-themed Q\&A pairs, conversations, and character-specific traits
* Used that dataset to **fine tune TinyLLaMA**

The training itself was no easy task. It took me **2.5 days of continuous training on my laptop (a literal potato 🥔)**. But in the end, the model started capturing Elsa’s tone **warm, regal, and magical**.

👉 **Why fine-tune?**
Fine-tuning a smaller model like TinyLLaMA with a custom dataset is much better than trying to make a base model pretend to be Elsa with prompts. Fine tuning **locks in personality & responses**, making Elsa far more consistent and authentic.

---

### 🔧 Train Your Own Elsa (or Any Character!)

You can train Elsa (or Anna, Olaf, even Darth Vader if you want 😅) on your own laptop or PC.

Steps:

1. Collect or create a dataset (dialogues, Q\&A, personality traits)
2. Place it in the training script’s folder
3. Run the training scripts one by one (inside `scripts/` or your own training pipeline)
4. Replace the `trained_model/` folder in the backend with your new adapter
5. Restart the Flask server → boom, your own chatbot is alive 🚀

⚠️ Remember:

* The filing is not done properly over here, you have to do it yourself ok, as we cant upload large files to Github
* app.py is the backend which you run in the backend folder, and the src with the public folder is for frontend 
* Always install all requirements first
* Run everything inside a **virtual environment**
* Be patient: training can take days depending on hardware

---

## 📖 Backstory

This project was inspired by the developer’s sister, who was watching **Frozen** on her tablet and asked:

> *“Is there any way I can talk to Elsa in real life?”*

That simple question sparked the idea for **Elsa AI Chatbot**.
The journey included:

* Hours of searching for datasets (none existed)
* Manually creating 800+ synthetic dialogue lines
* **2.5 days of training** on limited hardware
* Countless cups of coffee ☕

And at the end, Elsa came to life.

---

## ⚠️ Notes

* Elsa may occasionally **hallucinate** or give creative answers (that’s the charm of TinyLLaMA!).
* The model is optimized for **conversation & Frozen lore** but may not always be factually correct.
* Magic has its limits but Elsa will always respond in her warm, regal Frozen style.

---

## 👨‍💻 Developer

Made with ❤️, ❄️, and a touch of coffee magic ☕

If you like this project, ⭐ the repo and share it!
