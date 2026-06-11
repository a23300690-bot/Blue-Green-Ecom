from abc import ABC, abstractmethod


class AuthPort(ABC):

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass
