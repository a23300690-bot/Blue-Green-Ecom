from typing import List, Optional
from app.domain.models.producto import Producto
from app.domain.ports.producto_repository import ProductoRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLProductoRepository(ProductoRepository):

    def create(self, producto: Producto) -> Producto:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url) VALUES (%s, %s, %s, %s, %s)",
            (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.imagen_url),
        )
        conn.commit()
        producto.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return producto

    def get_all(self) -> List[Producto]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Producto(id=r["id"], nombre=r["nombre"], descripcion=r["descripcion"],
                         precio=float(r["precio"]), stock=r["stock"], imagen_url=r.get("imagen_url"))
                for r in rows]

    def get_by_id(self, id: int) -> Optional[Producto]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return Producto(id=row["id"], nombre=row["nombre"], descripcion=row["descripcion"],
                        precio=float(row["precio"]), stock=row["stock"], imagen_url=row.get("imagen_url"))

    def update(self, producto: Producto) -> Producto:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, imagen_url=%s WHERE id=%s",
            (producto.nombre, producto.descripcion, producto.precio, producto.stock,
             producto.imagen_url, producto.id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return producto

    def delete(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conn.commit()
        afectados = cursor.rowcount
        cursor.close()
        conn.close()
        return afectados > 0
