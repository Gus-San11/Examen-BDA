
-- =============================
-- CASO 2: Modelo Relacional-Objetual (PostgreSQL)
-- =============================

-- =============================
-- DOMINIOS
-- =============================
CREATE DOMAIN estado_civil_dom AS VARCHAR(20)
    CHECK (VALUE IN ('Soltero', 'Casado', 'Divorciado', 'Viudo', 'Union libre'));

CREATE DOMAIN telefono_dom AS VARCHAR(10)
    CHECK (VALUE ~ '^[0-9]{10}$');

CREATE DOMAIN salario_dom AS NUMERIC(12, 2)
    CHECK (VALUE >= 600000 AND VALUE <= 4900000);

-- =============================
-- TIPOS ENUM
-- =============================
CREATE TYPE tipo_actuacion_enum AS ENUM ('Protagonista', 'Secundario', 'De reparto', 'Extra');
CREATE TYPE tipo_certamen_enum AS ENUM ('Nacional', 'Internacional');

-- =============================
-- PERSONA (PADRE)
-- =============================
CREATE TABLE persona (
    id_persona SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    fecha_nac DATE,
    estado_civil estado_civil_dom,
    telefono telefono_dom
);

-- =============================
-- ACTOR, DIRECTOR, PRODUCTOR (HERENCIA)
-- =============================
CREATE TABLE actor (
    salario salario_dom,
    PRIMARY KEY (id_persona)
) INHERITS (persona);

CREATE TABLE director (
    PRIMARY KEY (id_persona)
) INHERITS (persona);

CREATE TABLE productor (
    PRIMARY KEY (id_persona)
) INHERITS (persona);

-- =============================
-- PELICULA Y RELACIONES
-- =============================
CREATE TABLE pelicula (
    id_pelicula SERIAL PRIMARY KEY,
    titulo VARCHAR(100),
    fecha_estreno DATE,
    resumen TEXT CHECK (char_length(resumen) BETWEEN 250 AND 450),
    ranking NUMERIC(2,1) CHECK (ranking >= 1.0 AND ranking <= 5.0),
    id_director INT REFERENCES director(id_persona)
);

CREATE TABLE actuacion (
    id_pelicula INT REFERENCES pelicula(id_pelicula),
    id_actor INT REFERENCES actor(id_persona),
    tipo_actuacion tipo_actuacion_enum,
    PRIMARY KEY (id_pelicula, id_actor)
);

CREATE TABLE produccion (
    id_pelicula INT REFERENCES pelicula(id_pelicula),
    id_productor INT REFERENCES productor(id_persona),
    aportacion NUMERIC(12,2) CHECK (aportacion > 0),
    PRIMARY KEY (id_pelicula, id_productor)
);

CREATE TABLE critica (
    id_critica SERIAL PRIMARY KEY,
    id_pelicula INT REFERENCES pelicula(id_pelicula),
    medio VARCHAR(100),
    autor VARCHAR(100),
    fecha DATE
);

CREATE TABLE premio (
    id_premio SERIAL PRIMARY KEY,
    id_pelicula INT REFERENCES pelicula(id_pelicula),
    nombre VARCHAR(100),
    lugar_certamen VARCHAR(100),
    tipo_certamen tipo_certamen_enum
);
