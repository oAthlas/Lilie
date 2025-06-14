import requests
import tkinter as tk
from modules.chat_ui import add_message_to_ui

def test_api_key(app):
    key = app.api_entry.get().strip()
    if not key:
        tk.messagebox.showerror("Erro", "Insira uma chave para testar.", parent=app)
        return
    try:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [{"role": "user", "content": "Olá"}],
            "temperature": 0.1
        }
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            tk.messagebox.showinfo("Sucesso", "Chave válida!", parent=app)
        else:
            tk.messagebox.showerror("Erro", f"Chave inválida ou erro: {resp.text}", parent=app)
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Falha ao conectar: {e}", parent=app)

def get_ai_response(app, message):
    try:
        headers = {
            "Authorization": f"Bearer {app.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek/deepseek-r1:free",  # Modelo DeepSeek R1
            "messages": app.chat_history + [{"role": "user", "content": message}],
            "temperature": 0.7
        }
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        if resp.status_code == 200:
            resposta = resp.json()["choices"][0]["message"]["content"]
            app.chat_history.append({"role": "assistant", "content": resposta})
            add_message_to_ui(app, "Lilie", resposta, "ai")
            app.status_bar.configure(text="Pronto para conversar")
            app.start_voice_animation(resposta)
        else:
            app.show_error(f"Erro na resposta da IA: {resp.text}")
    except Exception as e:
        app.show_error(f"Erro ao conectar com a IA: {e}")