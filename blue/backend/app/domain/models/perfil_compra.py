from dataclasses import dataclass
from typing import Optional


@dataclass
class PerfilCompra:
    id: Optional[int]
    nombre: str
    email: str
    telefono: str
    direccion: str

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("Email invalido")
