from typing import List, Optional
from app.domain.models.perfil_compra import PerfilCompra
from app.domain.ports.perfil_repository import PerfilRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLPerfilRepository(PerfilRepository):

    def create(self, perfil: PerfilCompra) -> PerfilCompra:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perfiles_compra WHERE email = %s", (perfil.email,))
        existente = cursor.fetchone()
        if existente:
            cursor.execute(
                "UPDATE perfiles_compra SET nombre=%s, telefono=%s, direccion=%s WHERE email=%s",
                (perfil.nombre, perfil.telefono, perfil.direccion, perfil.email),
            )
            conn.commit()
            perfil.id = existente["id"]
        else:
            cursor.execute(
                "INSERT INTO perfiles_compra (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)",
                (perfil.nombre, perfil.email, perfil.telefono, perfil.direccion),
            )
            conn.commit()
            perfil.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return perfil

    def get_all(self) -> List[PerfilCompra]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perfiles_compra")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [PerfilCompra(id=r["id"], nombre=r["nombre"], email=r["email"],
                             telefono=r["telefono"], direccion=r["direccion"]) for r in rows]

    def get_by_id(self, id: int) -> Optional[PerfilCompra]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perfiles_compra WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return PerfilCompra(id=row["id"], nombre=row["nombre"], email=row["email"],
                            telefono=row["telefono"], direccion=row["direccion"])

    def delete(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM perfiles_compra WHERE id = %s", (id,))
        conn.commit()
        afectados = cursor.rowcount
        cursor.close()
        conn.close()
        return afectados > 0