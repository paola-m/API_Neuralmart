import os
import uuid
import requests
from dotenv import load_dotenv
from src.services.supabase_service import supabase

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

HEADERS = {
    "Content-Type": "application/json"
}
PARAMS = {
    "key": API_KEY
}

def obtener_productos_relacionados(consulta: str):
    try:
        resultado = (
            supabase
            .table("products")
            .select("name, description")
            .or_(f"name.ilike.%{consulta}%,description.ilike.%{consulta}%")
            .execute()
        )
        return resultado.data or []
    except Exception as e:
        print("Error consultando productos relacionados:", e)
        return []

def generar_respuesta_con_contexto(prompt_usuario: str, user_id: str = None) -> str:
    productos_disponibles = obtener_productos_relacionados(prompt_usuario)

    if productos_disponibles:
        nombre_principal = productos_disponibles[0]["name"]
        contexto_productos = "\n".join([
            f"{p['name']}: {p['description']}" for p in productos_disponibles
        ])
        prompt = (
            f"Eres un asistente de compras. El usuario está interesado en: {prompt_usuario}.\n"
            f"En nuestra tienda SÍ tenemos el producto {nombre_principal} disponible.\n"
            f"También contamos con estas opciones:\n{contexto_productos}\n"
            "Responde de forma breve, útil y conversacional. No uses listas, asteriscos ni markdown. "
            "Confirma que el producto está disponible y ofrece sugerencias breves de otros similares."
        )
    else:
        prompt = (
            f"Eres un asistente de compras. El usuario busca: {prompt_usuario}. "
            "Lamentablemente, no tenemos ese producto disponible. "
            "Haz preguntas para conocer mejor lo que necesita y ofrecer alternativas. "
            "Usa un tono amigable y breve, sin listas ni asteriscos."
        )

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_URL, headers=HEADERS, params=PARAMS, json=data)

    if response.status_code == 200:
        result = response.json()
        respuesta = result["candidates"][0]["content"]["parts"][0]["text"]

        if user_id:
            supabase.table("user_queries").insert({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "product_id": None,
                "query": prompt_usuario,
                "response": respuesta
            }).execute()

        return respuesta
    else:
        raise Exception(f"{response.status_code}: {response.json()}")
