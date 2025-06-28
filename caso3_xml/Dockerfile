FROM postgres:15

# Instalar Python y pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar librerías de Python necesarias usando --break-system-packages
RUN pip3 install --break-system-packages psycopg2-binary

# Crear directorio de trabajo para la aplicación
WORKDIR /app

# Copiar archivos necesarios
COPY peliculas.xml /app/
COPY carga.py /app/
COPY test.py /app/

# Crear directorio de inicialización si no existe
RUN mkdir -p /docker-entrypoint-initdb.d

# Crear script combinado de inicialización
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ejecutar el script SQL de estructura\n\
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL\n\
	DROP TABLE IF EXISTS peliculas_xml;\n\
	CREATE TABLE peliculas_xml (\n\
	    id SERIAL PRIMARY KEY,\n\
	    contenido XML NOT NULL\n\
	);\n\
EOSQL\n\
\n\
# Ejecutar el script de carga de datos con Python\n\
cd /app\n\
python3 carga.py\n\
' > /docker-entrypoint-initdb.d/02-init-complete.sh

RUN chmod +x /docker-entrypoint-initdb.d/02-init-complete.sh

# Exponer puerto de PostgreSQL
EXPOSE 5432
