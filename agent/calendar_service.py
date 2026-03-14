from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import timedelta
import os
import pickle

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send"
]

def create_event(title, fecha):

    creds = None

    # cargar token guardado
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # si no existe token, autenticar
    if not creds:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials/credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    # evento con zona horaria
    event = {
        "summary": title,
        "start": {
            "dateTime": fecha.isoformat(),
            "timeZone": "America/Guatemala"
        },
        "end": {
            "dateTime": (fecha + timedelta(hours=1)).isoformat(),
            "timeZone": "America/Guatemala"
        }
    }

    service.events().insert(calendarId="primary", body=event).execute()

    print("Evento creado en Google Calendar")