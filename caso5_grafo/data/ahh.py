import pandas as pd
import os
import json

# Diccionario con los archivos y su ruta
archivos_csv = {
    "actor": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\actor.csv",
    "actuacion": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\actuacion.csv",
    "critica": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\critica.csv",
    "director": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\director.csv",
    "pelicula": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\pelicula.csv",
    "premio": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\premio.csv",
    "produccion": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\produccion.csv",
    "productor": r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\productor.csv"
}

# Carpeta de salida para los JSON
output_dir = r"C:\Users\Hogar\OneDrive\Documents\BDA\Examen\caso5_grafo\data\json"

# Crear carpeta si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesar cada archivo
for nombre, ruta in archivos_csv.items():
    try:
        df = pd.read_csv(ruta)
        json_data = df.to_dict(orient='records')
        output_path = os.path.join(output_dir, f"{nombre}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print(f"[✔] {nombre}.json generado correctamente.")
    except Exception as e:
        print(f"[✘] Error al procesar {nombre}: {e}")
