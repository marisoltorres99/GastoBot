from flask import request, jsonify, Blueprint

from database import db

from services.telegram_service import enviarMensaje
from services.usuario_service import getOrCreateUsuario, baja
from services.dashboard_service import generarLinkDashboard
from services.gasto_service import nuevoGasto, gastos, eliminarGasto, resumen
from services.categoria_service import categorias
from services.vencimiento_service import nuevoVencimiento, vencimientos, eliminarVencimiento

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" not in data or "text" not in data["message"]:
        return jsonify({}), 200

    chat_id = data["message"]["chat"]["id"]
    nombre = data["message"]["chat"].get("first_name", "Sin nombre")
    texto = data["message"]["text"].strip().lower()
    
    usuario = getOrCreateUsuario(chat_id, nombre)

    if usuario.FechaBaja is not None and not texto.startswith("/start"):
        enviarMensaje(chat_id, "Diste de baja nuestro bot 😭. Si querés volver a usarlo, simplemente escribe /start")
        return jsonify({}), 200

    if texto.startswith("/start"):
        if usuario.FechaBaja is not None:
            usuario.FechaBaja = None
            db.session.commit()
        generarLinkDashboard(usuario)
        enviarMensaje(chat_id, 
        f"¡Hola {nombre}! 👋\n\n"

        "Bienvenido a MisGastos, tu asistente personal de finanzas 💸\n\n"

        "En este chat podés registrar tus gastos fácilmente y después llevar control de ellos. \n\n"

        "Tenés disponible las siguientes funciones:\n\n"

        "/gasto 100.50 comida — Registrar un gasto\n"
        "/gastos — Ver tus últimos gastos\n"
        "/eliminar ID — Eliminar un gasto específico del registro (ej: /eliminar 5)\n"
        "/eliminar YYYY-MM-DD — Eliminar todos los gastos de una fecha particula (ej: /eliminar 2026-04-29)\n"
        "/categorias — Ver tus categorías de gastos\n\n"

        "/midashboard — Ver un dashboard con tus gastos\n\n"

        "/resumen — Ver el resumen mensual por categoría 📊\n\n"

        "/vencimiento luz 2026-05-20 — Registrar un vencimiento 📅\n"
        "/vencimientos — Ver tus vencimientos registrados\n"
        "/eliminarvencimiento ID — Eliminar un vencimiento específico\n\n"

        "/baja — Para dejar de usar el bot\n\n"

        "Las categorías se crean automáticamente cuando registrás tus gastos!\n"
        "Para poder agrupar los gastos en una misma categoría, recordá escribirla siempre de la misma manera✅\n\n"
        "¿Todo listo? ¡Empecemos a ordenar tus finanzas! 🚀"
    )
    elif texto.startswith("/gasto "):
        args = texto[len("/gasto "):].strip()
        nuevoGasto(usuario, chat_id, args)
    elif texto.startswith("/gastos"):
        gastos(usuario, chat_id)
    elif texto.startswith("/eliminar"):
        args = texto[len("/eliminar"):].strip()
        eliminarGasto(usuario, chat_id, args)
    elif texto.startswith("/categorias"):
        categorias(usuario, chat_id)
    elif texto.startswith("/resumen"):
        resumen(usuario, chat_id)
    elif texto.startswith("/baja"):
        baja(usuario, chat_id)
    elif texto.startswith("/vencimiento "):
        args = texto[len("/vencimiento "):].strip()
        nuevoVencimiento(usuario, chat_id, args)
    elif texto.startswith("/vencimientos"):
        vencimientos(usuario, chat_id)
    elif texto.startswith("/eliminarvencimiento"):
        args = texto[len("/eliminarvencimiento"):].strip()
        eliminarVencimiento(usuario, chat_id, args)
    elif texto.startswith("/midashboard"):
        if not usuario.LinkDashboard:
            generarLinkDashboard(usuario)
        enviarMensaje(chat_id, f'📊 <a href="{usuario.LinkDashboard}">Ver mi dashboard</a>', parse_mode="HTML")
    else:
        enviarMensaje(chat_id, "No pude entender el mensaje 🧐\nTe dejo los comandos disponibles:\n/gasto Ejemplo: 100.50 comida\n/gastos\n/categorias")

    return jsonify({}), 200