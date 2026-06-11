from typing import List, Optional
from app.domain.models.usuario import Usuario, Rol
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLUsuarioRepository(UsuarioRepository):

    def _row_to_usuario(self, row: dict) -> Usuario:
        return Usuario(
            id=row["id"], nombre=row["nombre"], email=row["email"],
            password_hash=row["password_hash"], rol=Rol(row["rol"]), activo=row["activo"],
            pregunta_seguridad=row.get("pregunta_seguridad"),
            respuesta_seguridad_hash=row.get("respuesta_seguridad_hash"),
        )

    def create(self, usuario: Usuario) -> Usuario:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, rol, activo, pregunta_seguridad, respuesta_seguridad_hash) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (usuario.nombre, usuario.email, usuario.password_hash, usuario.rol.value,
             usuario.activo, usuario.pregunta_seguridad, usuario.respuesta_seguridad_hash),
        )
        conn.commit()
        usuario.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return usuario

    def get_by_email(self, email: str) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND activo = 1", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._row_to_usuario(row) if row else None

    def get_by_email_completo(self, email: str) -> Optional[Usuario]:
        return self.get_by_email(email)

    def get_by_id(self, id: int) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s AND activo = 1", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._row_to_usuario(row) if row else None

    def get_all(self) -> List[Usuario]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE activo = 1")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [self._row_to_usuario(r) for r in rows]

    def delete(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = %s", (id,))
        conn.commit()
        afectados = cursor.rowcount
        cursor.close()
        conn.close()
        return afectados > 0

    def update_password(self, id: int, nuevo_hash: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET password_hash = %s WHERE id = %s", (nuevo_hash, id))
        conn.commit()
        cursor.close()
        conn.close()

    def update_seguridad(self, id: int, pregunta: str, respuesta_hash: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET pregunta_seguridad = %s, respuesta_seguridad_hash = %s WHERE id = %s",
            (pregunta, respuesta_hash, id)
        )
        conn.commit()
        cursor.close()
        conn.close()