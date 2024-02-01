import warnings
import pyttsx3
import speech_recognition as sr

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice to a female voice (you can adjust this based on available voices)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female

# Function to speak text
def talk(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to perform speech recognition
def rec_audio():
    recog = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recog.listen(source)
    data = " "
    try:
        # Using Google Speech Recognition (as in the provided link)
        data = recog.recognize_google(audio)
        print("You said " + data)
    except sr.RequestError as ex:
        print("Request Error from Google Speech Recognition: " + str(ex))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    return data
# Call the rec_audio function
result = rec_audio()

