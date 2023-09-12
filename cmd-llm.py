import speech_recognition as SR
import os
import openai
import datetime
import time
import pygame
from gtts import gTTS
from mutagen.mp3 import MP3
import threading  # Import the threading module
import keyboard

# Set up OpenAI API
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_API_BASE")
openai.api_version = os.getenv("AZURE_API_VERSION")
openai.api_key = os.getenv("AZURE_API_KEY")
output_file = "output/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".py"

# Function to play audio

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    audio = MP3(file_path)
    time.sleep(audio.info.length)
    pygame.mixer.music.stop()
    pygame.quit()

# Function for TTS and audio playback

def tts_and_play_audio(text):
    # Text-to-Speech (TTS) for the plan
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False, tld='com.au')
    speech.save("speech.mp3")

    # Play the TTS audio
    play_audio("speech.mp3")
    os.remove("speech.mp3")
    # print("Done with TTS and audio playback")

# Function for speech recognition


def SpeechRecognition():
    print("Press the 'S' key to start listening or 'Q' to quit.")
    SpeechRecognizer = SR.Recognizer()
    with SR.Microphone() as mic:
        while True:
            if keyboard.is_pressed('s'):  # Press 'S' to start listening
                print("Listening...")
                SpeechRecognizer.adjust_for_ambient_noise(mic, duration=0.4)
                try:
                    Text = SpeechRecognizer.recognize_google(
                        SpeechRecognizer.listen(mic), language="en-US")
                    Text = str(Text).lower()
                    print("You said:", Text)
                    return Text
                except SR.exceptions.UnknownValueError:
                    print("Could not understand audio.")
                except Exception as e:
                    print("Error:", str(e))
            elif keyboard.is_pressed('q'):  # Press 'Q' to quit
                break


# Input message
initialmachineprompt = "What would you like me to do, sir: "

# tts the initial machine prompt
tts_thread = threading.Thread(
    target=tts_and_play_audio, args=(initialmachineprompt,))
tts_thread.start()  # Start the TTS thread

# Get input from speech recognition

message = SpeechRecognition()

# Create a response using OpenAI Chat API
response = openai.ChatCompletion.create(
    engine="gpt-35-turbo",
    messages=[
        {"role": "user", "content": "You are a computer with the ability to run any code you want when you are given a prompt and return a response with a plan of what code you want to run. You should start your response with a plan, The commands you provide should be in a single code block encapsulated in '''python and ''' for Python and should be valid Python programs."},
        {"role": "assistant", "content": "I am a computer with the ability to run any code I want when I am given a prompt and return a response with a plan of what code I want to run I Will start my response with a plan. The commands I provide should be in a single code block encapulated in '''python and ''' and should be a valid Python program."},
        {"role": "user", "content": message}
    ],
    temperature=0.001,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
)

if response:
    print(response.choices[0].message.content)

    # Extract plan from the response
    plan = response.choices[0].message.content.split("```python")[0]
    plan = plan.replace("'", "")
    plan = plan.replace('`', "")
    print("plan:", plan)

    # Create a thread for TTS and audio playback
    tts_thread = threading.Thread(target=tts_and_play_audio, args=(plan,))
    tts_thread.start()  # Start the TTS thread

    # Check if there's Python code in the response
    if "```python" in response.choices[0].message.content:
        python_code = response.choices[0].message.content.split(
            "```python")[1].split("```")[0].strip()
        print("Python code:", python_code)

        # Run and possibly save the Python code
        if python_code:
            save_python_code = input(
                "Do you want to save the Python code? (y/n): ")
            if save_python_code.lower() == "y":
                filename = input("Enter a filename: ")
                if not filename.endswith(".py"):
                    filename += ".py"
                    if os.path.exists(filename):
                        print("File already exists")
                        exit()
                    else:
                        filename = output_file
                with open(filename, "w") as f:
                    f.write(python_code)
                print("Python code saved as", filename)

            run_python_code = input(
                "Do you want to run the Python code? (y/n): ")
            if run_python_code.lower() == "y":
                print("Running Python code:")
                try:
                    exec(python_code)
                except Exception as e:
                    print("Error:", str(e))
            else:
                print("Not running Python code")
        else:
            print("No Python code found in the response")

# if we are at the end of the program, close the TTS thread
if tts_thread.is_alive():
    tts_thread.join()
    
