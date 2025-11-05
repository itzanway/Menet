# 🏥 Medical Health Chatbot

A simple **AI-powered Medical Health Chatbot** built from scratch using Python — **no APIs or external AI services used**.  
This chatbot provides general health-related guidance, symptom-based suggestions, and emergency recommendations in a conversational format.

---

## 📋 Features

- 💬 Interactive chatbot built using Python
- 🧠 Rule-based and keyword-driven health conversation logic
- ⚕️ Provides general advice for common symptoms
- 🚑 Emergency alert responses for severe conditions
- 🩺 Easily extendable knowledge base for new diseases or symptoms
- 🖥️ Simple command-line interface for local testing

---

## 🧠 How It Works

1. The chatbot uses a **pattern-matching and keyword-based approach** to understand user input.  
2. It compares user symptoms with predefined health conditions.
3. Based on matching confidence, it provides relevant medical advice or emergency warnings.
4. Responses are stored and managed in a **JSON knowledge base file** (`intents.json`).

---

## 🏗️ Tech Stack

| Component | Description |
|------------|-------------|
| **Language** | Python 3 |
| **Libraries** | NLTK (for tokenization), NumPy |
| **Interface** | Command-line (can be extended to GUI/web) |
| **Storage** | JSON file for intents/responses |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/itzanway/Menet.git
cd medical-health-chatbot
