# Caso 5: Base de Datos de Grafos - Películas

## Descripción del Proyecto

Este proyecto implementa una base de datos de grafos usando Neo4j para gestionar información de películas, actores, directores, productores, críticas y premios. El modelo de grafos permite analizar relaciones complejas entre entidades del mundo cinematográfico.

## Estructura del Proyecto

```
caso5_grafo/
│
├── data/                      ← CSV exportados desde PostgreSQL
│   ├── pelicula.csv
│   ├── actor.csv
│   ├── director.csv
│   ├── productor.csv
│   ├── critica.csv
│   ├── premio.csv
│   ├── actuacion.csv         ← Relaciones actor-película
│   └── produccion.csv        ← Relaciones productor-película
│
├── scripts/
│   └── carga_datos.py       ← Script Python para cargar nodos y relaciones a Neo4j
│
├── docker-compose.yml       ← Archivo Docker para levantar Neo4j
├── Dockerfile               ← Imagen para aplicación Python
├── consultas.cypher         ← Consultas del negocio en Cypher
├── diagrama_grafo.png       ← Imagen del grafo generado desde la GUI de Neo4j
└── README.md                ← Este archivo
```

## Modelo de Datos

### Nodos Principales

- **Película**: id, título, fecha_estreno, resumen, ranking
- **Actor**: id, nombre, fecha_nacimiento, lugar_nacimiento, direccion, telefono, estado_civil
- **Director**: id, nombre, direccion, telefono
- **Productor**: id, nombre, direccion, telefono
- **Crítica**: id, medio, autor, fecha
- **Premio**: id, nombre, resumen, certamen, lugar, tipo

### Nodos de Agrupación (Estructura Jerárquica)

- **Decada**: Agrupa películas por década de estreno
- **CalidadPelicula**: Agrupa películas por ranking (Excelente, Buena, Regular, Baja)
- **ExperienciaActor**: Agrupa actores por edad (Veterano, Experimentado, Establecido, Joven)
- **Region**: Agrupa actores por lugar de nacimiento
- **LugarPremio**: Agrupa premios por lugar de otorgamiento

### Relaciones Principales

- **DIRIGIDA_POR**: Película → Director
- **ACTUADA_POR**: Película → Actor (con propiedades: tipo, salario)
- **PRODUCIDA_POR**: Película → Productor (con propiedades: aporte_economico)
- **TIENE_CRITICA**: Película → Crítica
- **TIENE_PREMIO**: Película → Premio

### Relaciones de Agrupación (Estructura de Árbol)

- **DE_LA_DECADA**: Película → Decada
- **TIENE_CALIDAD**: Película → CalidadPelicula
- **TIENE_EXPERIENCIA**: Actor → ExperienciaActor
- **NACIO_EN**: Actor → Region
- **OTORGADO_EN**: Premio → LugarPremio

### Relaciones de Colaboración

- **TRABAJO_CON**: Actor/Director/Productor ↔ Actor/Director/Productor
- **COACTUA_CON**: Actor ↔ Actor (mismo film)

## Instrucciones de Uso

### 1. Iniciar Neo4j

```bash
# Navegar al directorio del proyecto
cd caso5_grafo

# Iniciar solo Neo4j
docker-compose up -d neo4j
```

### 2. Acceder a la Interfaz Web

Abrir navegador en: http://localhost:7474

- **Usuario**: neo4j
- **Contraseña**: password123

### 3. Cargar Datos

```bash
# Ejecutar script de carga de datos
docker-compose run --rm app python3 scripts/carga_datos.py
```

**Resultado esperado:**
```
Iniciando carga de datos a Neo4j...
Neo4j está disponible
Base de datos limpiada
Índices creados

Cargando nodos...
Cargadas 101 películas
Cargados [X] actores
Cargados [X] directores
Cargados [X] productores
Cargadas [X] críticas
Cargados [X] premios

Creando relaciones...
Relaciones DIRIGIDA_POR creadas: [X]
Relaciones ACTUADA_POR creadas: [X]
Relaciones PRODUCIDA_POR creadas: [X]
Relaciones TIENE_CRITICA creadas: [X]
Relaciones TIENE_PREMIO creadas: [X]

Resumen de nodos cargados:
  Pelicula: 101
  Actor: [X]
  Director: [X]
  Productor: [X]
  Critica: [X]
  Premio: [X]

Carga de datos completada exitosamente!
```

### 4. Verificar Carga

En la interfaz web de Neo4j, ejecutar:

```cypher
MATCH (n) RETURN labels(n) as tipo, count(n) as cantidad
```

### 5. Ejecutar Consultas

Copiar y pegar las consultas del archivo `consultas.cypher` en la interfaz web de Neo4j.

## Consultas Principales

### Consultas de Evaluación (A-E)
1. **A) Total de salarios de "Cinema Paradiso"**
2. **B) Premios de "Cinema Paradiso"**
3. **C) Aportes económicos de Franco Cristaldi**
4. **D) Críticas entre fechas específicas**
5. **E) Personas involucradas con detalles**

### Consultas de Agrupación Jerárquica (F-O)
6. **F) Estructura completa del grafo**
7. **G) Películas agrupadas por década**
8. **H) Películas agrupadas por calidad**
9. **I) Actores agrupados por experiencia**
10. **J) Actores agrupados por región**
11. **K) Red de colaboraciones**
12. **L) Coactores que trabajaron juntos**
13. **M) Estructura jerárquica completa**
14. **N) Árbol de premios por lugar**
15. **O) Películas más conectadas**

## Ventajas del Modelo de Grafos

1. **Relaciones Naturales**: Representa conexiones complejas entre entidades
2. **Consultas Eficientes**: Navegación rápida por relaciones
3. **Análisis de Redes**: Identificación de patrones y colaboraciones
4. **Flexibilidad**: Fácil adición de nuevos tipos de nodos y relaciones
5. **Visualización**: Interface gráfica intuitiva para explorar datos

## Tecnologías Utilizadas

- **Neo4j 5.15**: Base de datos de grafos
- **Python 3.11**: Scripts de carga y procesamiento
- **Pandas**: Manipulación de datos CSV
- **Docker**: Containerización
- **Cypher**: Lenguaje de consulta para grafos

## Comandos Útiles

```bash
# Ver logs de Neo4j
docker-compose logs neo4j

# Detener servicios
docker-compose down

# Limpiar volúmenes (eliminar datos)
docker-compose down -v

# Reconstruir servicios
docker-compose build --no-cache
```

## Solución de Problemas

### Error: 'fecha_nacimiento' no encontrado
Este error indica que la estructura del CSV no coincide con lo esperado. El script se ha actualizado para usar los campos correctos:
- Actor: `fecha_nac` en lugar de `fecha_nacimiento`
- Director: solo `nombre`, `direccion`, `telefono` (sin fecha de nacimiento)
- Productor: solo `nombre`, `direccion`, `telefono` (sin fecha de nacimiento)

### Si la carga falla
1. Verificar que Neo4j esté ejecutándose: `docker-compose logs neo4j`
2. Limpiar la base de datos: `docker-compose down -v && docker-compose up -d neo4j`
3. Ejecutar nuevamente la carga después de 30 segundos

### Verificar estructura de CSV
```bash
# Ver las primeras líneas de cada archivo
head -n 3 data/*.csv
```
