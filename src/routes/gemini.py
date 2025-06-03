from fastapi import APIRouter
from pydantic import BaseModel
from src.services.gemini_service import generar_respuesta_con_contexto

router = APIRouter()

class RecomendacionInput(BaseModel):
    producto: str
    user_id: str

@router.post("/recomendar")
async def recomendar(data: RecomendacionInput):

    respuesta = generar_respuesta_con_contexto(data.producto, user_id=data.user_id)
    return {"respuesta": respuesta}
