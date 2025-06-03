# src/routes/test_supabase.py
from fastapi import APIRouter
from src.infrastructure.supabase_client import supabase

router = APIRouter()

@router.get("/api/usuarios")
def listar_usuarios():
    response = supabase.table("user_profiles").select("*").execute()
    return response.data
