// Script de inicializacion simplificado para MongoDB
// Este script se ejecuta automaticamente cuando se inicia el contenedor

// Usar la base de datos peliculas_db
use('peliculas_db');

print('Iniciando configuracion simplificada de la base de datos de peliculas...');

// Crear colecciones sin validacion estricta para permitir carga inicial
db.createCollection('peliculas');

print('Coleccion "peliculas" creada sin validacion de esquema');

// Crear indices basicos para optimizar consultas
db.peliculas.createIndex({ "id_pelicula": 1 });
db.peliculas.createIndex({ "titulo": 1 });

print('Indices basicos creados');
print('Base de datos lista para recibir datos');

// Operacion de prueba
var conteo = db.peliculas.countDocuments();
print('Numero de peliculas en la coleccion: ' + conteo);
