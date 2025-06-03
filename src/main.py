from fastapi import FastAPI
from src.routes import gemini
from src.routes import test_supabase
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="NeuralMart - API de recomendación")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # donde corre tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gemini.router, prefix="/api")
app.include_router(test_supabase.router)