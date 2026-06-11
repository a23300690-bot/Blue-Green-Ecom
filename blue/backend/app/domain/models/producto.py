from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    descripcion: str
    precio: float
    stock: int
    imagen_url: Optional[str] = None

    def __post_init__(self):
        if self.precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

    def tiene_stock(self) -> bool:
        return self.stock > 0

    def reducir_stock(self, cantidad: int):
        if self.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}")
        self.stock -= cantidad
