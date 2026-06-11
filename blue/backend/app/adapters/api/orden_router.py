from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.application.services.orden_service import OrdenService
from app.adapters.dependencies.container import get_orden_service
from app.adapters.dependencies.auth_dependency import get_current_user, solo_admin, solo_operador

router = APIRouter(prefix="/ordenes", tags=["Ordenes"])


class ItemIn(BaseModel):
    producto_id: int
    cantidad: int


class OrdenIn(BaseModel):
    perfil_id: int
    items: List[ItemIn]
    metodo_pago: str = "efectivo"


@router.post("/", summary="Crear orden (usuario autenticado)")
def create_orden(
    data: OrdenIn,
    current_user=Depends(get_current_user),
    service: OrdenService = Depends(get_orden_service),
):
    try:
        items = [i.model_dump() for i in data.items]
        return service.create_orden(
            perfil_id=data.perfil_id,
            items_data=items,
            metodo_pago=data.metodo_pago,
            usuario_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get("/mis-ordenes", summary="Ver mis ordenes (cliente)")
def mis_ordenes(
    current_user=Depends(get_current_user),
    service: OrdenService = Depends(get_orden_service),
):
    return service.list_ordenes_usuario(current_user.id)


@router.get("/", summary="Listar todas las ordenes (admin/operador)")
def list_ordenes(
    current_user=Depends(solo_operador),
    service: OrdenService = Depends(get_orden_service),
):
    return service.list_ordenes()


@router.get("/{id}", summary="Ver orden (usuario autenticado)")
def get_orden(
    id: int,
    current_user=Depends(get_current_user),
    service: OrdenService = Depends(get_orden_service),
):
    try:
        return service.get_orden(id)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@router.patch("/{id}/cancelar", summary="Cancelar orden (solo admin)")
def cancelar_orden(
    id: int,
    current_user=Depends(solo_admin),
    service: OrdenService = Depends(get_orden_service),
):
    try:
        service.cancelar_orden(id)
        return {"mensaje": "Orden cancelada"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))