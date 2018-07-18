import speech_recognition as sr
import datetime as dt
from gtts import gTTS
import os, time, random, csv, os.path
from actions import Actions

awake = False
commandToSave = ""
actionToSave = ""
unknown_fieldnames = ['Command', 'Action']

def speak(audioString):
    print("Saying: " + audioString)
    '''
    tts = gTTS(text=audioString, lang='us')
    tts.save("audio.mp3")
    os.system("mp321 audio.mp3")
    '''
    #command = "say '" + audioString + "'"
    command = 'say "' + audioString + '"'
    os.system(command)

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
    adjs = ["swell", "great", "okay", "fantastic", "alright", "excellent"]
    index = random.randint(0, len(adjs) - 1)
    adj = adjs[index]
    return adj

def jarvis(data):
    data = data.lower()
    global awake
    if "hello" in data or "good morning" in data or "good afternoon" in data or "good evening" in data or "hey" in data or "hi" in data:
        tod = getTimeOfDay()
        if "how are you" in data:
            adjective = getRandomAdjective()
            text = "Good " + tod + " sir, I'm doing " + adjective + ", what can I do for you"
            speak(str(text))
            return
        else:
            text = "Good " + tod + " sir, what can I do for you"
            speak(str(text))
            return
    if "how are you" in data:
        adjective = getRandomAdjective()
        text = "I'm doing " + adjective + ", what can I help with"
        speak(str(text))
        return
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
            text = "the weather in " + city + " " + date + " is going to be " + condition + " with temperatures ranging from " + str(low) + " to " + str(high) + " degrees"
            speak(text)
            return
        else:
            text = "Sorry, I couldn't gather weather data for some reason"
            speak(text)
            return
    if "time" in data:
        if "date" in data:
            time = actions.getTime()
            date = actions.getDate()
            text = "it is " + str(time) + " on " + str(date)
            speak(text)
            return
        else:
            time = actions.getTime()
            text = "it is " + str(time)
            speak(text)
            return
    if "date" in data and "time" not in data:
        date = actions.getDate()
        text = "it is " + str(date)
        speak(text)
        return
    if "goodbye" in data:
        speak("Goodbye")
        awake = False
        #exit()
        return
    if data == "":
        return
    speak("Command unknown. Save command?")
    commandToSave = data
    data = recordAudio()
    if "yes" in data:
        speak("Ok, what is its action?")
        actionToSave = recordAudio()
        with open('unknown_commands.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=unknown_fieldnames)
            writer.writerow({'Command':commandToSave, 'Action':actionToSave})
        speak("Command recorded.")

actions = Actions("hoboken")
if os.path.isfile('unknown_commands.csv') == False:
    with open('unknown_commands.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=unknown_fieldnames)
        writer.writeheader()
time.sleep(2)
while 1:
    data = recordAudio()
    if "goodbye" in data:
        jarvis(data)
    if awake == True:
        jarvis(data)
    else:
        if "Jarvis" in data:
            awake = True
            jarvis(data)
    print