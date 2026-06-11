import uuid
from typing import List, Optional
from app.domain.models.mensaje import Mensaje, OrigenMensaje
from app.domain.models.sesion_chat import SesionChat
from app.domain.ports.mensaje_repository import MensajeRepository
from app.domain.ports.sesion_repository import SesionRepository
from app.domain.ports.respuesta_automatica_port import RespuestaAutomaticaPort

MENSAJE_SIN_RESPUESTA = (
    "Gracias por tu mensaje. Un agente te atenderá en breve. "
    "Si tienes dudas sobre pedidos, envíos o pagos, puedes preguntar directamente."
)


class ChatService:

    def __init__(
        self,
        mensaje_repo: MensajeRepository,
        sesion_repo: SesionRepository,
        respuesta_engine: RespuestaAutomaticaPort,
    ):
        self.mensaje_repo = mensaje_repo
        self.sesion_repo = sesion_repo
        self.respuesta_engine = respuesta_engine

    def iniciar_sesion(self, usuario_id: Optional[int] = None) -> SesionChat:
        sesion = SesionChat(id=str(uuid.uuid4()), usuario_id=usuario_id)
        return self.sesion_repo.save(sesion)

    def procesar_mensaje(self, sesion_id: str, contenido: str) -> dict:
        sesion = self.sesion_repo.get_by_id(sesion_id)
        if not sesion:
            raise ValueError(f"Sesion {sesion_id} no encontrada")

        # Guardar mensaje del cliente
        mensaje_cliente = Mensaje(
            sesion_id=sesion_id,
            contenido=contenido,
            origen=OrigenMensaje.CLIENTE,
        )
        self.mensaje_repo.save(mensaje_cliente)

        # Buscar respuesta automatica
        respuesta_texto = self.respuesta_engine.buscar_respuesta(contenido)
        es_automatico = respuesta_texto is not None

        if not respuesta_texto:
            respuesta_texto = MENSAJE_SIN_RESPUESTA

        # Guardar respuesta del asistente
        mensaje_respuesta = Mensaje(
            sesion_id=sesion_id,
            contenido=respuesta_texto,
            origen=OrigenMensaje.ASISTENTE,
            es_automatico=es_automatico,
        )
        self.mensaje_repo.save(mensaje_respuesta)

        return {
            "sesion_id": sesion_id,
            "respuesta": respuesta_texto,
            "es_automatico": es_automatico,
        }

    def obtener_historial(self, sesion_id: str) -> List[Mensaje]:
        return self.mensaje_repo.get_by_sesion(sesion_id)

    def cerrar_sesion(self, sesion_id: str) -> SesionChat:
        sesion = self.sesion_repo.get_by_id(sesion_id)
        if not sesion:
            raise ValueError(f"Sesion {sesion_id} no encontrada")
        sesion.cerrar()
        return self.sesion_repo.update(sesion)

    def listar_sesiones(self) -> List[SesionChat]:
        return self.sesion_repo.get_all()

    def eliminar_sesion(self, sesion_id: str) -> None:
        sesion = self.sesion_repo.get_by_id(sesion_id)
        if not sesion:
            raise ValueError(f"Sesion {sesion_id} no encontrada")
        self.mensaje_repo.delete_by_sesion(sesion_id)
        self.sesion_repo.delete(sesion_id)

    def eliminar_sesiones_cerradas(self) -> int:
        sesiones = self.sesion_repo.get_all()
        cerradas = [s for s in sesiones if s.estado == "cerrada"]
        for s in cerradas:
            self.mensaje_repo.delete_by_sesion(s.id)
            self.sesion_repo.delete(s.id)
        return len(cerradas)

    def guardar_mensaje_admin(self, sesion_id: str, contenido: str) -> None:
        sesion = self.sesion_repo.get_by_id(sesion_id)
        if not sesion:
            raise ValueError(f"Sesion {sesion_id} no encontrada")
        mensaje = Mensaje(
            sesion_id=sesion_id,
            contenido=contenido,
            origen=OrigenMensaje.ASISTENTE,
            es_automatico=False,
        )
        self.mensaje_repo.save(mensaje)