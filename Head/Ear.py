import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore,Style,init

init(autoreset = True) # Automatically reset Style After Each Print

def print_loop():
    while True:
        print(Fore.LIGHTGREEN_EX + "I am Listning... ", end="", flush=True)
        print(Style.RESET_ALL,end="",flush=True)
        print("",end="",flush=True)

def trans_hindi_to_english(txt):
    english_txt = translate(txt, to_language="en-in")
    return english_txt

def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = False
    recognizer.dynamic_energy_adjustment_damping = 0.03 # Adjust the damping factor for faster response
    recognizer.dynamic_energy_ratio = 1.9 # Adjust the ratio for more sensitivity
    recognizer.pause_threshold = 0.2
    recognizer.operation_timeout = None
    recognizer.non_speaking_duration = 0.1

    with sr.Microphone() as source: #here we are using mic as source to listen what we say
        recognizer.adjust_for_ambient_noise(source) #what will speak in mic is not affected by the surrounding noise
        while True:
            print(Fore.LIGHTGREEN_EX + "I am Listning... ", end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=None) #here source is mic what we say and timeout is how much time it will wait for us to speak

                print("\r" + Fore.LIGHTYELLOW_EX + "Got it , Recognizing... ", end="", flush=True)
                recognizer_txt = recognizer.recognize_google(audio).lower()
                if recognizer_txt:
                    translated_txt = trans_hindi_to_english(recognizer_txt)
                    print("\r" + Fore.MAGENTA + "you Said: " + translated_txt)
                    return translated_txt
                else:
                    return " "
            except sr.UnknownValueError:
                return " "
            finally:
                print("\r", end='', flush=True)

    # Clear screen and start status print threads (moved outside the with-block)
    os.system("cls" if os.name == "nt" else "clear")
    # threading part
    listen_thread = threading.Thread(target=print_loop)
    print_thread = threading.Thread(target=print_loop)
    listen_thread.start()
    print_thread.start()
    listen_thread.join()
    print_thread.join()

while True:
    listen()
             
