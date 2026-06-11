from typing import List, Optional
from app.domain.models.pregunta_frecuente import PreguntaFrecuente
from app.domain.ports.faq_repository import FaqRepository
from app.infrastructure.db.mysql.db_connection import get_connection


class MySQLFaqRepository(FaqRepository):

    def save(self, faq: PreguntaFrecuente) -> PreguntaFrecuente:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO preguntas_frecuentes (palabras_clave, respuesta, activa) VALUES (%s, %s, %s)",
            (faq.palabras_clave, faq.respuesta, faq.activa),
        )
        conn.commit()
        faq.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return faq

    def get_all_activas(self) -> List[PreguntaFrecuente]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM preguntas_frecuentes WHERE activa = 1")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [PreguntaFrecuente(id=r["id"], palabras_clave=r["palabras_clave"],
                                  respuesta=r["respuesta"], activa=bool(r["activa"]))
                for r in rows]

    def delete(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE preguntas_frecuentes SET activa = 0 WHERE id = %s", (id,))
        conn.commit()
        afectados = cursor.rowcount
        cursor.close()
        conn.close()
        return afectados > 0

    def buscar_por_palabras_clave(self, texto: str) -> Optional[PreguntaFrecuente]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        palabras = texto.lower().split()
        for palabra in palabras:
            if len(palabra) < 3:
                continue
            cursor.execute(
                "SELECT * FROM preguntas_frecuentes WHERE activa = 1 AND LOWER(palabras_clave) LIKE %s LIMIT 1",
                (f"%{palabra}%",),
            )
            row = cursor.fetchone()
            if row:
                cursor.close()
                conn.close()
                return PreguntaFrecuente(id=row["id"], palabras_clave=row["palabras_clave"],
                                         respuesta=row["respuesta"], activa=bool(row["activa"]))
        cursor.close()
        conn.close()
        return None
