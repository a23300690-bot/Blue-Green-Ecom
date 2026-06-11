from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class OrigenMensaje(str, Enum):
    CLIENTE = "cliente"
    ASISTENTE = "asistente"
    OPERADOR = "operador"


@dataclass
class Mensaje:
    sesion_id: str
    contenido: str
    origen: OrigenMensaje
    id: Optional[int] = None
    fecha: datetime = field(default_factory=datetime.utcnow)
    es_automatico: bool = False
