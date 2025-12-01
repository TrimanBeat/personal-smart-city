import pandas as pd

def parse_hours(value):
    if pd.isna(value):
        return None
    
    value = str(value).strip()

    # Caso 1: formato H:MM -> "6:30"
    if ":" in value:
        parts = value.split(":")
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            return hours + minutes / 60
        except:
            return None

    # Caso 2: número simple "6"
    try:
        return float(value)
    except:
        return None


def clean_fact_diario(df):
    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Convertir fecha
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
    
    # Numéricos
    if "horas_sueno" in df.columns:
        df["horas_sueno"] = df["horas_sueno"].apply(parse_hours).fillna(0)

    for c in ["pomodoros_estudio", "actividad_fisica", "gastos"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # Ubicación: trim
    if "ubicacion" in df.columns:
        df["ubicacion"] = df["ubicacion"].astype(str).str.strip()
    
    # Eliminar filas sin fecha
    df = df.dropna(subset=["fecha"])

    return df
