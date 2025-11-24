import pandas as pd

def clean_fact_diario(df):
    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Convertir fecha
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
    
    # Numéricos
    for c in ["horas_sueno", "pomodoros_estudio", "actividad_fisica", "gastos"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # Ubicación: trim
    if "ubicacion" in df.columns:
        df["ubicacion"] = df["ubicacion"].astype(str).str.strip()
    
    # Eliminar filas sin fecha
    df = df.dropna(subset=["fecha"])

    return df
