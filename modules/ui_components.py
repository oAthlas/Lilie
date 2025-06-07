# ui_components.py
import customtkinter as ctk
import tkinter as tk

def setup_ui(app):
    bg_color = "#121212"
    font_family = "Segoe UI Rounded"
    font_size = 18

    app.main_frame = ctk.CTkFrame(app, fg_color=bg_color)
    app.main_frame.pack(fill="both", expand=True)

    # Header
    app.header = ctk.CTkFrame(app.main_frame, height=70, fg_color=bg_color)
    app.header.pack(fill="x")
    app.settings_btn = ctk.CTkButton(
        app.header, text="⚙️", width=60, command=app.show_settings,
        fg_color="transparent", hover_color="#232323",
        font=ctk.CTkFont(family=font_family, size=font_size+2, weight="bold")
    )
    app.settings_btn.pack(side="left", padx=15)
    app.title_label = ctk.CTkLabel(
        app.header, text="Lilie - Assistente Pessoal",
        font=ctk.CTkFont(family=font_family, size=font_size+6, weight="bold")
    )
    app.title_label.pack(side="left", expand=True)

    # Chat area
    app.chat_frame = ctk.CTkScrollableFrame(app.main_frame, fg_color=bg_color)
    app.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Input panel
    app.input_panel = ctk.CTkFrame(app.main_frame, height=100, fg_color=bg_color)
    app.input_panel.pack(fill="x")
    app.user_input = ctk.CTkEntry(
        app.input_panel,
        placeholder_text="Digite sua mensagem aqui...",
        font=ctk.CTkFont(family=font_family, size=font_size+2),
        height=48,
        border_width=0,
        fg_color="#232323",
        text_color="#ffffff",
        corner_radius=20
    )
    app.user_input.pack(side="left", fill="x", expand=True, padx=20, pady=20)
    app.user_input.bind("<Return>", lambda e: app.send_message())
    app.send_btn = ctk.CTkButton(
        app.input_panel, text="Enviar", width=120, command=app.send_message,
        font=ctk.CTkFont(family=font_family, size=font_size+2, weight="bold"),
        height=48,
        corner_radius=20,
        fg_color="#232323",
        hover_color="#3a3a3a",
        text_color="#ffffff"
    )
    app.send_btn.pack(side="right", padx=20, pady=20)

    # Status bar
    app.status_bar = ctk.CTkLabel(
        app.main_frame,
        text="Pronto para conversar" if app.api_key else "Configure sua API Key",
        text_color="#a0a0a0",
        font=ctk.CTkFont(family=font_family, size=font_size)
    )
    app.status_bar.pack(fill="x", padx=20, pady=(0, 10))

    app.user_input.focus_set()