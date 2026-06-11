from passlib.context import CryptContext
from app.domain.models.usuario import Usuario, Rol
from app.domain.ports.usuario_repository import UsuarioRepository
from app.domain.ports.auth_port import AuthPort

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self, usuario_repo: UsuarioRepository, auth_provider: AuthPort):
        self.usuario_repo = usuario_repo
        self.auth_provider = auth_provider

    def registrar(self, nombre: str, email: str, password: str, rol: str = "cliente") -> Usuario:
        existente = self.usuario_repo.get_by_email(email)
        if existente:
            raise ValueError("Ya existe un usuario con ese email")
        password_hash = pwd_context.hash(password)
        usuario = Usuario(id=None, nombre=nombre, email=email,
                          password_hash=password_hash, rol=Rol(rol))
        return self.usuario_repo.create(usuario)

    def login(self, email: str, password: str) -> dict:
        usuario = self.usuario_repo.get_by_email(email)
        if not usuario:
            raise ValueError("Credenciales invalidas")
        if not pwd_context.verify(password, usuario.password_hash):
            raise ValueError("Credenciales invalidas")
        data = {"sub": str(usuario.id), "email": usuario.email, "rol": usuario.rol.value}
        access_token = self.auth_provider.create_access_token(data)
        refresh_token = self.auth_provider.create_refresh_token({"sub": str(usuario.id)})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh(self, refresh_token: str) -> dict:
        payload = self.auth_provider.verify_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Token invalido")
        usuario = self.usuario_repo.get_by_id(int(payload["sub"]))
        if not usuario:
            raise ValueError("Usuario no encontrado")
        data = {"sub": str(usuario.id), "email": usuario.email, "rol": usuario.rol.value}
        new_access_token = self.auth_provider.create_access_token(data)
        return {"access_token": new_access_token, "token_type": "bearer"}

    def obtener_usuario_por_id(self, id: int) -> Usuario:
        usuario = self.usuario_repo.get_by_id(id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario

    def listar_usuarios(self):
        return self.usuario_repo.get_all()

    def eliminar_usuario(self, id: int) -> bool:
        self.obtener_usuario_por_id(id)
        return self.usuario_repo.delete(id)

    def configurar_seguridad(self, usuario_id: int, pregunta: str, respuesta: str) -> None:
        respuesta_hash = pwd_context.hash(respuesta.strip().lower())
        self.usuario_repo.update_seguridad(usuario_id, pregunta, respuesta_hash)

    def obtener_pregunta(self, email: str) -> str:
        usuario = self.usuario_repo.get_by_email_completo(email)
        if not usuario or not usuario.pregunta_seguridad:
            raise ValueError("No se encontró una pregunta de seguridad para ese email")
        return usuario.pregunta_seguridad

    def recuperar_password(self, email: str, respuesta: str, nueva_password: str) -> None:
        usuario = self.usuario_repo.get_by_email_completo(email)
        if not usuario:
            raise ValueError("Email no encontrado")
        if not usuario.respuesta_seguridad_hash:
            raise ValueError("Este usuario no tiene pregunta de seguridad configurada")
        if not pwd_context.verify(respuesta.strip().lower(), usuario.respuesta_seguridad_hash):
            raise ValueError("Respuesta incorrecta")
        nuevo_hash = pwd_context.hash(nueva_password)
        self.usuario_repo.update_password(usuario.id, nuevo_hash)