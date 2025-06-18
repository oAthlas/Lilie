import tkinter as tk
import customtkinter as ctk
import re

def add_message_to_ui(app, sender, message, role):
    # Fontes diferenciadas
    font_user = "Segoe UI"
    font_ai = "Segoe UI Semibold"
    font_size_user = 18
    font_size_ai = 22
    fg_color = "#ffffff"
    anchor = "e" if role == "user" else "w"
    if role == "user":
        baloon_color = "#232323"
        border_color = "#0066cc"
        padx = 80
        msg_frame = ctk.CTkFrame(app.chat_frame, fg_color="transparent", corner_radius=0)
        msg_frame.pack(fill="x", padx=padx, pady=8, anchor=anchor)
        container = ctk.CTkFrame(msg_frame, fg_color=baloon_color, corner_radius=22, border_width=0)
        container.pack(fill="x", expand=True)
        msg_text = tk.Text(
            container, wrap="word",
            font=(font_user, font_size_user),
            bg=baloon_color, fg=fg_color,
            padx=16, pady=14, insertbackground=fg_color,
            highlightthickness=0, relief="flat", borderwidth=0
        )
        msg_text.insert("1.0", f"{sender}: ", "sender")
        msg_text.tag_config("sender", font=(font_user, font_size_user, "bold"))
        msg_text.insert("end", message)
        msg_text.configure(state="disabled")
        msg_text.update_idletasks()
        lines = int(msg_text.index('end-1c').split('.')[0])
        min_lines = 3
        max_lines = 10  # Limite máximo de expansão
        if lines < min_lines:
            lines = min_lines
        elif lines > max_lines:
            lines = max_lines
        msg_text.configure(height=lines)
        msg_text.pack(fill="both", expand=True, padx=0, pady=0)
        container.configure(border_color=border_color, border_width=2)
    else:
        # Remove símbolos indesejados da mensagem da IA
        message = re.sub(r'[*#@~^_`´=+\[\]\(\)\{\}\\|<>$%&]', '', message)
        msg_label = ctk.CTkLabel(
            app.chat_frame,
            text=f"{sender}: {message}",
            font=ctk.CTkFont(family=font_ai, size=font_size_ai),
            text_color=fg_color,
            anchor="w",
            justify="left",
            wraplength=app.chat_frame.winfo_width() - 40,
            fg_color="transparent"
        )
        msg_label.pack(fill="x", padx=20, pady=8, anchor="w")
        app.chat_frame._parent_canvas.yview_moveto(1.0)

def update_lilie_labels_wraplength(app):
    try:
        largura = app.chat_frame.winfo_width() - 40
        for widget in app.chat_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(wraplength=largura)
    except Exception:
        pass  # Ignora erro se o widget ainda não existir