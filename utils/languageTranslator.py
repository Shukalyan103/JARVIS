from translate import Translator

def translate_text(text, from_lang, to_lang):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(text)
    return translation
