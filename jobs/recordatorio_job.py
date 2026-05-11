from models import Vencimiento
from services.telegram_service import enviarMensaje
from database import db
from utils.datetime_utils import now

def verificar_vencimientos():
    hoy = now().date()

    vencimientos = (
        Vencimiento.query
        .filter_by(Avisado=False)
        .all()
    )

    for v in vencimientos:
        dias_restantes = (v.FechaVencimiento - hoy).days

        if dias_restantes <= 1:
            enviarMensaje(
                v.usuario.IdChat,
                f"📅 Recordatorio: el vencimiento '{v.Nombre}' vence el {v.FechaVencimiento}"
            )

            v.Avisado = True

    db.session.commit()