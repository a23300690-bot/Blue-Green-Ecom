from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoSesion(str, Enum):
    ACTIVA = "activa"
    CERRADA = "cerrada"
    ESCALADA = "escalada"


@dataclass
class SesionChat:
    id: str
    usuario_id: Optional[int] = None
    estado: EstadoSesion = EstadoSesion.ACTIVA
    fecha_inicio: datetime = field(default_factory=datetime.utcnow)
    fecha_fin: Optional[datetime] = None

    def cerrar(self):
        self.estado = EstadoSesion.CERRADA
        self.fecha_fin = datetime.utcnow()

    def escalar(self):
        self.estado = EstadoSesion.ESCALADA
