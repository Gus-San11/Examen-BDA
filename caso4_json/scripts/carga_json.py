#!/usr/bin/env python3
"""
Script para cargar datos JSON a MongoDB
Transforma el modelo relacional a modelo semiestructurado
"""

import json
import os
from datetime import datetime, date
from typing import Dict, List, Any
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PeliculasDataLoader:
    def __init__(self, mongodb_url: str = "mongodb://admin:admin123@localhost:27017/peliculas_db?authSource=admin"):
        """Inicializar conexion a MongoDB"""
        self.client = MongoClient(mongodb_url)
        self.db = self.client.peliculas_db
        self.collection = self.db.peliculas
        
    def load_json_files(self) -> Dict[str, List[Dict]]:
        """Cargar todos los archivos JSON desde la carpeta data"""
        data = {}
        data_dir = "data"
        
        json_files = [
            "pelicula.json", "actor.json", "director.json", 
            "productor.json", "actuacion.json", "produccion.json",
            "premio.json", "critica.json"
        ]
        
        for filename in json_files:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data[filename.replace('.json', '')] = json.load(f)
                logger.info(f"Archivo {filename} cargado: {len(data[filename.replace('.json', '')])} registros")
            else:
                logger.warning(f"Archivo {filename} no encontrado")
        
        return data
    
    def calcular_edad(self, fecha_nac: str) -> int:
        """Calcular edad actual basada en fecha de nacimiento"""
        try:
            fecha_nacimiento = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
            hoy = date.today()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            return max(0, edad)
        except:
            return 0
    
    def transformar_a_modelo_semiestructurado(self, data: Dict[str, List[Dict]]) -> List[Dict]:
        """Transformar datos relacionales a modelo semiestructurado"""
        logger.info("Iniciando transformacion a modelo semiestructurado...")
        
        peliculas_transformadas = []
        
        # Crear diccionarios de lookup para optimizar búsquedas
        directores_lookup = {d['id_director']: d for d in data.get('director', [])}
        actores_lookup = {a['id_actor']: a for a in data.get('actor', [])}
        productores_lookup = {p['id_productor']: p for p in data.get('productor', [])}
        
        # Crear lookup de relaciones
        actuaciones_por_pelicula = {}
        for act in data.get('actuacion', []):
            pid = act['id_pelicula']
            if pid not in actuaciones_por_pelicula:
                actuaciones_por_pelicula[pid] = []
            actuaciones_por_pelicula[pid].append(act)
        
        producciones_por_pelicula = {}
        for prod in data.get('produccion', []):
            pid = prod['id_pelicula']
            if pid not in producciones_por_pelicula:
                producciones_por_pelicula[pid] = []
            producciones_por_pelicula[pid].append(prod)
        
        premios_por_pelicula = {}
        for premio in data.get('premio', []):
            pid = premio['id_pelicula']
            if pid not in premios_por_pelicula:
                premios_por_pelicula[pid] = []
            premios_por_pelicula[pid].append(premio)
        
        criticas_por_pelicula = {}
        for critica in data.get('critica', []):
            pid = critica['id_pelicula']
            if pid not in criticas_por_pelicula:
                criticas_por_pelicula[pid] = []
            criticas_por_pelicula[pid].append(critica)
        
        # Procesar cada película
        for pelicula in data.get('pelicula', []):
            pid = pelicula['id_pelicula']
            
            # Información básica de la película
            pelicula_doc = {
                "id_pelicula": pid,
                "titulo": pelicula['titulo'],
                "fecha": datetime.strptime(pelicula['fecha'], "%Y-%m-%d"),
                "resumen": pelicula.get('resumen', ''),
                "ranking": float(pelicula.get('ranking', 0))
            }
            
            # Agregar director
            director_info = directores_lookup.get(pelicula['id_director'])
            if director_info:
                pelicula_doc['director'] = {
                    "id_director": director_info['id_director'],
                    "nombre": director_info['nombre'],
                    "direccion": director_info.get('direccion', ''),
                    "telefono": director_info.get('telefono', 0)
                }
            
            # Agregar actores
            actores_pelicula = []
            for actuacion in actuaciones_por_pelicula.get(pid, []):
                actor_info = actores_lookup.get(actuacion['id_actor'])
                if actor_info:
                    actor_doc = {
                        "id_actor": actor_info['id_actor'],
                        "nombre": actor_info['nombre'],
                        "fecha_nac": datetime.strptime(actor_info['fecha_nac'], "%Y-%m-%d"),
                        "lugar_nac": actor_info.get('lugar_nac', ''),
                        "direccion": actor_info.get('direccion', ''),
                        "telefono": actor_info.get('telefono', 0),
                        "estado_civil": actor_info.get('estado_civil', 'Soltero'),
                        "tipo_actuacion": actuacion.get('tipo', 'Extra'),
                        "salario": float(actuacion.get('salario', 0)),
                        "edad_actual": self.calcular_edad(actor_info['fecha_nac'])
                    }
                    actores_pelicula.append(actor_doc)
            
            pelicula_doc['actores'] = actores_pelicula
            
            # Agregar productores
            productores_pelicula = []
            for produccion in producciones_por_pelicula.get(pid, []):
                productor_info = productores_lookup.get(produccion['id_productor'])
                if productor_info:
                    productor_doc = {
                        "id_productor": productor_info['id_productor'],
                        "nombre": productor_info['nombre'],
                        "direccion": productor_info.get('direccion', ''),
                        "telefono": productor_info.get('telefono', 0),
                        "aportacion_economica": float(produccion.get('aportacion_economica', 0))
                    }
                    productores_pelicula.append(productor_doc)
            
            pelicula_doc['productores'] = productores_pelicula
            
            # Agregar premios
            premios_pelicula = []
            for premio in premios_por_pelicula.get(pid, []):
                premio_doc = {
                    "id_premio": premio.get('id_premio', 0),
                    "nombre": premio.get('nombre', ''),
                    "lugar_certamen": premio.get('lugar_certamen', ''),
                    "fecha": datetime.strptime(premio['fecha'], "%Y-%m-%d") if premio.get('fecha') else None,
                    "ranking_premio": float(premio.get('ranking', 0))
                }
                premios_pelicula.append(premio_doc)
            
            pelicula_doc['premios'] = premios_pelicula
            
            # Agregar críticas
            criticas_pelicula = []
            for critica in criticas_por_pelicula.get(pid, []):
                critica_doc = {
                    "id_critica": critica.get('id_critica', 0),
                    "medio": critica.get('medio', ''),
                    "fecha": datetime.strptime(critica['fecha'], "%Y-%m-%d") if critica.get('fecha') else None,
                    "autor": critica.get('autor', ''),
                    "contenido": critica.get('contenido', ''),
                    "ranking": float(critica.get('ranking', 0))
                }
                criticas_pelicula.append(critica_doc)
            
            pelicula_doc['criticas'] = criticas_pelicula
            
            peliculas_transformadas.append(pelicula_doc)
        
        logger.info(f"Transformacion completada: {len(peliculas_transformadas)} peliculas procesadas")
        return peliculas_transformadas
    
    def cargar_datos(self):
        """Proceso principal de carga de datos"""
        try:
            # Limpiar coleccion existente
            logger.info("Limpiando coleccion existente...")
            self.collection.delete_many({})
            
            # Cargar archivos JSON
            data = self.load_json_files()
            
            # Transformar datos
            peliculas_transformadas = self.transformar_a_modelo_semiestructurado(data)
            
            # Insertar en MongoDB
            if peliculas_transformadas:
                logger.info("Insertando datos en MongoDB...")
                result = self.collection.insert_many(peliculas_transformadas)
                logger.info(f"{len(result.inserted_ids)} documentos insertados exitosamente")
            
            # Mostrar estadísticas
            self.mostrar_estadisticas()
            
        except Exception as e:
            logger.error(f"Error durante la carga de datos: {str(e)}")
            raise
    
    def mostrar_estadisticas(self):
        """Mostrar estadisticas de la coleccion"""
        logger.info("Estadisticas de la coleccion:")
        logger.info(f"   Total de peliculas: {self.collection.count_documents({})}")
        logger.info(f"   Peliculas con premios: {self.collection.count_documents({'premios': {'$ne': []}})}")
        logger.info(f"   Peliculas con criticas: {self.collection.count_documents({'criticas': {'$ne': []}})}")
        
        # Buscar Cinema Paradiso específicamente
        cinema_paradiso = self.collection.find_one({"titulo": "Cinema Paradiso"})
        if cinema_paradiso:
            logger.info("Cinema Paradiso encontrada:")
            logger.info(f"   Director: {cinema_paradiso.get('director', {}).get('nombre', 'N/A')}")
            logger.info(f"   Actores: {len(cinema_paradiso.get('actores', []))}")
            logger.info(f"   Productores: {len(cinema_paradiso.get('productores', []))}")
            logger.info(f"   Premios: {len(cinema_paradiso.get('premios', []))}")
            logger.info(f"   Criticas: {len(cinema_paradiso.get('criticas', []))}")

def main():
    """Funcion principal"""
    logger.info("Iniciando carga de datos de peliculas a MongoDB...")
    
    # Determinar URL de MongoDB segun el entorno
    mongodb_url = os.getenv('MONGODB_URL', "mongodb://admin:admin123@localhost:27017/peliculas_db?authSource=admin")
    
    loader = PeliculasDataLoader(mongodb_url)
    loader.cargar_datos()
    
    logger.info("Proceso de carga completado exitosamente!")

if __name__ == "__main__":
    main()
