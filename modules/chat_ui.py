import tkinter as tk
import customtkinter as ctk

def add_message_to_ui(app, sender, message, role):
    font_family = "Segoe UI Rounded"
    font_size = 18
    fg_color = "#ffffff"
    anchor = "e" if role == "user" else "w"
    if role == "user":
        baloon_color = "#232323"
        border_color = "#0066cc"
        padx = 80
    else:
        baloon_color = "#181818"
        border_color = "#232323"
        padx = 20
    msg_frame = ctk.CTkFrame(app.chat_frame, fg_color="transparent", corner_radius=0)
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
        app.chat_frame._parent_canvas.yview_moveto(1.0)