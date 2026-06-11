from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.services.faq_service import FaqService
from app.adapters.dependencies.container import get_faq_service
from app.adapters.dependencies.auth_dependency import solo_admin

router = APIRouter(prefix="/faq", tags=["Preguntas Frecuentes"])


class FaqIn(BaseModel):
    palabras_clave: str
    respuesta: str


# Admin gestiona las FAQs, clientes solo las leen
@router.post("/", summary="Crear pregunta frecuente (admin)")
def create_faq(
    data: FaqIn,
    current_user=Depends(solo_admin),
    service: FaqService = Depends(get_faq_service),
):
    return service.create_faq(palabras_clave=data.palabras_clave, respuesta=data.respuesta)


@router.get("/", summary="Listar preguntas frecuentes (publico)")
def list_faqs(service: FaqService = Depends(get_faq_service)):
    return service.list_faqs()


@router.delete("/{id}", summary="Eliminar pregunta frecuente (admin)")
def delete_faq(
    id: int,
    current_user=Depends(solo_admin),
    service: FaqService = Depends(get_faq_service),
):
    if not service.delete_faq(id):
        raise HTTPException(404, detail="FAQ no encontrada")
    return {"mensaje": "FAQ eliminada"}
