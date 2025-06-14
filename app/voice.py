# app/voice.py
import threading

def start_voice_animation(self, text):
    self.is_speaking = True
    self.send_btn.configure(state="disabled")
    self.user_input.configure(state="disabled")

    threading.Thread(
        target=self.voice_engine.speak_text,
        args=(text, self.on_voice_end),
        daemon=True
    ).start()

def on_voice_end(self):
    self.is_speaking = False
    self.status_bar.configure(text="Pronto para conversar")
    self.send_btn.configure(state="normal")
    self.user_input.configure(state="normal")
    self.user_input.focus_set()