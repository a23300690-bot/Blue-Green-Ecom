from dataclasses import dataclass
from typing import Optional


@dataclass
class PreguntaFrecuente:
    palabras_clave: str
    respuesta: str
    id: Optional[int] = None
    activa: bool = True
