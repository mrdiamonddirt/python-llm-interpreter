import pyttsx3
# set driver name based on platform
# engine = pyttsx3.init(driver_name = 'sapi5') in windows
# driver_name = 'nsss' in mac
# driver_name = 'espeak' in linux
engine = pyttsx3.init()

# get possible voices
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice:", repr(voice))

engine.say("Hello World!")
engine.runAndWait()