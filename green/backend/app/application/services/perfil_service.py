from typing import List
from app.domain.models.perfil_compra import PerfilCompra
from app.domain.ports.perfil_repository import PerfilRepository


class PerfilService:

    def __init__(self, repository: PerfilRepository):
        self.repository = repository

    def create_perfil(self, nombre: str, email: str, telefono: str, direccion: str) -> PerfilCompra:
        perfil = PerfilCompra(id=None, nombre=nombre, email=email,
                              telefono=telefono, direccion=direccion)
        return self.repository.create(perfil)

    def list_perfiles(self) -> List[PerfilCompra]:
        return self.repository.get_all()

    def get_perfil(self, id: int) -> PerfilCompra:
        perfil = self.repository.get_by_id(id)
        if not perfil:
            raise ValueError(f"Perfil {id} no encontrado")
        return perfil

    def delete_perfil(self, id: int) -> bool:
        self.get_perfil(id)
        return self.repository.delete(id)
