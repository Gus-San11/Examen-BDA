#!/usr/bin/env python3
"""
Test script para probar las consultas XML del caso3
"""

import psycopg2
import os
import time
from datetime import datetime

class TestConsultasXML:
    def __init__(self):
        # Esperar a que la base de datos esté lista
        time.sleep(10)
        
        # Configuración de conexión
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME', 'caso3'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '123')
        )
        self.cur = self.conn.cursor()
        
    def ejecutar_consulta(self, nombre, consulta):
        """Ejecuta una consulta y muestra los resultados"""
        print(f"\n{'='*60}")
        print(f"CONSULTA {nombre}")
        print(f"{'='*60}")
        print(f"SQL: {consulta[:100]}...")
        print(f"{'='*60}")
        
        try:
            self.cur.execute(consulta)
            resultados = self.cur.fetchall()
            
            if resultados:
                # Obtener nombres de columnas
                columnas = [desc[0] for desc in self.cur.description]
                print(f"Columnas: {', '.join(columnas)}")
                print("-" * 60)
                
                for fila in resultados:
                    print(fila)
                    
                print(f"\nTotal de filas: {len(resultados)}")
            else:
                print("No se encontraron resultados")
                
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            
    def test_consulta_a(self):
        """A) Total de salarios de actores de Cinema Paradiso"""
        consulta = """
        SELECT SUM((xpath('//pelicula[titulo="Cinema Paradiso" and director/nombre="Giuseppe Tornatore"]/actores/actor/salario/text()', contenido))[i]::text::numeric)
        AS total_salarios
        FROM peliculas_xml, generate_series(1, array_length(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/salario/text()', contenido), 1)) i;
        """
        self.ejecutar_consulta("A", consulta)
        
    def test_consulta_b(self):
        """B) Premios recibidos por Cinema Paradiso ordenados por ranking DESC"""
        consulta = """
        SELECT 
            unnest(xpath('//pelicula[titulo="Cinema Paradiso" and director/nombre="Giuseppe Tornatore"]/premios/premio/ranking/text()', contenido))::text::int AS ranking,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/premios/premio/nombre/text()', contenido))::text AS nombre,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/premios/premio/lugar/text()', contenido))::text AS lugar
        FROM peliculas_xml
        ORDER BY ranking DESC;
        """
        self.ejecutar_consulta("B", consulta)
        
    def test_consulta_c(self):
        """C) Total de aportes del productor Franco Cristaldi"""
        consulta = """
        SELECT SUM((xpath('//pelicula/productores/productor[nombre="Franco Cristaldi"]/aporte_economico/text()', contenido))[i]::text::numeric)
        AS total_aporte
        FROM peliculas_xml, generate_series(1, array_length(xpath('//pelicula/productores/productor[nombre="Franco Cristaldi"]/aporte_economico/text()', contenido), 1)) i;
        """
        self.ejecutar_consulta("C", consulta)
        
    def test_consulta_d(self):
        """D) Críticas entre 15 y 30 de agosto de 1990 para Cinema Paradiso"""
        consulta = """
        SELECT 
            unnest(xpath('//pelicula[titulo="Cinema Paradiso" and director/nombre="Giuseppe Tornatore"]/criticas/critica/medio/text()', contenido))::text AS medio,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/criticas/critica/fecha/text()', contenido))::text::date AS fecha,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/criticas/critica/autor/text()', contenido))::text AS autor
        FROM peliculas_xml
        WHERE
            EXISTS (
                SELECT 1 FROM unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/criticas/critica/fecha/text()', contenido)) AS fecha(fecha_text)
                WHERE fecha_text::text::date BETWEEN '1990-08-15' AND '1990-08-30'
            )
        ORDER BY fecha DESC;
        """
        self.ejecutar_consulta("D", consulta)
        
    def test_consulta_e(self):
        """E) Personas involucradas en Cinema Paradiso"""
        consulta = """
        WITH datos AS (
          SELECT 
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/nombre/text()', contenido))::text AS nombre,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/fecha_nacimiento/text()', contenido))::text::date AS fecha_nac,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/estado_civil/text()', contenido))::text AS estado_civil,
            unnest(xpath('//pelicula[titulo="Cinema Paradiso"]/actores/actor/telefono/text()', contenido))::text AS telefono,
            'Actor' AS rol
          FROM peliculas_xml
          UNION ALL
          SELECT 
            (xpath('//pelicula[titulo="Cinema Paradiso"]/director/nombre/text()', contenido))[1]::text,
            (xpath('//pelicula[titulo="Cinema Paradiso"]/director/fecha_nacimiento/text()', contenido))[1]::text::date,
            (xpath('//pelicula[titulo="Cinema Paradiso"]/director/estado_civil/text()', contenido))[1]::text,
            (xpath('//pelicula[titulo="Cinema Paradiso"]/director/telefono/text()', contenido))[1]::text,
            'Director'
          FROM peliculas_xml
          UNION ALL
          SELECT 
            (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/nombre/text()', contenido))[1]::text,
            (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/fecha_nacimiento/text()', contenido))[1]::text::date,
            (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/estado_civil/text()', contenido))[1]::text,
            (xpath('//pelicula[titulo="Cinema Paradiso"]/productores/productor/telefono/text()', contenido))[1]::text,
            'Productor'
          FROM peliculas_xml
        )
        SELECT 
          nombre, 
          rol, 
          estado_civil,
          telefono,
          extract(year FROM age(current_date, fecha_nac)) AS edad_actual
        FROM datos
        ORDER BY rol;
        """
        self.ejecutar_consulta("E", consulta)
    
    def verificar_datos(self):
        """Verifica que los datos estén cargados correctamente"""
        print(f"\n{'='*60}")
        print("VERIFICACIÓN DE DATOS")
        print(f"{'='*60}")
        
        # Verificar que existe la tabla
        self.cur.execute("SELECT COUNT(*) FROM peliculas_xml;")
        count = self.cur.fetchone()[0]
        print(f"Registros en peliculas_xml: {count}")
        
        # Verificar contenido XML
        if count > 0:
            self.cur.execute("SELECT LENGTH(contenido::text) AS longitud FROM peliculas_xml LIMIT 1;")
            longitud = self.cur.fetchone()[0]
            print(f"Longitud del contenido XML: {longitud} caracteres")
            
            # Verificar estructura XML básica
            self.cur.execute("SELECT xpath('//pelicula/titulo/text()', contenido) FROM peliculas_xml;")
            titulos = self.cur.fetchone()[0]
            print(f"Títulos encontrados: {titulos}")
    
    def ejecutar_todas_las_pruebas(self):
        """Ejecuta todas las pruebas"""
        print("=" * 80)
        print("INICIANDO PRUEBAS DE CONSULTAS XML - CASO3")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        try:
            # Verificar datos
            self.verificar_datos()
            
            # Ejecutar consultas
            self.test_consulta_a()
            self.test_consulta_b()
            self.test_consulta_c()
            self.test_consulta_d()
            self.test_consulta_e()
            
            print(f"\n{'='*80}")
            print("TODAS LAS PRUEBAS COMPLETADAS")
            print(f"{'='*80}")
            
        except Exception as e:
            print(f"Error durante las pruebas: {e}")
        finally:
            self.cur.close()
            self.conn.close()

if __name__ == "__main__":
    test = TestConsultasXML()
    test.ejecutar_todas_las_pruebas()
