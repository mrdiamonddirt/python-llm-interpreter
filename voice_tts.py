import time
import threading
import speech_recognition as SR
import os
import pyttsx3


class SpeechAssistant:
    def __init__(self, wakeup_word="interpreter"):
        self.wakeup_word = wakeup_word
        self.speech_recognizer = SR.Recognizer()
        # use for windows use sapi5, nsss for mac and espeak for linux (sapi5-default)
        self.engine = pyttsx3.init()
        # self.engine.setProperty("rate", 150)
        # self.engine.setProperty("volume", 1.0)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id) # can get the voice array index from list_all_voices()

    def tts_and_play_audio(self, text):
        # stop if it is already speaking
        if self.engine._inLoop:
            print("inloop")
            self.engine.endLoop()
            self.engine.stop()
        self.engine.say(text)
        self.engine.runAndWait()

    def start_speech_recognition(self):
        while True:
            print("Listening for wakeup word...")
            with SR.Microphone() as mic:
                try:
                    self.speech_recognizer.adjust_for_ambient_noise(
                        mic, duration=0.4)
                    audio = self.speech_recognizer.listen(mic)

                    result = self.speech_recognizer.recognize_whisper(
                        audio, "base")
                    text = result
                    if self.wakeup_word in text:
                        print("Wakeup word", self.wakeup_word, "detected!")
                        print("You said:", text)
                        return text
                except SR.UnknownValueError:
                    pass
                except Exception as e:
                    print("Error:", str(e))
                finally:
                    pass
    
    def list_all_voices(self):
        voices = self.engine.getProperty("voices")
        for voice in voices:
            print(voice)


if __name__ == "__main__":
    assistant = SpeechAssistant(wakeup_word="interpreter")
    # assistant.list_all_voices()
    assistant.start_speech_recognition()
    assistant.tts_and_play_audio("Hello, my name is interpreter. I am a computer with the ability to run any code I want when I am given a prompt and return a response with a plan of what code I want to run. I will start my response with a plan. The commands I provide should be in a single code block encapsulated in triple quotes python and triple quotes and should be a valid Python program.")
