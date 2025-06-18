import customtkinter as ctk
import tkinter as tk
import threading
from modules.settings import load_settings, save_api_settings
from modules.ai_client import test_api_key, get_ai_response
from modules.chat_ui import add_message_to_ui, update_lilie_labels_wraplength
from modules.event_manager import processar_evento
from modules.ui_components import setup_ui
from modules.voice import VoiceEngine
from modules.calendar_integration import GoogleCalendar
from modules.event_parser import EventParser
from modules.google_search import buscar_google_cse
from modules.utils import resource_path
from playsound import playsound

def play_send_sound():
    try:
        from modules.utils import resource_path
        playsound(resource_path("send.mp3"), block=False)
    except Exception as e:
        print(f"Erro ao tocar som: {e}")

class AIChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            self.iconbitmap(resource_path("lilie.ico"))
        except Exception as e:
            print(f"Não foi possível definir o ícone: {e}")
        self.title("Lilie - Assistente AI")
        self.geometry("1100x600")  # Aumentei a largura para acomodar a barra lateral
        self.minsize(800, 400)
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.api_key = ""
        self.selected_model = "openai/gpt-3.5-turbo"
        self.is_speaking = False
        self.chat_history = []
        self.sidebar_visible = True  # Controle da visibilidade da barra lateral
        
        self.voice_engine = VoiceEngine()
        self.calendar = GoogleCalendar()
        self.event_parser = EventParser(self)

        setup_ui(self)
        load_settings(self)
        self.after(500, self.show_welcome_message)
        self.bind("<Configure>", lambda e: update_lilie_labels_wraplength(self))
        self.loading_animation_running = False
        self.loading_animation_step = 0

    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Esconde a barra lateral
            self.sidebar.place_forget()
            self.menu_btn.place(x=10, y=10)
            self.menu_btn.configure(text="☰")
        else:
            # Mostra a barra lateral do lado esquerdo
            self.show_sidebar()
            self.menu_btn.place_forget()
            self.menu_btn.configure(text="✕")
        self.sidebar_visible = not self.sidebar_visible

    def show_welcome_message(self):
        welcome = "Olá, sou a Lilie, sua assistente virtual pronta para te ajudar em qualquer atividade do seu dia!"
        add_message_to_ui(self, "Lilie", welcome, "ai")
        self.start_voice_animation(welcome)

    def show_settings(self):
        import tkinter as tk
        import customtkinter as ctk
        from modules.settings import save_api_settings
        from modules.ai_client import test_api_key

        # Carregar valores atuais
        import json
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except Exception:
            config = {}
        api_key = config.get("api_key", "")
        google_cse_api_key = config.get("google_cse_api_key", "")
        google_cse_cx = config.get("google_cse_cx", "")

        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Configurações da API")
        settings_window.geometry("420x340")
        settings_window.resizable(False, False)
        settings_window.grab_set()
        settings_window.focus_force()

        label1 = ctk.CTkLabel(settings_window, text="Chave da API OpenRouter:", font=("Segoe UI", 16))
        label1.pack(pady=(20, 5))
        self.api_entry = ctk.CTkEntry(settings_window, width=360)
        self.api_entry.insert(0, api_key)
        self.api_entry.pack(pady=5)

        label2 = ctk.CTkLabel(settings_window, text="Google CSE API Key:", font=("Segoe UI", 16))
        label2.pack(pady=(15, 5))
        self.google_api_entry = ctk.CTkEntry(settings_window, width=360)
        self.google_api_entry.insert(0, google_cse_api_key)
        self.google_api_entry.pack(pady=5)

        label3 = ctk.CTkLabel(settings_window, text="Google CSE CX:", font=("Segoe UI", 16))
        label3.pack(pady=(15, 5))
        self.google_cx_entry = ctk.CTkEntry(settings_window, width=360)
        self.google_cx_entry.insert(0, google_cse_cx)
        self.google_cx_entry.pack(pady=5)

        btn_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        btn_frame.pack(pady=25)

        save_btn = ctk.CTkButton(
            btn_frame, text="Salvar",
            command=lambda: save_api_settings(self, settings_window),
            height=40, width=120, corner_radius=20,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            border_width=1,
            border_color="#3a3a3a"
        )
        save_btn.pack(side="left", padx=20)

        test_btn = ctk.CTkButton(
            btn_frame, text="Testar chave",
            command=lambda: test_api_key(self),
            height=40, width=140, corner_radius=20,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            border_width=1,
            border_color="#3a3a3a"
        )
        test_btn.pack(side="left", padx=20)

    def start_loading_animation(self, text="Lilie está pensando..."):
        self.loading_animation_running = True
        self.loading_animation_step = 0
        self._animate_loading(text)

    def _animate_loading(self, text):
        if not self.loading_animation_running:
            return
        dots = "●" * ((self.loading_animation_step % 3) + 1)
        spaces = " " * (3 - len(dots))
        self.status_bar.configure(text=f"{text} {dots}{spaces}")
        self.loading_animation_step += 1
        self.after(400, lambda: self._animate_loading(text))

    def stop_loading_animation(self):
        self.loading_animation_running = False
        self.status_bar.configure(text="Pronto para conversar")

    def send_message(self):
        if self.is_speaking:
            return
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        self.voice_engine.stop()
        add_message_to_ui(self, "Você", user_message, "user")
        play_send_sound()
        self.chat_history.append({"role": "user", "content": user_message})
        self.user_input.delete(0, tk.END)
        self.send_btn.configure(state="disabled")
        self.user_input.configure(state="disabled")
        self.start_loading_animation()  # <-- INICIA ANIMAÇÃO

        # Busca online automática para perguntas comuns
        pesquisa_palavras = ["pesquisar", "quem", "como", "quando", "onde", "o que", "por que"]
        user_message_lower = user_message.lower().strip()
        if any(user_message_lower.startswith(x) for x in pesquisa_palavras):
            def do_search():
                import json
                from modules.ai_client import get_ai_response
                with open("config.json") as f:
                    config = json.load(f)
                api_key = config.get("google_cse_api_key", "")
                cx = config.get("google_cse_cx", "")
                resultado_online = buscar_google_cse(user_message, api_key, cx)
                # Remova ou comente a linha abaixo para não exibir o resultado bruto:
                # from modules.chat_ui import add_message_to_ui
                # add_message_to_ui(self, "Lilie", f"📡 Resultado da busca online:\n{resultado_online}", "ai")
                prompt_refinado = (
                    f"Com base nas informações abaixo, responda de forma direta, objetiva e resumida à pergunta: '{user_message}'. "
                    "Responda em no máximo 3 linhas ou 300 caracteres. "
                    "Use apenas as informações fornecidas, sem inventar dados. "
                    "Se não encontrar a resposta, diga 'Não encontrei a resposta com base nas informações pesquisadas.'\n\n"
                    f"Informações encontradas:\n{resultado_online}"
                )
                get_ai_response(self, prompt_refinado)
                self.status_bar.configure(text="Pronto para conversar")
                self.send_btn.configure(state="normal")
                self.user_input.configure(state="normal")
            threading.Thread(target=do_search, daemon=True).start()
            return

        if any(palavra in user_message.lower() for palavra in [
            "agendar", "marcar", "agendamento", "marcação", 
            "consulta", "reunião", "compromisso", "evento",
            "encontro", "visita", "sessão", "entrevista",
            "criar evento", "marcar horário", "agenda" "agende"
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
        self.stop_loading_animation()  # <-- PARA ANIMAÇÃO
        self.send_btn.configure(state="normal")
        self.user_input.configure(state="normal")
        self.user_input.focus_set()

    def show_error(self, msg):
        self.stop_loading_animation()  # <-- PARA ANIMAÇÃO EM CASO DE ERRO
        self.status_bar.configure(text="Erro: " + str(msg))
        self.send_btn.configure(state="normal")
        self.user_input.configure(state="normal")
        tk.messagebox.showerror("Erro", msg, parent=self)
        self.user_input.focus_set()

    def handle_ai_response(self, ai_response):
        add_message_to_ui(self, "Lilie", ai_response, "ai")
        self.stop_loading_animation()  # Para a animação assim que o texto aparece
        self.start_voice_animation(ai_response)  # Inicia a fala normalmente

    def show_home(self):
        # Limpa o chat frame
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        # Mostra a mensagem de boas-vindas
        self.show_welcome_message()

    def show_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("Sobre a Lilie")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.grab_set()
        about_window.focus_force()

        # Título
        title = ctk.CTkLabel(
            about_window,
            text="Lilie - Assistente Virtual IA",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=24, weight="bold"),
            text_color="#b388ff"
        )
        title.pack(pady=(20, 10))

        # Versão
        version = ctk.CTkLabel(
            about_window,
            text="Versão 5.1",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color="#a0a0a0"
        )
        version.pack(pady=(0, 20))

        # Descrição
        description = ctk.CTkLabel(
            about_window,
            text="Lilie é um assistente virtual inteligente desenvolvido para a feira de ciências do colégio.\n\n"
                 "Desenvolvido com Python e CustomTkinter, utilizando APIs de IA para fornecer respostas inteligentes "
                 "e interações naturais.",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#ffffff",
            wraplength=350,
            justify="center"
        )
        description.pack(pady=10, padx=20)

        # Créditos
        credits = ctk.CTkLabel(
            about_window,
            text="Desenvolvido por Athlas (Elder Luiz)",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#a0a0a0"
        )
        credits.pack(pady=(20, 0))

    def show_help(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title("Ajuda")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        help_window.grab_set()
        help_window.focus_force()

        # Título
        title = ctk.CTkLabel(
            help_window,
            text="Como usar a Lilie",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=24, weight="bold"),
            text_color="#b388ff"
        )
        title.pack(pady=(20, 10))

        # Frame para o conteúdo
        content_frame = ctk.CTkScrollableFrame(help_window, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Seções de ajuda
        sections = [
            ("Conversando com a Lilie", 
             "• Digite suas mensagens na caixa de texto\n"
             "• Pressione Enter ou clique em Enviar\n"
             "• A Lilie responderá usando IA"),
            
            ("Agendamento de Eventos",
             "• Digite frases como 'agendar reunião amanhã às 14h'\n"
             "• A Lilie criará o evento no Google Calendar\n"
             "• Você receberá um link para o evento"),
            
            ("Pesquisas",
             "• Faça perguntas começando com 'quem', 'como', 'quando', etc.\n"
             "• A Lilie buscará informações online\n"
             "• As respostas serão baseadas em fontes confiáveis"),
            
            ("Configurações",
             "• Configure sua chave de API em Configurações\n"
             "• A chave é necessária para o funcionamento da IA\n"
             "• Você pode testar a chave antes de salvar")
        ]

        for title_text, content in sections:
            section_frame = ctk.CTkFrame(content_frame, fg_color="#232323", corner_radius=10)
            section_frame.pack(fill="x", pady=5, padx=5)

            section_title = ctk.CTkLabel(
                section_frame,
                text=title_text,
                font=ctk.CTkFont(family="Segoe UI Semibold", size=16),
                text_color="#b388ff"
            )
            section_title.pack(pady=(10, 5), padx=10, anchor="w")

            section_content = ctk.CTkLabel(
                section_frame,
                text=content,
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color="#ffffff",
                justify="left"
            )
            section_content.pack(pady=(0, 10), padx=10, anchor="w")