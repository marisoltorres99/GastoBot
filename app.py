from flask import Flask
from dotenv import load_dotenv

from database import db
from config import Config

from routes.webhook_routes import webhook_bp
from routes.health_routes import health_bp


load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(webhook_bp)
app.register_blueprint(health_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

#TO-DO
# - Agregar comando /categorias para listar categorías del usuario  -- OK
# - Mejorar manejo de errores y validación de comandos
# - Agregar comando /resumen para mostrar resumen mensual de gastos por categoría -- OK
# - Validar montos y duplicados -- OK
# - Validar que no se repitan categorias para 1 mismo usuario o que no sean similares o con nombres vacios --OK
# - Agregar comando /eliminar para eliminar un gasto por ID o fecha --OK

# - Agregar comando /vencimientos para listar vencimientos -- Pendiente
# - Agregar comando /eliminarvencimiento -- Pendiente
# - Agregar alertas automáticas de vencimientos