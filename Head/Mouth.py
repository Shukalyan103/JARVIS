import asyncio
import os 
import edge_tts
import pygame


VOICE = "en-AU-WilliamNeural"  # You can change this to any available voice


def remove_file(file_path):
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            break
        except Exception as e:
            attempts += 1
            pygame.time.wait(100)


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
        print(f"Error playing audio: {e}")
    finally:
        pygame.mixer.quit()


async def amain(TEXT, output_file) -> None:
    try:
        cm_text = edge_tts.Communicate(TEXT, VOICE)
        await cm_text.save(output_file)
        await asyncio.to_thread(play_audio, output_file)
    except Exception as e:
        print(f"Error in amain: {e}")
    finally:
        remove_file(output_file)


def speak(TEXT, output_file=None):
    if output_file is None:
        output_file = os.path.join(os.getcwd(), 'speak.mp3')
    asyncio.run(amain(TEXT, output_file))


if __name__ == "__main__":
    speak("Hello, I am your virtual assistant. How can I help you today?")

