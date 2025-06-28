#!/usr/bin/env python3
"""
Script de prueba para conexión a PostgreSQL desde Python
Asegúrate de tener psycopg2 instalado: pip install psycopg2-binary
"""
import psycopg2
import sys

def test_connection():
    try:
        # Configura los parámetros de conexión (PUERTO 5433!)
        conn = psycopg2.connect(
            dbname="caso1",
            user="postgres",
            password="123",
            host="localhost",
            port="5433"  # ¡Importante! Usar puerto 5433, no 5432
        )
        
        print("✅ Conexión exitosa a PostgreSQL!")
        
        # Crear cursor
        cur = conn.cursor()
        
        # Consulta de prueba - verificar tablas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tablas = cur.fetchall()
        print(f"\n Tablas encontradas ({len(tablas)}):")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
          # Consulta del modelo estrella - estadísticas generales
        cur.execute("""
            SELECT 
                COUNT(*) as total_hechos,
                COUNT(DISTINCT id_actor) as actores_distintos,
                COUNT(DISTINCT id_director) as directores_distintos,
                ROUND(AVG(salario), 2) as salario_promedio
            FROM hechos_peliculas;
        """)
        
        resultado = cur.fetchone()
        print(f"\n Estadísticas del modelo estrella:")
        print(f"  - Total hechos: {resultado[0]}")
        print(f"  - Actores distintos: {resultado[1]}")
        print(f"  - Directores distintos: {resultado[2]}")
        print(f"  - Salario promedio: ${resultado[3]:,}")
        
        # A) Total de salarios pagados a los actores de "Cinema Paradiso" dirigida por Giuseppe Tornatore
        print(f"\n Consulta A: Total salarios Cinema Paradiso (Giuseppe Tornatore)")
        cur.execute("""
            SELECT SUM(salario) AS total_salarios
            FROM hechos_peliculas h
            JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
            JOIN dim_director d ON h.id_director = d.id_director
            WHERE p.titulo = 'Cinema Paradiso'
              AND d.nombre = 'Giuseppe Tornatore';
        """)
        
        resultado_a = cur.fetchone()
        if resultado_a[0]:
            print(f"  Total salarios: ${resultado_a[0]:,}")
        else:
            print("  No se encontraron datos para Cinema Paradiso con Giuseppe Tornatore")
          # B) NOTA: Premios no están en el modelo estrella 
        print(f"\n  Consulta B: Premios (No disponible en modelo estrella)")
        
        # C) Total de aportes económicos realizados por el productor "Franco Cristaldi"
        print(f"\n Consulta C: Total aportes del productor Franco Cristaldi")
        cur.execute("""
            SELECT SUM(aportacion) AS total_aporte
            FROM hechos_peliculas h
            JOIN dim_productor pr ON h.id_productor = pr.id_productor
            WHERE pr.nombre = 'Franco Cristaldi';
        """)
        
        resultado_c = cur.fetchone()
        if resultado_c[0]:
            print(f"  Total aportes: ${resultado_c[0]:,}")
        else:
            print("  No se encontraron datos para el productor Franco Cristaldi")
          # D) NOTA: Críticas no están en el modelo estrella puro  
        print(f"\n  Consulta D: Críticas (No disponible en modelo estrella)")
        print(f"\n Consulta C: Total aportes del productor Franco Cristaldi")
        cur.execute("""
            SELECT SUM(aportacion) AS total_aporte
            FROM hechos_peliculas h
            JOIN dim_productor pr ON h.id_productor = pr.id_productor
            WHERE pr.nombre = 'Franco Cristaldi';
        """)
        
        resultado_c = cur.fetchone()
        if resultado_c[0]:
            print(f"  Total aportes: ${resultado_c[0]:,}")
        else:
            print("  No se encontraron datos para el productor Franco Cristaldi")        # E) Listado de personas involucradas en Cinema Paradiso
        print(f"\n Consulta E: Personas involucradas en Cinema Paradiso")
        cur.execute("""
            SELECT a.nombre, 'Actor' AS rol, a.edad, a.estado_civil
            FROM dim_actor a
            JOIN hechos_peliculas h ON a.id_actor = h.id_actor
            JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
            WHERE p.titulo = 'Cinema Paradiso'
            
            UNION
            
            SELECT d.nombre, 'Director', NULL, NULL
            FROM dim_director d
            JOIN hechos_peliculas h ON d.id_director = h.id_director
            JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
            WHERE p.titulo = 'Cinema Paradiso'
            
            UNION
            
            SELECT pr.nombre, 'Productor', NULL, NULL
            FROM dim_productor pr
            JOIN hechos_peliculas h ON pr.id_productor = h.id_productor
            JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
            WHERE p.titulo = 'Cinema Paradiso';
        """)
        
        personas = cur.fetchall()
        if personas:
            for persona in personas:
                edad_str = f", {persona[2]} años" if persona[2] else ""
                estado_str = f", {persona[3]}" if persona[3] else ""
                print(f"  - {persona[0]} ({persona[1]}{edad_str}{estado_str})")
        else:
            print("  No se encontraron personas para Cinema Paradiso")
        
        # Consulta adicional: Top películas por salarios (usando datos disponibles)
        print(f"\n Consulta adicional: Top 5 películas por inversión en salarios")
        cur.execute("""
            SELECT 
                p.titulo,
                d.nombre as director,
                COUNT(h.id_actor) as num_actores,
                SUM(h.salario) as total_salarios
            FROM hechos_peliculas h
            JOIN dim_pelicula p ON h.id_pelicula = p.id_pelicula
            JOIN dim_director d ON h.id_director = d.id_director
            WHERE h.salario IS NOT NULL
            GROUP BY p.titulo, d.nombre
            ORDER BY total_salarios DESC
            LIMIT 5;
        """)
        
        peliculas = cur.fetchall()
        for i, pelicula in enumerate(peliculas, 1):
            print(f"  {i}. {pelicula[0]} (Dir: {pelicula[1]})")
            print(f"     Actores: {pelicula[2]}, Total salarios: ${pelicula[3]:,}")
          # Cerrar conexión
        cur.close()
        conn.close()
        
        print(f"\n Prueba completada exitosamente!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    print(" Probando conexión a PostgreSQL (Modelo Estrella)...")
    success = test_connection()
    sys.exit(0 if success else 1)
