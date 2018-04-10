import speech_recognition as sr
import datetime as dt
from gtts import gTTS
import os, time

def speak(audioString):
    print("Saying: " + audioString)
    '''
    tts = gTTS(text=audioString, lang='us')
    tts.save("audio.mp3")
    os.system("mp321 audio.mp3")
    '''
    os.system("say -v Oliver " + audioString)

def recordAudio():
    r = sr.Recognizer()    
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    if (audio == None):
        print("no audio")
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech API is confused.")
    except sr.RequestError as e:
        data = "Request to Google Speech API failed, request error: ", e

    return data

def getTimeOfDay():
    hour = dt.datetime.today().hour
    if (0 <= hour < 12):
        return "morning"
    elif (12 <= hour < 18):
        return "afternoon"
    elif (18 <= hour < 24):
        return "evening"
    return ""

def jarvis(data):
    if "hello" in data or "good morning" in data or "good afternoon" in data or "good evening" in data:
        tod = getTimeOfDay()
        speak("Good " + tod + " how can I help you")
    if "how are you" in data:
        speak("I'm doing just swell, considering I'm a program")
    if "goodbye" in data:
        speak("Goodbye")
        exit()

if __name__ == "__main__":
    time.sleep(2)
    while 1:
        data = recordAudio()
        jarvis(data)