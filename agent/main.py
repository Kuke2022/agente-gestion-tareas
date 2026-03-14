import os
from dotenv import load_dotenv
from google import genai
from task_manager import process_tasks

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

print("Agente iniciado correctamente")

# intentar usar Gemini
try:

    client = genai.Client(api_key=API_KEY)

    with open("GEMINI.md", "r", encoding="utf-8") as f:
        instrucciones = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Resume el rol de este agente:\n" + instrucciones
    )

    print("Gemini respondió:")
    print(response.text)

except Exception as e:

    print("No se pudo usar Gemini (posible problema de cuota)")
    print("El agente continuará sin IA.\n")

# ejecutar lógica del agente
process_tasks()