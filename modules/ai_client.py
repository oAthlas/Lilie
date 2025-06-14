import requests
import tkinter as tk

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
            "model": "openai/gpt-3.5-turbo",
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
        # Aqui você implementa a chamada real à API e manipulação da resposta
        pass
    except Exception as e:
        app.show_error(str(e))