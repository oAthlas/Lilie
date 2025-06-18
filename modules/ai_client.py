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
            "temperature": 0.95
        }
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            tk.messagebox.showinfo("Sucesso", "Chave válida!", parent=app)
        else:
            tk.messagebox.showerror("Erro", f"Chave inválida ou erro: {resp.text}", parent=app)
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Falha ao conectar: {e}", parent=app)

def get_ai_response(app, prompt):
    try:
        headers = {
            "Authorization": f"Bearer {app.api_key}",
            "Content-Type": "application/json"
        }
        curta_message = (
            "Responda de forma direta e esboçe emoções. Jamais use emojis. Se lhe for dito algo que você não tem certeza, faça perguntas ao usuário. "
            f"{prompt}"
        )
        data = {
            "model": "deepseek/deepseek-r1:free",
            "messages": app.chat_history + [{"role": "user", "content": curta_message}],
            "temperature": 0.3
        }
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        if resp.status_code == 200:
            resposta = resp.json()["choices"][0]["message"]["content"]
            app.chat_history.append({"role": "assistant", "content": resposta})
            app.handle_ai_response(resposta)  # <-- Centraliza exibição, animação e voz
        else:
            app.show_error(f"Erro na resposta da IA: {resp.text}")
    except Exception as e:
        app.show_error(f"Erro ao conectar com a IA: {e}")