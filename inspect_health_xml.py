from pathlib import Path
from lxml import etree
from collections import Counter

# Ruta absoluta al archivo actual
ROOT_DIR = Path(__file__).resolve().parent

# Ruta al pipeline
PIPELINE_DIR = ROOT_DIR / "smartcity_pipeline"

XML_PATH = PIPELINE_DIR / "data" / "apple_health_export" / "export.xml"

print("📂 ROOT_DIR:", ROOT_DIR)
print("📂 PIPELINE_DIR:", PIPELINE_DIR)
print("📄 XML_PATH:", XML_PATH)
print("📄 Existe:", XML_PATH.exists())

if not XML_PATH.exists():
    raise FileNotFoundError(f"No se encuentra el archivo: {XML_PATH}")

tree = etree.parse(str(XML_PATH))
records = tree.xpath("//Record")

types = Counter(r.attrib.get("type") for r in records)
print("✅ Total de registros:", len(records))
print("📊 Top 10 tipos:")
for t, c in types.most_common(10):
    print(t, c)


