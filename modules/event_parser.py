# event_parser.py
import dateparser
from datetime import datetime, timedelta
import json
import requests

class EventParser:
    def __init__(self, app):
        self.app = app

    def interpretar_evento(self, frase):
        data = dateparser.parse(frase, languages=['pt'])

        if not data:
            return None

        inicio = data
        fim = data + timedelta(hours=1)

        palavras_excluir = [
            "agende", "agendar", "marque", "marcar", "crie", "criar",
            "um", "uma", "evento", "compromisso", "para", "no", "em",
            "dia", "às", "as", "a", "o", "meu", "minha", "do", "da",
            "de", "com"
        ]
        palavras = frase.split()
        titulo = " ".join([p.capitalize() for p in palavras if p.lower() not in palavras_excluir])

        return {
            "titulo": titulo or "Evento",
            "descricao": frase,
            "inicio": inicio.isoformat(),
            "fim": fim.isoformat()
        }
    
    def extrair_evento_com_ia(self, mensagem):
        modelo = self.app.selected_model
        chave = self.app.api_key

        prompt =  f"""
Extraia da seguinte mensagem os detalhes para um evento de calendário:

1. Título (3-5 palavras)
2. Data e hora de início (no formato ISO 8601 COMPLETO: AAAA-MM-DDTHH:MM:SS)
3. Duração (padrão de 1 hora se não especificado)

REGRAS IMPORTANTES:
- Para expressões relativas como "amanhã" ou "próxima semana", use SEMPRE a data correta em relação a hoje ({datetime.now().strftime('%d/%m/%Y')})
- NUNCA interprete "amanhã" como o dia 15 do mês
- Para horários, use sempre o formato 24h
- Responda APENAS com um JSON válido contendo: "titulo", "inicio", "fim"

Exemplo 1:
Mensagem: "marcar consulta médica amanhã às 14h"
Resposta:
{{
  "titulo": "Consulta Médica",
  "inicio": "{ (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') }T14:00:00",
  "fim": "{ (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') }T15:00:00"
}}

Exemplo 2:
Mensagem: "reunião com equipe na próxima segunda às 10h30"
Resposta:
{{
  "titulo": "Reunião com Equipe",
  "inicio": "[data correta da próxima segunda no formato ISO]T10:30:00",
  "fim": "[data correta da próxima segunda no formato ISO]T11:30:00"
}}

    Frase: "{mensagem}"
    """

        payload = {
            "model": modelo,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1
        }

        headers = {
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json"
        }

        try:
            resposta = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                json=payload, 
                                headers=headers,
                                timeout=10)
            resposta.raise_for_status()
            texto = resposta.json()["choices"][0]["message"]["content"]
            
            texto = texto.replace("```json", "").replace("```", "").strip()
            evento = json.loads(texto)
            
            if not all(key in evento for key in ["titulo", "inicio"]):
                raise ValueError("Resposta da IA não contém todos campos necessários")
                
            return evento

        except Exception as e:
            print(f"❌ Erro ao extrair evento com IA: {e}")
            return self.interpretar_evento(mensagem)