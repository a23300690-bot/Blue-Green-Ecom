from app.infrastructure.db.mysql.usuario_repository_mysql import MySQLUsuarioRepository
from app.infrastructure.db.mysql.producto_repository_mysql import MySQLProductoRepository
from app.infrastructure.db.mysql.perfil_repository_mysql import MySQLPerfilRepository
from app.infrastructure.db.mysql.orden_repository_mysql import MySQLOrdenRepository
from app.infrastructure.db.mysql.mensaje_repository_mysql import MySQLMensajeRepository
from app.infrastructure.db.mysql.sesion_repository_mysql import MySQLSesionRepository
from app.infrastructure.db.mysql.faq_repository_mysql import MySQLFaqRepository
from app.infrastructure.auth.jwt_service import JWTService
from app.infrastructure.chat.keyword_respuesta_service import KeywordRespuestaService
from app.application.services.auth_service import AuthService
from app.application.services.producto_service import ProductoService
from app.application.services.perfil_service import PerfilService
from app.application.services.orden_service import OrdenService
from app.application.services.chat_service import ChatService
from app.application.services.faq_service import FaqService


def get_auth_service() -> AuthService:
    return AuthService(
        usuario_repo=MySQLUsuarioRepository(),
        auth_provider=JWTService(),
    )

def get_producto_service() -> ProductoService:
    return ProductoService(repository=MySQLProductoRepository())

def get_perfil_service() -> PerfilService:
    return PerfilService(repository=MySQLPerfilRepository())

def get_orden_service() -> OrdenService:
    return OrdenService(
        orden_repo=MySQLOrdenRepository(),
        perfil_repo=MySQLPerfilRepository(),
        producto_repo=MySQLProductoRepository(),
    )

def get_faq_service() -> FaqService:
    return FaqService(repo=MySQLFaqRepository())

def get_chat_service() -> ChatService:
    faq_repo = MySQLFaqRepository()
    return ChatService(
        mensaje_repo=MySQLMensajeRepository(),
        sesion_repo=MySQLSesionRepository(),
        respuesta_engine=KeywordRespuestaService(faq_repo=faq_repo),
    )
