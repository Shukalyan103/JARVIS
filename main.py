import os
import sys 
import datetime
import psutil
from colorama import Fore, Style, init

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from Head.Mouth import speak
from Head.Ear import listen
from Head.Eyes import capture_webcam, capture_screen, encode_image
from model.geminiModel import askJarvis
from model.openRounterModel import askJarvisVision
from utils.routineManager import is_routine_trigger, execute_daily_routine

init(autoreset=True)


def print_banner():
    banner = f"""{Fore.CYAN}{Style.BRIGHT}
    ╔══════════════════════════════════════════════════════════════╗
    ║                 J . A . R . V . I . S .                      ║
    ║        Just A Rather Very Intelligent System                 ║
    ╚══════════════════════════════════════════════════════════════╝
    {Fore.YELLOW}Voice Trigger: Say "Start my daily routine"
    {Fore.LIGHTMAGENTA_EX}Vision Triggers: "What do you see?" (Camera) | "What's on my screen?" (Screen)
    {Fore.LIGHTBLACK_EX}Available Commands: Daily Routine | Vision | Time | System Status | Exit
    """
    print(banner)


def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        period_greeting = "Good morning, sir."
    elif 12 <= hour < 18:
        period_greeting = "Good afternoon, sir."
    else:
        period_greeting = "Good evening, sir."

    speak(f"{period_greeting} JARVIS is online and listening.")


def handle_system_commands(query):
    """
    Handles quick built-in voice commands before forwarding to AI model.
    Returns True if a command was handled, False otherwise.
    """
    cleaned = query.lower()

    # 1. Exit / Shutdown commands
    if any(word in cleaned for word in ["exit jarvis", "quit jarvis", "shutdown", "goodbye jarvis", "bye jarvis", "stop listening"]):
        speak("Powering down systems. Have a wonderful and productive day, sir.")
        print(Fore.GREEN + "\n[JARVIS Terminated Gracefully]\n")
        sys.exit(0)

    # 2. Time query
    if "time" in cleaned and ("what" in cleaned or "tell" in cleaned or "current" in cleaned):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}, sir.")
        return True

    # 3. System / Hardware status
    if "system status" in cleaned or "hardware status" in cleaned or "cpu status" in cleaned or "pc status" in cleaned:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        speak(f"Systems are running smoothly. CPU usage is at {cpu} percent, and RAM usage is at {ram} percent.")
        return True

    return False


def handle_vision_commands(query):
    """
    Handles vision queries using webcam or desktop screen capture + OpenRouter Vision.
    Returns True if a vision command was handled, False otherwise.
    """
    cleaned = query.lower()

    # 1. Webcam capture ("What do you see", "Look at this", "Take a look", "Look through camera")
    webcam_triggers = [
        "what do you see",
        "look at this",
        "take a look",
        "look through camera",
        "what am i holding",
        "what is in front of you",
        "describe what you see",
        "look at me",
    ]
    if any(trigger in cleaned for trigger in webcam_triggers):
        speak("Activating optical camera sensors now, sir. Allow me a moment.")
        img_path = capture_webcam()
        if img_path:
            img_b64 = encode_image(img_path)
            if img_b64:
                print(Fore.LIGHTBLUE_EX + "👁️ JARVIS is analyzing optical feed with OpenRouter...")
                vision_analysis = askJarvisVision(img_b64, question=query)
                speak(vision_analysis)
            else:
                speak("I was unable to process the camera frame, sir.")
        else:
            speak("I was unable to access the camera sensor, sir. Please verify your webcam is connected.")
        return True

    # 2. Desktop screen capture ("What's on my screen", "Look at my screen", "Read my screen")
    screen_triggers = [
        "what's on my screen",
        "what is on my screen",
        "look at my screen",
        "read my screen",
        "analyze my screen",
        "describe my screen",
        "check my screen",
        "explain my screen",
    ]
    if any(trigger in cleaned for trigger in screen_triggers):
        speak("Scanning your desktop display, sir.")
        img_path = capture_screen()
        if img_path:
            img_b64 = encode_image(img_path)
            if img_b64:
                print(Fore.LIGHTBLUE_EX + "👁️ JARVIS is analyzing your screen with OpenRouter...")
                vision_analysis = askJarvisVision(img_b64, question=query)
                speak(vision_analysis)
            else:
                speak("I was unable to process the screen image, sir.")
        else:
            speak("I could not capture your display, sir.")
        return True

    return False


def main():
    print_banner()
    greet()

    print(Fore.GREEN + "\n[Ready] Speak into your microphone to issue commands.\n")

    while True:
        try:
            # Listen to voice command from microphone
            query = listen()

            # If silence or unintelligible, continue listening
            if not query or not query.strip():
                continue

            # 1. Check if user requested Daily Routine
            if is_routine_trigger(query):
                print(Fore.MAGENTA + Style.BRIGHT + "\n[Action] Triggered Daily Workspace Routine!")
                execute_daily_routine(speak_callback=speak)
                continue

            # 2. Check if user issued built-in utility commands (time, system status, exit)
            if handle_system_commands(query):
                continue

            # 3. Check if user issued vision command (Webcam or Screen)
            if handle_vision_commands(query):
                continue

            # 4. Otherwise, forward inquiry to Gemini AI model
            print(Fore.LIGHTBLUE_EX + "🤖 JARVIS is thinking...")
            ai_response = askJarvis(query)
            speak(ai_response)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n[Interrupted] Shutting down JARVIS...")
            speak("Systems disconnected. Goodbye, sir.")
            break
        except Exception as e:
            print(Fore.RED + f"[Error in main loop]: {e}")


if __name__ == "__main__":
    main()
