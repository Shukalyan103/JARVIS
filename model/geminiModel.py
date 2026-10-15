import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Initialize client using Google GenAI SDK
client = None
if api_key:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[GeminiModel] Error initializing google.genai client: {e}")


def askJarvis(question):
    """
    Queries Gemini for general conversational responses when not executing system commands.
    """
    if not client:
        return "My generative brain is not configured. Please check your GEMINI_API_KEY in the .env file."

    try:
        system_instruction = (
            "You are JARVIS, an advanced, highly intelligent, and loyal AI assistant created for Shukalyan Pramanik. "
            "Address the user politely (you may use 'sir'). "
            "Keep answers concise, direct, and conversational so they are pleasant to hear spoken out loud."
        )
        prompt = f"{system_instruction}\n\nUser: {question}\nJARVIS:"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        reply = response.text.strip() if response.text else "I am here to assist, sir."
        return reply
    except Exception as e:
        print(f"[GeminiModel] API call error: {e}")
        return "I apologize, sir. I am currently unable to connect to my online neural network."


if __name__ == "__main__":
    print(askJarvis("Hello JARVIS, are you operational?"))
