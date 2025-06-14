# app/ai.py
import requests

def get_ai_response(self, message):
    try:
        if not self.api_key:
            self.show_error("API Key não configurada. Por favor, vá em Configurações.")
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://lilie-app.com",
            "X-Title": "Lilie Assistant"
        }

        max_history = 10
        limited_history = self.chat_history[-max_history:]

        api_messages = [
            {
                "role": "system",
                "content": (
                    "Você é a Lilie, uma inteligência artificial criada pela equipe da feira de ciência do 3º ano A. "
                    "Você é especializada em ajudar com pesquisas, automação e tarefas criativas. "
                    "Quando perguntarem sobre seu criador, responda que foi desenvolvida pela equipe da feira de ciência do 3º ano A. "
                    "Use um tom sofisticado e profissional, mantendo respostas precisas. "
                    "Se não souber algo, diga que vai consultar seu desenvolvedor. "
                    "Você foi criada em 2025 e está em constante evolução."
                )
            }
        ]

        # ➕ Inclui resultado da busca web como contexto, se houver
        if hasattr(self, "info_web") and self.info_web:
            api_messages.append({
                "role": "assistant",
                "content": f"{self.info_web}"
            })

        api_messages += limited_history

        data = {
            "model": self.selected_model,
            "messages": api_messages,
            "temperature": 0.7
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", f"Erro desconhecido: Status {response.status_code}")
            raise Exception(f"Erro na API: {error_msg}")

        response_text = response.json()["choices"][0]["message"]["content"]
        self.add_message_to_ui("Lilie", response_text, "ai")
        self.start_voice_animation(response_text)

    except Exception as e:
        self.show_error(str(e))