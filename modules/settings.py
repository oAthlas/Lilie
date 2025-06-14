import json
import tkinter as tk
import customtkinter as ctk

def load_settings(app):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            app.api_key = config.get("api_key", "")
    except Exception:
        app.api_key = ""

def save_api_settings(app, settings_window):
    new_api_key = app.api_entry.get().strip()
    if not new_api_key:
        tk.messagebox.showerror("Erro", "Por favor, insira uma chave API válida", parent=settings_window)
        return
    app.api_key = new_api_key
    try:
        with open("config.json", "w") as f:
            json.dump({"api_key": app.api_key}, f)
        app.status_bar.configure(text="Pronto para conversar")
        settings_window.destroy()
        tk.messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!", parent=app)
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Não foi possível salvar: {str(e)}", parent=settings_window)