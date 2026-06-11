from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.sesion_chat import SesionChat


class SesionRepository(ABC):

    @abstractmethod
    def save(self, sesion: SesionChat) -> SesionChat:
        pass

    @abstractmethod
    def get_by_id(self, sesion_id: str) -> Optional[SesionChat]:
        pass

    @abstractmethod
    def update(self, sesion: SesionChat) -> SesionChat:
        pass

    @abstractmethod
    def get_all(self) -> List[SesionChat]:
        pass

    @abstractmethod
    def delete(self, sesion_id: str) -> None:
        pass