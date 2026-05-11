from database import db
from services.telegram_service import enviarMensaje
from datetime import datetime
from utils.datetime_utils import now
from models import Vencimiento

def nuevoVencimiento(usuario, chat_id, args):
    try:
        partes = args.split(" ", 1)
        vencimiento_nombre = partes[0].strip().lower()
        fecha = datetime.strptime(partes[1], "%Y-%m-%d")
    except (ValueError, IndexError):
        enviarMensaje(chat_id, "🚫 Formato incorrecto. Usá: /vencimiento luz 2026-05-20")
        return
    
    if fecha.date() < now().date():
        enviarMensaje(chat_id, "🚫 Debés ingresar una fecha posterior al día de hoy.")
        return

    if not vencimiento_nombre:
        enviarMensaje(chat_id, "🚫 Debés indicar un vencimiento")
        return
    
    existe = Vencimiento.query.filter_by(
        Nombre=vencimiento_nombre,
        IdUsuario=usuario.Id
        ).first()
    
    if existe:
        enviarMensaje(chat_id, 
        "✋ Ya registraste un vencimiento con ese nombre")
        return

    vencimiento = Vencimiento(Nombre=vencimiento_nombre, FechaVencimiento=fecha, IdUsuario=usuario.Id)
    db.session.add(vencimiento)
    db.session.commit()
    enviarMensaje(chat_id, f"✅ Vencimiento de {vencimiento_nombre} en '{fecha.strftime("%Y-%m-%d")}' registrado.")
