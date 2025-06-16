import requests

def buscar_google_cse(pergunta, api_key, cx):
    try:
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
        if "items" not in data:
            return "🔍 Nenhum resultado encontrado."

        texto = ""
        for item in data["items"]:
            texto += f"🔹 {item['title']}\n{item['link']}\n{item['snippet']}\n\n"

        return texto.strip()
    except Exception as e:
        return f"❌ Erro ao buscar no Google: {e}"