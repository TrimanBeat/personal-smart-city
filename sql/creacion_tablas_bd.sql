-- =========================================================
-- 1. BORRAR TABLAS EXISTENTES (en orden por claves externas)
-- =========================================================
DROP TABLE IF EXISTS fact_daylio_actividad;
DROP TABLE IF EXISTS fact_daylio;
DROP TABLE IF EXISTS dim_mood;
DROP TABLE IF EXISTS dim_actividad;

-- =========================================================
-- 2. DIMENSIONES
-- =========================================================

-- Dimensión de actividades
CREATE TABLE dim_actividad (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL
);

-- Dimensión de estados de ánimo
CREATE TABLE dim_mood (
    id SERIAL PRIMARY KEY,
    mood_name TEXT UNIQUE NOT NULL
);

-- =========================================================
-- 3. TABLA DE HECHOS PRINCIPAL DE DAYLIO
-- =========================================================
CREATE TABLE fact_daylio (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    mood_id INTEGER REFERENCES dim_mood(id),
    note TEXT
);

-- =========================================================
-- 4. TABLA PUENTE (N:M)
-- =========================================================
CREATE TABLE fact_daylio_actividad (
    id_fact_daylio INTEGER REFERENCES fact_daylio(id) ON DELETE CASCADE,
    id_actividad INTEGER REFERENCES dim_actividad(id) ON DELETE CASCADE,
    PRIMARY KEY (id_fact_daylio, id_actividad)
);





