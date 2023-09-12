# Description

This is a python code interpreter that uses speech reconition to take in a command parse it via an llm namely azure gpt-3.5 in this case and the llm will return a python code string that will be executed by the iterpreter. it just a prototype to show off some ideas and to get some feedback.

## inspired by the following

inspired by but in no way coppied from [Open-Interpreter](https://github.com/KillianLucas/open-interpreter) this project is a prototype of some ideas discussed with Killian and is an attempt to make some cool interactions with the command line and python. and very little overhead.

[KillianLucas](https://github.com/KillianLucas) and his [Open-Interpreter](https://github.com/KillianLucas/open-interpreter)
and [DarkAcorn](https://github.com/darkacorn) for moral support 😊

## Installation

install python 3.8.5 or higher
install all the dependencies
if you run the script and it says something is missing install it
also you need to get an to set the environment variables AZURE_API_KEY to your azure api key, AZURE_API_BASE to your azure endpoint, AZURE_API_VERSION to your azure api version,

### lots of dependencies

```bash
pip install SpeechRecognition
pip install openai
pip install pygame
pip install gtts
pip install mutagen
pip install keyboard
pip install pyaudio
```
```could be more let me know if you find any```

might make a requirements.txt file later

## Usage

python cmd-llm.py

press s to start listening
press q to quit