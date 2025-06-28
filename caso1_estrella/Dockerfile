# Dockerfile para el caso1_estrella - Base de datos PostgreSQL con modelo estrella
FROM postgres:15

# Establecer variables de entorno para PostgreSQL
ENV POSTGRES_DB=caso1
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123

# Crear directorio para scripts SQL
RUN mkdir -p /docker-entrypoint-initdb.d

# Copiar scripts SQL al contenedor (ejecutados en orden alfabético)
COPY ./caso1.sql /docker-entrypoint-initdb.d/01-caso1.sql
COPY ./poblado_modelo_estrella.sql /docker-entrypoint-initdb.d/02-poblado_modelo_estrella.sql

# Exponer puerto PostgreSQL
EXPOSE 5432

# El comando por defecto ya está definido en la imagen base de postgres
