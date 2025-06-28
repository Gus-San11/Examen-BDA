
-- estructura_xml.sql
DROP TABLE IF EXISTS peliculas_xml;

CREATE TABLE peliculas_xml (
    id SERIAL PRIMARY KEY,
    contenido XML NOT NULL
);

SELECT id, LENGTH(contenido::text) AS longitud, contenido
FROM peliculas_xml
LIMIT 5;


-- A) Total de salarios de actores de "Cinema Paradiso"
SELECT SUM((xpath('//pelicula[titulo="Cinema Paradiso" and director/nombre="Giuseppe Tornatore"]/actores/actor/salario/text()', contenido))[i]::text::numeric)
AS total_salarios
FROM peliculas_xml, generate_series(1, array_length(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/salario/text()', contenido), 1)) i;

-- B) Premios recibidos por "Cinema Paradiso" ordenados por ranking DESC
SELECT 
    unnest(xpath('//pelicula[titulo="Cinema Paradiso" and director/nombre="Giuseppe Tornatore"]/premios/premio/ranking/text()', contenido))::text::int AS ranking,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/premios/premio/nombre/text()', contenido))::text AS nombre,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/premios/premio/lugar/text()', contenido))::text AS lugar
FROM peliculas_xml
ORDER BY ranking DESC;

-- C) Total de aportes del productor "Franco Cristaldi"
SELECT SUM((xpath('//pelicula/productores/productor[nombre="Franco Cristaldi"]/aporte_economico/text()', contenido))[i]::text::numeric)
AS total_aporte
FROM peliculas_xml, generate_series(1, array_length(xpath('//pelicula/productores/productor[nombre="Franco Cristaldi"]/aporte_economico/text()', contenido), 1)) i;

-- D) Críticas entre 15 y 30 de agosto de 1990 para "Cinema Paradiso"
SELECT 
    unnest(xpath('//pelicula[titulo="Cinema Paradiso" and director/nombre="Giuseppe Tornatore"]/criticas/critica/medio/text()', contenido))::text AS medio,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/criticas/critica/fecha/text()', contenido))::text::date AS fecha,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/criticas/critica/autor/text()', contenido))::text AS autor
FROM peliculas_xml
WHERE
    EXISTS (
        SELECT 1 FROM unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/criticas/critica/fecha/text()', contenido)) AS fecha(fecha_text)
        WHERE fecha_text::text::date BETWEEN '1990-08-15' AND '1990-08-30'
    )
ORDER BY fecha DESC;

-- E) Personas involucradas en "Cinema Paradiso"
-- Incluye actores, director y productor con rol, edad, estado civil y teléfono
WITH datos AS (
  SELECT 
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/nombre/text()', contenido))::text AS nombre,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/fecha_nacimiento/text()', contenido))::text::date AS fecha_nac,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/estado_civil/text()', contenido))::text AS estado_civil,
    unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/telefono/text()', contenido))::text AS telefono,
    'Actor' AS rol
  FROM peliculas_xml
  UNION ALL
  SELECT 
    (xpath('//pelicula[titulo="Cinema Paradiso"]/director/nombre/text()', contenido))[1]::text,
    (xpath('//pelicula[titulo="Cinema Paradiso"]/director/fecha_nacimiento/text()', contenido))[1]::text::date,
    (xpath('//pelicula[titulo="Cinema Paradiso"]/director/estado_civil/text()', contenido))[1]::text,
    (xpath('//pelicula[titulo="Cinema Paradiso"]/director/telefono/text()', contenido))[1]::text,
    'Director'
  FROM peliculas_xml
  UNION ALL
  SELECT 
    (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/nombre/text()', contenido))[1]::text,
    (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/fecha_nacimiento/text()', contenido))[1]::text::date,
    (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/estado_civil/text()', contenido))[1]::text,
    (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/telefono/text()', contenido))[1]::text,
    'Productor'
  FROM peliculas_xml
)
SELECT 
  nombre, 
  rol, 
  estado_civil,
  telefono,
  extract(year FROM age(current_date, fecha_nac)) AS edad_actual
FROM datos
ORDER BY rol;

