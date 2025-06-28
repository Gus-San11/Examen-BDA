-- =================================================================
-- SIMULACIÓN DE CUBO OLAP - IMPLEMENTACIÓN SQL EJECUTABLE
-- =================================================================
-- Este archivo implementa un cubo OLAP funcional usando PostgreSQL
-- Permite ejecutar consultas tipo MDX usando SQL avanzado
-- =================================================================

-- ===========================
-- 1. VISTAS PARA SIMULAR DIMENSIONES OLAP
-- ===========================

-- Dimensión temporal con jerarquías
CREATE OR REPLACE VIEW dim_tiempo_olap AS
SELECT 
    id_fecha,
    anio,
    mes,
    dia,
    trimestre,
    CASE 
        WHEN trimestre = 1 THEN 'Q1-' || anio
        WHEN trimestre = 2 THEN 'Q2-' || anio  
        WHEN trimestre = 3 THEN 'Q3-' || anio
        WHEN trimestre = 4 THEN 'Q4-' || anio
    END as periodo_trimestral,
    CASE 
        WHEN mes <= 6 THEN 'H1-' || anio
        ELSE 'H2-' || anio
    END as semestre,
    anio || '-' || LPAD(mes::text, 2, '0') as periodo_mensual,
    EXTRACT(week FROM id_fecha) as semana,
    TO_CHAR(id_fecha, 'Day') as dia_semana
FROM dim_fecha;

-- Hechos enriquecidos con métricas calculadas
CREATE OR REPLACE VIEW hechos_olap AS
SELECT 
    h.*,
    -- Métricas calculadas (simulando medidas OLAP)
    CASE 
        WHEN h.aportacion > 0 THEN h.ranking / h.aportacion * 100 
        ELSE 0 
    END as roi_porcentaje,
    h.salario / NULLIF(h.aportacion, 0) * 100 as costo_salario_porcentaje,
    RANK() OVER (ORDER BY h.salario DESC) as ranking_salario,
    PERCENT_RANK() OVER (ORDER BY h.salario) as percentil_salario,
    NTILE(4) OVER (ORDER BY h.salario) as cuartil_salario,
    h.salario - AVG(h.salario) OVER () as desviacion_salario_promedio
FROM hechos_peliculas h;

-- Dimensión de personas consolidada
CREATE OR REPLACE VIEW dim_personas_olap AS
SELECT 
    'Actor' as tipo_persona,
    id_actor as id_persona,
    nombre,
    edad,
    estado_civil,
    NULL as telefono
FROM dim_actor
UNION ALL
SELECT 
    'Director' as tipo_persona,
    id_director as id_persona,
    nombre,
    NULL as edad,
    NULL as estado_civil,
    NULL as telefono
FROM dim_director
UNION ALL
SELECT 
    'Productor' as tipo_persona,
    id_productor as id_persona,
    nombre,
    NULL as edad,
    NULL as estado_civil,
    NULL as telefono
FROM dim_productor;

-- ===========================
-- 2. FUNCIONES PARA SIMULACIÓN OLAP
-- ===========================

-- Función drill-through detallado
CREATE OR REPLACE FUNCTION drill_through_detallado(
    titulo_param TEXT DEFAULT NULL,
    director_param TEXT DEFAULT NULL,
    actor_param TEXT DEFAULT NULL,
    productor_param TEXT DEFAULT NULL
)
RETURNS TABLE (
    pelicula TEXT,
    director TEXT,
    actor TEXT,
    productor TEXT,
    fecha DATE,
    anio INTEGER,
    trimestre TEXT,
    salario NUMERIC,
    aportacion NUMERIC,
    ranking NUMERIC,
    roi_porcentaje NUMERIC,
    cuartil_salario INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.titulo::TEXT,
        d.nombre::TEXT,
        a.nombre::TEXT,
        pr.nombre::TEXT,
        h.id_fecha,
        t.anio,
        t.periodo_trimestral::TEXT,
        h.salario,
        h.aportacion,
        h.ranking,
        h.roi_porcentaje,
        h.cuartil_salario
    FROM hechos_olap h
    JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
    JOIN dim_director d ON h.id_director = d.id_director
    JOIN dim_actor a ON h.id_actor = a.id_actor
    JOIN dim_productor pr ON h.id_productor = pr.id_productor
    JOIN dim_tiempo_olap t ON h.id_fecha = t.id_fecha
    WHERE (titulo_param IS NULL OR p.titulo = titulo_param)
      AND (director_param IS NULL OR d.nombre = director_param)  
      AND (actor_param IS NULL OR a.nombre = actor_param)
      AND (productor_param IS NULL OR pr.nombre = productor_param);
END;
$$ LANGUAGE plpgsql;

-- Función para análisis de contribución
CREATE OR REPLACE FUNCTION analisis_contribucion(dimension_param TEXT)
RETURNS TABLE (
    elemento TEXT,
    valor_absoluto NUMERIC,
    porcentaje_total NUMERIC,
    ranking INTEGER
) AS $$
BEGIN
    IF dimension_param = 'actor' THEN
        RETURN QUERY
        WITH totales AS (
            SELECT SUM(salario) as total_general FROM hechos_olap
        )
        SELECT 
            a.nombre::TEXT,
            SUM(h.salario) as valor_absoluto,
            ROUND((SUM(h.salario) / t.total_general * 100)::NUMERIC, 2) as porcentaje_total,
            RANK() OVER (ORDER BY SUM(h.salario) DESC)::INTEGER as ranking
        FROM hechos_olap h
        JOIN dim_actor a ON h.id_actor = a.id_actor
        CROSS JOIN totales t
        GROUP BY a.nombre, t.total_general
        ORDER BY valor_absoluto DESC;
    
    ELSIF dimension_param = 'director' THEN
        RETURN QUERY
        WITH totales AS (
            SELECT SUM(salario) as total_general FROM hechos_olap
        )
        SELECT 
            d.nombre::TEXT,
            SUM(h.salario) as valor_absoluto,
            ROUND((SUM(h.salario) / t.total_general * 100)::NUMERIC, 2) as porcentaje_total,
            RANK() OVER (ORDER BY SUM(h.salario) DESC)::INTEGER as ranking
        FROM hechos_olap h
        JOIN dim_director d ON h.id_director = d.id_director
        CROSS JOIN totales t
        GROUP BY d.nombre, t.total_general
        ORDER BY valor_absoluto DESC;
        
    ELSIF dimension_param = 'productor' THEN
        RETURN QUERY
        WITH totales AS (
            SELECT SUM(aportacion) as total_general FROM hechos_olap
        )
        SELECT 
            pr.nombre::TEXT,
            SUM(h.aportacion) as valor_absoluto,
            ROUND((SUM(h.aportacion) / t.total_general * 100)::NUMERIC, 2) as porcentaje_total,
            RANK() OVER (ORDER BY SUM(h.aportacion) DESC)::INTEGER as ranking
        FROM hechos_olap h
        JOIN dim_productor pr ON h.id_productor = pr.id_productor
        CROSS JOIN totales t
        GROUP BY pr.nombre, t.total_general
        ORDER BY valor_absoluto DESC;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ===========================
-- 3. CONSULTAS OLAP PREDEFINIDAS
-- ===========================

-- Vista para dashboard principal
CREATE OR REPLACE VIEW dashboard_principal AS
SELECT 
    'Métricas Generales' as categoria,
    'Total Salarios' as metrica,
    TO_CHAR(SUM(salario), 'FM$999,999,999.00') as valor,
    1 as orden
FROM hechos_olap
UNION ALL
SELECT 
    'Métricas Generales',
    'Total Aportaciones',
    TO_CHAR(SUM(aportacion), 'FM$999,999,999.00'),
    2
FROM hechos_olap
UNION ALL
SELECT 
    'Métricas Generales',
    'ROI Promedio',
    ROUND(AVG(roi_porcentaje), 2) || '%',
    3
FROM hechos_olap
UNION ALL
SELECT 
    'Métricas Generales',
    'Ranking Promedio',
    ROUND(AVG(ranking), 2)::TEXT,
    4
FROM hechos_olap
UNION ALL
SELECT 
    'Distribución',
    'Películas',
    COUNT(DISTINCT id_pelicula)::TEXT,
    5
FROM hechos_olap
UNION ALL
SELECT 
    'Distribución',
    'Actores',
    COUNT(DISTINCT id_actor)::TEXT,
    6
FROM hechos_olap
UNION ALL
SELECT 
    'Distribución', 
    'Directores',
    COUNT(DISTINCT id_director)::TEXT,
    7
FROM hechos_olap
UNION ALL
SELECT 
    'Distribución',
    'Productores', 
    COUNT(DISTINCT id_productor)::TEXT,
    8
FROM hechos_olap
ORDER BY orden;

-- Vista para análisis temporal
CREATE OR REPLACE VIEW analisis_temporal AS
SELECT 
    t.anio,
    t.periodo_trimestral,
    t.semestre,
    COUNT(*) as registros,
    SUM(h.salario) as total_salarios,
    SUM(h.aportacion) as total_aportaciones,
    AVG(h.ranking) as ranking_promedio,
    AVG(h.roi_porcentaje) as roi_promedio
FROM hechos_olap h
JOIN dim_tiempo_olap t ON h.id_fecha = t.id_fecha
GROUP BY t.anio, t.periodo_trimestral, t.semestre, t.trimestre
ORDER BY t.anio, t.trimestre;

-- Vista para ranking de personas
CREATE OR REPLACE VIEW ranking_personas AS
SELECT 
    'Actor' as tipo,
    a.nombre,
    a.edad,
    SUM(h.salario) as total_salarios,
    AVG(h.ranking) as ranking_promedio,
    COUNT(*) as participaciones,
    RANK() OVER (ORDER BY SUM(h.salario) DESC) as posicion
FROM hechos_olap h
JOIN dim_actor a ON h.id_actor = a.id_actor
GROUP BY a.id_actor, a.nombre, a.edad
UNION ALL
SELECT 
    'Director',
    d.nombre,
    NULL,
    SUM(h.salario),
    AVG(h.ranking),
    COUNT(*),
    RANK() OVER (ORDER BY SUM(h.salario) DESC)
FROM hechos_olap h
JOIN dim_director d ON h.id_director = d.id_director
GROUP BY d.id_director, d.nombre
UNION ALL
SELECT 
    'Productor',
    pr.nombre,
    NULL,
    SUM(h.aportacion), -- Para productores usamos aportación
    AVG(h.ranking),
    COUNT(*),
    RANK() OVER (ORDER BY SUM(h.aportacion) DESC)
FROM hechos_olap h
JOIN dim_productor pr ON h.id_productor = pr.id_productor
GROUP BY pr.id_productor, pr.nombre
ORDER BY tipo, posicion;

-- ===========================
-- 4. CONSULTAS DE EJEMPLO PARA TESTING
-- ===========================

-- Ejemplo 1: Dashboard completo
-- SELECT * FROM dashboard_principal;

-- Ejemplo 2: Análisis temporal
-- SELECT * FROM analisis_temporal;

-- Ejemplo 3: Ranking de personas
-- SELECT * FROM ranking_personas WHERE tipo = 'Actor';

-- Ejemplo 4: Drill-through específico
-- SELECT * FROM drill_through_detallado('Cinema Paradiso');

-- Ejemplo 5: Análisis de contribución por actor
-- SELECT * FROM analisis_contribucion('actor');

-- Ejemplo 6: Cubo multidimensional simple
/*
SELECT 
    COALESCE(p.titulo, 'TOTAL') as pelicula,
    COALESCE(t.periodo_trimestral, 'TODOS') as periodo,
    SUM(h.salario) as total_salarios,
    AVG(h.roi_porcentaje) as roi_promedio
FROM hechos_olap h
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
JOIN dim_tiempo_olap t ON h.id_fecha = t.id_fecha
GROUP BY CUBE(p.titulo, t.periodo_trimestral)
ORDER BY total_salarios DESC NULLS LAST;
*/

-- ===========================
-- 5. ÍNDICES PARA OPTIMIZACIÓN OLAP
-- ===========================

-- Índices para mejorar rendimiento de consultas OLAP
CREATE INDEX IF NOT EXISTS idx_hechos_pelicula ON hechos_peliculas(id_pelicula);
CREATE INDEX IF NOT EXISTS idx_hechos_actor ON hechos_peliculas(id_actor);
CREATE INDEX IF NOT EXISTS idx_hechos_director ON hechos_peliculas(id_director);
CREATE INDEX IF NOT EXISTS idx_hechos_productor ON hechos_peliculas(id_productor);
CREATE INDEX IF NOT EXISTS idx_hechos_fecha ON hechos_peliculas(id_fecha);
CREATE INDEX IF NOT EXISTS idx_hechos_salario ON hechos_peliculas(salario);
CREATE INDEX IF NOT EXISTS idx_hechos_aportacion ON hechos_peliculas(aportacion);

-- Índice compuesto para consultas multidimensionales
CREATE INDEX IF NOT EXISTS idx_hechos_multidim ON hechos_peliculas(id_pelicula, id_actor, id_fecha);

-- ===========================
-- 6. PROCEDIMIENTO DE ACTUALIZACIÓN DEL CUBO
-- ===========================

CREATE OR REPLACE FUNCTION actualizar_cubo_olap()
RETURNS TEXT AS $$
BEGIN
    -- Refresh de vistas materializadas si las hubiera
    -- REFRESH MATERIALIZED VIEW hechos_olap_mv;
    
    -- Actualizar estadísticas para optimización
    ANALYZE hechos_peliculas;
    ANALYZE dim_pelicula;
    ANALYZE dim_actor;
    ANALYZE dim_director;
    ANALYZE dim_productor;
    ANALYZE dim_fecha;
    
    RETURN 'Cubo OLAP actualizado exitosamente en ' || NOW();
END;
$$ LANGUAGE plpgsql;

-- Ejecutar actualización del cubo
-- SELECT actualizar_cubo_olap();
