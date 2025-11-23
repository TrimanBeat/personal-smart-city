import xml.etree.ElementTree as ET
import pandas as pd

def extract_apple_health(path="apple_health_export/export.xml"):
    tree = ET.parse(path)
    root = tree.getroot()

    records = []

    for record in root.findall("Record"):
        records.append({
            "type": record.get("type"),
            "value": record.get("value"),
            "startDate": record.get("startDate"),
            "endDate": record.get("endDate")
        })

    return pd.DataFrame(records)
