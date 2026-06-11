from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from pydantic import BaseModel
from app.application.services.chat_service import ChatService
from app.adapters.dependencies.container import get_chat_service
from app.adapters.websockets.connection_manager import manager
from app.adapters.dependencies.auth_dependency import get_current_user, solo_admin, solo_operador

router = APIRouter(tags=["Chat"])


# ── WebSocket CLIENTE ─────────────────────────────────────────────────────────

@router.websocket("/ws/chat/{sesion_id}")
async def websocket_chat(
    sesion_id: str,
    websocket: WebSocket,
    service: ChatService = Depends(get_chat_service),
):
    await manager.conectar_cliente(sesion_id, websocket)
    try:
        while True:
            texto = await websocket.receive_text()

            resultado = service.procesar_mensaje(
                sesion_id=sesion_id,
                contenido=texto,
            )

            # Enviar respuesta al cliente
            await manager.enviar_a_cliente(sesion_id, {
                "tipo": "respuesta",
                "sesion_id": resultado["sesion_id"],
                "respuesta": resultado["respuesta"],
                "es_automatico": resultado["es_automatico"],
            })

            # Notificar al admin que llegó un mensaje nuevo
            await manager.enviar_a_admins(sesion_id, {
                "tipo": "mensaje_cliente",
                "sesion_id": sesion_id,
                "contenido": texto,
                "origen": "cliente",
            })

    except WebSocketDisconnect:
        manager.desconectar(sesion_id)
        try:
            service.cerrar_sesion(sesion_id)
        except ValueError:
            pass


# ── WebSocket ADMIN ───────────────────────────────────────────────────────────

@router.websocket("/ws/admin/chat/{sesion_id}")
async def websocket_admin_chat(
    sesion_id: str,
    websocket: WebSocket,
    service: ChatService = Depends(get_chat_service),
):
    await manager.conectar_admin(sesion_id, websocket)
    try:
        while True:
            texto = await websocket.receive_text()

            # Guardar mensaje del admin en BD
            service.guardar_mensaje_admin(
                sesion_id=sesion_id,
                contenido=texto,
            )

            # Enviar al cliente
            await manager.enviar_a_cliente(sesion_id, {
                "tipo": "respuesta",
                "sesion_id": sesion_id,
                "respuesta": texto,
                "es_automatico": False,
            })

            # Confirmar al admin que se envió
            await manager.enviar_a_admins(sesion_id, {
                "tipo": "mensaje_admin",
                "sesion_id": sesion_id,
                "contenido": texto,
                "origen": "asistente",
            })

    except WebSocketDisconnect:
        manager.desconectar_admin(sesion_id, websocket)


# ── REST ──────────────────────────────────────────────────────────────────────

class MensajeAdminIn(BaseModel):
    contenido: str


@router.post("/chat/sesion/{sesion_id}/responder", summary="Admin responde manualmente (REST fallback)")
def responder_manualmente(
    sesion_id: str,
    data: MensajeAdminIn,
    current_user=Depends(solo_operador),
    service: ChatService = Depends(get_chat_service),
):
    service.guardar_mensaje_admin(sesion_id=sesion_id, contenido=data.contenido)
    return {"mensaje": "Respuesta enviada", "contenido": data.contenido}


@router.post("/chat/sesion", summary="Iniciar sesion de chat")
def iniciar_sesion(
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    sesion = service.iniciar_sesion(usuario_id=current_user.id)
    return {
        "sesion_id": sesion.id,
        "mensaje": "Sesion iniciada. Conéctate por WebSocket a /ws/chat/" + sesion.id,
    }


@router.post("/chat/sesion/anonima", summary="Iniciar sesion de chat sin autenticacion")
def iniciar_sesion_anonima(service: ChatService = Depends(get_chat_service)):
    sesion = service.iniciar_sesion()
    return {
        "sesion_id": sesion.id,
        "mensaje": "Sesion iniciada. Conéctate por WebSocket a /ws/chat/" + sesion.id,
    }


@router.get("/chat/sesion/{sesion_id}/historial", summary="Ver historial de la sesion")
def historial(
    sesion_id: str,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return service.obtener_historial(sesion_id)


@router.patch("/chat/sesion/{sesion_id}/cerrar", summary="Cerrar sesion (admin)")
def cerrar_sesion(
    sesion_id: str,
    current_user=Depends(solo_admin),
    service: ChatService = Depends(get_chat_service),
):
    try:
        sesion = service.cerrar_sesion(sesion_id)
        return {"sesion_id": sesion.id, "estado": sesion.estado}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@router.get("/chat/sesiones", summary="Listar todas las sesiones (admin)")
def listar_sesiones(
    current_user=Depends(solo_admin),
    service: ChatService = Depends(get_chat_service),
):
    return service.listar_sesiones()


@router.delete("/chat/sesion/{sesion_id}", summary="Eliminar sesion (admin)")
def eliminar_sesion(
    sesion_id: str,
    current_user=Depends(solo_admin),
    service: ChatService = Depends(get_chat_service),
):
    try:
        manager.desconectar(sesion_id)
    except Exception:
        pass
    try:
        service.eliminar_sesion(sesion_id)
        return {"mensaje": "Sesion eliminada"}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@router.delete("/chat/sesiones/cerradas", summary="Eliminar todas las sesiones cerradas (admin)")
def eliminar_sesiones_cerradas(
    current_user=Depends(solo_admin),
    service: ChatService = Depends(get_chat_service),
):
    eliminadas = service.eliminar_sesiones_cerradas()
    return {"eliminadas": eliminadas, "mensaje": f"{eliminadas} sesiones eliminadas"}