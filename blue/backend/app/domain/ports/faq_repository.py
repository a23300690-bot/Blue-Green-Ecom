from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.pregunta_frecuente import PreguntaFrecuente


class FaqRepository(ABC):

    @abstractmethod
    def save(self, faq: PreguntaFrecuente) -> PreguntaFrecuente:
        pass

    @abstractmethod
    def get_all_activas(self) -> List[PreguntaFrecuente]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def buscar_por_palabras_clave(self, texto: str) -> Optional[PreguntaFrecuente]:
        pass
