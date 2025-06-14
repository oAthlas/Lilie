def processar_evento(app, mensagem):
    evento = app.event_parser.extrair_evento_com_ia(mensagem)
    if not evento:
        app.show_error("Não foi possível extrair informações do evento.")
        return
    try:
        # Aqui você pode integrar com o Google Calendar, por exemplo
        pass
    except Exception as e:
        app.show_error(str(e))