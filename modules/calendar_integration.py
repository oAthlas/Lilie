# calendar_integration.py
import os.path
import pickle
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import traceback

class GoogleCalendar:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']

    def conectar_google_calendar(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service
    
    def criar_evento_no_google(self, titulo, descricao, inicio_iso, fim_iso):
        try:
            inicio = datetime.fromisoformat(inicio_iso)
            fim = datetime.fromisoformat(fim_iso)
            
            if fim <= inicio:
                raise ValueError("A data de término deve ser após a data de início")
                
            service = self.conectar_google_calendar()
            
            evento = {
                'summary': titulo,
                'description': descricao,
                'start': {
                    'dateTime': inicio_iso,
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': fim_iso,
                    'timeZone': 'America/Sao_Paulo',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }

            evento_resultado = service.events().insert(
                calendarId='primary', 
                body=evento
            ).execute()
            
            return evento_resultado.get('htmlLink')
            
        except Exception as e:
            print(f"Erro detalhado ao criar evento: {traceback.format_exc()}")
            raise Exception(f"Falha ao criar evento no Google Agenda: {str(e)}")