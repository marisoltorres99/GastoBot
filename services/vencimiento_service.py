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

def vencimientos(usuario, chat_id):

    lista = (
        Vencimiento.query
        .filter_by(IdUsuario=usuario.Id)
        .order_by(Vencimiento.FechaVencimiento.asc())
        .all()
    )

    if not lista:
        enviarMensaje(chat_id, "📅 No tenés vencimientos registrados")
        return

    texto = "📅 Tus vencimientos:\n\n"

    hoy = now().date()

    for v in lista:

        dias_restantes = (v.FechaVencimiento.date() - hoy).days

        if dias_restantes == 0:
            estado = "🔴 Vence hoy"
        elif dias_restantes <= 3:
            estado = f"🟡 Vence en {dias_restantes} días"
        else:
            estado = f"🟢 Faltan {dias_restantes} días"

        texto += (
            f"• #{v.Id} | "
            f"{v.Nombre} — "
            f"{v.FechaVencimiento.strftime('%Y-%m-%d')} "
            f"({estado})\n"
        )

    enviarMensaje(chat_id, texto)
