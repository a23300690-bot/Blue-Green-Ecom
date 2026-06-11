import os, shutil, uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from app.application.services.producto_service import ProductoService
from app.adapters.dependencies.container import get_producto_service
from app.adapters.dependencies.auth_dependency import get_current_user, solo_admin, solo_operador

router = APIRouter(prefix="/productos", tags=["Productos"])

IMAGES_DIR = "static/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

HERO_EXTS = ("jpg", "jpeg", "png", "webp")


def _save_image(imagen: UploadFile, filename: str) -> str:
    ext = imagen.filename.split(".")[-1].lower()
    if ext not in HERO_EXTS:
        raise HTTPException(400, detail="Formato de imagen no permitido")
    ruta = os.path.join(IMAGES_DIR, filename)
    with open(ruta, "wb") as f:
        shutil.copyfileobj(imagen.file, f)
    return f"/static/images/{filename}"


# ── CATÁLOGO PÚBLICO ──────────────────────────────────
@router.get("/", summary="Ver catálogo (público)")
def list_productos(service: ProductoService = Depends(get_producto_service)):
    return service.list_productos()


@router.get("/{id}", summary="Ver producto (público)")
def get_producto(id: int, service: ProductoService = Depends(get_producto_service)):
    try:
        return service.get_producto(id)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


# ── HERO IMAGE ────────────────────────────────────────
@router.post("/hero", summary="Subir imagen del hero (admin/operador)")
async def set_hero(
    imagen: UploadFile = File(...),
    current_user=Depends(solo_operador),
):
    # Elimina cualquier hero anterior
    for ext in HERO_EXTS:
        path = os.path.join(IMAGES_DIR, f"hero.{ext}")
        if os.path.exists(path):
            os.remove(path)

    ext = imagen.filename.split(".")[-1].lower()
    if ext not in HERO_EXTS:
        raise HTTPException(400, detail="Formato no permitido. Usa JPG, PNG o WebP.")

    ruta = os.path.join(IMAGES_DIR, f"hero.{ext}")
    with open(ruta, "wb") as f:
        shutil.copyfileobj(imagen.file, f)

    return {"imagen_url": f"/static/images/hero.{ext}", "mensaje": "Imagen del hero actualizada"}


@router.delete("/hero", summary="Eliminar imagen del hero (admin/operador)")
def delete_hero(current_user=Depends(solo_operador)):
    eliminado = False
    for ext in HERO_EXTS:
        path = os.path.join(IMAGES_DIR, f"hero.{ext}")
        if os.path.exists(path):
            os.remove(path)
            eliminado = True
    if not eliminado:
        raise HTTPException(404, detail="No hay imagen del hero para eliminar")
    return {"mensaje": "Imagen del hero eliminada"}


# ── CRUD PRODUCTOS ────────────────────────────────────
@router.post("/", summary="Crear producto con imagen (admin/operador)")
async def create_producto(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    imagen: Optional[UploadFile] = File(None),
    current_user=Depends(solo_operador),
    service: ProductoService = Depends(get_producto_service),
):
    imagen_url = None
    if imagen and imagen.filename:
        nombre_archivo = f"{uuid.uuid4()}.{imagen.filename.split('.')[-1].lower()}"
        imagen_url = _save_image(imagen, nombre_archivo)
    try:
        return service.create_producto(nombre=nombre, descripcion=descripcion,
                                       precio=precio, stock=stock, imagen_url=imagen_url)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.put("/{id}", summary="Actualizar producto (admin/operador)")
async def update_producto(
    id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    precio: Optional[float] = Form(None),
    stock: Optional[int] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    current_user=Depends(solo_operador),
    service: ProductoService = Depends(get_producto_service),
):
    datos = {}
    if nombre:      datos["nombre"] = nombre
    if descripcion: datos["descripcion"] = descripcion
    if precio:      datos["precio"] = precio
    if stock is not None: datos["stock"] = stock
    if imagen and imagen.filename:
        nombre_archivo = f"{uuid.uuid4()}.{imagen.filename.split('.')[-1].lower()}"
        datos["imagen_url"] = _save_image(imagen, nombre_archivo)
    try:
        return service.update_producto(id, datos)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.delete("/{id}", summary="Eliminar producto (solo admin)")
def delete_producto(
    id: int,
    current_user=Depends(solo_admin),
    service: ProductoService = Depends(get_producto_service),
):
    try:
        service.delete_producto(id)
        return {"mensaje": "Producto eliminado"}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
