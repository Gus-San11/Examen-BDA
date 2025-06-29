#!/usr/bin/env python3
"""
Script de prueba simple para cargar datos básicos en MongoDB
"""

import os
import json
import logging
from pymongo import MongoClient
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Función principal para carga simple de datos"""
    
    # Conectar a MongoDB
    mongodb_url = "mongodb://admin:admin123@mongodb:27017/peliculas_db?authSource=admin"
    
    try:
        client = MongoClient(mongodb_url)
        db = client.peliculas_db
        collection = db.peliculas
        
        logger.info("Conexión exitosa a MongoDB")
        
        # Limpiar colección
        collection.delete_many({})
        logger.info("Colección limpiada")
        
        # Cargar datos básicos de películas
        data_path = "/app/data/pelicula.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            peliculas = json.load(f)
        
        logger.info(f"Cargando {len(peliculas)} películas...")
        
        # Insertar documentos básicos (sin transformación compleja)
        documentos_simples = []
        for pelicula in peliculas[:5]:  # Solo primeras 5 para prueba
            doc = {
                "id_pelicula": pelicula["id_pelicula"],
                "titulo": pelicula["titulo"],
                "fecha": pelicula["fecha"],  # Mantener como string por ahora
                "resumen": pelicula.get("resumen", ""),
                "ranking": pelicula.get("ranking", 0),
                "id_director": pelicula.get("id_director", 0)
            }
            documentos_simples.append(doc)
        
        # Insertar en MongoDB
        result = collection.insert_many(documentos_simples)
        logger.info(f"Insertados {len(result.inserted_ids)} documentos")
        
        # Verificar inserción
        count = collection.count_documents({})
        logger.info(f"Total de documentos en colección: {count}")
        
        # Mostrar algunos documentos
        for doc in collection.find().limit(2):
            logger.info(f"Documento: {doc['titulo']}")
        
        logger.info("Carga de prueba completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
