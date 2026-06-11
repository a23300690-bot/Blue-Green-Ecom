from typing import List, Optional
from app.domain.models.producto import Producto
from app.domain.ports.producto_repository import ProductoRepository


class ProductoService:

    def __init__(self, repository: ProductoRepository):
        self.repository = repository

    def create_producto(self, nombre: str, descripcion: str, precio: float,
                        stock: int, imagen_url: Optional[str] = None) -> Producto:
        producto = Producto(id=None, nombre=nombre, descripcion=descripcion,
                            precio=precio, stock=stock, imagen_url=imagen_url)
        return self.repository.create(producto)

    def list_productos(self) -> List[Producto]:
        return self.repository.get_all()

    def get_producto(self, id: int) -> Producto:
        producto = self.repository.get_by_id(id)
        if not producto:
            raise ValueError(f"Producto {id} no encontrado")
        return producto

    def update_producto(self, id: int, datos: dict) -> Producto:
        producto = self.get_producto(id)
        for campo, valor in datos.items():
            if valor is not None:
                setattr(producto, campo, valor)
        return self.repository.update(producto)

    def delete_producto(self, id: int) -> bool:
        self.get_producto(id)
        return self.repository.delete(id)
