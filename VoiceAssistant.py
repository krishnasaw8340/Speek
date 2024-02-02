import warnings
import speech_recognition as sr
import pyttsx3
import os
import datetime
import calendar
import wikipedia

# Suppress warnings
warnings.filterwarnings('ignore')

def rec_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def response_to_query(query):
    now = datetime.datetime.now()

    if "date" in query:
        response_text = f"Today is {now.strftime('%A, %B %d, %Y')}."
    elif any(word in query for word in ["hi", "hello"]):
        response_text = "Hello there! How are you? By the way, I am great."
    elif any(word in query.lower() for word in ["i am also fine", "i am fine"]):
        response_text = "Great, buddy!"
    elif any(word in query.lower() for word in ["Your name", " tell me your name", "your name"]):
        response_text = "My name is Speek Assistant. thanks for asking !"
    elif any(word in query for word in ["who are you","define yourself"]):
        response_text = "Hello, I am the voice assistant of Krishna. I am here to make your life easier. You can command me to perform tasks like opening applications on the computer, writing emails, opening YouTube, etc."
    elif "time" in query:
        response_text = f"It is {now.strftime('%I:%M %p')}."
    elif "month" in query:
        response_text = f"We are in the month of {now.strftime('%B')}."
    elif "wikipedia" in query:
        if "who is" in query:
            person = wiki_person(query)
            wiki_summary = wikipedia.summary(person, sentences=2)
            response_text = f"{person} is {wiki_summary}"
        else:
            response_text = "I'm sorry, I didn't understand that Wikipedia query."
    elif "thank you" in query:
        response_text = "You're welcome! Exiting the program."
        exit()
    else:
        response_text = "I'm sorry, I didn't understand that query."

    return response_text

def wiki_person(text):
    list_wiki = text.split()
    for i in range(0, len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == "who" and list_wiki[i + 1].lower() == "is":
            return list_wiki[i + 2] + " " + list_wiki[i + 3]

def response(response_text):
    print(response_text)
    engine = pyttsx3.init()
    # Set the voice to a female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 1 for female
    engine.say(response_text)
    engine.runAndWait()

# Main loop
while True:
    try:
        query = rec_audio()
        if query:
            response_text = response_to_query(query)
            response(response_text)
    except KeyboardInterrupt:
        print("Exiting the program.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        response("I don't know that.")
