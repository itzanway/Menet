import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import streamlit as st

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "I'm not sure I understand. Could you describe your symptoms again?"
    tag = intents_list[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "Sorry, I don't have enough information for that."

# Streamlit UI Setup
st.set_page_config(page_title="💬 Medical Health Chatbot", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #f7f7f8;
    }
    .chat-container {
        max-width: 750px;
        margin: 0 auto;
        padding: 20px;
    }
    .message {
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
        line-height: 1.5;
        font-size: 16px;
        word-wrap: break-word;
    }
    .user {
        background-color: #0078FF;
        color: white;
        margin-left: auto;
        text-align: left;
    }
    .bot {
        background-color: #E5E5EA;
        color: black;
        margin-right: auto;
        text-align: left;
    }
    input {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.title("💬 Medical Health Chatbot")
st.caption("💡 Ask health-related questions — powered by AI (not a substitute for professional medical advice).")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    role_class = "user" if chat["role"] == "user" else "bot"
    st.markdown(f"<div class='message {role_class}'>{chat['message']}</div>", unsafe_allow_html=True)

user_input = st.text_input("Type your message here...", placeholder="e.g., I have a fever and headache.")

if st.button("Send"):
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        ints = predict_class(user_input)
        res = get_response(ints, intents)
        st.session_state.chat_history.append({"role": "bot", "message": res})
        st.rerun()
    else:
        st.warning("Please enter a message before sending.")

st.markdown("</div>", unsafe_allow_html=True)
