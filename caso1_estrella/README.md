# Caso 1: Modelo Estrella - Base de Datos de Peliculas

## Descripcion
Este proyecto implementa un modelo de base de datos en estrella para el analisis de informacion cinematografica, especificamente enfocado en la pelicula "Cinema Paradiso" y sus datos relacionados.

## Arquitectura del Sistema

### Modelo Estrella Implemen### 3. Migración a OLAP (Opcional)
Para aprovech### 5. Comparación SQL vs MDX vs Cubo OLAP Simulado

#### SQL Tradicional (Implementacion base):
- Funciona con PostgreSQL existente
- Sintaxis familiar y estandar
- Mayor flexibilidad para consultas ad-hoc
- Mejor para operaciones transaccionales

#### MDX Real (Conceptual):
- Optimizado para analisis multidimensional
- Manejo nativo de jerarquias temporales
- Funciones avanzadas de ranking y comparacion
- Mejor rendimiento para consultas analiticas complejas
- Requiere infraestructura OLAP especifica (SSAS)

#### Cubo OLAP Simulado (Implementado):
- **Combina lo mejor de ambos mundos**
- Analisis multidimensional con PostgreSQL
- Vistas y funciones optimizadas para OLAP
- Drill-down, drill-through y metricas calculadas
- Dashboard y KPIs automaticos
- Sin necesidad de infraestructura adicional
- Escalable y mantenibleas MDX:
- **SQL Server Analysis Services**: Crear cubo basado en el modelo estrella
- **Power BI**: Conectar directamente al modelo tabular
- **Excel**: Crear tablas dinamicas avanzadas

### 4. Simulacion de Cubo OLAP Implementada

**NOVEDAD!** Se ha implementado una simulacion completa de cubo OLAP usando PostgreSQL que permite:

#### Funcionalidades OLAP Disponibles:
- **Vistas dimensionales** con jerarquias temporales
- **Metricas calculadas** (ROI, percentiles, rankings)
- **Drill-through** para obtener datos detallados
- **Funciones de analisis** multidimensional
- **Dashboard principal** con KPIs
- **Analisis de contribucion** por dimensiones
- **Consultas CUBE y ROLLUP** para agregaciones
- **Indices optimizados** para consultas analiticas

#### Componentes del Cubo OLAP:
```sql
-- Vistas principales
dim_tiempo_olap          -- Dimension temporal con jerarquias
hechos_olap             -- Hechos con metricas calculadas
dim_personas_olap       -- Dimension consolidada de personas

-- Funciones analiticas
drill_through_detallado()     -- Exploracion detallada
analisis_contribucion()       -- Analisis de participacion
actualizar_cubo_olap()       -- Mantenimiento del cubo

-- Vistas de analisis
dashboard_principal          -- KPIs y metricas generales
analisis_temporal           -- Tendencias temporales
ranking_personas           -- Clasificacion por performance
```

#### Ventajas de la Simulacion OLAP:
- **Rendimiento mejorado** con indices especializados
- **Analisis multidimensional** sin infraestructura adicional
- **Drill-down y drill-through** funcionales
- **Metricas calculadas** automaticas (ROI, percentiles)
- **Compatibilidad total** con PostgreSQL existente
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
- **hechos_peliculas**: Contiene las metricas y hechos centrales
  - `id_pelicula` (FK)
  - `id_actor` (FK)
  - `id_director` (FK)
  - `id_productor` (FK)
  - `id_fecha` (FK)
  - `salario` (NUMERIC)
  - `aportacion` (NUMERIC)
  - `ranking` (NUMERIC)

#### Tablas de Dimensiones
- **dim_pelicula**: Informacion de peliculas
- **dim_actor**: Informacion de actores
- **dim_director**: Informacion de directores
- **dim_productor**: Informacion de productores
- **dim_fecha**: Dimension temporal

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

### 1. Preparacion del Entorno
```powershell
# Navegar al directorio del proyecto
cd "c:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso1_estrella"

# Verificar que Docker este corriendo
docker --version
docker-compose --version
```

### 2. Construccion y Ejecucion
```powershell
# Construir y levantar todos los servicios
docker-compose up --build

# Para ejecutar en segundo plano (opcional)
docker-compose up --build -d
```

### 3. Verificacion del Estado
```powershell
# Verificar que los contenedores esten corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs postgres-caso1

# Ver logs de las consultas
docker-compose logs consultas-caso1
```

### 4. Acceso a la Base de Datos

#### Opcion A: Adminer (Interfaz Web)
1. Abrir navegador en `http://localhost:8080`
2. Configurar conexion:
   - **Sistema**: PostgreSQL
   - **Servidor**: postgres-caso1
   - **Usuario**: postgres
   - **Contrasena**: 123
   - **Base de datos**: caso1

#### Opcion B: Linea de Comandos
```powershell
# Conectar directamente a PostgreSQL
docker-compose exec postgres-caso1 psql -U postgres -d caso1

# Listar todas las tablas
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "\dt"

# Ver estructura de tabla especifica
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "\d hechos_peliculas"
```

## Estructura de Archivos

```
caso1_estrella/
├── docker-compose.yml            # Orquestacion de contenedores
├── Dockerfile                   # Imagen personalizada de PostgreSQL
├── caso1.sql                    # Estructura del modelo estrella
├── poblado_modelo_estrella.sql  # Datos de prueba
├── consultas_sql_corregidas.sql      # Consultas SQL funcionales 
├── consultas_mdx_conceptuales.mdx    # Consultas MDX conceptuales para OLAP
├── test_connection.py           # Script de prueba de conexion
├── README.md                    # Esta documentacion
```

## Menu de Opciones de Consulta

El proyecto ofrece **DOS ENFOQUES** para trabajar con el modelo estrella:

### **Opcion A: Consultas SQL Tradicionales (Recomendado para PostgreSQL)**
- **Archivo**: `consultas_sql_corregidas.sql`
- **Tecnologia**: SQL estandar con PostgreSQL
- **Ventajas**: 
  - Funciona inmediatamente con la infraestructura actual
  - Sintaxis familiar y probada
  - Ideal para analisis directo y reportes

### **Opcion B: Consultas MDX Conceptuales (Referencia para OLAP)**
- **Archivo**: `consultas_mdx_conceptuales.mdx`
- **Tecnologia**: MDX (Multidimensional Expressions)
- **Ventajas**:
  - Referencia para implementaciones OLAP futuras
  - Sintaxis optimizada para analisis multidimensional
  - Ideal para migracion a SQL Server Analysis Services

## Servicios del Docker Compose

### 1. postgres-caso1
- **Imagen**: Personalizada basada en postgres:15
- **Puerto**: 5433:5432
- **Base de datos**: caso1
- **Usuario**: postgres
- **Contrasena**: 123
- **Funcion**: Base de datos principal con modelo estrella

### 2. consultas-caso1
- **Imagen**: postgres:15
- **Funcion**: Ejecuta automaticamente las consultas de prueba
- **Dependencia**: Espera a que postgres-caso1 este saludable

### 3. adminer
- **Imagen**: adminer:latest
- **Puerto**: 8080:8080
- **Funcion**: Interfaz web para administracion de base de datos

## Consultas de Analisis Disponibles

### Archivos de Consultas

1. **`consultas_sql_corregidas.sql`** - **Consultas SQL funcionales para PostgreSQL**
2. **`consultas_mdx_conceptuales.mdx`** - **Consultas MDX conceptuales para cubos OLAP**

---

### **OPCION A: Consultas SQL Funcionales (PostgreSQL)**

#### A) Total de Salarios por Pelicula
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

#### B) Informacion Completa de la Pelicula
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

### **OPCION B: Consultas MDX Conceptuales (Cubos OLAP)**

#### A) Total Salarios con MDX
```mdx
SELECT 
  [Measures].[Salario] ON COLUMNS,
  [Pelicula].[Titulo].MEMBERS ON ROWS
FROM [Peliculas]
WHERE [Pelicula].[Titulo].[Cinema Paradiso]
```

#### B) Analisis Temporal con Jerarquias
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

**Nota**: Las consultas MDX requieren SQL Server Analysis Services o similar para ejecutarse. Son conceptuales para planificacion futura.

## Comandos Utiles

### Gestion de Contenedores
```powershell
# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reiniciar un servicio especifico
docker-compose restart postgres-caso1

# Ver logs en tiempo real
docker-compose logs -f postgres-caso1
```

### Comandos de Ejecucion por Opcion

#### **OPCION A: Ejecutar Consultas SQL (Recomendado)**

```powershell
# Verificar datos basicos
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT COUNT(*) FROM hechos_peliculas;"
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT * FROM dim_pelicula;"

# Ejecutar consulta simple de prueba
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT SUM(h.salario) AS total_salarios, p.titulo FROM hechos_peliculas h JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula WHERE p.titulo = 'Cinema Paradiso' GROUP BY p.titulo;"

# Ejecutar todas las consultas SQL corregidas
docker cp consultas_sql_corregidas.sql postgres-caso1-estrella:/tmp/
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -f /tmp/consultas_sql_corregidas.sql
```

#### **OPCION B: Referencia MDX (Solo Conceptual)**

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

### **Inicio Rapido - Opcion Recomendada**

```powershell
# 1. Levantar el entorno
docker-compose up --build

# 2. Verificar que funciona
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -c "SELECT p.titulo, d.nombre AS director, a.nombre AS actor, h.salario FROM hechos_peliculas h JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula JOIN dim_director d ON h.id_director = d.id_director JOIN dim_actor a ON h.id_actor = a.id_actor;"

# 3. Ejecutar analisis completo
docker cp consultas_sql_corregidas.sql postgres-caso1-estrella:/tmp/
docker-compose exec postgres-caso1 psql -U postgres -d caso1 -f /tmp/consultas_sql_corregidas.sql
```

## Solucion de Problemas

### Error: Puerto en Uso
```powershell
# Verificar que esta usando el puerto 5433
netstat -ano | findstr :5433

# Cambiar puerto en docker-compose.yml si es necesario
```

### Error: Docker no Disponible
```powershell
# Verificar que Docker Desktop este corriendo
docker info

# Reiniciar Docker Desktop si es necesario
```

### Error en Consultas
- Las consultas estan disenadas para el modelo estrella especifico
- Verificar que las tablas y columnas existan antes de ejecutar
- Revisar logs: `docker-compose logs consultas-caso1`

## Datos de Prueba

El sistema incluye datos de ejemplo para:
- **Pelicula**: Cinema Paradiso (1990)
- **Director**: Giuseppe Tornatore
- **Actor**: Ejemplo de actor principal
- **Productor**: Franco Cristaldi
- **Metricas**: Salarios, aportes economicos, rankings

## Proximos Pasos

### 1. **Migracion a OLAP Real (Opcion B)**
Para implementar las consultas MDX:
- **SQL Server Analysis Services (SSAS)**: Crear cubo basado en el modelo estrella
- **Power BI**: Crear modelo tabular y conectar
- **Azure Analysis Services**: Implementacion en la nube

Para problemas o mejoras, revisar:
- Logs de Docker: `docker-compose logs`
- Estado de servicios: `docker-compose ps`
- Conexion a BD: Usar test_connection.py

