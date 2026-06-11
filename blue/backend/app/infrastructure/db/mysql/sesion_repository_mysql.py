from typing import List, Optional
from app.domain.models.sesion_chat import SesionChat, EstadoSesion
from app.domain.ports.sesion_repository import SesionRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLSesionRepository(SesionRepository):

    def save(self, sesion: SesionChat) -> SesionChat:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sesiones_chat (id, usuario_id, estado, fecha_inicio) VALUES (%s, %s, %s, %s)",
            (sesion.id, sesion.usuario_id, sesion.estado.value, sesion.fecha_inicio),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return sesion

    def get_by_id(self, sesion_id: str) -> Optional[SesionChat]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sesiones_chat WHERE id = %s", (sesion_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return SesionChat(id=row["id"], usuario_id=row["usuario_id"],
                          estado=EstadoSesion(row["estado"]),
                          fecha_inicio=row["fecha_inicio"], fecha_fin=row["fecha_fin"])

    def update(self, sesion: SesionChat) -> SesionChat:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sesiones_chat SET estado = %s, fecha_fin = %s WHERE id = %s",
            (sesion.estado.value, sesion.fecha_fin, sesion.id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return sesion

    def get_all(self) -> List[SesionChat]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sesiones_chat ORDER BY fecha_inicio DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [SesionChat(id=r["id"], usuario_id=r["usuario_id"],
                           estado=EstadoSesion(r["estado"]),
                           fecha_inicio=r["fecha_inicio"], fecha_fin=r["fecha_fin"])
                for r in rows]

    def delete(self, sesion_id: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sesiones_chat WHERE id = %s", (sesion_id,))
        conn.commit()
        cursor.close()
        conn.close()