# speech.py
# speechrecognition, pyaudio, brew install portaudio
import speech_recognition as sr
import os
import requests

class Speech(object):
    def __init__(self, launch_phrase="okay jarvis", debugger_enabled=False):
        print("Launch phrase = " + launch_phrase)
        self.launch_phrase = launch_phrase
        self.debugger_enabled = debugger_enabled
        self.debugger_microphone(enable=False)
    
    def google_speech_recognition(self, recognizer, audio):
        speech = None
        try:
            speech = recognizer.recognize_google(audio)
            print("You said: " + speech.lower())
        except sr.UnknownValueError:
            print("Speech recognition didn't understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return speech

    def listen_for_audio(self, awake=False):
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            #r.adjust_for_ambient_noise(source)
            if (awake):
                self.debugger_microphone(enable=True)
            print("Listening...")
            audio = r.listen(source)
        self.debugger_microphone(enable=False)
        print("Found audio.")
        return r, audio

    def is_call_to_action(self, recognizer, audio):
        speech = self.google_speech_recognition(recognizer, audio)
        if speech is not None and self.launch_phrase in speech.lower():
            return True
        return False

    def synthesize_text(self, text):
        print("Saying: " + text)
        command = 'say -v Daniel "' + text + '"'
        os.system(command)

    def debugger_microphone(self, enable=True):
        if self.debugger_enabled:
            try:
                r = requests.get("http://localhost:8080/microphone?enabled=%s" % str(enable))
                if r.status_code != 200:
                    print("Used wrong endpoint for microphone debugging")
            except Exception as e:
                print(e)