import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib  
import googlesearch
import json  
import requests  
import subprocess  
from email.message import EmailMessage  
import time
import winsound  # For playing alarm sound (Windows-specific)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!!")
    else:
        speak("Good Evening!!")
    speak("I am Jarvis sir. Please tell me how may I help you?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:", query)
    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        return "None"
    return query

def search_web(query):
    search_results = googlesearch.search(query, num_results=5, lang="en")
    if search_results:
        speak("Here are the top search results:")
        for result in search_results:
            webbrowser.open(result)
    else:
        speak("No results found for your query.")

def send_email(receiver_email, subject, content):
    try:
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = "your_email@gmail.com"  # Update with your email
        msg['To'] = receiver_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")  # Update with your email and password
        server.send_message(msg)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

def get_weather(city):
    api_key = "your_openweathermap_api_key"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather in {city} is {weather_info}. The temperature is {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather data.")

def set_alarm(hour, minute):
    current_time = datetime.datetime.now()
    alarm_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
    time_diff = (alarm_time - current_time).total_seconds()

    if time_diff <= 0:
        speak("The specified time has already passed. Please set a future time.")
    else:
        speak(f"Alarm set for {hour}:{minute} AM.")
        time.sleep(time_diff)
        speak("Time to wake up!")
        winsound.Beep(1000, 1000)  # Play a sound (adjust frequency and duration)


if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)
        elif 'search the web for' in query:
            search_query = query.replace('search the web for', '')
            search_web(search_query)
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open stack overflow' in query:
            webbrowser.open("https://stackoverflow.com")
        elif 'play music' in query:
            music_dir = 'C:\\Users\\vansh\\Music'  # Adjust this path
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak("Sir, the time is " + strTime)
        elif 'open code' in query:
            code_path = '"C:\\Users\\vansh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"'  # Adjust this path
            subprocess.Popen(code_path, shell=True)
        elif 'send email' in query:
            try:
                speak("To whom should I send the email?")
                receiver_email = takecommand().lower()
                speak("What should be the subject of the email?")
                subject = takecommand().lower()
                speak("What should be the content of the email?")
                content = takecommand()
                send_email(receiver_email, subject, content)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")
        elif 'check the weather in' in query:
            city = query.split("in")[1].strip()
            get_weather(city)
        elif 'set alarm for' in query:
            # Extract the hour and minute from the query and call set_alarm
            set_alarm(8, 30)  # Set an example alarm for 8:30 AM
