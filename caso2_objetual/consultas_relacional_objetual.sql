
-- CONSULTAS DEL NEGOCIO: MODELO RELACIONAL-OBJETUAL

-- A) Total de salarios pagados a los actores de "Cinema Paradiso", dirigida por "Giuseppe Tornatore"
SELECT SUM(a.salario) AS total_salarios
FROM actor a
JOIN actuacion ac ON a.id_persona = ac.id_actor
JOIN pelicula p ON ac.id_pelicula = p.id_pelicula
JOIN director d ON p.id_director = d.id_persona
WHERE p.titulo = 'Cinema Paradiso'
  AND d.nombre = 'Giuseppe Tornatore';

-- B) Listado de premios recibidos por "Cinema Paradiso", con ranking, nombre y lugar del certamen
SELECT p.ranking, pr.nombre, pr.lugar_certamen
FROM premio pr
JOIN pelicula p ON pr.id_pelicula = p.id_pelicula
JOIN director d ON p.id_director = d.id_persona
WHERE p.titulo = 'Cinema Paradiso'
  AND d.nombre = 'Giuseppe Tornatore'
ORDER BY p.ranking DESC;

-- C) Total de aportaciones económicas del productor "Franco Cristaldi"
SELECT SUM(pr.aportacion) AS total_aportes
FROM produccion pr
JOIN productor p ON pr.id_productor = p.id_persona
WHERE p.nombre = 'Franco Cristaldi';

-- D) Críticas entre el 15 y 30 de agosto de 1990 a "Cinema Paradiso"
SELECT c.medio, c.fecha, c.autor
FROM critica c
JOIN pelicula p ON c.id_pelicula = p.id_pelicula
JOIN director d ON p.id_director = d.id_persona
WHERE p.titulo = 'Cinema Paradiso'
  AND d.nombre = 'Giuseppe Tornatore'
  AND c.fecha BETWEEN '1990-08-15' AND '1990-08-30'
ORDER BY c.fecha DESC;

-- E) Personas involucradas en "Cinema Paradiso": nombre, rol, edad, estado civil y teléfono
SELECT per.nombre, 'Actor' AS rol, per.estado_civil, per.telefono,
       DATE_PART('year', CURRENT_DATE) - DATE_PART('year', per.fecha_nac) AS edad
FROM actor a
JOIN persona per ON a.id_persona = per.id_persona
JOIN actuacion act ON a.id_persona = act.id_actor
WHERE act.id_pelicula = 999

UNION

SELECT per.nombre, 'Director' AS rol, per.estado_civil, per.telefono,
       DATE_PART('year', CURRENT_DATE) - DATE_PART('year', per.fecha_nac) AS edad
FROM director d
JOIN persona per ON d.id_persona = per.id_persona
JOIN pelicula p ON d.id_persona = p.id_director
WHERE p.id_pelicula = 999

UNION

SELECT per.nombre, 'Productor' AS rol, per.estado_civil, per.telefono,
       DATE_PART('year', CURRENT_DATE) - DATE_PART('year', per.fecha_nac) AS edad
FROM productor prod
JOIN persona per ON prod.id_persona = per.id_persona
JOIN produccion pr ON prod.id_persona = pr.id_productor
WHERE pr.id_pelicula = 999;
