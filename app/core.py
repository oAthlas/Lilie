# app/core.py
import tkinter as tk
import threading
import customtkinter as ctk
import json
import traceback
from datetime import datetime, timedelta
import dateparser

from ..modules.ui_components import setup_ui
from modules.voice import VoiceEngine
from modules.calendar_integration import GoogleCalendar
from modules.event_parser import EventParser

from app.search import buscar_google_cse
from app.ai import get_ai_response
from app.events import processar_evento
from app.voice import start_voice_animation, on_voice_end


class AIChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            self.iconbitmap("assets/lilie.ico")
        except Exception as e:
            print(f"Não foi possível definir o ícone: {e}")

        self.title("Lilie - Assistente AI")
        self.geometry("900x600")
        self.minsize(600, 400)
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.api_key = ""
        self.selected_model = "openai/gpt-3.5-turbo"
        self.is_speaking = False
        self.chat_history = []

        self.voice_engine = VoiceEngine()
        self.calendar = GoogleCalendar()
        self.event_parser = EventParser(self)

        setup_ui(self)
        self.load_settings()
        self.after(500, self.show_welcome_message)

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                self.api_key = config.get("api_key", "")
                self.selected_model = config.get("model", "")
                self.google_api_key = config.get("google_cse_key", "")
                self.google_cx = config.get("google_cse_cx", "")
        except Exception:
            self.api_key = ""
            self.selected_model = "openai/gpt-3.5-turbo"

    def show_welcome_message(self):
        welcome = "Olá! Sou a Lilie, estou pronta para te ajudar com tarefas, agendamentos e dúvidas!"
        self.add_message_to_ui("Lilie", welcome, "ai")
        start_voice_animation(self, welcome)

    def send_message(self):
        if self.is_speaking:
            return

        user_message = self.user_input.get().strip()
        if not user_message:
            return

        info_web = ""
        if any(x in user_message.lower() for x in ["quem é", "o que é", "quando foi", "como funciona", "qual é", "pesquisa", "pesquisar"]):
            info_web = buscar_google_cse(user_message, self.google_api_key, self.google_cx)

        self.voice_engine.stop()
        self.add_message_to_ui("Você", user_message, "user")
        self.chat_history.append({"role": "user", "content": user_message})
        self.user_input.delete(0, tk.END)
        self.info_web = info_web

        try:
            from playsound import playsound
            threading.Thread(target=lambda: playsound("send.mp3"), daemon=True).start()
        except Exception as e:
            print("Erro ao tocar som:", e)

        self.send_btn.configure(state="disabled")
        self.user_input.configure(state="disabled")
        self.status_bar.configure(text="Lilie está pensando...")

        if any(palavra in user_message.lower() for palavra in [
            "agendar", "marcar", "agendamento", "marcação", "consulta", "reunião", "compromisso",
            "evento", "encontro", "visita", "sessão", "entrevista", "criar evento", "marcar horário", "agenda"
        ]):
            threading.Thread(target=processar_evento, args=(self, user_message), daemon=True).start()
        else:
            threading.Thread(target=get_ai_response, args=(self, user_message), daemon=True).start()

    def start_voice_animation(self, text):
        self.is_speaking = True
        self.send_btn.configure(state="disabled")
        self.user_input.configure(state="disabled")
        threading.Thread(target=self.voice_engine.speak_text, args=(text, self.on_voice_end), daemon=True).start()

    def on_voice_end(self):
        self.is_speaking = False
        self.status_bar.configure(text="Pronto para conversar")
        self.send_btn.configure(state="normal")
        self.user_input.configure(state="normal")
        self.user_input.focus_set()

    def add_message_to_ui(self, sender, message, role):
        font_family = "Segoe UI Rounded"
        font_size = 18
        fg_color = "#ffffff"
        anchor = "e" if role == "user" else "w"

        if role == "user":
            baloon_color = "#3a3a3a"
            border_color = "#555555"
            padx = (120, 10)
        else:
            baloon_color = "#181818"
            border_color = "#232323"
            padx = (10, 120)

        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent", corner_radius=0)
        msg_frame.pack(fill="x", padx=padx, pady=8, anchor=anchor)

        container = ctk.CTkFrame(msg_frame, fg_color=baloon_color, corner_radius=22, border_width=0)
        container.pack(fill="x", expand=True)

        msg_text = tk.Text(
            container, wrap="word",
            font=(font_family, font_size),
            bg=baloon_color, fg=fg_color,
            padx=16, pady=14, insertbackground=fg_color,
            highlightthickness=0, relief="flat", borderwidth=0
        )
        msg_text.insert("1.0", f"{sender}: ", "sender")
        msg_text.tag_config("sender", font=(font_family, font_size, "bold"))
        msg_text.insert("end", message)
        msg_text.configure(state="disabled")
        msg_text.update_idletasks()
        lines = int(msg_text.index('end-1c').split('.')[0])
        msg_text.configure(height=max(lines, 3))
        msg_text.pack(fill="both", expand=True, padx=0, pady=0)
        container.configure(border_color=border_color, border_width=2)

        if role == "ai":
            self.chat_history.append({"role": "assistant", "content": message})

        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def show_error(self, msg):
        self.status_bar.configure(text="Erro: " + str(msg))
        self.send_btn.configure(state="normal")
        self.user_input.configure(state="normal")
        tk.messagebox.showerror("Erro", msg, parent=self)
        self.user_input.focus_set()