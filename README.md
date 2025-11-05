# 🏥 Medical Health Chatbot

A simple **AI-powered Medical Health Chatbot** built from scratch using Python — **no APIs or external AI services used**.  
This chatbot provides general health-related guidance, symptom-based suggestions, and emergency recommendations in a conversational format.

---

## 📸 Project Overview

![Medical Chatbot Screenshot](Screenshot%202025-11-05%20184751.png)
> 💡 *Sample terminal interface of the Medical Health Chatbot.*

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
2. It compares user symptoms with predefined health conditions stored in a JSON file.  
3. Based on the similarity score, it provides relevant medical advice or emergency instructions.  
4. All responses are dynamically selected from `intents.json`.

---

## 🧩 Workflow Diagram

```mermaid
flowchart TD
    A([🧍 User Input]) --> B([🧹 Tokenize & Clean Text])
    B --> C([🔍 Keyword Matching from intents.json])
    C --> D([🧠 Identify Possible Condition])
    D --> E([💬 Select Response])
    E --> F([⚕️ Display Health Advice])
    D -->|❌ No Match| G([🤖 Default / Fallback Response])
