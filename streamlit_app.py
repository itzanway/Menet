import streamlit as st
import pickle, json
import nltk
from tensorflow.keras.models import load_model
from symptom_checker import analyze_symptoms
from nltk.stem import WordNetLemmatizer
import numpy as np
import random

st.set_page_config(page_title="Offline Medical Chatbot", layout="centered")

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
    return [{"intent": classes[r[0]], "probability": float(r[1])} for r in results]

def get_response(ints, intents_json):
    if not ints:
        return "I couldn't identify a clear intent. Try describing symptoms more specifically."
    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I don't have a response for that."

st.title("Offline Medical Chatbot")
st.write("Local, privacy-friendly medical helper (not a replacement for a clinician).")

# Symptom triage panel
st.header("Symptom Triage")
symptom_text = st.text_input("Enter symptoms (comma-separated)", placeholder="e.g. fever, cough, chest pain")
if st.button("Run Triage"):
    if symptom_text.strip() == "":
        st.warning("Please enter at least one symptom.")
    else:
        symptoms = [s.strip() for s in symptom_text.split(",") if s.strip()]
        analysis = analyze_symptoms(symptoms)
        st.subheader("Triage Result")
        st.write("Detected symptoms:", analysis["detected_symptoms"])
        st.info(f"Action level: {analysis['action']['level']}")
        st.write(analysis['action']['message'])

st.markdown("---")
st.header("Chat with the Bot")
user_input = st.text_input("Ask a question or describe a symptom", key="chat_input")
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please type a message first.")
    else:
        ints = predict_class(user_input)
        resp = get_response(ints, intents)
        st.write("Bot:", resp)
        # quick prompt to run triage if symptoms found
        for kw in ["fever", "cough", "chest", "breath", "headache", "vomit", "bleed", "dizzy", "confusion"]:
            if kw in user_input.lower():
                st.info("I detected symptom keywords — try the triage box above for specific action.")
                break
