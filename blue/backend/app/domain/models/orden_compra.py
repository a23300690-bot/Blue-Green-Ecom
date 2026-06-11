from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class ItemOrden:
    producto_id: int
    nombre_producto: str
    precio_unitario: float
    cantidad: int

    @property
    def subtotal(self) -> float:
        return round(self.precio_unitario * self.cantidad, 2)


@dataclass
class OrdenCompra:
    id: Optional[int]
    perfil_id: int
    items: List[ItemOrden]
    estado: str = "pendiente"
    fecha: datetime = field(default_factory=datetime.utcnow)
    metodo_pago: str = "efectivo"
    usuario_id: Optional[int] = None

    def __post_init__(self):
        if not self.items:
            raise ValueError("La orden debe tener al menos un producto")

    @property
    def total(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    def cancelar(self):
        if self.estado not in ("pendiente", "confirmada"):
            raise ValueError(f"No se puede cancelar una orden en estado: {self.estado}")
        self.estado = "cancelada"