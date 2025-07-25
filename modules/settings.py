import json
import tkinter as tk
import customtkinter as ctk

def load_settings(app):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            app.api_key = config.get("api_key", "")
            app.google_cse_api_key = config.get("google_cse_api_key", "")
            app.google_cse_cx = config.get("google_cse_cx", "")
    except Exception:
        app.api_key = ""
        app.google_cse_api_key = ""
        app.google_cse_cx = ""

def save_api_settings(app, settings_window):
    new_api_key = app.api_entry.get().strip()
    new_google_api_key = app.google_api_entry.get().strip()
    new_google_cx = app.google_cx_entry.get().strip()
    if not new_api_key:
        tk.messagebox.showerror("Erro", "Por favor, insira uma chave API válida", parent=settings_window)
        return
    app.api_key = new_api_key
    app.google_cse_api_key = new_google_api_key
    app.google_cse_cx = new_google_cx
    try:
        # Carrega o config.json atual, atualiza os campos e salva de volta
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except Exception:
            config = {}
        config["api_key"] = app.api_key
        config["google_cse_api_key"] = app.google_cse_api_key
        config["google_cse_cx"] = app.google_cse_cx
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        app.status_bar.configure(text="Pronto para conversar")
        settings_window.destroy()
        tk.messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!", parent=app)
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Não foi possível salvar: {str(e)}", parent=settings_window)