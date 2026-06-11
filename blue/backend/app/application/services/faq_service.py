from typing import List
from app.domain.models.pregunta_frecuente import PreguntaFrecuente
from app.domain.ports.faq_repository import FaqRepository


class FaqService:

    def __init__(self, repo: FaqRepository):
        self.repo = repo

    def create_faq(self, palabras_clave: str, respuesta: str) -> PreguntaFrecuente:
        faq = PreguntaFrecuente(id=None, palabras_clave=palabras_clave, respuesta=respuesta)
        return self.repo.save(faq)

    def list_faqs(self) -> List[PreguntaFrecuente]:
        return self.repo.get_all_activas()

    def delete_faq(self, id: int) -> bool:
        return self.repo.delete(id)
