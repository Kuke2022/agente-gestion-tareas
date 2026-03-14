import pandas as pd
from datetime import datetime
from calendar_service import create_event
from gmail_service import send_email
import os

def process_tasks():

    df = pd.read_csv("data/tareas.csv")

    hoy = datetime.now()

    for _, row in df.iterrows():

        tarea = row["Tarea"]
        curso = row["Curso"]
        fecha = datetime.fromisoformat(row["Fecha_Entrega"])
        estado = row["Estado"]

        titulo = f"{tarea} - {curso}"

        if estado == "Pendiente":
            create_event(titulo, fecha)

        if fecha < hoy and estado != "Entregado":

            mensaje = f"""
            La tarea {tarea} del curso {curso}
            ya venció.

            Fecha límite: {fecha}
            """

            send_email(
                os.getenv("EMAIL_DESTINO"),
                "ALERTA: tarea vencida",
                mensaje
            )