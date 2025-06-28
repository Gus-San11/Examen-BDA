-- Script de inicialización de la base de datos para el sistema de gestión de películas
-- Eliminar tablas si existen
DROP TABLE IF EXISTS critica, premio, produccion, actuacion, pelicula, productor, director, actor CASCADE;

-- ============================
-- Tablas base
-- ============================

-- Tabla: Actor
CREATE TABLE actor (
    id_actor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nac DATE NOT NULL,
    lugar_nac VARCHAR(100),
    direccion TEXT,
    telefono VARCHAR(20),
    estado_civil VARCHAR(20) 
        CHECK (estado_civil IN ('Soltero', 'Casado', 'Divorciado', 'Viudo', 'Union libre'))
);

-- Tabla: Director
CREATE TABLE director (
    id_director SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20)
);

-- Tabla: Productor
CREATE TABLE productor (
    id_productor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20)
);

-- Tabla: Película
CREATE TABLE pelicula (
    id_pelicula SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    fecha DATE NOT NULL,
    resumen TEXT CHECK (char_length(resumen) BETWEEN 250 AND 450),
    ranking NUMERIC(2,1) CHECK (ranking >= 1.0 AND ranking <= 5.0),
    id_director INT NOT NULL,
    FOREIGN KEY (id_director) REFERENCES director(id_director)
);


-- Tabla: Actuación (relación actor-película)
CREATE TABLE actuacion (
    id_actor INT,
    id_pelicula INT,
    tipo VARCHAR(20)
        CHECK (tipo IN ('Protagonista', 'Secundario', 'De reparto', 'Extra')),
    salario NUMERIC(10,2)
        CHECK (salario BETWEEN 600000.00 AND 4900000.00),
    PRIMARY KEY (id_actor, id_pelicula),
    FOREIGN KEY (id_actor) REFERENCES actor(id_actor),
    FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula)
);

-- Tabla: Producción (relación productor-película)
CREATE TABLE produccion (
    id_productor INT,
    id_pelicula INT,
    aportacion_economica NUMERIC(12,2)
        CHECK (aportacion_economica >= 0),
    PRIMARY KEY (id_productor, id_pelicula),
    FOREIGN KEY (id_productor) REFERENCES productor(id_productor),
    FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula)
);

-- Tabla: Premio
CREATE TABLE premio (
    id_premio SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    resumen TEXT,
    certamen VARCHAR(20) 
        CHECK (certamen IN ('Nacional', 'Internacional')),
    lugar VARCHAR(100),
    tipo VARCHAR(20),
    id_pelicula INT NOT NULL,
    FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula)
);

-- Tabla: Crítica
CREATE TABLE critica (
    id_critica SERIAL PRIMARY KEY,
    medio VARCHAR(100),
    fecha DATE NOT NULL,
    autor VARCHAR(100),
    id_pelicula INT NOT NULL,
    FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula)
);
