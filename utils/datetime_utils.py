from zoneinfo import ZoneInfo
from datetime import datetime

TZ = ZoneInfo("America/Argentina/Buenos_Aires")

def now():
    return datetime.now(TZ)