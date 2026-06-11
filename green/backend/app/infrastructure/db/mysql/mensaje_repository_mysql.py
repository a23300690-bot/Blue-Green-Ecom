from typing import List
from app.domain.models.mensaje import Mensaje, OrigenMensaje
from app.domain.ports.mensaje_repository import MensajeRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLMensajeRepository(MensajeRepository):

    def save(self, mensaje: Mensaje) -> Mensaje:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensajes (sesion_id, contenido, origen, fecha, es_automatico) VALUES (%s, %s, %s, %s, %s)",
            (mensaje.sesion_id, mensaje.contenido, mensaje.origen.value,
             mensaje.fecha, mensaje.es_automatico),
        )
        conn.commit()
        mensaje.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return mensaje

    def get_by_sesion(self, sesion_id: str) -> List[Mensaje]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM mensajes WHERE sesion_id = %s ORDER BY fecha ASC",
            (sesion_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            Mensaje(id=r["id"], sesion_id=r["sesion_id"], contenido=r["contenido"],
                    origen=OrigenMensaje(r["origen"]), fecha=r["fecha"],
                    es_automatico=bool(r["es_automatico"]))
            for r in rows
        ]

    def delete_by_sesion(self, sesion_id: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mensajes WHERE sesion_id = %s", (sesion_id,))
        conn.commit()
        cursor.close()
        conn.close()