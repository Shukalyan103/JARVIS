from langdetect import detect

def detect_language(text):
    
    try:
        language = detect(text)
        return language
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None

