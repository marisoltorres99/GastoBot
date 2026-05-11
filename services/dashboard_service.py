from config import Config
from database import db

def generarLinkDashboard(usuario):
    link = f"{Config.GRAFANA_URL}/d/{Config.GRAFANA_DASHBOARD_ID}/gastos?var-Usuario={usuario.IdChat}&kiosk=tv"
    usuario.LinkDashboard = link
    db.session.commit()
    return link
