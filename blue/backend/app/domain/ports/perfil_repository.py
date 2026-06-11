from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.perfil_compra import PerfilCompra


class PerfilRepository(ABC):

    @abstractmethod
    def create(self, perfil: PerfilCompra) -> PerfilCompra:
        pass

    @abstractmethod
    def get_all(self) -> List[PerfilCompra]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[PerfilCompra]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
