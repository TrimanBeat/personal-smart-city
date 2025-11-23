
CREATE TABLE dim_ubicacion (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    lat FLOAT,
    lon FLOAT
);




CREATE TABLE fact_diario (
    id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    horas_sueno FLOAT,
    pomodoros_estudio INT,
    actividad_fisica FLOAT,
    gastos FLOAT,
    ubicacion_id INT REFERENCES dim_ubicacion(id)
);

CREATE INDEX idx_fact_diario_fecha ON fact_diario(fecha);


CREATE TABLE fact_dailyo (
    id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    mood_score INT,
    notas TEXT
);



CREATE TABLE dim_actividad (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE fact_dailyo_actividad (
    dailyo_id INT REFERENCES fact_dailyo(id) ON DELETE CASCADE,
    actividad_id INT REFERENCES dim_actividad(id),
    PRIMARY KEY (dailyo_id, actividad_id)
);

CREATE INDEX idx_dailyoact_dailyo ON fact_dailyo_actividad(dailyo_id);
CREATE INDEX idx_dailyoact_act ON fact_dailyo_actividad(actividad_id);

CREATE TABLE fact_salud_apple (
    id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    pasos INT,
    distancia FLOAT,            -- km
    calorias_activas FLOAT,
    frecuencia_media FLOAT,
    tiempo_sueno_min INT
);

CREATE INDEX idx_salud_fecha ON fact_salud_apple(fecha);





