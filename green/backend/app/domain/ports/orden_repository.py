from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.orden_compra import OrdenCompra


class OrdenRepository(ABC):

    @abstractmethod
    def create(self, orden: OrdenCompra) -> OrdenCompra:
        pass

    @abstractmethod
    def get_all(self) -> List[OrdenCompra]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[OrdenCompra]:
        pass

    @abstractmethod
    def update_estado(self, id: int, estado: str) -> bool:
        pass

    @abstractmethod
    def get_by_usuario(self, usuario_id: int) -> List[OrdenCompra]:
        pass