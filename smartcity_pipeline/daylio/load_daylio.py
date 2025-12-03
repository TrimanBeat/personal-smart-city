from utils.db_connection import get_connection

def get_or_create_mood_id(conn, mood):
    cur = conn.cursor()
    cur.execute("SELECT id FROM dim_mood WHERE mood_name = %s;", (mood,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO dim_mood (mood_name) VALUES (%s) RETURNING id;", (mood,))
    conn.commit()
    return cur.fetchone()[0]

def get_or_create_actividad_id(conn, actividad):
    cur = conn.cursor()
    cur.execute("SELECT id FROM dim_actividad WHERE nombre = %s;", (actividad,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO dim_actividad (nombre) VALUES (%s) RETURNING id;", (actividad,))
    conn.commit()
    return cur.fetchone()[0]

def load_daylio(df):
    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        mood_id = get_or_create_mood_id(conn, row["mood"])
        # Verificar si el registro ya existe
        cur.execute("""
            SELECT id FROM fact_daylio
            WHERE fecha = %s AND mood_id = %s AND note = %s;
        """, (row["date"], mood_id, row.get("note")))
        
        ya_existe = cur.fetchone()
        
        if ya_existe:
            fact_id = ya_existe[0]
        else:
            cur.execute("""
                INSERT INTO fact_daylio (fecha, mood_id, note)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (row["date"], mood_id, row.get("note")))
        
            fact_id = cur.fetchone()[0]

        for act in row["activities_list"]:
            act_id = get_or_create_actividad_id(conn, act)

            cur.execute("""
                INSERT INTO fact_daylio_actividad (id_fact_daylio, id_actividad)
                VALUES (%s, %s)
                ON CONFLICT (id_fact_daylio, id_actividad) DO NOTHING;
            """, (fact_id, act_id))

    conn.commit()
    conn.close()
