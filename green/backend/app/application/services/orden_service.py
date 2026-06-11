from typing import List
from app.domain.models.orden_compra import OrdenCompra, ItemOrden
from app.domain.ports.orden_repository import OrdenRepository
from app.domain.ports.perfil_repository import PerfilRepository
from app.domain.ports.producto_repository import ProductoRepository


class OrdenService:

    def __init__(self, orden_repo: OrdenRepository, perfil_repo: PerfilRepository,
                 producto_repo: ProductoRepository):
        self.orden_repo = orden_repo
        self.perfil_repo = perfil_repo
        self.producto_repo = producto_repo

    def create_orden(self, perfil_id: int, items_data: list,
                     metodo_pago: str = "efectivo", usuario_id: int = None) -> OrdenCompra:
        perfil = self.perfil_repo.get_by_id(perfil_id)
        if not perfil:
            raise ValueError(f"Perfil {perfil_id} no encontrado")
        items = []
        for dato in items_data:
            producto = self.producto_repo.get_by_id(dato["producto_id"])
            if not producto:
                raise ValueError(f"Producto {dato['producto_id']} no encontrado")
            producto.reducir_stock(dato["cantidad"])
            self.producto_repo.update(producto)
            items.append(ItemOrden(producto_id=producto.id, nombre_producto=producto.nombre,
                                   precio_unitario=producto.precio, cantidad=dato["cantidad"]))
        orden = OrdenCompra(id=None, perfil_id=perfil_id, items=items,
                            metodo_pago=metodo_pago, usuario_id=usuario_id)
        return self.orden_repo.create(orden)

    def list_ordenes(self) -> List[OrdenCompra]:
        return self.orden_repo.get_all()

    def list_ordenes_usuario(self, usuario_id: int) -> List[OrdenCompra]:
        return self.orden_repo.get_by_usuario(usuario_id)

    def get_orden(self, id: int) -> OrdenCompra:
        orden = self.orden_repo.get_by_id(id)
        if not orden:
            raise ValueError(f"Orden {id} no encontrada")
        return orden

    def cancelar_orden(self, id: int) -> bool:
        orden = self.get_orden(id)
        orden.cancelar()
        return self.orden_repo.update_estado(id, orden.estado)