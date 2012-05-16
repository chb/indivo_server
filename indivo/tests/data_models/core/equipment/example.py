from indivo.models import Equipment
from indivo.lib.iso8601 import parse_utc_date as date

equipment_fact = Equipment(
    date_started=date("2009-02-05"),
    date_stopped=date("2009-06-12"),
    name="Pacemaker",
    vendor="Acme Medical Devices",
    description="it works!"
    )
