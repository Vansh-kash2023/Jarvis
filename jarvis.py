import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!!") 
    else:
        speak("Good Evening!!")
    speak("I am Jarvis sir. Please tell me how may I Help you?")


def takecommand():
    # It takes microphone input from the user and return string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)
    
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print("User said: ",query,end='\n')
    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        return "None"
    return query

if __name__=="__main__":
    wishme()
    while True:
        query=takecommand().lower()
        # Logic for executing tasks based on query.
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query=query.replace('wikipedia','')
            results=wikipedia.summary(query,sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'play music' in query:
            music_dir='C:\\Users\\vansh\\Music'
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))
        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak("sir the time is "+strTime)
        elif 'open code' in query:
            code_path='"C:\\Users\\vansh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"'
            os.startfile(code_path)
        elif 'open spotify' in query:
            code_path1='C:\\Users\\vansh\\AppData\\Local\\Microsoft\\WindowsApps\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0\\Spotify.exe'
            os.startfile(code_path1)