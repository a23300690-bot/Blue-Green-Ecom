from abc import ABC, abstractmethod
from typing import Optional


class RespuestaAutomaticaPort(ABC):
    """
    Puerto que define el contrato para el motor de respuestas automaticas.

    Actualmente implementado con busqueda por palabras clave (LIKE en MySQL).
    Disenado para ser reemplazado en el futuro por:
      - un asistente de IA
      - embeddings semanticos
      - RAG (Retrieval-Augmented Generation)
      - modelos LLM
    sin modificar ningun caso de uso ni capa de dominio.
    """

    @abstractmethod
    def buscar_respuesta(self, mensaje: str) -> Optional[str]:
        """
        Recibe el mensaje del cliente y retorna una respuesta automatica
        si detecta una coincidencia, o None si no hay respuesta disponible.
        """
        pass
