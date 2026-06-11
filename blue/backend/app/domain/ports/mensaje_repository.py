from abc import ABC, abstractmethod
from typing import List
from app.domain.models.mensaje import Mensaje


class MensajeRepository(ABC):

    @abstractmethod
    def save(self, mensaje: Mensaje) -> Mensaje:
        pass

    @abstractmethod
    def get_by_sesion(self, sesion_id: str) -> List[Mensaje]:
        pass

    @abstractmethod
    def delete_by_sesion(self, sesion_id: str) -> None:
        pass