def processar_evento(app, mensagem):
    evento = app.event_parser.extrair_evento_com_ia(mensagem)
    if not evento:
        app.show_error("Não foi possível extrair informações do evento.")
        return
    try:
        link = app.calendar.criar_evento_no_google(
            evento["titulo"],
            evento.get("descricao", ""),
            evento["inicio"],
            evento.get("fim", "")
        )
        resposta = f"Evento '{evento['titulo']}' agendado com sucesso!\n[Ver no Google Agenda]({link})"
        from modules.chat_ui import add_message_to_ui
        add_message_to_ui(app, "Lilie", resposta, "ai")
        app.status_bar.configure(text="Pronto para conversar")
        app.start_voice_animation(f"Evento {evento['titulo']} agendado com sucesso!")
    except Exception as e:
        app.show_error(str(e))