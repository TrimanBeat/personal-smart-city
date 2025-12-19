from lxml import etree
from pathlib import Path
from datetime import datetime, timedelta
import psycopg2

# --- Configuración ---
INTERESTING_TYPES = {
    "HKQuantityTypeIdentifierStepCount",
    "HKQuantityTypeIdentifierHeartRate",
    "HKQuantityTypeIdentifierDistanceWalkingRunning",
    "HKQuantityTypeIdentifierBodyMass"
}

# Paths
ROOT_DIR = Path(__file__).resolve().parent
PIPELINE_DIR = ROOT_DIR / "smartcity_pipeline"
XML_PATH = PIPELINE_DIR / "data/apple_health_export/export.xml"

# --- Parse XML ---
tree = etree.parse(str(XML_PATH))
records = tree.xpath("//Record")

# --- Fecha límite (último año) ---
one_year_ago = datetime.now() - timedelta(days=365)

# --- Conexión a PostgreSQL ---
conn = psycopg2.connect(
    dbname="tu_base",
    user="tu_usuario",
    password="tu_password",
    host="localhost",
    port=5432
)
cur = conn.cursor()

inserted = 0

for r in records:
    t = r.attrib.get("type")
    if t not in INTERESTING_TYPES:
        continue

    # Filtrar por fecha
    start_date_str = r.attrib.get("startDate")
    start_date = datetime.strptime(start_date_str[:19], "%Y-%m-%d %H:%M:%S")  # Ignorando zona horaria
    if start_date < one_year_ago:
        continue

    value = r.attrib.get("value")
    unit = r.attrib.get("unit")
    source = r.attrib.get("sourceName")
    end_date_str = r.attrib.get("endDate")
    end_date = datetime.strptime(end_date_str[:19], "%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO apple_health_records(type, value, unit, source, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (t, value, unit, source, start_date, end_date))

    inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Insertados {inserted} registros nuevos (último año)")
