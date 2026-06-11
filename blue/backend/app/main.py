from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from app.adapters.api.auth_router import router as auth_router
from app.adapters.api.producto_router import router as producto_router
from app.adapters.api.perfil_router import router as perfil_router
from app.adapters.api.orden_router import router as orden_router
from app.adapters.api.chat_router import router as chat_router
from app.adapters.api.faq_router import router as faq_router

app = FastAPI(
    title="FiguraZone API",
    description="E-commerce de figuras de accion — Arquitectura Hexagonal + JWT + WebSockets",
    version="4.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(producto_router)
app.include_router(perfil_router)
app.include_router(orden_router)
app.include_router(chat_router)
app.include_router(faq_router)


@app.get("/")
def root():
    return {"mensaje": "FiguraZone API v4", "docs": "/docs"}
