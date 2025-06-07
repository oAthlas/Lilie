# voice.py
import pyttsx3
import threading

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def stop(self):
        self.engine.stop()
    
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
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass
        if callback:
            callback()