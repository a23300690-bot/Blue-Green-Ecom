from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.producto import Producto


class ProductoRepository(ABC):

    @abstractmethod
    def create(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def get_all(self) -> List[Producto]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def update(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
