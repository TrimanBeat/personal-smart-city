from utils.db_connection import get_connection

def get_or_create_ubicacion_id(conn, nombre):
    if nombre is None or nombre.strip() == "":
        return None
    
    cur = conn.cursor()
    cur.execute("SELECT id FROM dim_ubicacion WHERE nombre = %s", (nombre,))
    r = cur.fetchone()

    if r:
        return r[0]

    # Insertar nueva ubicación
    cur.execute(
        "INSERT INTO dim_ubicacion (nombre) VALUES (%s) RETURNING id;",
        (nombre,)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    return new_id


def load_fact_diario(df):
    conn = get_connection()
    cur = conn.cursor()

    for _, r in df.iterrows():
        ubicacion_id = get_or_create_ubicacion_id(conn, r["ubicacion"])

        cur.execute("""
            INSERT INTO fact_diario 
            (fecha, horas_sueno, pomodoros_estudio, actividad_fisica, gastos, ubicacion_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (fecha) DO UPDATE
            SET horas_sueno = EXCLUDED.horas_sueno,
                pomodoros_estudio = EXCLUDED.pomodoros_estudio,
                actividad_fisica = EXCLUDED.actividad_fisica,
                gastos = EXCLUDED.gastos,
                ubicacion_id = EXCLUDED.ubicacion_id;
        """, (
            r["fecha"],
            r["horas_sueno"],
            r["pomodoros_estudio"],
            r["actividad_fisica"],
            r["gastos"],
            ubicacion_id
        ))

    conn.commit()
    conn.close()
