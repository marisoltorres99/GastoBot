import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT', '3306')}"
        f"/{os.getenv('MYSQL_DATABASE')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GRAFANA_URL = os.getenv("GRAFANA_URL")

    GRAFANA_DASHBOARD_ID = os.getenv("GRAFANA_DASHBOARD_ID")

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")