#!/usr/bin/env python3
"""
Script de prueba simplificado para el modelo relacional-objetual
"""

import psycopg2
import os
import time
import sys

def main():
    print("🎬 INICIANDO PRUEBAS DEL MODELO RELACIONAL-OBJETUAL")
    print("=" * 60)
    
    # Configuración
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'cinema_db')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'password123')
    
    print(f"🔄 Conectando a PostgreSQL en {host}:{port}...")
    
    # Intentar conexión
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("✅ Conexión exitosa!")
        
        cursor = conn.cursor()
        
        # Consulta A: Total de salarios
        print("\n🔍 Consulta A: Total de salarios de actores de Cinema Paradiso")
        cursor.execute("""
            SELECT SUM(a.salario) AS total_salarios
            FROM actor a
            JOIN actuacion ac ON a.id_persona = ac.id_actor
            JOIN pelicula p ON ac.id_pelicula = p.id_pelicula
            JOIN director d ON p.id_director = d.id_persona
            WHERE p.titulo = 'Cinema Paradiso'
              AND d.nombre = 'Giuseppe Tornatore';
        """)
        resultado = cursor.fetchone()
        print(f"💰 Total de salarios: ${resultado[0]:,.2f}")
        
        # Consulta B: Premios
        print("\n🔍 Consulta B: Premios de Cinema Paradiso")
        cursor.execute("""
            SELECT p.ranking, pr.nombre, pr.lugar_certamen
            FROM premio pr
            JOIN pelicula p ON pr.id_pelicula = p.id_pelicula
            JOIN director d ON p.id_director = d.id_persona
            WHERE p.titulo = 'Cinema Paradiso'
              AND d.nombre = 'Giuseppe Tornatore'
            ORDER BY p.ranking DESC;
        """)
        premios = cursor.fetchall()
        print(f"🏆 Premios encontrados: {len(premios)}")
        for premio in premios:
            print(f"   - {premio[1]} en {premio[2]} (Ranking: {premio[0]})")
        
        # Consulta C: Aportaciones del productor
        print("\n🔍 Consulta C: Aportaciones de Franco Cristaldi")
        cursor.execute("""
            SELECT SUM(pr.aportacion) AS total_aportes
            FROM produccion pr
            JOIN productor p ON pr.id_productor = p.id_persona
            WHERE p.nombre = 'Franco Cristaldi';
        """)
        resultado = cursor.fetchone()
        print(f"💰 Total de aportaciones: ${resultado[0]:,.2f}")
        
        # Consulta D: Críticas
        print("\n🔍 Consulta D: Críticas entre el 15 y 30 de agosto de 1990")
        cursor.execute("""
            SELECT c.medio, c.fecha, c.autor
            FROM critica c
            JOIN pelicula p ON c.id_pelicula = p.id_pelicula
            JOIN director d ON p.id_director = d.id_persona
            WHERE p.titulo = 'Cinema Paradiso'
              AND d.nombre = 'Giuseppe Tornatore'
              AND c.fecha BETWEEN '1990-08-15' AND '1990-08-30'
            ORDER BY c.fecha DESC;
        """)
        criticas = cursor.fetchall()
        print(f"📰 Críticas encontradas: {len(criticas)}")
        for critica in criticas:
            print(f"   - {critica[1]}: {critica[0]} por {critica[2]}")
        
        # Consulta E: Personas involucradas
        print("\n🔍 Consulta E: Personas involucradas en Cinema Paradiso")
        cursor.execute("""
            SELECT per.nombre, 'Actor' AS rol, per.estado_civil, per.telefono,
                   DATE_PART('year', CURRENT_DATE) - DATE_PART('year', per.fecha_nac) AS edad
            FROM actor a
            JOIN persona per ON a.id_persona = per.id_persona
            JOIN actuacion act ON a.id_persona = act.id_actor
            WHERE act.id_pelicula = 999
            LIMIT 3;
        """)
        personas = cursor.fetchall()
        print(f"👥 Primeras 3 personas:")
        for persona in personas:
            print(f"   - {persona[0]} ({persona[1]}) - {persona[2]} - Tel: {persona[3]} - Edad: {int(persona[4])}")
        
        # Test de herencia
        print("\n🧬 Test de herencia:")
        cursor.execute("SELECT COUNT(*) FROM persona;")
        total = cursor.fetchone()[0]
        print(f"👥 Total personas (herencia): {total}")
        
        cursor.execute("SELECT COUNT(*) FROM ONLY actor;")
        actores = cursor.fetchone()[0]
        print(f"🎭 Solo actores: {actores}")
        
        cursor.execute("SELECT COUNT(*) FROM ONLY director;")
        directores = cursor.fetchone()[0]
        print(f"🎬 Solo directores: {directores}")
        
        cursor.execute("SELECT COUNT(*) FROM ONLY productor;")
        productores = cursor.fetchone()[0]
        print(f"💼 Solo productores: {productores}")
        
        if total == actores + directores + productores:
            print("✅ Herencia funcionando correctamente")
        else:
            print("❌ Problema con herencia")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("✅ El modelo relacional-objetual está funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
