-- =================================================================
-- CONSULTAS MODELO ESTRELLA - VERSIÓN CORREGIDA
-- =================================================================
-- Estas consultas están adaptadas al modelo estrella real implementado
-- en PostgreSQL y funcionan con las tablas y columnas existentes.
-- =================================================================

-- A) Total salarios pagados a los actores de "Cinema Paradiso"
SELECT 
    SUM(h.salario) AS total_salarios,
    p.titulo,
    d.nombre AS director
FROM hechos_peliculas h
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
JOIN dim_director d ON h.id_director = d.id_director
WHERE p.titulo = 'Cinema Paradiso'
GROUP BY p.titulo, d.nombre;

-- B) Información general de "Cinema Paradiso" 
SELECT 
    p.titulo,
    d.nombre AS director,
    a.nombre AS actor,
    pr.nombre AS productor,
    h.salario,
    h.aportacion,
    h.ranking,
    h.id_fecha
FROM hechos_peliculas h
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
JOIN dim_director d ON h.id_director = d.id_director
JOIN dim_actor a ON h.id_actor = a.id_actor
JOIN dim_productor pr ON h.id_productor = pr.id_productor
WHERE p.titulo = 'Cinema Paradiso';

-- C) Total de aportes económicos por productor
SELECT 
    pr.nombre AS productor,
    SUM(h.aportacion) AS total_aporte,
    COUNT(*) AS num_peliculas
FROM hechos_peliculas h
JOIN dim_productor pr ON h.id_productor = pr.id_productor
GROUP BY pr.nombre
ORDER BY total_aporte DESC;

-- D) Análisis temporal - Información por fecha
SELECT 
    f.anio,
    f.mes,
    f.trimestre,
    p.titulo,
    h.salario,
    h.aportacion
FROM hechos_peliculas h
JOIN dim_fecha f ON h.id_fecha = f.id_fecha
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
WHERE f.anio = 1990;

-- E) Listado completo de personas involucradas en "Cinema Paradiso"
SELECT 
    'Actor' AS rol,
    a.nombre,
    a.edad,
    a.estado_civil,
    NULL as telefono  -- Columna no disponible en modelo actual
FROM hechos_peliculas h
JOIN dim_actor a ON h.id_actor = a.id_actor
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
WHERE p.titulo = 'Cinema Paradiso'

UNION

SELECT 
    'Director' AS rol,
    d.nombre,
    NULL as edad,
    NULL as estado_civil,
    NULL as telefono
FROM hechos_peliculas h
JOIN dim_director d ON h.id_director = d.id_director
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
WHERE p.titulo = 'Cinema Paradiso'

UNION

SELECT 
    'Productor' AS rol,
    pr.nombre,
    NULL as edad,
    NULL as estado_civil,
    NULL as telefono
FROM hechos_peliculas h
JOIN dim_productor pr ON h.id_productor = pr.id_productor
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
WHERE p.titulo = 'Cinema Paradiso';

-- F) Análisis de métricas agregadas
SELECT 
    AVG(h.salario) AS salario_promedio,
    MAX(h.salario) AS salario_maximo,
    MIN(h.salario) AS salario_minimo,
    SUM(h.aportacion) AS total_inversion,
    AVG(h.ranking) AS ranking_promedio
FROM hechos_peliculas h;

-- G) Análisis por dimensiones - Top actores por salario
SELECT 
    a.nombre AS actor,
    a.edad,
    a.estado_civil,
    SUM(h.salario) AS total_salarios,
    COUNT(*) AS num_peliculas
FROM hechos_peliculas h
JOIN dim_actor a ON h.id_actor = a.id_actor
GROUP BY a.id_actor, a.nombre, a.edad, a.estado_civil
ORDER BY total_salarios DESC;

-- H) Análisis por dimensiones - Productores más activos
SELECT 
    pr.nombre AS productor,
    SUM(h.aportacion) AS inversion_total,
    AVG(h.ranking) AS ranking_promedio,
    COUNT(*) AS peliculas_producidas
FROM hechos_peliculas h
JOIN dim_productor pr ON h.id_productor = pr.id_productor
GROUP BY pr.id_productor, pr.nombre
ORDER BY inversion_total DESC;
