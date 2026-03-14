import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send"
]

def send_email(destinatario, asunto, mensaje):

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

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(mensaje)

    message["to"] = destinatario
    message["subject"] = asunto

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {"raw": raw}

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()

    print("Correo enviado correctamente")