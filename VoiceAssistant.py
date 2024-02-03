import warnings
import speech_recognition as sr
import pyttsx3
import os
import wikipedia
import webbrowser
import pyjokes
import subprocess
import requests

import datetime
import os.path
import wolframalpha


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

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-")+ "note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

# Replace 'YOUR_APP_ID' with your actual Wolfram Alpha app ID
app_id = '3J4KK6-E4PQG4V7V2'

# Base URL for the Conversational API
base_url = 'http://api.wolframalpha.com/v1/conversation.jsp'

def make_wolfram_alpha_query(query, conversation_id=None, s=None):
    # Prepare query parameters
    params = {
        'appid': app_id,
        'i': query,
    }

    # Add optional parameters if available
    if conversation_id:
        params['conversationid'] = conversation_id
    if s:
        params['s'] = s

    # Make the HTTP request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()

        # Check for errors
        if 'error' in result:
            print(f"Error: {result['error']}")
            return None
        else:
            # Extract relevant information from the response
            conversation_id = result.get('conversationID')
            host = result.get('host')
            spoken_text = result.get('result')

            return conversation_id, host, spoken_text
    else:
        print(f"Error: HTTP status code {response.status_code}")
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
    elif "open" in query.lower():
        if "chrome" in query.lower():
            response_text = f"Opening Google Chrome...."
            os.startfile(
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            )
        elif "vs code" in query.lower():
            response_text = f"Opening VS code...."
            os.startfile((
                r'C:\Users\Nandan PC\AppData\Local\Programs\Microsoft VS Code\Code.exe'
            ))
        elif "youtube" in query.lower():
            ind = query.lower().split().index("youtube")
            search = query.split()[ind + 1:]
            search_query = "+".join(search)
            webbrowser.open("https://www.youtube.com/results?search_query=" + search_query)
            response_text = f"Opening {search_query} on Youtube"

        elif "search" in query.lower():
            ind = query.lower().split().index("search")
            search = query.split()[ind +1:]
            webbrowser.open("https://google.com/search?q="+"+".join(search))
            response_text = f"Searching " +str(search) + "on google"
        elif "google" in query.lower():
            response_text = f"Opening Google..."
            webbrowser.open("https://google.com")

        else:
            response_text = f"Application Not found !"
    elif "note" in query or "write a note" in query.lower():
        response_text= "What would you like me to write down?"
        response(response_text)
        note_text = rec_audio()
        note(note_text)
        response_text = "I have a made a note of that"
    elif "joke" in query or "jokes" in query:
        joke = pyjokes.get_joke()
        response_text = joke

    elif "wikipedia" in query:
        if "who is" in query:
            person = wiki_person(query)
            wiki_summary = wikipedia.summary(person, sentences=2)
            response_text = f"{person} is {wiki_summary}"
        else:
            response_text = "I'm sorry, I didn't understand that Wikipedia query."
    elif "where is" in query.lower():
        ind = query.lower().split().index("is")
        location = query.split()[ind+1:]
        url = "https://www.google.com/maps/place/"+"".join(location)
        response_text="This is where" + str(location) + "is"
        # response(response_text)
        webbrowser.open(url)
    elif "weather" in query:
        key = "19b99ad811adc54b48634240f3503076"
        weather_url = "https://api.openweathermap.org/data/2.5/weather?"
        ind = query.split().index("in")
        location = query.split()[ind + 1:]
        location = "".join(location)
        url = weather_url + "q=" + location + "&appid=" + key + "&units=metric"
        js = requests.get(url).json()
        if js["cod"] != "404":
            weather_main = js["weather"][0]["main"]
            temperature = js["main"]["temp"]
            humidity = js["main"]["humidity"]
            description = js["weather"][0]["description"]
            cloudiness = js["clouds"]["all"]
            wind_speed = js["wind"]["speed"]

            weather_response = f"The weather in {location} is {description}."
            weather_response += f"\nTemperature: {temperature}°C | Humidity: {humidity}%"
            weather_response += f"\nCloudiness: {cloudiness}% | Wind Speed: {wind_speed} m/s"

            response_text = weather_response
        else:
            response_text = "City not found"
    elif "news" in query:
        api_key = "171b0706669c49deab91dce3c848a65b"
        url = ('https://newsapi.org/v2/top-headlines?'
               'country=in&'
               f'apiKey={api_key}')
        try:
            response_data = requests.get(url)
            response_data.raise_for_status()  # Raise an HTTPError for bad responses

            news = response_data.json()

            if 'articles' in news:
                counter = 0  # Counter for tracking the number of news articles printed

                for new in news["articles"]:
                    title = str(new.get("title", ""))
                    description = str(new.get("description", ""))

                    print(title, "\n")
                    response(title)

                    print(description, "\n")
                    response(description)

                    counter += 1
                    if counter == 5:
                        break  # Break out of the loop after printing the first 5 articles
            else:
                print("Unexpected news API response format.")
                response_text = "Sorry, I couldn't fetch the latest news at the moment."
        except Exception as e:
            print(f"An error occurred while fetching news: {e}")
            response_text = "Sorry, I couldn't fetch the latest news at the moment."
    elif "calculate" in query.lower():
        app_id="3J4KK6-E4PQG4V7V2"
        client = wolframalpha.Client(app_id)
        ind = query.lower().split().index("calculate")
        text = query.split()[ind +1:]
        res = client.query(" ".join(text))
        answer = next(res.results).text
        response_text = "The Answer is "+answer
        response(response_text)
    elif "what is " in query.lower() or "who is" in query.lower():
        app_id = "3J4KK6-E4PQG4V7V2"
        client = wolframalpha.Client(app_id)
        ind = query.lower().split().index("is")
        text = query.split()[ind + 1:]
        res = client.query(" ".join(text))
        answer = next(res.results).text
        response_text = "The Answer is " + answer
    elif "tell me" in query.lower() or "explain" in query.lower():
        response("Ask the Query")
        query1 = rec_audio()
        conversation_id, host, response_text1 = make_wolfram_alpha_query(query1)
        # Print the result of the single query
        response_text = f"Response 1: {response_text1}"

    elif any(word in query.lower() for word in ["thank you", "thanks", "thank", "bye"]):
        response_text = "Have a great day ...See you buddy!"
        response(response_text)
        exit()
    else:
        response_text = "I'm sorry, I didn't understand that query."

    return response_text


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
