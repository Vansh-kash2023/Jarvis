import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib  
import json  
import requests  
import subprocess  
from email.message import EmailMessage  
import time
import winsound  
import pyautogui
import re
import geocoder

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
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print("User said:", query)
            return query.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, I couldn't connect to the recognition service.")
            return ""
        except Exception:
            return ""

def open_command(query):
    apps = {
        "code": "C:\\Users\\vansh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe"
    }
    match = re.search(r'open (.+)', query)
    if match:
        item = match.group(1)
        if item in apps:
            subprocess.Popen(apps[item], shell=True)
        else:
            webbrowser.open(f"https://www.{item}.com")

def get_weather():
    g = geocoder.ip('me')
    city = g.city
    if city:
        url = f"https://www.google.com/search?q=weather+in+{city}"
        webbrowser.open(url)
        speak(f"Here is the weather update for {city}.")
    else:
        speak("Sorry, I couldn't detect your location.")

def set_alarm(query):
    match = re.search(r'set alarm for (\d+) hours (\d+) minutes', query)
    if match:
        hours, minutes = map(int, match.groups())
        alarm_time = datetime.datetime.now() + datetime.timedelta(hours=hours, minutes=minutes)
        time_diff = (alarm_time - datetime.datetime.now()).total_seconds()
        speak(f"Alarm set for {hours} hours and {minutes} minutes from now.")
        time.sleep(time_diff)
        speak("Time to wake up!")
        winsound.Beep(1000, 1000)

def play_music():
    webbrowser.open("https://music.youtube.com")
    speak("Opening YouTube Music")


def main():
    wishme()
    while True:
        query = takecommand()
        if not query:
            continue
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            results = wikipedia.summary(query.replace('wikipedia', ''), sentences=2)
            speak(results)
        elif 'open' in query:
            open_command(query)
        elif 'play music' in query:
            play_music()
        elif 'the time' in query:
            speak(datetime.datetime.now().strftime("%H:%M:%S"))
        elif 'check the weather' in query:
            get_weather()
        elif 'set alarm for' in query:
            set_alarm(query)
        elif 'exit' in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
