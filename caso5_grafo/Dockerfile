FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
RUN pip install neo4j pandas

# Copiar archivos
COPY scripts/ /app/scripts/
COPY data/ /app/data/

# Exponer puerto (opcional, para futuras APIs)
EXPOSE 8000
