# Caso 1: Modelo Estrella - Base de Datos de Películas

## Descripción
Este proyecto implementa un modelo de base de datos en estrella para el análisis de información cinematográfica, específicamente enfocado en la película "Cinema Paradiso" y sus datos relacionados.

## Arquitectura del Sistema

### Modelo Estrella Implemen### 3. Migración a OLAP (Opcional)
Para aprovech### 5. Comparación SQL vs MDX vs Cubo OLAP Simulado

#### SQL Tradicional (Implementación base):
- ✅ Funciona con PostgreSQL existente
- ✅ Sintaxis familiar y estándar
- ✅ Mayor flexibilidad para consultas ad-hoc
- ✅ Mejor para operaciones transaccionales

#### MDX Real (Conceptual):
- ✅ Optimizado para análisis multidimensional
- ✅ Manejo nativo de jerarquías temporales
- ✅ Funciones avanzadas de ranking y comparación
- ✅ Mejor rendimiento para consultas analíticas complejas
- ❌ Requiere infraestructura OLAP específica (SSAS)

#### Cubo OLAP Simulado (Implementado) ⭐:
- ✅ **Combina lo mejor de ambos mundos**
- ✅ Análisis multidimensional con PostgreSQL
- ✅ Vistas y funciones optimizadas para OLAP
- ✅ Drill-down, drill-through y métricas calculadas
- ✅ Dashboard y KPIs automáticos
- ✅ Sin necesidad de infraestructura adicional
- ✅ Escalable y mantenibleas MDX:
- **SQL Server Analysis Services**: Crear cubo basado en el modelo estrella
- **Power BI**: Conectar directamente al modelo tabular
- **Excel**: Crear tablas dinámicas avanzadas

### 4. Simulación de Cubo OLAP Implementada ✅

**¡NOVEDAD!** Se ha implementado una simulación completa de cubo OLAP usando PostgreSQL que permite:

#### Funcionalidades OLAP Disponibles:
- ✅ **Vistas dimensionales** con jerarquías temporales
- ✅ **Métricas calculadas** (ROI, percentiles, rankings)
- ✅ **Drill-through** para obtener datos detallados
- ✅ **Funciones de análisis** multidimensional
- ✅ **Dashboard principal** con KPIs
- ✅ **Análisis de contribución** por dimensiones
- ✅ **Consultas CUBE y ROLLUP** para agregaciones
- ✅ **Índices optimizados** para consultas analíticas

#### Componentes del Cubo OLAP:
```sql
-- Vistas principales
dim_tiempo_olap          -- Dimensión temporal con jerarquías
hechos_olap             -- Hechos con métricas calculadas
dim_personas_olap       -- Dimensión consolidada de personas

-- Funciones analíticas
drill_through_detallado()     -- Exploración detallada
analisis_contribucion()       -- Análisis de participación
actualizar_cubo_olap()       -- Mantenimiento del cubo

-- Vistas de análisis
dashboard_principal          -- KPIs y métricas generales
analisis_temporal           -- Tendencias temporales
ranking_personas           -- Clasificación por performance
```

#### Ventajas de la Simulación OLAP:
- 🚀 **Rendimiento mejorado** con índices especializados
- 📊 **Análisis multidimensional** sin infraestructura adicional
- 🔍 **Drill-down y drill-through** funcionales
- 📈 **Métricas calculadas** automáticas (ROI, percentiles)
- 🎯 **Compatibilidad total** con PostgreSQL existente
```
           dim_fecha
               |
               |
dim_actor --- hechos_peliculas --- dim_productor
               |
               |
         dim_pelicula
               |
               |
          dim_director
```

### Tablas del Modelo

#### Tabla de Hechos
- **hechos_peliculas**: Contiene las métricas y hechos centrales
  - `id_pelicula` (FK)
  - `id_actor` (FK)
  - `id_director` (FK)
  - `id_productor` (FK)
  - `id_fecha` (FK)
  - `salario` (NUMERIC)
  - `aportacion` (NUMERIC)
  - `ranking` (NUMERIC)

#### Tablas de Dimensiones
- **dim_pelicula**: Información de películas
- **dim_actor**: Información de actores
- **dim_director**: Información de directores
- **dim_productor**: Información de productores
- **dim_fecha**: Dimensión temporal

## Requisitos del Sistema

### Software Necesario
- Docker Desktop
- Docker Compose
- PostgreSQL (incluido en el contenedor)
- Adminer (incluido para administración web)

### Puertos Utilizados
- **5433**: PostgreSQL Database
- **8080**: Adminer Web Interface

## Pasos para Ejecutar el Proyecto

### 1. Preparación del Entorno
```powershell
# Navegar al directorio del proyecto
cd "c:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso1_estrella"

# Verificar que Docker esté corriendo
docker --version
docker-compose --version
```

### 2. Construcción y Ejecución
```powershell
# Construir y levantar todos los servicios
docker-compose up --build

# Para ejecutar en segundo plano (opcional)
docker-compose up --build -d
```

### 3. Verificación del Estado
```powershell
# Verificar que los contenedores estén corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs postgres-caso1

# Ver logs de las consultas
docker-compose logs consultas-caso1
```

### 4. Acceso a la Base de Datos

#### Opción A: Adminer (Interfaz Web)
1. Abrir navegador en `http://localhost:8080`
2. Configurar conexión:
   - **Sistema**: PostgreSQL
   - **Servidor**: postgres-caso1
   - **Usuario**: postgres
   - **Contraseña**: 123
   - **Base de datos**: caso1

#### Opción B: Línea de Comandos
```powershell
# Conectar directamente a PostgreSQL
docker-compose exec postgres-caso1 psql -U postgres -d caso1

# Listar todas las tablas
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "\dt"

# Ver estructura de tabla específica
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "\d hechos_peliculas"
```

## Estructura de Archivos

```
caso1_estrella/
├── docker-compose.yml            # Orquestación de contenedores
├── Dockerfile                   # Imagen personalizada de PostgreSQL
├── caso1.sql                    # Estructura del modelo estrella
├── poblado_modelo_estrella.sql  # Datos de prueba
├── consultas_sql_corregidas.sql      # ✅ Consultas SQL funcionales 
├── consultas_mdx_conceptuales.mdx    # ✅ Consultas MDX conceptuales para OLAP
├── test_connection.py           # Script de prueba de conexión
├── README.md                    # Esta documentación
└── scripts/                     # Scripts adicionales
```

## 🎯 Menú de Opciones de Consulta

El proyecto ofrece **DOS ENFOQUES** para trabajar con el modelo estrella:

### 📊 **Opción A: Consultas SQL Tradicionales (Recomendado para PostgreSQL)**
- **Archivo**: `consultas_sql_corregidas.sql`
- **Tecnología**: SQL estándar con PostgreSQL
- **Ventajas**: 
  - ✅ Funciona inmediatamente con la infraestructura actual
  - ✅ Sintaxis familiar y probada
  - ✅ Ideal para análisis directo y reportes

### 🔮 **Opción B: Consultas MDX Conceptuales (Referencia para OLAP)**
- **Archivo**: `consultas_mdx_conceptuales.mdx`
- **Tecnología**: MDX (Multidimensional Expressions)
- **Ventajas**:
  - ✅ Referencia para implementaciones OLAP futuras
  - ✅ Sintaxis optimizada para análisis multidimensional
  - ✅ Ideal para migración a SQL Server Analysis Services

### 🤔 **¿Cuál elegir?**

| Criterio | SQL Tradicional | MDX Conceptual |
|----------|----------------|----------------|
| **Ejecución inmediata** | ✅ Si | ❌ No (requiere SSAS) |
| **Infraestructura actual** | ✅ PostgreSQL | ❌ Requiere OLAP Server |
| **Curva de aprendizaje** | ✅ Baja | ⚠️ Media-Alta |
| **Análisis multidimensional** | ⚠️ Limitado | ✅ Nativo |
| **Flexibilidad** | ✅ Alta | ⚠️ Media |
| **Rendimiento OLAP** | ⚠️ Bueno | ✅ Excelente |

**💡 Recomendación**: Comienza con **Opción A** (SQL) para resultados inmediatos, usa **Opción B** (MDX) como referencia para futuras implementaciones OLAP.

## Servicios del Docker Compose

### 1. postgres-caso1
- **Imagen**: Personalizada basada en postgres:15
- **Puerto**: 5433:5432
- **Base de datos**: caso1
- **Usuario**: postgres
- **Contraseña**: 123
- **Función**: Base de datos principal con modelo estrella

### 2. consultas-caso1
- **Imagen**: postgres:15
- **Función**: Ejecuta automáticamente las consultas de prueba
- **Dependencia**: Espera a que postgres-caso1 esté saludable

### 3. adminer
- **Imagen**: adminer:latest
- **Puerto**: 8080:8080
- **Función**: Interfaz web para administración de base de datos

## Consultas de Análisis Disponibles

### 📁 Archivos de Consultas

1. **`consultas_sql_corregidas.sql`** ✅ - **Consultas SQL funcionales para PostgreSQL**
2. **`consultas_mdx_conceptuales.mdx`** ✅ - **Consultas MDX conceptuales para cubos OLAP**

---

### 🚀 **OPCIÓN A: Consultas SQL Funcionales (PostgreSQL)**

#### A) Total de Salarios por Película
```sql
SELECT 
    SUM(h.salario) AS total_salarios,
    p.titulo,
    d.nombre AS director
FROM hechos_peliculas h
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
JOIN dim_director d ON h.id_director = d.id_director
WHERE p.titulo = 'Cinema Paradiso'
GROUP BY p.titulo, d.nombre;
```

#### B) Información Completa de la Película
```sql
SELECT 
    p.titulo, d.nombre AS director, a.nombre AS actor,
    pr.nombre AS productor, h.salario, h.aportacion, h.ranking
FROM hechos_peliculas h
JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
JOIN dim_director d ON h.id_director = d.id_director
JOIN dim_actor a ON h.id_actor = a.id_actor
JOIN dim_productor pr ON h.id_productor = pr.id_productor
WHERE p.titulo = 'Cinema Paradiso';
```

#### C) Aportes por Productor
```sql
SELECT 
    pr.nombre AS productor,
    SUM(h.aportacion) AS total_aporte,
    COUNT(*) AS num_peliculas
FROM hechos_peliculas h
JOIN dim_productor pr ON h.id_productor = pr.id_productor
GROUP BY pr.nombre ORDER BY total_aporte DESC;
```

---

### 🎯 **OPCIÓN B: Consultas MDX Conceptuales (Cubos OLAP)**

#### A) Total Salarios con MDX
```mdx
SELECT 
  [Measures].[Salario] ON COLUMNS,
  [Pelicula].[Titulo].MEMBERS ON ROWS
FROM [Peliculas]
WHERE [Pelicula].[Titulo].[Cinema Paradiso]
```

#### B) Análisis Temporal con Jerarquías
```mdx
SELECT 
  {[Measures].[Salario], [Measures].[Aportacion]} ON COLUMNS,
  [Tiempo].[Año-Trimestre-Mes].MEMBERS ON ROWS
FROM [Peliculas]
WHERE [Tiempo].[Año].[1990]
```

#### C) Top Actores con TOPCOUNT
```mdx
SELECT 
  [Measures].[Salario] ON COLUMNS,
  TOPCOUNT([Actor].[Nombre].MEMBERS, 5, [Measures].[Salario]) ON ROWS
FROM [Peliculas]
```

**📋 Nota**: Las consultas MDX requieren SQL Server Analysis Services o similar para ejecutarse. Son conceptuales para planificación futura.

## Comandos Útiles

### Gestión de Contenedores
```powershell
# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart postgres-caso1

# Ver logs en tiempo real
docker-compose logs -f postgres-caso1
```

### Comandos de Ejecución por Opción

#### 🚀 **OPCIÓN A: Ejecutar Consultas SQL (Recomendado)**

```powershell
# Verificar datos básicos
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT COUNT(*) FROM hechos_peliculas;"
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT * FROM dim_pelicula;"

# Ejecutar consulta simple de prueba
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT SUM(h.salario) AS total_salarios, p.titulo FROM hechos_peliculas h JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula WHERE p.titulo = 'Cinema Paradiso' GROUP BY p.titulo;"

# Ejecutar todas las consultas SQL corregidas
docker cp consultas_sql_corregidas.sql postgres-caso1-estrella:/tmp/
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -f /tmp/consultas_sql_corregidas.sql
```

#### 🎯 **OPCIÓN B: Referencia MDX (Solo Conceptual)**

```powershell
# Ver archivo de consultas MDX conceptuales
Get-Content consultas_mdx_conceptuales.mdx

# Para implementar MDX realmente, necesitarías:
# 1. SQL Server Analysis Services (SSAS)
# 2. Crear un proyecto de cubo OLAP
# 3. Definir dimensiones y medidas basadas en el modelo estrella
# 4. Procesar el cubo con datos del data warehouse
```

---

### ⚡ **Inicio Rápido - Opción Recomendada**

```powershell
# 1. Levantar el entorno
docker-compose up --build

# 2. Verificar que funciona
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT p.titulo, d.nombre AS director, a.nombre AS actor, h.salario FROM hechos_peliculas h JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula JOIN dim_director d ON h.id_director = d.id_director JOIN dim_actor a ON h.id_actor = a.id_actor;"

# 3. Ejecutar análisis completo
docker cp consultas_sql_corregidas.sql postgres-caso1-estrella:/tmp/
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -f /tmp/consultas_sql_corregidas.sql
```

## Solución de Problemas

### Error: Puerto en Uso
```powershell
# Verificar qué está usando el puerto 5433
netstat -ano | findstr :5433

# Cambiar puerto en docker-compose.yml si es necesario
```

### Error: Docker no Disponible
```powershell
# Verificar que Docker Desktop esté corriendo
docker info

# Reiniciar Docker Desktop si es necesario
```

### Error en Consultas
- Las consultas están diseñadas para el modelo estrella específico
- Verificar que las tablas y columnas existan antes de ejecutar
- Revisar logs: `docker-compose logs consultas-caso1`

## Datos de Prueba

El sistema incluye datos de ejemplo para:
- **Película**: Cinema Paradiso (1990)
- **Director**: Giuseppe Tornatore
- **Actor**: Ejemplo de actor principal
- **Productor**: Franco Cristaldi
- **Métricas**: Salarios, aportes económicos, rankings

## Próximos Pasos

### 1. **Optimización SQL (Opción A)**
- Implementar índices específicos para el modelo estrella
- Crear vistas materializadas para consultas frecuentes
- Agregar más datos de prueba para análisis más completos

### 2. **Migración a OLAP Real (Opción B)**
Para implementar las consultas MDX:
- **SQL Server Analysis Services (SSAS)**: Crear cubo basado en el modelo estrella
- **Power BI**: Crear modelo tabular y conectar
- **Azure Analysis Services**: Implementación en la nube

### 3. **Comparación Final de Enfoques**

| Aspecto | SQL (Opción A) | MDX (Opción B) |
|---------|----------------|----------------|
| **Estado** | ✅ Funcional | 📋 Conceptual |
| **Ejecución** | ✅ Inmediata | ❌ Requiere SSAS |
| **Aprendizaje** | ✅ Fácil | ⚠️ Complejo |
| **Infraestructura** | ✅ Mínima | ❌ Especializada |
| **Análisis OLAP** | ⚠️ Limitado | ✅ Nativo |
| **Futuro** | ✅ Extensible | ✅ Escalable |

### 4. **Recomendación de Uso**

- **Desarrollo/Testing**: Usar **Opción A** (SQL)
- **Producción Empresarial**: Considerar **Opción B** (MDX + SSAS)
- **Prototipado rápido**: **Opción A** siempre
- **Análisis avanzado futuro**: Planificar migración a **Opción B**

### 5. **Expansión del Modelo**
- Ampliar el dataset con más películas y personal
- Incluir dimensiones adicionales (género, país, presupuesto)
- Integrar herramientas de visualización (Power BI, Tableau)

## Contacto y Soporte

Para problemas o mejoras, revisar:
- Logs de Docker: `docker-compose logs`
- Estado de servicios: `docker-compose ps`
- Conexión a BD: Usar test_connection.py
