-- A) Total de salarios pagados a los actores de "Cinema Paradiso" dirigida por "Giuseppe Tornatore"
SELECT SUM(a.salario) AS total_salarios
FROM actuacion a
JOIN actor ac ON a.id_actor = ac.id_actor
JOIN pelicula p ON a.id_pelicula = p.id_pelicula
JOIN director d ON p.id_director = d.id_director
WHERE p.titulo = 'Cinema Paradiso'
  AND d.nombre = 'Giuseppe Tornatore';

-- B) Premios de "Cinema Paradiso", su ranking, nombre del premio y lugar (ordenado de mayor a menor)
SELECT p.ranking, pr.nombre, pr.lugar
FROM pelicula p
JOIN director d ON p.id_director = d.id_director
JOIN premio pr ON p.id_pelicula = pr.id_pelicula
WHERE p.titulo = 'Cinema Paradiso'
  AND d.nombre = 'Giuseppe Tornatore'
ORDER BY p.ranking DESC;

-- C) Total de aportes económicos realizados por "Franco Cristaldi"
SELECT SUM(pr.aportacion_economica) AS total_aporte
FROM produccion pr
JOIN productor p ON pr.id_productor = p.id_productor
WHERE p.nombre = 'Franco Cristaldi';

-- D) Críticas recibidas por "Cinema Paradiso" entre el 15 y 30 de agosto de 1990
SELECT c.medio, c.fecha, c.autor
FROM critica c
JOIN pelicula p ON c.id_pelicula = p.id_pelicula
JOIN director d ON p.id_director = d.id_director
WHERE p.titulo = 'Cinema Paradiso'
  AND d.nombre = 'Giuseppe Tornatore'
  AND c.fecha BETWEEN '1990-08-15' AND '1990-08-30'
ORDER BY c.fecha DESC;

-- E) Todas las personas involucradas en "Cinema Paradiso"
SELECT a.nombre, 'Actor' AS rol, DATE_PART('year', AGE(a.fecha_nac)) AS edad, a.estado_civil, a.telefono
FROM actor a
JOIN actuacion ac ON a.id_actor = ac.id_actor
WHERE ac.id_pelicula = 999

UNION

SELECT d.nombre, 'Director' AS rol, NULL AS edad, NULL AS estado_civil, d.telefono
FROM director d
JOIN pelicula p ON d.id_director = p.id_director
WHERE p.id_pelicula = 999

UNION

SELECT pr.nombre, 'Productor' AS rol, NULL AS edad, NULL AS estado_civil, pr.telefono
FROM productor pr
JOIN produccion pd ON pr.id_productor = pd.id_productor
WHERE pd.id_pelicula = 999;
