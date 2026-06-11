from typing import List, Optional
from app.domain.models.orden_compra import OrdenCompra, ItemOrden
from app.domain.ports.orden_repository import OrdenRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLOrdenRepository(OrdenRepository):

    def create(self, orden: OrdenCompra) -> OrdenCompra:
        conn = get_connection()
        cursor = conn.cursor()
        total = round(sum(i.precio_unitario * i.cantidad for i in orden.items), 2)
        cursor.execute(
            "INSERT INTO ordenes_compra (perfil_id, estado, total, fecha, metodo_pago, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (orden.perfil_id, orden.estado, total, orden.fecha, orden.metodo_pago, orden.usuario_id),
        )
        orden_id = cursor.lastrowid
        for item in orden.items:
            cursor.execute(
                "INSERT INTO items_orden (orden_id, producto_id, nombre_producto, precio_unitario, cantidad) VALUES (%s, %s, %s, %s, %s)",
                (orden_id, item.producto_id, item.nombre_producto, item.precio_unitario, item.cantidad),
            )
        conn.commit()
        orden.id = orden_id
        cursor.close()
        conn.close()
        return orden

    def get_all(self) -> List[OrdenCompra]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ordenes_compra")
        ordenes_rows = cursor.fetchall()
        ordenes = []
        for row in ordenes_rows:
            cursor.execute("SELECT * FROM items_orden WHERE orden_id = %s", (row["id"],))
            items = [ItemOrden(producto_id=i["producto_id"], nombre_producto=i["nombre_producto"],
                               precio_unitario=float(i["precio_unitario"]), cantidad=i["cantidad"])
                     for i in cursor.fetchall()]
            ordenes.append(OrdenCompra(id=row["id"], perfil_id=row["perfil_id"],
                                       estado=row["estado"], fecha=row["fecha"],
                                       metodo_pago=row.get("metodo_pago", "efectivo"),
                                       usuario_id=row.get("usuario_id"),
                                       items=items))
        cursor.close()
        conn.close()
        return ordenes

    def get_by_id(self, id: int) -> Optional[OrdenCompra]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ordenes_compra WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None
        cursor.execute("SELECT * FROM items_orden WHERE orden_id = %s", (id,))
        items = [ItemOrden(producto_id=i["producto_id"], nombre_producto=i["nombre_producto"],
                           precio_unitario=float(i["precio_unitario"]), cantidad=i["cantidad"])
                 for i in cursor.fetchall()]
        cursor.close()
        conn.close()
        return OrdenCompra(id=row["id"], perfil_id=row["perfil_id"],
                           estado=row["estado"], fecha=row["fecha"],
                           metodo_pago=row.get("metodo_pago", "efectivo"),
                           usuario_id=row.get("usuario_id"),
                           items=items)

    def get_by_usuario(self, usuario_id: int) -> List[OrdenCompra]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ordenes_compra WHERE usuario_id = %s ORDER BY fecha DESC", (usuario_id,))
        ordenes_rows = cursor.fetchall()
        ordenes = []
        for row in ordenes_rows:
            cursor.execute("SELECT * FROM items_orden WHERE orden_id = %s", (row["id"],))
            items = [ItemOrden(producto_id=i["producto_id"], nombre_producto=i["nombre_producto"],
                               precio_unitario=float(i["precio_unitario"]), cantidad=i["cantidad"])
                     for i in cursor.fetchall()]
            ordenes.append(OrdenCompra(id=row["id"], perfil_id=row["perfil_id"],
                                       estado=row["estado"], fecha=row["fecha"],
                                       metodo_pago=row.get("metodo_pago", "efectivo"),
                                       usuario_id=row.get("usuario_id"),
                                       items=items))
        cursor.close()
        conn.close()
        return ordenes

    def update_estado(self, id: int, estado: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ordenes_compra SET estado = %s WHERE id = %s", (estado, id))
        conn.commit()
        afectados = cursor.rowcount
        cursor.close()
        conn.close()
        return afectados > 0