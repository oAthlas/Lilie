# app/search.py
import requests
import json

def buscar_google_cse(pergunta, api_key, cx):
    try:
        if not api_key or not cx:
            return "❌ A chave da API ou o ID do motor de busca (cx) não estão configurados."

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cx,
            "q": pergunta,
            "num": 3,
            "hl": "pt"
        }

        resposta = requests.get(url, params=params)
        data = resposta.json()

        print("\n🧪 DEBUG JSON DA API GOOGLE:\n")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        if not data.get("items"):
            return "🔍 Nenhum resultado encontrado."

        texto = ""
        for item in data["items"]:
            titulo = item.get("title", "Sem título")
            link = item.get("link", "Sem link")
            snippet = item.get("snippet", "Sem descrição")
            texto += f"🔹 {titulo}\n{link}\n{snippet}\n\n"

        return texto.strip()

    except Exception as e:
        return f"❌ Erro ao buscar no Google: {e}"