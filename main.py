import psutil
from Head.Mouth import speak
import platform
import datetime

# print(platform.system())



dated = datetime.datetime.now().strftime("%I:%M:%p")
# dated = datetime.datetime.now().strftime("%d:%B:%Y")
# print(dated)
cpu = psutil.cpu_percent(interval =0.5)
ram = psutil.virtual_memory().percent

speak(f"The time is {dated}. CPU usage is at {cpu}%. RAM usage is at {ram}%.")

def greet():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")


def main ():
    greet()


if __name__ == "__main__":
    main()

