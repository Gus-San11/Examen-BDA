#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión y funcionalidad de MongoDB
"""

import os
import sys
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json

def test_mongodb_connection():
    """Probar conexión a MongoDB"""
    try:
        # URL de conexión
        mongodb_url = os.getenv('MONGODB_URL', "mongodb://admin:admin123@localhost:27017/peliculas_db?authSource=admin")
        
        print("Probando conexion a MongoDB...")
        print(f"URL: {mongodb_url}")
        
        # Conectar
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Probar conexión
        client.admin.command('ping')
        print("Conexion exitosa a MongoDB")
        
        # Obtener base de datos
        db = client.peliculas_db
        
        # Listar colecciones
        collections = db.list_collection_names()
        print(f"Colecciones disponibles: {collections}")
        
        # Probar la coleccion de peliculas
        peliculas_collection = db.peliculas
        
        # Contar documentos
        count = peliculas_collection.count_documents({})
        print(f"Total de peliculas en la coleccion: {count}")
        
        # Buscar Cinema Paradiso
        cinema_paradiso = peliculas_collection.find_one({"titulo": "Cinema Paradiso"})
        if cinema_paradiso:
            print("Cinema Paradiso encontrada:")
            print(f"   Titulo: {cinema_paradiso.get('titulo')}")
            print(f"   Director: {cinema_paradiso.get('director', {}).get('nombre')}")
            print(f"   Fecha: {cinema_paradiso.get('fecha')}")
            print(f"   Ranking: {cinema_paradiso.get('ranking')}")
            print(f"   Actores: {len(cinema_paradiso.get('actores', []))}")
            print(f"   Productores: {len(cinema_paradiso.get('productores', []))}")
        else:
            print("Cinema Paradiso no encontrada en la base de datos")
        
        # Probar consulta simple
        print("\nProbando consulta de agregacion...")
        pipeline = [
            {"$group": {"_id": None, "promedio_ranking": {"$avg": "$ranking"}}},
            {"$project": {"_id": 0, "promedio_ranking": {"$round": ["$promedio_ranking", 2]}}}
        ]
        
        result = list(peliculas_collection.aggregate(pipeline))
        if result:
            print(f"Ranking promedio de todas las peliculas: {result[0]['promedio_ranking']}")
        
        return True
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Error: No se pudo conectar a MongoDB. Verifique que el servicio este ejecutandose.")
        return False
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return False

def test_environment():
    """Probar configuracion del entorno"""
    print("Probando configuracion del entorno...")
    
    # Verificar variables de entorno
    mongodb_url = os.getenv('MONGODB_URL')
    if mongodb_url:
        print(f"MONGODB_URL configurada: {mongodb_url}")
    else:
        print("MONGODB_URL no configurada, usando valor por defecto")
    
    # Verificar archivos de datos
    data_dir = "data"
    if os.path.exists(data_dir):
        print(f"Directorio de datos encontrado: {data_dir}")
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        print(f"Archivos JSON encontrados: {len(json_files)}")
        for file in json_files:
            filepath = os.path.join(data_dir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"   {file}: {len(data)} registros")
            except Exception as e:
                print(f"   Error leyendo {file}: {str(e)}")
    else:
        print(f"Directorio de datos no encontrado: {data_dir}")
    
    # Verificar directorio de scripts
    scripts_dir = "scripts"
    if os.path.exists(scripts_dir):
        print(f"Directorio de scripts encontrado: {scripts_dir}")
        scripts = [f for f in os.listdir(scripts_dir) if f.endswith(('.py', '.js'))]
        print(f"Scripts encontrados: {scripts}")
    else:
        print(f"Directorio de scripts no encontrado: {scripts_dir}")

def main():
    """Funcion principal de pruebas"""
    print("INICIANDO PRUEBAS DEL SISTEMA")
    print("=" * 50)
    print(f"Fecha y hora: {datetime.now()}")
    print(f"Python version: {sys.version}")
    print()
    
    # Probar entorno
    test_environment()
    print()
    
    # Probar MongoDB
    if test_mongodb_connection():
        print("\nTodas las pruebas pasaron exitosamente!")
        return True
    else:
        print("\nAlgunas pruebas fallaron. Revise la configuracion.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
