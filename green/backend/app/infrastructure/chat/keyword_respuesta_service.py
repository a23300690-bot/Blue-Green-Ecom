from typing import Optional
from app.domain.ports.respuesta_automatica_port import RespuestaAutomaticaPort
from app.domain.ports.faq_repository import FaqRepository


class KeywordRespuestaService(RespuestaAutomaticaPort):
    """
    Implementacion actual del motor de respuestas automaticas.
    Usa busqueda por palabras clave contra la tabla preguntas_frecuentes.

    Para reemplazar por IA en el futuro: crear una nueva clase que implemente
    RespuestaAutomaticaPort y actualizar el container.py. Nada mas cambia.
    """

    def __init__(self, faq_repo: FaqRepository):
        self.faq_repo = faq_repo

    def buscar_respuesta(self, mensaje: str) -> Optional[str]:
        faq = self.faq_repo.buscar_por_palabras_clave(mensaje)
        if faq:
            return faq.respuesta
        return None
