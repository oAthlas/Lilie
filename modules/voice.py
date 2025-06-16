# voice.py
import pyttsx3
import threading
import re

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def stop(self):
        self.engine.stop()

    def clean_text(self, text):
        # Substituições específicas para junções de símbolos
        text = text.replace("R$", "reais ")
        text = re.sub(r'(?<!R)\$', "dólar ", text)  # $ que não seja precedido de R
        # Remove emojis e caracteres especiais, mantendo letras, números e pontuação básica
        text = re.sub(r'[^\w\s,.!?áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ-]', '', text, flags=re.UNICODE)
        return text

    def speak_text(self, text, callback=None):
        try:
            self.engine.stop()
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if "female" in voice.name.lower() or "feminina" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            self.engine.setProperty('rate', 235)
            self.engine.setProperty('volume', 1.0)
            clean = self.clean_text(text)
            self.engine.say(clean)
            self.engine.runAndWait()
        except Exception:
            pass
        if callback:
            callback()