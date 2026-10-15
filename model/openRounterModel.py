import os
from dotenv import load_dotenv
from colorama import Fore, init

init(autoreset=True)

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
VISION_MODEL = os.getenv("OPENROUTER_VISION_MODEL", "google/gemini-2.0-flash-001")

# Initialize OpenRouter client via OpenAI SDK
client = None
if API_KEY and API_KEY != "your_openrouter_api_key_here":
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
            default_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "JARVIS Desktop Assistant",
            }
        )
    except Exception as e:
        print(Fore.RED + f"[OpenRouter] Client initialization error: {e}")


def is_openrouter_configured():
    """Returns True if a valid OpenRouter API key is configured."""
    return bool(client and API_KEY and API_KEY != "your_openrouter_api_key_here")


def askJarvisVision(image_base64, question="What do you see, sir?"):
    """
    Sends visual input (base64 encoded image) and a user prompt to OpenRouter multimodal model.
    Returns a spoken-ready conversational response.
    """
    if not is_openrouter_configured():
        return (
            "I apologize, sir, but my optical neural link is not yet configured. "
            "Please provide your OPENROUTER_API_KEY in the .env file."
        )

    if not image_base64:
        return "I was unable to retrieve a valid optical feed to analyze, sir."

    try:
        system_instruction = (
            "You are JARVIS, an advanced, highly intelligent, and loyal AI assistant created for Shukalyan Pramanik. "
            "Address the user politely (you may use 'sir'). "
            "Analyze the provided image and respond concisely and conversationally in 2 to 3 sentences, "
            "optimized to be spoken out loud."
        )

        prompt_text = question if question and question.strip() else "What do you see? Please describe it concisely."

        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        return reply if reply else "I observe the scene, but cannot discern any notable details, sir."

    except Exception as e:
        print(Fore.RED + f"[OpenRouter] Vision API call error: {e}")
        return "I encountered an error processing visual data through OpenRouter, sir."


def askJarvisOpenRouter(question):
    """
    Queries OpenRouter for general conversational responses.
    """
    if not is_openrouter_configured():
        return "My OpenRouter language model is not configured. Please check your OPENROUTER_API_KEY in the .env file."

    try:
        system_instruction = (
            "You are JARVIS, an advanced, loyal AI assistant created for Shukalyan Pramanik. "
            "Address the user politely (you may use 'sir'). "
            "Keep answers concise, direct, and conversational so they are pleasant to hear spoken out loud."
        )
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": question}
            ],
            max_tokens=250,
        )
        reply = response.choices[0].message.content.strip()
        return reply if reply else "I am here to assist, sir."
    except Exception as e:
        print(Fore.RED + f"[OpenRouter] API call error: {e}")
        return "I apologize, sir. I am currently unable to reach the OpenRouter neural network."


if __name__ == "__main__":
    print("Testing OpenRouter configured status:", is_openrouter_configured())
