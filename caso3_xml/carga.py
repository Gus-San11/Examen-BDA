import psycopg2
import os
import time

# Esperar a que PostgreSQL esté listo
time.sleep(5)

# Configuración de conexión usando variables de entorno
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    dbname=os.getenv('DB_NAME', 'caso3'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', '123')
)

cur = conn.cursor()

# Ruta del archivo XML adaptada para Docker
xml_file_path = os.path.join(os.path.dirname(__file__), 'peliculas.xml')
with open(xml_file_path, 'r', encoding='utf-8') as f:
    xml_content = f.read()

try:
    cur.execute("""
        INSERT INTO peliculas_xml (contenido)
        VALUES (XMLPARSE(DOCUMENT %s))
    """, (xml_content,))
    
    conn.commit()
    print("Datos XML cargados exitosamente")
except Exception as e:
    print(f"Error al cargar datos: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()
