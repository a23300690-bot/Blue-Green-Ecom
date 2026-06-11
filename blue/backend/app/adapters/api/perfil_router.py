from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.services.perfil_service import PerfilService
from app.adapters.dependencies.container import get_perfil_service
from app.adapters.dependencies.auth_dependency import get_current_user, solo_admin

router = APIRouter(prefix="/perfiles", tags=["Perfiles"])


class PerfilIn(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str


# Cliente autenticado puede crear su perfil
@router.post("/", summary="Crear perfil (usuario autenticado)")
def create_perfil(
    data: PerfilIn,
    current_user=Depends(get_current_user),
    service: PerfilService = Depends(get_perfil_service),
):
    try:
        return service.create_perfil(**data.model_dump())
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


# Solo admin puede ver todos los perfiles
@router.get("/", summary="Listar perfiles (solo admin)")
def list_perfiles(
    current_user=Depends(solo_admin),
    service: PerfilService = Depends(get_perfil_service),
):
    return service.list_perfiles()


@router.get("/{id}", summary="Ver perfil (usuario autenticado)")
def get_perfil(
    id: int,
    current_user=Depends(get_current_user),
    service: PerfilService = Depends(get_perfil_service),
):
    try:
        return service.get_perfil(id)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@router.delete("/{id}", summary="Eliminar perfil (solo admin)")
def delete_perfil(
    id: int,
    current_user=Depends(solo_admin),
    service: PerfilService = Depends(get_perfil_service),
):
    try:
        service.delete_perfil(id)
        return {"mensaje": "Perfil eliminado"}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
