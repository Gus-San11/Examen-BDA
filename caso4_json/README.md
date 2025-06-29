# Caso 4: Modelo Semiestructurado JSON con MongoDB

Este proyecto implementa un modelo semiestructurado usando MongoDB para gestionar una base de datos de peliculas. El sistema transforma un modelo relacional a documentos JSON anidados, optimizando consultas complejas y reduciendo la necesidad de joins.

## Arquitectura del Proyecto

```
caso4_json/
│
├── data/                           # Datos originales en formato JSON
│   ├── actor.json                  # Informacion de actores
│   ├── actuacion.json              # Relacion actor-pelicula
│   ├── critica.json                # Criticas de peliculas
│   ├── director.json               # Informacion de directores
│   ├── pelicula.json               # Informacion basica de peliculas
│   ├── premio.json                 # Premios recibidos
│   ├── produccion.json             # Relacion productor-pelicula
│   └── productor.json              # Informacion de productores
│
├── schema/                         # Esquemas de validacion
│   └── peliculas_schema.json       # JSON Schema para MongoDB
│
├── scripts/                        # Scripts de procesamiento
│   ├── carga_json.py               # Script de transformacion y carga
│   └── consultas_mongodb.js        # Consultas BSON del negocio
│
├── mongo-init/                     # Inicializacion de MongoDB
│   └── init.js                     # Script de configuracion inicial
│
├── docker-compose.yml              # Orquestacion de contenedores
├── Dockerfile                      # Imagen Python personalizada
├── requirements.txt                # Dependencias Python
├── test_mongodb.py                 # Script de pruebas
└── README.md                       # Documentacion del proyecto
```

## Configuracion del Entorno de Desarrollo

### Contenedores Docker Incluidos:

1. **MongoDB** (Puerto 27017)
   - Base de datos principal
   - Autenticacion: admin/admin123
   - Volumen persistente para datos

2. **Mongo Express** (Puerto 8081)
   - Interfaz web de administracion
   - Acceso sin autenticacion basica
   - URL: http://localhost:8081

### Inicio Rapido

1. **Clonar y navegar al directorio:**
   ```bash
   cd caso4_json
   ```

2. **Levantar los servicios:**
   ```bash
   docker-compose up -d
   ```

3. **Verificar que los servicios estén ejecutándose:**
   ```bash
   docker-compose ps
   ```

4. **Ejecutar script de prueba:**
   ```bash
   docker-compose exec python-app python test_mongodb.py
   ```

5. **Cargar datos transformados:**
   ```bash
   docker-compose exec python-app python scripts/carga_json.py
   ```

## Modelo Semiestructurado

### Transformacion Relacional → Documento

El modelo transforma las tablas relacionales en documentos JSON anidados:

**Antes (Relacional):**
- 8 tablas independientes
- Multiples JOINs para consultas complejas
- Normalizacion estricta

**Despues (Semiestructurado):**
- 1 coleccion principal `peliculas`
- Documentos auto-contenidos
- Consultas optimizadas con agregaciones

### Estructura del Documento

```json
{
  "id_pelicula": 999,
  "titulo": "Cinema Paradiso",
  "fecha": ISODate("1990-08-15"),
  "resumen": "...",
  "ranking": 4.8,
  "director": {
    "id_director": 999,
    "nombre": "Giuseppe Tornatore",
    "direccion": "Via Roma 1, Italia",
    "telefono": 405178901
  },
  "actores": [
    {
      "id_actor": 999,
      "nombre": "Salvatore Cascio",
      "fecha_nac": ISODate("1979-01-08"),
      "estado_civil": "Soltero",
      "tipo_actuacion": "Protagonista",
      "salario": 1500000.0,
      "edad_actual": 46
    }
  ],
  "productores": [
    {
      "id_productor": 999,
      "nombre": "Franco Cristaldi",
      "aportacion_economica": 2500000.0
    }
  ],
  "premios": [...],
  "criticas": [...]
}
```

## Consultas del Negocio

### A) Total de salarios - Cinema Paradiso
```javascript
db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "director.nombre": "Giuseppe Tornatore"
    }
  },
  {
    $unwind: "$actores"
  },
  {
    $group: {
      _id: null,
      "total_salarios": { $sum: "$actores.salario" }
    }
  }
]);
```

### B) Premios ordenados por ranking
```javascript
db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "director.nombre": "Giuseppe Tornatore"
    }
  },
  {
    $unwind: "$premios"
  },
  {
    $sort: { "premios.ranking_premio": -1 }
  }
]);
```

### C) Total de aportes de Franco Cristaldi
```javascript
db.peliculas.aggregate([
  {
    $unwind: "$productores"
  },
  {
    $match: {
      "productores.nombre": "Franco Cristaldi"
    }
  },
  {
    $group: {
      _id: null,
      "total_aportes": { $sum: "$productores.aportacion_economica" }
    }
  }
]);
```

### D) Críticas en rango de fechas
```javascript
db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "criticas.fecha": {
        $gte: ISODate("1990-08-15"),
        $lte: ISODate("1990-08-30")
      }
    }
  },
  {
    $unwind: "$criticas"
  },
  {
    $sort: { "criticas.fecha": -1 }
  }
]);
```

### E) Todas las personas involucradas
```javascript
db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso"
    }
  },
  {
    $project: {
      personas: {
        $concatArrays: [
          [{ nombre: "$director.nombre", rol: "Director" }],
          { $map: { input: "$actores", as: "actor", in: { nombre: "$$actor.nombre", rol: "Actor" }}},
          { $map: { input: "$productores", as: "prod", in: { nombre: "$$prod.nombre", rol: "Productor" }}}
        ]
      }
    }
  }
]);
```

## Comandos Utiles

### Gestion de Docker
```bash
# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Parar y limpiar volúmenes
docker-compose down -v

# Ejecutar comandos en el contenedor Python
docker-compose exec python-app bash
```

### Conexion directa a MongoDB
```bash
# Desde el host con autenticacion
docker exec -it caso4_mongodb mongosh -u admin -p admin123 --authenticationDatabase admin peliculas_db

# Desde el contenedor Python
docker-compose exec python-app python -c "from pymongo import MongoClient; print('Conexion exitosa')"
```

### Acceso a herramientas web
- **Mongo Express**: http://localhost:8081
- **MongoDB Shell**: `docker exec -it caso4_mongodb mongosh`

## Desarrollo y Testing

### Ejecutar pruebas
```bash
# Prueba completa del sistema
docker-compose exec python-app python test_mongodb.py

# Cargar datos de prueba
docker-compose exec python-app python scripts/carga_json.py

# Ejecutar consultas especificas con autenticacion
docker exec -it caso4_mongodb mongosh -u admin -p admin123 --authenticationDatabase admin peliculas_db --eval "load('/docker-entrypoint-initdb.d/init.js')"
```

### Modo desarrollo
```bash
# Entrar al contenedor Python
docker-compose exec python-app bash

# Instalar dependencias adicionales
pip install nueva_dependencia

# Ejecutar scripts interactivamente
python -i scripts/carga_json.py
```

## Monitoreo y Logs

- **Logs de aplicacion**: `docker-compose logs python-app`
- **Logs de MongoDB**: `docker-compose logs mongodb`
- **Metricas**: Disponibles en Mongo Express
- **Estado de servicios**: `docker-compose ps`
