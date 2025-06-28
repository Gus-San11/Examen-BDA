#!/usr/bin/env python3
"""
Script para cargar datos CSV a Neo4j
Caso 5: Base de Datos de Grafos - Películas
"""

import os
import time
import pandas as pd
from neo4j import GraphDatabase

class Neo4jDataLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.data_path = "/app/data"
        
    def close(self):
        self.driver.close()
    
    def wait_for_neo4j(self, max_retries=30):
        """Esperar a que Neo4j esté disponible"""
        for i in range(max_retries):
            try:
                with self.driver.session() as session:
                    session.run("RETURN 1")
                print("Neo4j está disponible")
                return True
            except Exception as e:
                print(f"Esperando Neo4j... intento {i+1}/{max_retries}")
                time.sleep(2)
        return False
    
    def limpiar_base_datos(self):
        """Limpiar la base de datos antes de cargar"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Base de datos limpiada")
    
    def crear_indices(self):
        """Crear índices para mejorar el rendimiento"""
        indices = [
            "CREATE INDEX pelicula_id IF NOT EXISTS FOR (p:Pelicula) ON (p.id)",
            "CREATE INDEX actor_id IF NOT EXISTS FOR (a:Actor) ON (a.id)",
            "CREATE INDEX director_id IF NOT EXISTS FOR (d:Director) ON (d.id)",
            "CREATE INDEX productor_id IF NOT EXISTS FOR (p:Productor) ON (p.id)",
            "CREATE INDEX critica_id IF NOT EXISTS FOR (c:Critica) ON (c.id)",
            "CREATE INDEX premio_id IF NOT EXISTS FOR (p:Premio) ON (p.id)"
        ]
        
        with self.driver.session() as session:
            for indice in indices:
                session.run(indice)
        print("Índices creados")
    
    def cargar_peliculas(self):
        """Cargar nodos de películas"""
        df = pd.read_csv(f"{self.data_path}/pelicula.csv")
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (p:Pelicula {
                        id: $id,
                        titulo: $titulo,
                        fecha_estreno: date($fecha),
                        resumen: $resumen,
                        ranking: $ranking,
                        id_director: $id_director
                    })
                """, 
                id=int(row['id_pelicula']),
                titulo=str(row['titulo']),
                fecha=str(row['fecha']),
                resumen=str(row['resumen']),
                ranking=float(row['ranking']),
                id_director=int(row['id_director'])
                )
        print(f"Cargadas {len(df)} películas")
    
    def cargar_actores(self):
        """Cargar nodos de actores"""
        df = pd.read_csv(f"{self.data_path}/actor.csv")
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (a:Actor {
                        id: $id,
                        nombre: $nombre,
                        fecha_nacimiento: date($fecha_nac),
                        lugar_nacimiento: $lugar_nac,
                        direccion: $direccion,
                        telefono: $telefono,
                        estado_civil: $estado_civil
                    })
                """,
                id=int(row['id_actor']),
                nombre=str(row['nombre']),
                fecha_nac=str(row['fecha_nac']),
                lugar_nac=str(row['lugar_nac']),
                direccion=str(row['direccion']),
                telefono=str(row['telefono']),
                estado_civil=str(row['estado_civil'])
                )
        print(f"Cargados {len(df)} actores")
    
    def cargar_directores(self):
        """Cargar nodos de directores"""
        df = pd.read_csv(f"{self.data_path}/director.csv")
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (d:Director {
                        id: $id,
                        nombre: $nombre,
                        direccion: $direccion,
                        telefono: $telefono
                    })
                """,
                id=int(row['id_director']),
                nombre=str(row['nombre']),
                direccion=str(row['direccion']),
                telefono=str(row['telefono'])
                )
        print(f"Cargados {len(df)} directores")
    
    def cargar_productores(self):
        """Cargar nodos de productores"""
        df = pd.read_csv(f"{self.data_path}/productor.csv")
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (p:Productor {
                        id: $id,
                        nombre: $nombre,
                        direccion: $direccion,
                        telefono: $telefono
                    })
                """,
                id=int(row['id_productor']),
                nombre=str(row['nombre']),
                direccion=str(row['direccion']),
                telefono=str(row['telefono'])
                )
        print(f"Cargados {len(df)} productores")
    
    def cargar_criticas(self):
        """Cargar nodos de críticas"""
        df = pd.read_csv(f"{self.data_path}/critica.csv")
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (c:Critica {
                        id: $id,
                        medio: $medio,
                        autor: $autor,
                        fecha: date($fecha),
                        id_pelicula: $id_pelicula
                    })
                """,
                id=int(row['id_critica']),
                medio=str(row['medio']),
                autor=str(row['autor']),
                fecha=str(row['fecha']),
                id_pelicula=int(row['id_pelicula'])
                )
        print(f"Cargadas {len(df)} críticas")
    
    def cargar_premios(self):
        """Cargar nodos de premios"""
        df = pd.read_csv(f"{self.data_path}/premio.csv")
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (pr:Premio {
                        id: $id,
                        nombre: $nombre,
                        resumen: $resumen,
                        certamen: $certamen,
                        lugar: $lugar,
                        tipo: $tipo,
                        id_pelicula: $id_pelicula
                    })
                """,
                id=int(row['id_premio']),
                nombre=str(row['nombre']),
                resumen=str(row['resumen']) if pd.notna(row['resumen']) else "",
                certamen=str(row['certamen']) if pd.notna(row['certamen']) else "",
                lugar=str(row['lugar']),
                tipo=str(row['tipo']) if pd.notna(row['tipo']) else "",
                id_pelicula=int(row['id_pelicula'])
                )
        print(f"Cargados {len(df)} premios")
    
    def crear_relaciones_direccion(self):
        """Crear relaciones DIRIGIDA_POR entre películas y directores"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Pelicula), (d:Director)
                WHERE p.id_director = d.id
                CREATE (p)-[:DIRIGIDA_POR]->(d)
            """)
            
            # Contar las relaciones creadas
            result = session.run("MATCH (p:Pelicula)-[:DIRIGIDA_POR]->(d:Director) RETURN count(*) as count")
            count = result.single()['count']
            print(f"Relaciones DIRIGIDA_POR creadas: {count}")
    
    def crear_relaciones_actuacion(self):
        """Crear relaciones ACTUADA_POR entre películas y actores"""
        try:
            df = pd.read_csv(f"{self.data_path}/actuacion.csv")
            
            with self.driver.session() as session:
                for _, row in df.iterrows():
                    session.run("""
                        MATCH (p:Pelicula {id: $id_pelicula}), (a:Actor {id: $id_actor})
                        CREATE (p)-[:ACTUADA_POR {
                            tipo_actuacion: $tipo,
                            salario: $salario
                        }]->(a)
                    """,
                    id_pelicula=int(row['id_pelicula']),
                    id_actor=int(row['id_actor']),
                    tipo=str(row['tipo']),
                    salario=float(row['salario'])
                    )
            print(f"Relaciones ACTUADA_POR creadas: {len(df)}")
        except FileNotFoundError:
            print("Archivo actuacion.csv no encontrado, saltando relaciones de actuación")
        except Exception as e:
            print(f"Error en relaciones de actuación: {e}")
    
    def crear_relaciones_produccion(self):
        """Crear relaciones PRODUCIDA_POR entre películas y productores"""
        try:
            df = pd.read_csv(f"{self.data_path}/produccion.csv")
            
            with self.driver.session() as session:
                for _, row in df.iterrows():
                    session.run("""
                        MATCH (p:Pelicula {id: $id_pelicula}), (pr:Productor {id: $id_productor})
                        CREATE (p)-[:PRODUCIDA_POR {
                            aporte_economico: $aporte_economico
                        }]->(pr)
                    """,
                    id_pelicula=int(row['id_pelicula']),
                    id_productor=int(row['id_productor']),
                    aporte_economico=float(row['aportacion_economica'])
                    )
            print(f"Relaciones PRODUCIDA_POR creadas: {len(df)}")
        except FileNotFoundError:
            print("Archivo produccion.csv no encontrado, saltando relaciones de producción")
        except Exception as e:
            print(f"Error en relaciones de producción: {e}")
    
    def crear_relaciones_criticas(self):
        """Crear relaciones TIENE_CRITICA entre películas y críticas"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Pelicula), (c:Critica)
                WHERE p.id = c.id_pelicula
                CREATE (p)-[:TIENE_CRITICA]->(c)
            """)
            
            # Contar las relaciones creadas
            result = session.run("MATCH (p:Pelicula)-[:TIENE_CRITICA]->(c:Critica) RETURN count(*) as count")
            count = result.single()['count']
            print(f"Relaciones TIENE_CRITICA creadas: {count}")
    
    def crear_relaciones_premios(self):
        """Crear relaciones TIENE_PREMIO entre películas y premios"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Pelicula), (pr:Premio)
                WHERE p.id = pr.id_pelicula
                CREATE (p)-[:TIENE_PREMIO]->(pr)
            """)
            
            # Contar las relaciones creadas
            result = session.run("MATCH (p:Pelicula)-[:TIENE_PREMIO]->(pr:Premio) RETURN count(*) as count")
            count = result.single()['count']
            print(f"Relaciones TIENE_PREMIO creadas: {count}")
    
    def crear_relaciones_colaboracion(self):
        """Crear relaciones de colaboración entre personas que trabajaron en las mismas películas"""
        with self.driver.session() as session:
            # Relaciones Actor-Director (trabajaron juntos)
            session.run("""
                MATCH (a:Actor)<-[:ACTUADA_POR]-(p:Pelicula)-[:DIRIGIDA_POR]->(d:Director)
                CREATE (a)-[:TRABAJO_CON {pelicula: p.titulo, rol: 'actor-director'}]->(d)
            """)
            
            # Relaciones Actor-Productor
            session.run("""
                MATCH (a:Actor)<-[:ACTUADA_POR]-(p:Pelicula)-[:PRODUCIDA_POR]->(pr:Productor)
                CREATE (a)-[:TRABAJO_CON {pelicula: p.titulo, rol: 'actor-productor'}]->(pr)
            """)
            
            # Relaciones Director-Productor
            session.run("""
                MATCH (d:Director)<-[:DIRIGIDA_POR]-(p:Pelicula)-[:PRODUCIDA_POR]->(pr:Productor)
                CREATE (d)-[:TRABAJO_CON {pelicula: p.titulo, rol: 'director-productor'}]->(pr)
            """)
            
            # Relaciones entre Actores del mismo film
            session.run("""
                MATCH (a1:Actor)<-[:ACTUADA_POR]-(p:Pelicula)-[:ACTUADA_POR]->(a2:Actor)
                WHERE id(a1) < id(a2)
                CREATE (a1)-[:COACTUA_CON {pelicula: p.titulo}]->(a2)
            """)
            
            print("Relaciones de colaboración creadas")
    
    def crear_nodos_centrales(self):
        """Crear nodos centrales para agrupar por categorías"""
        with self.driver.session() as session:
            # Crear nodos de género/década para agrupar películas
            session.run("""
                MATCH (p:Pelicula)
                WITH p, toInteger(substring(toString(p.fecha_estreno), 0, 3)) * 10 as decada
                MERGE (d:Decada {valor: decada, nombre: toString(decada) + 's'})
                CREATE (p)-[:DE_LA_DECADA]->(d)
            """)
            
            # Crear nodos de calidad basados en ranking
            session.run("""
                MATCH (p:Pelicula)
                WITH p, 
                CASE 
                    WHEN p.ranking >= 4.0 THEN 'Excelente'
                    WHEN p.ranking >= 3.0 THEN 'Buena'
                    WHEN p.ranking >= 2.0 THEN 'Regular'
                    ELSE 'Baja'
                END as categoria_calidad
                MERGE (c:CalidadPelicula {categoria: categoria_calidad})
                CREATE (p)-[:TIENE_CALIDAD]->(c)
            """)
            
            print("Nodos centrales de agrupación creados")
    
    def crear_jerarquia_personas(self):
        """Crear jerarquía entre personas basada en experiencia/edad"""
        with self.driver.session() as session:
            # Crear nodos de experiencia para actores
            session.run("""
                MATCH (a:Actor)
                WHERE a.fecha_nac IS NOT NULL
                WITH a, duration.between(date(a.fecha_nac), date()).years as edad
                WITH a, edad,
                CASE 
                    WHEN edad >= 70 THEN 'Veterano'
                    WHEN edad >= 50 THEN 'Experimentado'
                    WHEN edad >= 30 THEN 'Establecido'
                    ELSE 'Joven'
                END as categoria_experiencia
                MERGE (e:ExperienciaActor {categoria: categoria_experiencia})
                CREATE (a)-[:TIENE_EXPERIENCIA]->(e)
            """)
            
            print("Jerarquía de personas creada")
    
    def crear_clusters_geograficos(self):
        """Crear clusters geográficos basados en lugares"""
        with self.driver.session() as session:
            # Agrupar por lugares de nacimiento de actores
            session.run("""
                MATCH (a:Actor)
                WHERE exists(a.lugar_nacimiento)
                WITH a, split(a.lugar_nacimiento, ' ')[0] as region
                MERGE (r:Region {nombre: region})
                CREATE (a)-[:NACIO_EN]->(r)
            """)
            
            # Agrupar premios por lugar
            session.run("""
                MATCH (pr:Premio)
                WHERE exists(pr.lugar)
                MERGE (l:LugarPremio {nombre: pr.lugar})
                CREATE (pr)-[:OTORGADO_EN]->(l)
            """)
            
            print("Clusters geográficos creados")
    
    def verificar_carga(self):
            print("Clusters geográficos creados")
    
    def verificar_carga(self):
        """Verificar que los datos se cargaron correctamente"""
        with self.driver.session() as session:
            # Contar nodos
            result = session.run("MATCH (n) RETURN labels(n) as tipo, count(n) as cantidad")
            print("\nResumen de nodos cargados:")
            for record in result:
                print(f"  {record['tipo'][0]}: {record['cantidad']}")
            
            # Contar relaciones
            result = session.run("MATCH ()-[r]->() RETURN type(r) as tipo, count(r) as cantidad")
            print("\nResumen de relaciones creadas:")
            for record in result:
                print(f"  {record['tipo']}: {record['cantidad']}")
    
    def cargar_todos_los_datos(self):
        """Cargar todos los datos y crear todas las relaciones"""
        print("Iniciando carga de datos a Neo4j...")
        
        if not self.wait_for_neo4j():
            print("Error: No se pudo conectar a Neo4j")
            return False
        
        try:
            # Limpiar y preparar
            self.limpiar_base_datos()
            self.crear_indices()
            
            # Cargar nodos
            print("\nCargando nodos...")
            self.cargar_peliculas()
            self.cargar_actores()
            self.cargar_directores()
            self.cargar_productores()
            self.cargar_criticas()
            self.cargar_premios()
            
            # Crear relaciones
            print("\nCreando relaciones...")
            self.crear_relaciones_direccion()
            self.crear_relaciones_actuacion()
            self.crear_relaciones_produccion()
            self.crear_relaciones_criticas()
            self.crear_relaciones_premios()
            
            # Crear agrupaciones y estructura jerárquica
            print("\nCreando estructura jerárquica y agrupaciones...")
            self.crear_relaciones_colaboracion()
            self.crear_nodos_centrales()
            self.crear_jerarquia_personas()
            self.crear_clusters_geograficos()
            
            # Verificar
            self.verificar_carga()
            
            print("\nCarga de datos completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"Error durante la carga: {e}")
            return False

def main():
    # Configuración de conexión
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password123')
    
    loader = Neo4jDataLoader(uri, user, password)
    
    try:
        success = loader.cargar_todos_los_datos()
        if success:
            print("\nPuedes acceder a la interfaz web de Neo4j en: http://localhost:7474")
            print("Usuario: neo4j")
            print("Contraseña: password123")
        else:
            print("La carga de datos falló")
    finally:
        loader.close()

if __name__ == "__main__":
    main()
