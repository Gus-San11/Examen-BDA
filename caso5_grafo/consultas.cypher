// A) Total de salarios pagados a los actores de "Cinema Paradiso", dirigida por Giuseppe Tornatore
MATCH (p:Pelicula {titulo: "Cinema Paradiso"})-[:DIRIGIDA_POR]->(d:Director {nombre: "Giuseppe Tornatore"}),
      (p)-[act:ACTUADA_POR]->(a:Actor)
RETURN p.titulo AS pelicula, sum(act.salario) AS total_salarios_pagados;

// B) Premios de "Cinema Paradiso", dirigida por Giuseppe Tornatore
MATCH (p:Pelicula {titulo: "Cinema Paradiso"})-[:DIRIGIDA_POR]->(d:Director {nombre: "Giuseppe Tornatore"}),
      (p)-[:TIENE_PREMIO]->(pr:Premio)
RETURN pr.ranking AS ranking, pr.nombre AS nombre_premio, pr.lugar AS lugar
ORDER BY ranking DESC;

// C) Total de aportes económicos del productor Franco Cristaldi
MATCH (pr:Productor {nombre: "Franco Cristaldi"})<-[prod:PRODUCIDA_POR]-(p:Pelicula)
RETURN pr.nombre AS productor, sum(toFloat(prod.aportacion_economica)) AS total_aportes;

// D) Críticas de "Cinema Paradiso" dirigidas por Giuseppe Tornatore entre el 15 y 30 de agosto de 1990
MATCH (p:Pelicula {titulo: "Cinema Paradiso"})-[:DIRIGIDA_POR]->(d:Director {nombre: "Giuseppe Tornatore"}),
      (p)-[:TIENE_CRITICA]->(c:Critica)
WHERE date(c.fecha) >= date("1990-08-15") AND date(c.fecha) <= date("1990-08-30")
RETURN c.medio AS medio, c.fecha AS fecha, c.autor AS autor
ORDER BY c.fecha DESC;

// E) Personas involucradas en "Cinema Paradiso" con su rol, edad, estado civil y teléfono
MATCH (p:Pelicula {titulo: "Cinema Paradiso"})
OPTIONAL MATCH (p)-[r1:ACTUADA_POR]->(a:Actor)
OPTIONAL MATCH (p)-[r2:DIRIGIDA_POR]->(d:Director)
OPTIONAL MATCH (p)-[r3:PRODUCIDA_POR]->(pr:Productor)
WITH collect({nombre: a.nombre, rol: "Actor", fecha_nacimiento: a.fecha_nac, estado_civil: a.estado_civil, telefono: a.telefono}) +
     collect({nombre: d.nombre, rol: "Director", fecha_nacimiento: null, estado_civil: null, telefono: d.telefono}) +
     collect({nombre: pr.nombre, rol: "Productor", fecha_nacimiento: null, estado_civil: null, telefono: pr.telefono}) AS personas
UNWIND personas AS persona
WITH persona
WHERE persona.nombre IS NOT NULL
RETURN persona.nombre AS nombre, persona.rol AS rol,
       CASE 
         WHEN persona.fecha_nacimiento IS NOT NULL 
         THEN duration.between(date(persona.fecha_nacimiento), date()).years 
         ELSE null 
       END AS edad_actual,
       persona.estado_civil AS estado_civil, persona.telefono AS telefono
ORDER BY rol;

// ========================================
// CONSULTAS DE AGRUPACIÓN Y JERARQUÍA
// (Para visualizar el grafo como estructura de árbol)
// ========================================

// F) Visualizar la estructura completa del grafo (muestra conexiones jerárquicas)
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 200;

// G) Películas agrupadas por década (nodos centrales)
MATCH (p:Pelicula)-[:DE_LA_DECADA]->(d:Decada)
RETURN d.nombre AS decada, collect(p.titulo) AS peliculas, count(p) AS cantidad_peliculas
ORDER BY d.valor;

// H) Películas agrupadas por calidad (estructura jerárquica por ranking)
MATCH (p:Pelicula)-[:TIENE_CALIDAD]->(c:CalidadPelicula)
RETURN c.categoria AS calidad, collect(p.titulo) AS peliculas, count(p) AS cantidad
ORDER BY 
    CASE c.categoria 
        WHEN 'Excelente' THEN 1 
        WHEN 'Buena' THEN 2 
        WHEN 'Regular' THEN 3 
        ELSE 4 
    END;

// I) Actores agrupados por experiencia/edad (jerarquía por experiencia)
MATCH (a:Actor)-[:TIENE_EXPERIENCIA]->(e:ExperienciaActor)
RETURN e.categoria AS experiencia, collect(a.nombre) AS actores, count(a) AS cantidad
ORDER BY 
    CASE e.categoria 
        WHEN 'Veterano' THEN 1 
        WHEN 'Experimentado' THEN 2 
        WHEN 'Establecido' THEN 3 
        ELSE 4 
    END;

// J) Actores agrupados por región de nacimiento (clusters geográficos)
MATCH (a:Actor)-[:NACIO_EN]->(r:Region)
RETURN r.nombre AS region, collect(a.nombre) AS actores, count(a) AS cantidad
ORDER BY cantidad DESC;

// K) Red de colaboraciones: quien trabajó con quien (conexiones entre nodos)
MATCH (p1)-[:TRABAJO_CON]->(p2)
RETURN p1.nombre AS persona1, p2.nombre AS persona2, 
       labels(p1)[0] AS tipo1, labels(p2)[0] AS tipo2
ORDER BY persona1;

// L) Coactores: actores que trabajaron juntos (subgrafo de colaboración)
MATCH (a1:Actor)-[r:COACTUA_CON]->(a2:Actor)
RETURN a1.nombre AS actor1, a2.nombre AS actor2, r.pelicula AS pelicula_comun
ORDER BY pelicula_comun;

// M) Estructura jerárquica completa: Película -> Director/Actores/Productores
MATCH (p:Pelicula)
OPTIONAL MATCH (p)-[:DIRIGIDA_POR]->(d:Director)
OPTIONAL MATCH (p)-[:ACTUADA_POR]->(a:Actor)
OPTIONAL MATCH (p)-[:PRODUCIDA_POR]->(pr:Productor)
RETURN p.titulo AS pelicula, 
       collect(DISTINCT d.nombre) AS directores,
       collect(DISTINCT a.nombre) AS actores,
       collect(DISTINCT pr.nombre) AS productores
ORDER BY p.titulo
LIMIT 10;

// N) Árbol de premios por lugar (agrupación geográfica de premios)
MATCH (pr:Premio)-[:OTORGADO_EN]->(l:LugarPremio)
RETURN l.nombre AS lugar, collect(pr.nombre) AS premios, count(pr) AS cantidad_premios
ORDER BY cantidad_premios DESC;

// O) Películas más conectadas del grafo (nodos centrales con más relaciones)
MATCH (p:Pelicula)
OPTIONAL MATCH (p)-[r1]->()
OPTIONAL MATCH (p)<-[r2]-()
WITH p, count(r1) + count(r2) AS total_conexiones
RETURN p.titulo AS pelicula, p.ranking AS ranking, total_conexiones
ORDER BY total_conexiones DESC
LIMIT 10;

