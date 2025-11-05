import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from symptom_checker import analyze_symptoms

lemmatizer = WordNetLemmatizer()

# load resources (train model first)
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
        return "I couldn't identify a clear intent. Could you describe symptoms or ask directly?"
    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I don't have a response for that."

print("Medical Chatbot (CLI) — type 'quit' to exit. Type 'symptom:' followed by comma-separated symptoms to run triage.")
while True:
    text = input("You: ")
    if text.lower() == "quit":
        print("Bot: Take care — seek medical help as needed.")
        break
    if text.lower().startswith("symptom:"):
        # user provided explicit symptom list
        raw = text[len("symptom:"):].strip()
        symptoms = [s.strip() for s in raw.split(",") if s.strip()]
        analysis = analyze_symptoms(symptoms)
        print("Bot: Triage result:")
        print(f"  Detected: {analysis['detected_symptoms']}")
        print(f"  Action: {analysis['action']['level']} - {analysis['action']['message']}")
        continue

    ints = predict_class(text)
    resp = get_response(ints, intents)
    print(f"Bot: {resp}")

    # if user mentions symptoms in sentence, run simple symptom check
    # quick keyword extraction (very simple)
    maybe_symptoms = []
    for k in ["fever", "cough", "chest", "breath", "pain", "headache", "nausea", "vomit", "bleed", "dizzy", "confusion"]:
        if k in text.lower():
            maybe_symptoms.append(text)
            break
    # If we detected symptom words, ask to run triage
    if maybe_symptoms:
        print("Bot: I detected possible symptoms. You can run triage by typing: symptom: fever, cough")
