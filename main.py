import speech_recognition as sr
import datetime as dt
from gtts import gTTS
import os, time, random
from actions import Actions

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

def getRandomAdjective():
    adjs = ["swell", "great", "okay", "fantastic", "alright"]
    index = random.randint(0, len(adjs) - 1)
    adj = adjs[index]
    return adj

def jarvis(data):
    if "hello" in data or "good morning" in data or "good afternoon" in data or "good evening" in data:
        tod = getTimeOfDay()
        if "how are you" in data:
            adjective = getRandomAdjective()
            text = "Good " + tod + " sir, I'm doing " + adjective + ", what can I do for you"
            speak(text)
        else:
            text = "Good " + tod + " sir, what can I do for you"
            speak(text)
    if "how are you" in data:
        adjective = getRandomAdjective()
        text = "I'm doing " + adjective + ", what can I do for you"
        speak(text)
    if "weather" in data:
        if "today" in data:
            weatherData = actions.getWeather("today")
        elif "tomorrow" in data:
            weatherData = actions.getWeather("tomorrow")
        else:
            weatherData = actions.getWeather(None)
        if weatherData != None:
            city = weatherData['city'].encode('ascii', 'ignore')
            date = weatherData['date']
            condition = weatherData['condition'].encode('ascii', 'ignore')
            low = weatherData['low'].encode('ascii', 'ignore')
            high = weatherData['high'].encode('ascii', 'ignore')
            print city
            print date
            print condition
            print low
            print high
            text = "the weather in " + city + " " + date + " is going to be " + condition + " with temperatures ranging from " + str(low) + " to " + str(high)
            speak(text)
        else:
            text = "Sorry, I couldn't gather weather data for some reason"
            speak(text)
    if "goodbye" in data:
        speak("Goodbye")
        exit()


actions = Actions("hoboken")
time.sleep(2)
while 1:
    data = recordAudio()
    jarvis(data)