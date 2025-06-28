# Modelo Relacional-Objetual - Cinema Paradiso

Este proyecto implementa un modelo relacional-objetual en PostgreSQL para gestionar información sobre películas, actores, directores y productores, específicamente centrado en la película "Cinema Paradiso".

##  Arquitectura

El proyecto utiliza las características avanzadas de PostgreSQL:
- **Herencia de tablas**: `actor`, `director` y `productor` heredan de `persona`
- **Dominios personalizados**: Para validar estado civil, teléfonos y salarios
- **Tipos ENUM**: Para tipos de actuación y certámenes
- **Restricciones CHECK**: Para validar datos de entrada

##  Estructura de archivos

```
caso2_objetual/
├── docker-compose.yml              # Configuración de Docker Compose
├── Dockerfile                      # Imagen personalizada para tests
├── requirements.txt                # Dependencias de Python
├── estructura_relacional_objetual.sql  # DDL del modelo
├── poblado_relacional_objetual.sql     # DML con datos
├── consultas_relacional_objetual.sql   # Consultas del negocio
├── test_simple.py         # Script de pruebas
└── README.md                       # Este archivo
```

##  Inicio rápido

### Prerrequisitos
- Docker
- Docker Compose

### Levantar el entorno

1. **Clonar o navegar al directorio del proyecto:**
   ```bash
   cd caso2_objetual
   ```

2. **Levantar los servicios:**
   ```bash
   docker-compose up --build
   ```

3. **Ver los logs en tiempo real:**
   ```bash
   docker-compose logs -f
   ```

### Parar el entorno

```bash
docker-compose down
```

### Limpiar completamente (incluye volúmenes)

```bash
docker-compose down -v
```

##  Pruebas automatizadas

El script `test_simple.py` ejecuta las siguientes verificaciones:

1. **Conexión a la base de datos** - Verifica conectividad con PostgreSQL
2. **Estructura de la BD** - Valida dominios, tipos ENUM, tablas y herencia
3. **Población de datos** - Confirma que los datos se insertaron correctamente
4. **Funcionalidad de herencia** - Prueba las consultas con herencia
5. **Consultas del negocio** - Ejecuta todas las consultas requeridas

### Ejecutar pruebas manualmente

```bash
# Ejecutar solo el contenedor de pruebas

docker run --network caso2_objetual_cinema_network -e DB_HOST=postgres -e DB_PORT=5432 -e DB_NAME=cinema_db -e DB_USER=postgres -e DB_PASSWORD=password123 -v "${PWD}/test_simple.py:/app/test_simple.py" --rm caso2_objetual-test_app python test_simple.py


## 🔍 Consultas del negocio

El modelo implementa las siguientes consultas:

1. **Total de salarios** - Suma de salarios de actores en Cinema Paradiso
2. **Premios recibidos** - Lista de premios con ranking y lugar
3. **Aportaciones del productor** - Total de aportes de Franco Cristaldi
4. **Críticas del período** - Críticas entre el 15-30 de agosto de 1990
5. **Personas involucradas** - Actores, directores y productores con detalles

##  Acceso directo a la base de datos

### Usando psql desde el contenedor

```bash
# Conectar a PostgreSQL
docker-compose exec postgres psql -U postgres -d cinema_db

# Ejemplo de consultas
\dt                    # Listar tablas
\dD                    # Listar dominios
\dT                    # Listar tipos
SELECT * FROM persona; # Ver todas las personas
```

### Usando un cliente externo

- **Host:** localhost
- **Puerto:** 5432
- **Base de datos:** cinema_db
- **Usuario:** postgres
- **Contraseña:** password123

##  Servicios Docker

### PostgreSQL
- **Imagen:** postgres:15
- **Puerto:** 5432
- **Healthcheck:** Verifica disponibilidad cada 30s
- **Volúmenes:** 
  - Datos persistentes en `postgres_data`
  - Scripts SQL montados en `/docker-entrypoint-initdb.d/`

### Test App
- **Build:** Dockerfile personalizado
- **Dependencias:** psycopg2-binary, python-dotenv
- **Comando:** Ejecuta automáticamente las pruebas
- **Variables de entorno:** Configuración de BD

##  Desarrollo

### Modificar datos

1. Editar `poblado_relacional_objetual.sql`
2. Recrear los contenedores:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

### Agregar nuevas consultas

1. Editar `consultas_relacional_objetual.sql`
2. Actualizar `test_simple.py` si es necesario
3. Recrear el contenedor de pruebas:
   ```bash
   docker-compose build test_app
   docker-compose run --rm test_app
   ```

##  Características del modelo

### Herencia
- `persona` es la tabla padre
- `actor`, `director`, `productor` son tablas hijas
- Consultas automáticas incluyen datos heredados

### Dominios
- `estado_civil_dom`: Validación de estados civiles
- `telefono_dom`: Formato de 10 dígitos
- `salario_dom`: Rango de $600,000 a $4,900,000

### Restricciones
- Resúmenes de películas: 250-450 caracteres
- Rankings: 1.0 a 5.0
- Aportaciones: Mayor a 0

## 🔧 Troubleshooting

### Error de conexión
```
FATAL: password authentication failed
```
**Solución:** Verificar credenciales en docker-compose.yml

### PostgreSQL no inicia
```
PostgreSQL Database directory appears to contain a database
```
**Solución:** Limpiar volúmenes con `docker-compose down -v`

### Errores en scripts SQL
```
ERROR: relation "tabla" does not exist
```
**Solución:** Verificar orden de ejecución de scripts en docker-entrypoint-initdb.d

##  Logs útiles

```bash
# Ver logs de PostgreSQL
docker-compose logs postgres

# Ver logs de las pruebas
docker-compose logs test_app

# Seguir logs en vivo
docker-compose logs -f
```

