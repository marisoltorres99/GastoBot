from models import Gasto, Categoria
from database import db
from services.telegram_service import enviarMensaje
from services.categoria_service import getOrCreateCategoria
from datetime import datetime, timedelta
from utils.datetime_utils import now, TZ

def nuevoGasto(usuario, chat_id, args):
    try:
        partes = args.split(" ", 1)
        monto = float(partes[0])
        categoria_nombre = partes[1].strip().lower()
    except (ValueError, IndexError):
        enviarMensaje(chat_id, "🚫 Formato incorrecto. Usá: /gasto 100.50 comida")
        return

    if monto <= 0:
        enviarMensaje(chat_id, "🚫 El monto debe ser un número positivo")
        return
    
    if not categoria_nombre:
        enviarMensaje(chat_id, "🚫 Debés indicar una categoría")
        return
    
    categoria = getOrCreateCategoria(categoria_nombre, usuario.Id)

    hace_un_minuto = now() - timedelta(minutes=1)
    
    existe = Gasto.query.filter(db.func.abs(db.cast(Gasto.Monto, db.Float) - monto) < 0.001,
    Gasto.IdUsuario == usuario.Id, Gasto.IdCategoria == categoria.Id,Gasto.Fecha >= hace_un_minuto).first()
    
    if existe:
        enviarMensaje(chat_id, 
        "✋ Ya registraste un gasto por el mismo monto y categoria hace menos de 1 minuto! Verificá tus gastos recientes")
        return

    gasto = Gasto(IdCategoria=categoria.Id, Monto=monto, IdUsuario=usuario.Id)
    db.session.add(gasto)
    db.session.commit()
    enviarMensaje(chat_id, f"✅ Gasto de ${monto} en '{categoria_nombre}' registrado.")

def gastos(usuario, chat_id):
    lista = (
        Gasto.query
        .filter_by(IdUsuario=usuario.Id)
        .order_by(Gasto.Fecha.desc())
        .limit(10)
        .all()
    )

    if not lista:
        enviarMensaje(chat_id, "No tenés gastos registrados 😪")
        return

    texto = "Últimos gastos:\n\n"
    total = 0
    for g in lista:
        texto += f"• #{g.Id} | {g.Fecha.strftime('%d/%m %H:%M')} — {g.categoria.Nombre}: ${g.Monto}\n"
        total += g.Monto

    texto += f"\nTotal: ${total:.2f}"
    enviarMensaje(chat_id, texto)

def eliminarGasto(usuario, chat_id, args):
    if not args:
        enviarMensaje(chat_id, "❌ Usá:\n/eliminar ID\n/eliminar YYYY-MM-DD")
        return

    if args.isdigit():
        eliminarPorId(usuario, chat_id, int(args))
    else:
        eliminarPorFecha(usuario, chat_id, args)

def eliminarPorId(usuario, chat_id, gasto_id):
    gasto = Gasto.query.filter_by(Id=gasto_id, IdUsuario=usuario.Id).first()

    if not gasto:
        enviarMensaje(chat_id, "❌ No se encontró el gasto")
        return

    db.session.delete(gasto)
    db.session.commit()

    enviarMensaje(chat_id, f"🗑️ Gasto #{gasto_id} eliminado correctamente")

def eliminarPorFecha(usuario, chat_id, fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except:
        enviarMensaje(chat_id, "❌ Formato inválido. Usá YYYY-MM-DD")
        return

    gastos = Gasto.query.filter(
        Gasto.IdUsuario == usuario.Id,
        db.func.date(Gasto.Fecha) == fecha.date()
    ).all()

    if not gastos:
        enviarMensaje(chat_id, "❌ No hay gastos en esa fecha")
        return

    for g in gastos:
        db.session.delete(g)

    db.session.commit()

    enviarMensaje(chat_id, f"🗑️ Se eliminaron {len(gastos)} gastos del {fecha_str}")

def resumen(usuario, chat_id):
    hoy = now()
    inicio_mes = datetime(hoy.year, hoy.month, 1, tzinfo=TZ)

    resultados = (
        db.session.query(
            Categoria.Nombre,
            db.func.sum(Gasto.Monto)
        )
        .join(Gasto, Gasto.IdCategoria == Categoria.Id)
        .filter(
            Gasto.IdUsuario == usuario.Id,
            Gasto.Fecha >= inicio_mes
        )
        .group_by(Categoria.Nombre)
        .order_by(db.func.sum(Gasto.Monto).desc())
        .all()
    )

    if not resultados:
        enviarMensaje(chat_id, "📊 No tenés gastos registrados este mes")
        return

    texto = "📊 Resumen mensual:\n\n"
    total_general = 0

    for nombre, total in resultados:
        texto += f"• {nombre}: ${total:.2f}\n"
        total_general += total

    texto += f"\n💰 Total del mes: ${total_general:.2f}"

    enviarMensaje(chat_id, texto)