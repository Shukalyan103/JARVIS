import os
import sys
import speech_recognition as sr
from colorama import Fore, Style, init

init(autoreset=True)

# Shared recognizer instance to preserve ambient noise calibration
_recognizer = sr.Recognizer()
_recognizer.dynamic_energy_threshold = True
_recognizer.pause_threshold = 0.8
_recognizer.operation_timeout = None
_calibrated = False


def calibrate_mic(source):
    global _calibrated
    if not _calibrated:
        print(Fore.CYAN + "🎙️ Calibrating microphone for ambient noise...", end="", flush=True)
        _recognizer.adjust_for_ambient_noise(source, duration=0.6)
        _calibrated = True
        print(Fore.GREEN + " Ready!\n")


def listen(timeout=None, phrase_time_limit=10):
    """
    Listens to the microphone and returns recognized speech in lowercase.
    Returns empty string '' if speech could not be recognized or timed out.
    """
    try:
        with sr.Microphone() as source:
            calibrate_mic(source)
            print(Fore.LIGHTGREEN_EX + "🎙️ [JARVIS]: Listening for voice command...", end="", flush=True)

            audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("\r" + Fore.LIGHTYELLOW_EX + "⚡ [JARVIS]: Processing speech...             ", end="", flush=True)

            try:
                recognized_text = _recognizer.recognize_google(audio).lower().strip()
                if recognized_text:
                    print("\r" + Fore.MAGENTA + f"🗣️ [You Said]: \"{recognized_text}\"          ")
                    return recognized_text
                else:
                    print("\r" + Fore.LIGHTBLACK_EX + "   (No speech detected)                      ")
                    return ""
            except sr.UnknownValueError:
                print("\r" + Fore.LIGHTBLACK_EX + "   (Could not understand audio)              ")
                return ""
            except sr.RequestError as e:
                print("\r" + Fore.RED + f"   (Google Speech recognition error: {e})    ")
                return ""

    except sr.WaitTimeoutError:
        print("\r" + Fore.LIGHTBLACK_EX + "   (Listening timed out)                     ")
        return ""
    except Exception as e:
        print("\r" + Fore.RED + f"   (Microphone error: {e})                   ")
        return ""


if __name__ == "__main__":
    print(Fore.CYAN + "=== Testing JARVIS Ear ===")
    while True:
        text = listen()
        if text:
            print(f"Result: {text}")
        if text in ["exit", "quit", "stop"]:
            break
