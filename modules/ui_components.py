# ui_components.py
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

def setup_ui(app):
    bg_color = "#121212"
    font_family = "Segoe UI Rounded"
    font_size = 18

    # Frame principal ocupa toda a tela
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    # Frame principal (conteúdo)
    app.main_frame = ctk.CTkFrame(app, fg_color=bg_color)
    app.main_frame.grid(row=0, column=0, sticky="nsew")

    # Botão hambúrguer fixo no topo esquerdo
    app.menu_btn = ctk.CTkButton(
        app,
        text="☰",
        width=40,
        height=40,
        command=app.toggle_sidebar,
        fg_color="transparent",
        hover_color="#232323",
        font=ctk.CTkFont(family=font_family, size=20)
    )
    app.menu_btn.place(x=10, y=10)

    # Barra lateral (drawer), inicialmente oculta
    app.sidebar = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color="#1a1a1a")
    app.sidebar.place_forget()

    # Frame horizontal para logo e botão X
    app.sidebar_top = ctk.CTkFrame(app.sidebar, fg_color="transparent")
    app.sidebar_top.pack(fill="x", pady=(10, 0), padx=0)

    # Logo à esquerda
    app.logo_label = ctk.CTkLabel(
        app.sidebar_top,
        text="Lilie",
        font=ctk.CTkFont(family="Segoe UI Semibold", size=24, weight="bold"),
        text_color="#b388ff"
    )
    app.logo_label.pack(side="left", padx=(20, 0), pady=0)

    # Botão fechar (X) à direita
    app.close_btn = ctk.CTkButton(
        app.sidebar_top,
        text="✕",
        width=30,
        height=30,
        command=app.toggle_sidebar,
        fg_color="transparent",
        hover_color="#232323",
        font=ctk.CTkFont(family=font_family, size=18)
    )
    app.close_btn.pack(side="right", padx=(0, 10), pady=0)

    # Botões da barra lateral
    def create_sidebar_button(text, icon_text, command):
        btn = ctk.CTkButton(
            app.sidebar,
            text=f"{icon_text} {text}",
            anchor="w",
            command=command,
            fg_color="transparent",
            hover_color="#232323",
            height=40,
            font=ctk.CTkFont(family=font_family, size=16)
        )
        btn.pack(fill="x", padx=20, pady=5)
        return btn

    # Ícones do FontAwesome
    home_icon = "🏠"
    settings_icon = "⚙️"
    about_icon = "ℹ️"
    help_icon = "❓"

    # Botões
    app.home_btn = create_sidebar_button("Início", home_icon, lambda: app.show_home())
    app.settings_btn = create_sidebar_button("Configurações", settings_icon, app.show_settings)
    app.about_btn = create_sidebar_button("Sobre", about_icon, lambda: app.show_about())

    # Espaço para empurrar o botão de ajuda para baixo
    app.sidebar_spacer = ctk.CTkLabel(app.sidebar, text="", fg_color="#1a1a1a")
    app.sidebar_spacer.pack(expand=True, fill="both")

    # Botão de ajuda no final
    app.help_btn = ctk.CTkButton(
        app.sidebar,
        text=f"{help_icon} Ajuda",
        anchor="w",
        command=lambda: app.show_help(),
        fg_color="transparent",
        hover_color="#232323",
        height=40,
        font=ctk.CTkFont(family=font_family, size=16)
    )
    app.help_btn.pack(fill="x", padx=20, pady=10, side="bottom")

    # Header
    app.header = ctk.CTkFrame(app.main_frame, height=90, fg_color=bg_color)
    app.header.pack(fill="x")

    # Título principal
    app.title_label = ctk.CTkLabel(
        app.header, text="Lilie",
        font=ctk.CTkFont(family="Segoe UI Semibold", size=34, weight="bold"),
        text_color="#b388ff"
    )
    app.title_label.pack(side="top", pady=(8, 0), anchor="center", expand=True)

    # Subtítulo
    app.subtitle_label = ctk.CTkLabel(
        app.header,
        text="Sua assistente pessoal com inteligência artificial",
        font=ctk.CTkFont(family="Segoe UI", size=18, weight="normal"),
        text_color="#a0a0a0"
    )
    app.subtitle_label.pack(side="top", pady=(0, 8), anchor="center", expand=True)

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