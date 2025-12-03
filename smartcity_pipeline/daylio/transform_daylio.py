# daylio/transform_daylio.py
import pandas as pd

def transform_daylio(df):
    """
    Limpia y transforma el DataFrame exportado desde Daylio.
    - Parsea full_date -> date (DATE)
    - Normaliza mood (minusculas, strip)
    - Convierte activities en lista (separador '|' observado en tus datos)
    - Elimina filas sin fecha válida
    """

    # Aseguramos nombres de columnas en minúscula y sin espacios
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Algunas exportaciones usan 'full_date', otras 'date' — priorizamos full_date
    if "full_date" in df.columns:
        fecha_col = "full_date"
    elif "date" in df.columns:
        fecha_col = "date"
    else:
        # Si no existe, intentamos buscar timestamps comunes
        possible = [c for c in df.columns if "date" in c or "time" in c]
        fecha_col = possible[0] if possible else None

    if fecha_col is None:
        raise ValueError("No se encontró columna de fecha en el CSV (buscando 'full_date' o 'date').")

    # Parseamos la fecha a tipo date (coerce convierte errores a NaT)
    df["date"] = pd.to_datetime(df[fecha_col], errors="coerce").dt.date

    # Procesar actividades:
    # En tus ejemplos las actividades vienen como: "emocionado(a) | relajado(a) | ..."
    # Por eso usamos '|' como separador y limpiamos espacios.
    if "activities" in df.columns:
        df["activities_list"] = df["activities"].fillna("").apply(
            lambda x: [a.strip() for a in str(x).split("|") if a.strip()]
        )
    else:
        df["activities_list"] = [[] for _ in range(len(df))]

    # Normalizar mood (si existe)
    if "mood" in df.columns:
        df["mood"] = df["mood"].astype(str).str.lower().str.strip()
    else:
        df["mood"] = None

    # Normalizar note si existe
    if "note" in df.columns:
        df["note"] = df["note"].astype(str).replace("nan", None)
    else:
        df["note"] = None

    # Mostrar advertencia opcional sobre filas sin fecha
    invalid = df[df["date"].isna()]
    if not invalid.empty:
        print(f"⚠️ {len(invalid)} filas sin fecha válida serán descartadas. Muestra:")
        print(invalid[[fecha_col, "activities", "mood", "note"]].head(5))

    # Eliminar filas sin fecha
    df = df.dropna(subset=["date"])

    # Opcional: eliminar duplicados exactos (misma fecha + mismo mood + misma nota)
    df = df.drop_duplicates(subset=["date", "mood", "note"], keep="first")

    # Devolver DataFrame con columnas importantes
    return df[["date", "mood", "activities_list", "note"]]

