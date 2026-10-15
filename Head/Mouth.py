import asyncio
import os
import uuid
import tempfile
import edge_tts
import pygame
from colorama import Fore, Style, init

init(autoreset=True)

VOICE = "en-AU-WilliamNeural"  # British/Australian butler-style JARVIS voice


def remove_file(file_path):
    max_attempts = 8
    attempts = 0
    while attempts < max_attempts:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            break
        except Exception:
            attempts += 1
            pygame.time.wait(80)


def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except Exception as e:
        print(Fore.RED + f"[Mouth] Audio playback error: {e}")
    finally:
        try:
            pygame.mixer.quit()
        except Exception:
            pass


async def _generate_and_play(text, voice_name):
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"jarvis_voice_{uuid.uuid4().hex[:8]}.mp3")
    try:
        communicator = edge_tts.Communicate(text, voice_name)
        await communicator.save(temp_file)
        await asyncio.to_thread(play_audio, temp_file)
    except Exception as e:
        print(Fore.RED + f"[Mouth] TTS generation error: {e}")
    finally:
        remove_file(temp_file)


def speak(text, voice=None):
    """
    Speaks the given text using Edge TTS and pygame playback.
    Also displays the text in the terminal in cyan.
    """
    if not text or not str(text).strip():
        return

    text_str = str(text).strip()
    print(Fore.CYAN + Style.BRIGHT + f"🤖 [JARVIS]: {text_str}")

    selected_voice = voice if voice else VOICE
    try:
        asyncio.run(_generate_and_play(text_str, selected_voice))
    except Exception as e:
        print(Fore.RED + f"[Mouth] Speak exception: {e}")


if __name__ == "__main__":
    speak("Hello sir, JARVIS voice synthesis is functioning properly.")
