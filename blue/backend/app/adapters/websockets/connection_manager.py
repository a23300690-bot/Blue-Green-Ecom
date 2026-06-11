from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """
    Gestiona conexiones WebSocket activas.
    Cada sesion_id puede tener:
    - Una conexion de cliente
    - Multiples conexiones de admin/operador
    """

    def __init__(self):
        self.clientes: Dict[str, WebSocket] = {}
        self.admins: Dict[str, List[WebSocket]] = {}

    async def conectar_cliente(self, sesion_id: str, websocket: WebSocket):
        await websocket.accept()
        self.clientes[sesion_id] = websocket

    async def conectar_admin(self, sesion_id: str, websocket: WebSocket):
        await websocket.accept()
        if sesion_id not in self.admins:
            self.admins[sesion_id] = []
        self.admins[sesion_id].append(websocket)

    def desconectar(self, sesion_id: str):
        self.clientes.pop(sesion_id, None)

    def desconectar_admin(self, sesion_id: str, websocket: WebSocket):
        if sesion_id in self.admins:
            self.admins[sesion_id] = [
                ws for ws in self.admins[sesion_id] if ws != websocket
            ]

    async def enviar_a_cliente(self, sesion_id: str, mensaje: dict):
        ws = self.clientes.get(sesion_id)
        if ws:
            try:
                await ws.send_json(mensaje)
            except Exception:
                self.desconectar(sesion_id)

    async def enviar_a_admins(self, sesion_id: str, mensaje: dict):
        for ws in self.admins.get(sesion_id, []):
            try:
                await ws.send_json(mensaje)
            except Exception:
                pass

    async def enviar_mensaje(self, sesion_id: str, mensaje: dict):
        await self.enviar_a_cliente(sesion_id, mensaje)
        await self.enviar_a_admins(sesion_id, mensaje)

    async def broadcast(self, mensaje: dict):
        for ws in self.clientes.values():
            try:
                await ws.send_json(mensaje)
            except Exception:
                pass
    
    


manager = ConnectionManager()