-- LIMPIEZA INICIAL
DROP TABLE IF EXISTS hechos_peliculas CASCADE;
DROP TABLE IF EXISTS dim_actor, dim_director, dim_productor, dim_pelicula, dim_fecha CASCADE;

-- DIMENSIONES
CREATE TABLE dim_actor (
    id_actor INT PRIMARY KEY,
    nombre VARCHAR(100),
    estado_civil VARCHAR(20),
    edad INT,
    telefono VARCHAR(20)
);

CREATE TABLE dim_director (
    id_director INT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE dim_productor (
    id_productor INT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE dim_pelicula (
    id_pelicula INT PRIMARY KEY,
    titulo VARCHAR(200),
    -- Información de premios integrada en la dimensión película
    premio_nombre VARCHAR(200),
    premio_lugar VARCHAR(100),
    premio_ranking INT
);

CREATE TABLE dim_fecha (
    id_fecha DATE PRIMARY KEY,
    anio INT,
    mes INT,
    dia INT,
    trimestre INT
);

-- TABLA DE HECHOS CENTRAL (MODELO ESTRELLA)
CREATE TABLE hechos_peliculas (
    id_pelicula INT,
    id_actor INT,
    id_director INT,
    id_productor INT,
    id_fecha DATE,
    salario NUMERIC(10,2),
    aportacion NUMERIC(12,2),

    FOREIGN KEY (id_pelicula) REFERENCES dim_pelicula(id_pelicula),
    FOREIGN KEY (id_actor) REFERENCES dim_actor(id_actor),
    FOREIGN KEY (id_director) REFERENCES dim_director(id_director),
    FOREIGN KEY (id_productor) REFERENCES dim_productor(id_productor),
    FOREIGN KEY (id_fecha) REFERENCES dim_fecha(id_fecha)
);
