from cgitb import reset
from datetime import datetime
from email.mime import audio
from lib2to3.pgen2 import driver
from msilib.schema import Error
import pprint
from re import M
from this import d
from tkinter import Y, Place
from turtle import distance
from unittest import result
import pyttsx3
import pyaudio
import speech_recognition as sr
import smtplib
from decouple import config
import wikipedia
import subprocess as sp
import requests
import os
import pywhatkit as kit
import webbrowser
import wolframalpha
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')

voices= engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print("  ")
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.now().hour)
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME} sir.")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME} sir.")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

def takeCommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        command.pause_threshold = 1
        audio = command.listen(source)

        try:
            print("Recognizing.....")
            query = command.recognize_google(audio, language='en-in')
            print(f"You said : {query}")
        
        except Exception as Error:
            print("Say that again please...")
            return "None"

        return query.lower()

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_cmd():
    os.system('Start cmd')

paths = {
    'notepad': "C:\Windows\System32\notepad.exe",
    'terminal': "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    'calculator': "C:\Windows\System32\calc.exe"
}

def open_notepad():
    os.startfile(paths['notepad'])

def open_terminal():
    os.startfile(paths["terminal"])

def open_calc():
    os.startfile(paths["calculator"])

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def get_random_jokes():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

def googleMaps(place):
    Url_Place = "https://www.google.com/maps/place/" + str(place)
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_lat_long = location.latitude, location.longitude
    location = location.raw['address']
    target = {'city' : location.get('city', ''), 'state' : location.get('state', ''), 'country' : location.get('country', '')}
    curr_location = geocoder.ip('me')
    curr_lat_long = curr_location.latlng
    distance = str(great_circle(curr_lat_long, target_lat_long))
    distance = str(distance.split(' ', 1)[0])
    distance = round(float(distance), 2)
    webbrowser.open(url=Url_Place)

    speak(target)
    print(f"{place} is {distance} kilometer away from your location . ")
    speak(f"Sir, {place} is {distance} kilometer away from your location . ")

def ask_wolfram(self, question):
        client = wolframalpha.Client(self.key)
        res = client.query(question)
        if len(res.pods) > 0:
            pod = res.pods[1]
            if pod.text:
                texts = pod.text
            else:
                raise Error('Wolfram API failed.')
            # to skip ascii character in case of error
            texts = texts.encode('ascii', 'ignore')
            return texts
        else:
            raise Error('Wolfram API failed.') 

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        if 'how are you' in query:
            speak("I'm fine sir, Thank you so much for asking.")
            speak(f" How are you, {USERNAME} Sir ?")

        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine.")

        elif "time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")

        elif "date" in query:
            strDate = datetime.now().strftime("%d/%m/%Y")
            print(strDate)
            speak(f"Sir, today's date is {strDate}")

        elif 'open notepad' in query:
            open_notepad()
        
        elif 'open terminal' in query:
            open_terminal()

        elif 'open calculator' in query:
            open_calc()

        elif 'open camera' in query:
            open_camera()

        elif 'cmd' in query:
            open_cmd()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = takeCommand().lower()
            results = search_on_wikipedia(search_query)
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)
            speak(f"According to Wikipedia, {results}")

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = takeCommand().lower()
            play_on_youtube(video)

        elif 'maps' in query or 'map' in query:
              speak("Opening Google Maps")
              speak("Sir, please enter place you want to find on map.")
              googleMaps(input("Enter the location(place): "));

        elif 'search on google' in query or 'google search' in query or 'search' in query:
            speak('What do you want to search on Google, sir?')
            query = takeCommand().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = takeCommand().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_jokes()
            speak("For your convenience, I am printing it on the screen sir.")
            pprint.pprint(joke)
            speak(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak("For your convenience, I am printing it on the screen sir.")
            pprint.pprint(advice)
            speak(advice)

        elif "open wolfram alpha" in query:   
            app_id = "5Y88XT-PHJ56EA2J8"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif "open stack overflow" in query:
            webbrowser.open("https://stackoverflow.com")

        elif "close" in query or "bye" in query or "exit" in query:
            speak("Thanks so much sir for giving me your time")
            exit()
