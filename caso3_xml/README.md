# Caso 3: Base de Datos XML - Películas

## Descripción del Proyecto

Este proyecto implementa una base de datos XML para gestionar información de películas utilizando PostgreSQL con soporte nativo para XML. Se centra en la película "Cinema Paradiso" como caso de estudio principal.

## Justificación de las Características XML Utilizadas

### 1. Estructura Jerárquica
- **Elemento raíz `<peliculas>`**: Contiene una colección de películas
- **Elemento `<pelicula>`**: Representa cada película individual con atributo `id` único
- **Justificación**: XML es ideal para representar datos jerárquicos complejos como la información de películas que incluye múltiples niveles de anidación (actores, productores, premios, críticas)

### 2. Elementos Anidados Complejos
- **`<director>`**: Información del director (nombre, teléfono, estado civil, fecha de nacimiento)
- **`<actores>`**: Colección de actores con detalles individuales
- **`<productores>`**: Información de productores con aportes económicos
- **`<premios>`**: Lista de premios recibidos con ranking
- **`<criticas>`**: Críticas de medios especializados
- **Justificación**: Permite modelar relaciones uno-a-muchos de forma natural sin necesidad de tablas de unión

### 3. Atributos vs Elementos
- **Atributos**: Utilizados para identificadores únicos (`id` en película)
- **Elementos**: Utilizados para datos descriptivos y contenido estructurado
- **Justificación**: Los atributos son ideales para metadatos simples, mientras que los elementos permiten mejor extensibilidad y validación

### 4. Tipos de Datos Específicos
- **Fechas**: `fecha_estreno`, `fecha_nacimiento` (formato ISO 8601)
- **Números**: `ranking`, `salario`, `aporte_economico`
- **Texto**: `titulo`, `resumen`, `nombre`
- **Justificación**: XML permite validación de tipos de datos específicos y conversión automática en PostgreSQL

### 5. Repetición de Elementos
- **Múltiples actores**: `<actor>` dentro de `<actores>`
- **Múltiples premios**: `<premio>` dentro de `<premios>`
- **Múltiples críticas**: `<critica>` dentro de `<criticas>`
- **Justificación**: XML maneja naturalmente colecciones de elementos similares sin restricciones de cardinalidad

### 6. Schema de Validación (XSD)
- **Validación estructural**: Garantiza que el XML sigue la estructura esperada
- **Tipos de datos**: Valida que los campos tengan el tipo correcto
- **Restricciones**: Define elementos obligatorios y opcionales
- **Justificación**: Asegura integridad de datos y consistencia en la estructura

## Ventajas del Enfoque XML

### 1. **Flexibilidad Estructural**
- Permite agregar nuevos campos sin alterar la estructura de la base de datos
- Facilita la evolución del esquema de datos
- Soporte para datos semi-estructurados

### 2. **Consultas XPath Potentes**
- Búsquedas específicas en la estructura jerárquica
- Filtrado basado en múltiples criterios
- Navegación por nodos padre-hijo

### 3. **Integridad de Datos**
- Validación mediante XSD
- Datos auto-contenidos en un solo documento
- Reducción de inconsistencias relacionales

### 4. **Interoperabilidad**
- Formato estándar reconocido universalmente
- Fácil intercambio de datos entre sistemas
- Soporte nativo en PostgreSQL

## Consultas Implementadas

### A) Agregación de Salarios
```sql
SELECT SUM(...) AS total_salarios
FROM peliculas_xml, generate_series(...)
```
**Propósito**: Calcular el total de salarios de actores usando funciones de agregación con XPath

### B) Ordenamiento por Atributos
```sql
SELECT unnest(xpath(...)) AS ranking
FROM peliculas_xml
ORDER BY ranking DESC
```
**Propósito**: Extraer y ordenar premios por ranking utilizando `unnest()` para descomponer arrays

### C) Búsqueda por Atributo Específico
```sql
SELECT SUM(...) WHERE nombre="Franco Cristaldi"
```
**Propósito**: Filtrar por nombre específico de productor y sumar aportes económicos

### D) Filtrado por Rango de Fechas
```sql
WHERE fecha_text::date BETWEEN '1990-08-15' AND '1990-08-30'
```
**Propósito**: Demostrar consultas temporales con conversión de tipos de XML a PostgreSQL

### E) Unión de Múltiples Elementos
```sql
WITH datos AS (
  SELECT ... 'Actor' AS rol
  UNION ALL
  SELECT ... 'Director' AS rol
  UNION ALL
  SELECT ... 'Productor' AS rol
)
```
**Propósito**: Consolidar información de diferentes roles en una vista unificada

## Tecnologías Utilizadas

- **PostgreSQL 15**: Base de datos con soporte nativo para XML
- **Python 3**: Para scripts de carga y pruebas
- **psycopg2**: Conector PostgreSQL para Python
- **Docker**: Containerización para portabilidad
- **XPath 1.0**: Lenguaje de consulta XML

## Estructura del Proyecto

```
caso3_xml/
├── docker-compose.yml     # Configuración de servicios
├── Dockerfile            # Imagen personalizada PostgreSQL + Python
├── peliculas.xml         # Datos XML de películas
├── schema_peliculas.xsd  # Schema de validación
├── estructura_xml.sql    # DDL y consultas
├── carga.py             # Script de carga de datos
├── test.py              # Script de pruebas
└── README.md            # Este archivo
```

## Instrucciones de Uso

### 1. Construcción y Ejecución

```bash
# Navegar al directorio del proyecto
cd "c:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso3_xml"

# Construir las imágenes Docker
docker-compose build

# Iniciar el servicio PostgreSQL
docker-compose up -d postgres

# Esperar a que PostgreSQL esté completamente inicializado (15-20 segundos)
```

### 2. Carga de Datos

```bash
# Cargar los datos XML en la base de datos
docker-compose exec postgres python3 /app/carga.py
```

### 3. Ejecución de Pruebas

```bash
# Ejecutar todas las consultas XML de prueba
docker-compose exec postgres python3 /app/test.py
```

### 4. Verificación Manual

```bash
# Verificar que los datos están cargados
docker-compose exec postgres psql -U postgres -d caso3 -c "SELECT COUNT(*) FROM peliculas_xml;"

# Probar consulta XPath simple
docker-compose exec postgres psql -U postgres -d caso3 -c "SELECT xpath('//pelicula/titulo/text()', contenido) FROM peliculas_xml;"
```

### 5. Conexión Directa a PostgreSQL

```bash
# Conectar directamente a la base de datos
docker-compose exec postgres psql -U postgres -d caso3
```

### 6. Limpieza

```bash
# Detener y limpiar contenedores
docker-compose down
```
