from database import db
from models import Categoria
from services.telegram_service import enviarMensaje

def getOrCreateCategoria(nombre, id_usuario):
    nombre = nombre.strip().lower()
    categoria = Categoria.query.filter(db.func.lower(Categoria.Nombre) == nombre, Categoria.IdUsuario == id_usuario).first()
    
    if not categoria:
        categoria = Categoria(Nombre=nombre, IdUsuario=id_usuario)
        db.session.add(categoria)
        db.session.commit()
    return categoria

def categorias(usuario, chat_id):
    lista = Categoria.query.filter_by(IdUsuario=usuario.Id).order_by(Categoria.Nombre).all()

    if not lista:
        enviarMensaje(chat_id, "No tenés categorías creadas 😪")
        return

    texto = "🗒️ Tus categorías:\n\n"
    for c in lista:
        texto += f"• {c.Nombre}\n"
    enviarMensaje(chat_id, texto)