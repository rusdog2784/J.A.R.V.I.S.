import datetime as dt
import dateutil.parser
import traceback
import json
import requests
import os
import time
import random
import csv
import os.path
from speech import Speech
from nlg import NLG
from actions import Actions

class Jarvis(object):
    my_name = "Scott"
    launch_phrase = "jarvis"
    use_launch_phrase = True
    debugger_enabled = True
    location = "hoboken"
    unknown_fieldnames = ['Command', 'Action']
    awake = False

    def __init__(self):
        self.nlg = NLG(user_name=self.my_name)
        self.speech = Speech(launch_phrase=self.launch_phrase, debugger_enabled=self.debugger_enabled)
        self.actions = Actions(self.location)
        if os.path.isfile('unknown_commands.csv') == False:
            with open('unknown_commands.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.unknown_fieldnames)
                writer.writeheader()

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        """
        while True:
            requests.get('http://localhost:8080/clear')
            if self.use_launch_phrase:
                recognizer, audio = self.speech.listen_for_audio(self.awake)
                text = self.speech.google_speech_recognition(recognizer, audio)
                if text is not None and self.launch_phrase in text.lower():
                    self.awake = True
                    #self.__acknowledge_action()
                    self.decide_action(text)
                else:
                    if self.awake == True:
                        self.decide_action(text)
                    else:
                        self.speech.debugger_microphone(enable=False)

    def decide_action(self, text):
        """
        Reursively decides an action based on the intent.
        """
        acknowledgement = False
        if text is not None and self.awake == True:
            text = text.lower()
            if "hide" in text:
                if "time" in text:
                    self.__hide_action("time")
                if "weather" in text:
                    self.__hide_action("weather")
                if "calendar" in text:
                    self.__hide_action("calendar")
                if "commute" in text:
                    self.__hide_action("commute")
                if "all" in text:
                    self.__hide_action("all")
                return
            if "show" in text:
                if "time" in text:
                    self.__show_action("time")
                if "weather" in text:
                    self.__show_action("weather")
                if "calendar" in text:
                    self.__show_action("calendar")
                if "commute" in text:
                    self.__show_action("commute")
                if "all" in text:
                    self.__show_action("all")
                return
            if "hello" in text or "good morning" in text or "good afternoon" in text or "good evening" in text or "hey" in text or "hi" in text:
                if "jarvis" in text:
                    self.__acknowledge_action()
                    acknowledgement = True
                else:
                    self.__greet_action()
                    return
            if "how are you" in text or "how's it going" in text or "what's going on" in text:
                self.__personal_status()
                return
            if "weather" in text:
                if "today" in text:
                    self.__weather_action("today")
                elif "tomorrow" in text:
                    self.__weather_action("tomorrow")
                else:
                    self.__weather_action("today")
                return
            if "time" in text:
                if "date" in text:
                    self.__time_action(withDate=True)
                    return
                else:
                    self.__time_action(withDate=False)
                    return
            if "date" in text and "time" not in text:
                self.__date_action()
                return
            if "play" in text and "music" in text:
                if "some" in text:
                    self.__play_spotify_action()
                return
            if "goodbye" in text or "thank you" in text or "that's all" in text or "that is all" in text or "that's it" in text or "thanks" in text:
                self.__done_action()
                return
            if text == "":
                return
            if acknowledgement == True:
                return
            self.__unknown_command_action(text)

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)
        
    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())

    def __greet_action(self):
        self.__text_action(self.nlg.greet())

    def __personal_status(self):
        self.__text_action(self.nlg.personal_status())

    def __weather_action(self, tod):
        if tod is not None:
            weathertext = self.actions.getWeather(tod)
            if weathertext is not None:
                city = weathertext['city'].encode('ascii', 'ignore')
                date = weathertext['date']
                condition = weathertext['condition'].encode('ascii', 'ignore')
                low = weathertext['low'].encode('ascii', 'ignore')
                high = weathertext['high'].encode('ascii', 'ignore')
                response = "The weather in " + city + " " + date + " is going to be " + condition + " with temperatures ranging from " + str(low) + " to " + str(high) + " degrees"
                self.__text_action(response)
            else:
                response = "Sorry, I couldn't gather weather text for some reason"
                self.__text_action(response)

    def __time_action(self, withDate=False):
        if withDate:
            time = self.actions.getTime()
            date = self.actions.getDate()
            response = "It is " + str(time) + " on " + str(date)
            self.__text_action(response)
        else:
            time = self.actions.getTime()
            response = "It is " + str(time)
            self.__text_action(response)

    def __date_action(self):
        date = self.actions.getDate()
        response = "It is " + str(date)
        self.__text_action(response)

    def __done_action(self):
        self.speech.debugger_microphone(enable=False)
        self.__text_action("Have a great day")
        self.awake = False

    def __unknown_command_action(self, text):
        self.__text_action("Command unknown. Save command?")
        commandToSave = text
        recognizer, audio = self.speech.listen_for_audio(self.awake)
        text = self.speech.google_speech_recognition(recognizer, audio)
        if text is not None:
            if "yes" in text:
                self.__text_action("Ok, what is its action?")
                recognizer, audio = self.speech.listen_for_audio(self.awake)
                actionToSave = self.speech.google_speech_recognition(recognizer, audio)
                if actionToSave is not None:
                    with open('unknown_commands.csv', 'a') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=self.unknown_fieldnames)
                        writer.writerow({'Command':commandToSave, 'Action':actionToSave})
                    self.__text_action("Command recorded.")

    def __hide_action(self, widget):
        if (widget == "all"):
            requests.get("http://localhost:8080/hide?widget=%s" % "time")
            requests.get("http://localhost:8080/hide?widget=%s" % "weather")
            requests.get("http://localhost:8080/hide?widget=%s" % "calendar")
            requests.get("http://localhost:8080/hide?widget=%s" % "commute")
        else:
            requests.get("http://localhost:8080/hide?widget=%s" % widget)
        self.__text_action(self.nlg.confirmation())

    def __show_action(self, widget):
        if (widget == "all"):
            requests.get("http://localhost:8080/show?widget=%s" % "time")
            requests.get("http://localhost:8080/show?widget=%s" % "weather")
            requests.get("http://localhost:8080/show?widget=%s" % "calendar")
            requests.get("http://localhost:8080/show?widget=%s" % "commute")
        else:
            requests.get("http://localhost:8080/show?widget=%s" % widget)
        self.__text_action(self.nlg.confirmation())

    def __play_spotify_action(self):
        self.__text_action("Here you go")
        self.actions.playRandomSpotify()
        self.__done_action()

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.start()