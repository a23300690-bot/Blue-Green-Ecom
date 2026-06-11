from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Rol(str, Enum):
    ADMIN = "admin"
    CLIENTE = "cliente"
    OPERADOR = "operador"


@dataclass
@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    email: str
    password_hash: str
    rol: Rol = Rol.CLIENTE
    activo: bool = True
    pregunta_seguridad: Optional[str] = None
    respuesta_seguridad_hash: Optional[str] = None

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("Email invalido")
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacio")

    def es_admin(self) -> bool:
        return self.rol == Rol.ADMIN

    def es_operador(self) -> bool:
        return self.rol in (Rol.ADMIN, Rol.OPERADOR)
