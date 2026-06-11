from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.usuario import Usuario


class UsuarioRepository(ABC):

    @abstractmethod
    def create(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_all(self) -> List[Usuario]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def get_by_email_completo(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def update_password(self, id: int, nuevo_hash: str) -> None:
        pass

    @abstractmethod
    def update_seguridad(self, id: int, pregunta: str, respuesta_hash: str) -> None:
        pass