# app/events.py
import traceback
from datetime import datetime, timedelta
import dateparser

def processar_evento(self, mensagem):
    evento = self.event_parser.extrair_evento_com_ia(mensagem)
    if not evento:
        raise ValueError("Não consegui entender os detalhes do evento.")

    try:
        agora = datetime.now()
        inicio = dateparser.parse(evento["inicio"], settings={'RELATIVE_BASE': agora})
        if not inicio:
            raise ValueError("Data de início inválida")

        if inicio < agora:
            raise ValueError("A data do evento deve ser no futuro")

        if "fim" not in evento or not evento["fim"]:
            fim = inicio + timedelta(hours=1)
            evento["fim"] = fim.isoformat()

        link = self.calendar.criar_evento_no_google(
            titulo=evento["titulo"],
            descricao=mensagem,
            inicio_iso=inicio.isoformat(),
            fim_iso=evento["fim"]
        )

        resposta = f"✅ Evento '{evento['titulo']}' agendado para {inicio.strftime('%d/%m/%Y às %H:%M')}\n{link}"
        self.add_message_to_ui("Lilie", resposta, "ai")
        self.start_voice_animation(f"Evento {evento['titulo']} agendado com sucesso.")

    except Exception as e:
        erro_msg = f"❌ Falha ao agendar: {str(e)}"
        self.add_message_to_ui("Lilie", erro_msg, "ai")
        self.start_voice_animation("Desculpe, não consegui agendar o evento.")
        print(f"Erro detalhado: {traceback.format_exc()}")