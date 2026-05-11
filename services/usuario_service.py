from database import db
from models import Usuario
from utils.datetime_utils import now
from services.telegram_service import enviarMensaje

def getOrCreateUsuario(chat_id, nombre):
    usuario = Usuario.query.filter_by(IdChat=chat_id).first()
    
    if not usuario:
        usuario = Usuario(Nombre=nombre, IdChat=chat_id, IdTipo=1)
        db.session.add(usuario)
        db.session.commit()
    
    return usuario

def baja(usuario, chat_id):
    usuario.FechaBaja = now()
    db.session.commit()
    enviarMensaje(chat_id, "Lamentamos que te vayas 😢. Si cambias de opinión, siempre podés volver a escribir /start")
