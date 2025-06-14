# app.py
import tkinter as tk
import threading
import customtkinter as ctk
import requests
import json
import traceback
from datetime import datetime, timedelta
import dateparser
from modules.ui_components import setup_ui
from modules.voice import VoiceEngine
from modules.calendar_integration import GoogleCalendar
from modules.event_parser import EventParser

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
        self.load_settings()
        self.after(500, self.show_welcome_message)

    def show_welcome_message(self):
        welcome = "Olá, sou a Lilie, sua assistente virtual pronta para te ajudar em qualquer atividade do seu dia!"
        self.add_message_to_ui("Lilie", welcome, "ai")
        self.start_voice_animation(welcome)

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                self.api_key = config.get("api_key", "")
                self.selected_model = config.get("model", "openai/gpt-3.5-turbo")
        except Exception:
            self.api_key = ""
            self.selected_model = "openai/gpt-3.5-turbo"

    def show_settings(self):
        font_family = "Segoe UI Rounded"
        font_size = 15
        settings = ctk.CTkToplevel(self)
        settings.title("Configurações da API")
        settings.geometry("480x370")
        settings.resizable(False, False)
        settings.transient(self)
        settings.grab_set()
        settings.configure(bg="#181818")

        main_frame = ctk.CTkFrame(
            settings,
            fg_color="#181818",
            border_width=4,
            border_color="#000000",
            corner_radius=16
        )
        main_frame.pack(fill="both", expand=True, padx=22, pady=22)

        title = ctk.CTkLabel(
            main_frame, text="Configurações da API",
            font=ctk.CTkFont(family=font_family, size=font_size+3, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(10, 16))

        # API Key
        api_label = ctk.CTkLabel(
            main_frame, text="OpenRouter API Key:",
            font=ctk.CTkFont(family=font_family, size=font_size, weight="bold"),
            text_color="#cccccc", anchor="w"
        )
        api_label.pack(fill="x", padx=40, pady=(0, 2))
        self.api_entry = ctk.CTkEntry(
            main_frame, placeholder_text="Cole sua chave API aqui...",
            show="*", font=ctk.CTkFont(family=font_family, size=font_size),
            fg_color="#232323", text_color="#ffffff", border_width=0, corner_radius=12, height=32,
            width=280
        )
        self.api_entry.pack(pady=(0, 14), padx=40)
        if self.api_key:
            self.api_entry.insert(0, self.api_key)

        # Modelos
        model_label = ctk.CTkLabel(
            main_frame, text="Modelo:",
            font=ctk.CTkFont(family=font_family, size=font_size, weight="bold"),
            text_color="#cccccc", anchor="w"
        )
        model_label.pack(fill="x", padx=40, pady=(0, 2))
        self.model_var = ctk.StringVar(value=self.selected_model)
        models = [
            ("GPT-3.5 Turbo", "openai/gpt-3.5-turbo"),
            ("Zephyr 7B Beta", "huggingfaceh4/zephyr-7b-beta"),
            ("Google Palm 2", "google/palm-2-chat-bison"),
            ("Claude Instant", "anthropic/claude-instant-v1")
        ]
        for name, model in models:
            rb = ctk.CTkRadioButton(
                main_frame, text=name, variable=self.model_var, value=model,
                font=ctk.CTkFont(family=font_family, size=font_size-2),
                fg_color="#232323", border_color="#232323", hover_color="#181818",
                text_color="#cccccc"
            )
            rb.pack(anchor="w", padx=60, pady=1)

        # Botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=(24, 0), padx=40, fill="x")

        test_btn = ctk.CTkButton(
            btn_frame, text="Testar conexão",
            command=self.test_api_key, height=36, width=150,
            font=ctk.CTkFont(family=font_family, size=font_size-2, weight="bold"),
            fg_color="#232323", hover_color="#333333", text_color="#ffffff", corner_radius=12
        )
        test_btn.pack(side="left", expand=True, padx=(0, 10), ipadx=4, ipady=2)

        save_btn = ctk.CTkButton(
            btn_frame, text="Salvar Configurações",
            command=lambda: self.save_api_settings(settings_window=settings), height=36, width=180,
            font=ctk.CTkFont(family=font_family, size=font_size-2, weight="bold"),
            fg_color="#0066cc", hover_color="#0055aa", text_color="#ffffff", corner_radius=12
        )
        save_btn.pack(side="right", expand=True, padx=(10, 0), ipadx=4, ipady=2)

    def test_api_key(self):
        key = self.api_entry.get().strip()
        if not key:
            tk.messagebox.showerror("Erro", "Insira uma chave para testar.", parent=self)
            return
        try:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Olá"}],
                "temperature": 0.1
            }
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=10)
            if resp.status_code == 200:
                tk.messagebox.showinfo("Sucesso", "Conexão bem-sucedida!", parent=self)
            else:
                tk.messagebox.showerror("Erro", f"Falha: {resp.json().get('error', {}).get('message', 'Chave inválida')}", parent=self)
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Falha ao conectar: {e}", parent=self)

    def save_api_settings(self, settings_window):
        new_api_key = self.api_entry.get().strip()
        new_selected_model = self.model_var.get()
        if not new_api_key:
            tk.messagebox.showerror("Erro", "Por favor, insira uma chave API válida", parent=settings_window)
            return
        self.api_key = new_api_key
        self.selected_model = new_selected_model
        try:
            with open("config.json", "w") as f:
                json.dump({
                    "api_key": self.api_key,
                    "model": self.selected_model
                }, f, indent=4)
            self.status_bar.configure(text="Pronto para conversar")
            settings_window.destroy()
            tk.messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!", parent=self)
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Não foi possível salvar: {str(e)}", parent=settings_window)

    def send_message(self):
        if self.is_speaking:
            return
            
        user_message = self.user_input.get().strip()
        if not user_message:
            return
            
        self.voice_engine.stop()
        self.add_message_to_ui("Você", user_message, "user")
        self.chat_history.append({"role": "user", "content": user_message})
        self.user_input.delete(0, tk.END)
        self.send_btn.configure(state="disabled")
        self.user_input.configure(state="disabled")
        self.status_bar.configure(text="Lilie está pensando...")

        if any(palavra in user_message.lower() for palavra in ["agendar", "marcar", "agendamento", "marcação", 
    "consulta", "reunião", "compromisso", "evento",
    "encontro", "visita", "sessão", "entrevista",
    "criar evento", "marcar horário", "agenda"]):
            threading.Thread(target=self.processar_evento, args=(user_message,), daemon=True).start()
        else:
            threading.Thread(target=self.get_ai_response, args=(user_message,), daemon=True).start()

    def processar_evento(self, mensagem):
        evento = self.event_parser.extrair_evento_com_ia(mensagem)
        if not evento:
            raise ValueError("Não consegui entender os detalhes do evento.")
        
        try:
            agora = datetime.now()
            inicio = dateparser.parse(evento["inicio"], settings={'RELATIVE_BASE': agora})
            if not inicio:
                raise ValueError("Data de início inválida")
                
            if inicio < agora:
                raise ValueError("A data do evento deve ser no futuro")
            
            if "fim" not in evento or not evento["fim"]:
                fim = inicio + timedelta(hours=1)
                evento["fim"] = fim.isoformat()
            
            link = self.calendar.criar_evento_no_google(
                titulo=evento["titulo"],
                descricao=mensagem,
                inicio_iso=inicio.isoformat(),
                fim_iso=evento["fim"]
            )
            
            resposta = f"✅ Evento '{evento['titulo']}' agendado para {inicio.strftime('%d/%m/%Y às %H:%M')}\n{link}"
            self.add_message_to_ui("Lilie", resposta, "ai")
            self.start_voice_animation(f"Evento {evento['titulo']} agendado com sucesso.")
            
        except Exception as e:
            erro_msg = f"❌ Falha ao agendar: {str(e)}"
            self.add_message_to_ui("Lilie", erro_msg, "ai")
            self.start_voice_animation("Desculpe, não consegui agendar o evento.")
            print(f"Erro detalhado: {traceback.format_exc()}")

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
        if lines < 3:
            lines = 3
        msg_text.configure(height=lines)
        msg_text.pack(fill="both", expand=True, padx=0, pady=0)
        container.configure(border_color=border_color, border_width=2)
        if role == "ai":
            self.chat_history.append({"role": "assistant", "content": message})
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def get_ai_response(self, message):
        try:
            if not self.api_key:
                self.show_error("API Key não configurada. Por favor, vá em Configurações.")
                return
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://lilie-app.com",
                "X-Title": "Lilie Assistant"
            }
            max_history = 10
            limited_history = self.chat_history[-max_history:]
            api_messages = [
                {
                    "role": "system",
                    "content": "Você é a Lilie, uma inteligência artificial criada pela equipe da feira de ciência do 3º ano A. "
                               "Você é especializada em ajudar com pesquisas, automação e tarefas criativas. "
                               "Quando perguntarem sobre seu criador, responda que foi desenvolvida pela equipe da feira de ciência do 3º ano A. "
                               "Use um tom sofisticado e profissional, mantendo respostas precisas. "
                               "Se não souber algo, diga que vai consultar seu desenvolvedor. "
                               "Você foi criada em 2025 e está em constante evolução."
                }
            ] + limited_history

            data = {
                "model": self.selected_model,
                "messages": api_messages,
                "temperature": 0.7
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            if response.status_code != 200:
                error_msg = response.json().get("error", {}).get("message", f"Erro desconhecido: Status {response.status_code}")
                raise Exception(f"Erro na API: {error_msg}")
            response_text = response.json()["choices"][0]["message"]["content"]
            self.add_message_to_ui("Lilie", response_text, "ai")
            self.start_voice_animation(response_text)
        except Exception as e:
            self.show_error(str(e))

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