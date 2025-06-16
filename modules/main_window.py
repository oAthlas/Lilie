import customtkinter as ctk
import tkinter as tk
import threading
from modules.settings import load_settings, save_api_settings
from modules.ai_client import test_api_key, get_ai_response
from modules.chat_ui import add_message_to_ui
from modules.event_manager import processar_evento
from modules.ui_components import setup_ui
from modules.voice import VoiceEngine
from modules.calendar_integration import GoogleCalendar
from modules.event_parser import EventParser
from modules.google_search import buscar_google_cse

class AIChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            self.iconbitmap("lilie.ico")
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
        load_settings(self)
        self.after(500, self.show_welcome_message)

    def show_welcome_message(self):
        welcome = "Olá, sou a Lilie, sua assistente virtual pronta para te ajudar em qualquer atividade do seu dia!"
        add_message_to_ui(self, "Lilie", welcome, "ai")
        self.start_voice_animation(welcome)

    def show_settings(self):
        import tkinter as tk
        import customtkinter as ctk
        from modules.settings import save_api_settings
        from modules.ai_client import test_api_key

        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Configurações da API")
        settings_window.geometry("400x200")
        settings_window.resizable(False, False)

        label = ctk.CTkLabel(settings_window, text="Chave da API OpenRouter:", font=("Segoe UI", 16))
        label.pack(pady=(30, 5))

        self.api_entry = ctk.CTkEntry(settings_window, width=320)
        self.api_entry.insert(0, self.api_key)
        self.api_entry.pack(pady=10)

        btn_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        btn_frame.pack(pady=20)

        save_btn = ctk.CTkButton(
            btn_frame, text="Salvar",
            command=lambda: save_api_settings(self, settings_window)
        )
        save_btn.pack(side="left", padx=10)

        test_btn = ctk.CTkButton(
            btn_frame, text="Testar chave",
            command=lambda: test_api_key(self)
        )
        test_btn.pack(side="left", padx=10)

    def send_message(self):
        if self.is_speaking:
            return
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        self.voice_engine.stop()
        add_message_to_ui(self, "Você", user_message, "user")
        self.chat_history.append({"role": "user", "content": user_message})
        self.user_input.delete(0, tk.END)
        self.send_btn.configure(state="disabled")
        self.user_input.configure(state="disabled")
        self.status_bar.configure(text="Lilie está pensando...")

        # Busca online automática para perguntas comuns
        if any(x in user_message.lower() for x in ["pesquisar", "quem", "como", "quando", "onde", "o que", "por que"]):
            def do_search():
                import json
                with open("config.json") as f:
                    config = json.load(f)
                api_key = config.get("google_cse_api_key", "")
                cx = config.get("google_cse_cx", "")
                resultado_online = buscar_google_cse(user_message, api_key, cx)
                from modules.chat_ui import add_message_to_ui
                add_message_to_ui(self, "Lilie", f"📡 Resultado da busca online:\n{resultado_online}", "ai")
                self.status_bar.configure(text="Pronto para conversar")
                self.send_btn.configure(state="normal")
                self.user_input.configure(state="normal")
                self.start_voice_animation(resultado_online)
            threading.Thread(target=do_search, daemon=True).start()
            return

        if any(palavra in user_message.lower() for palavra in [
            "agendar", "marcar", "agendamento", "marcação", 
            "consulta", "reunião", "compromisso", "evento",
            "encontro", "visita", "sessão", "entrevista",
            "criar evento", "marcar horário", "agenda"
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

    def show_error(self, msg):
        self.status_bar.configure(text="Erro: " + str(msg))
        self.send_btn.configure(state="normal")
        self.user_input.configure(state="normal")
        tk.messagebox.showerror("Erro", msg, parent=self)
        self.user_input.focus_set()