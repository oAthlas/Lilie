import json
import tkinter as tk
import customtkinter as ctk

def load_settings(app):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            app.api_key = config.get("api_key", "")
            app.selected_model = config.get("selected_model", "openai/gpt-3.5-turbo")
    except Exception:
        app.api_key = ""
        app.selected_model = "openai/gpt-3.5-turbo"

def save_api_settings(app, settings_window):
    new_api_key = app.api_entry.get().strip()
    new_selected_model = app.model_var.get()
    if not new_api_key:
        tk.messagebox.showerror("Erro", "Por favor, insira uma chave API válida", parent=settings_window)
        return
    app.api_key = new_api_key
    app.selected_model = new_selected_model
    try:
        with open("config.json", "w") as f:
            json.dump({"api_key": app.api_key, "selected_model": app.selected_model}, f)
        app.status_bar.configure(text="Pronto para conversar")
        settings_window.destroy()
        tk.messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!", parent=app)
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Não foi possível salvar: {str(e)}", parent=settings_window)