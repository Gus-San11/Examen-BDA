// Consultas BSON para MongoDB - Caso4 JSON
// Estas consultas resuelven los requerimientos del negocio

// ==========================================
// CONSULTA A: Total de salarios pagados a los actores de "Cinema Paradiso" dirigida por "Giuseppe Tornatore"
// ==========================================

use('peliculas_db');

print("CONSULTA A: Total de salarios - Cinema Paradiso");
print("=" .repeat(60));

db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "director.nombre": "Giuseppe Tornatore"
    }
  },
  {
    $unwind: "$actores"
  },
  {
    $group: {
      _id: null,
      "total_salarios": { $sum: "$actores.salario" },
      "pelicula": { $first: "$titulo" },
      "director": { $first: "$director.nombre" },
      "cantidad_actores": { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      pelicula: 1,
      director: 1,
      cantidad_actores: 1,
      total_salarios: { $round: ["$total_salarios", 2] }
    }
  }
]);

// ==========================================
// CONSULTA B: Listado de premios de "Cinema Paradiso" ordenados por ranking
// ==========================================

print("\nCONSULTA B: Premios de Cinema Paradiso");
print("=" .repeat(60));

db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "director.nombre": "Giuseppe Tornatore"
    }
  },
  {
    $unwind: "$premios"
  },
  {
    $sort: { "premios.ranking_premio": -1 }
  },
  {
    $project: {
      _id: 0,
      "ranking": "$premios.ranking_premio",
      "nombre_premio": "$premios.nombre",
      "lugar_certamen": "$premios.lugar_certamen",
      "fecha_premio": {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$premios.fecha"
        }
      }
    }
  }
]);

// ==========================================
// CONSULTA C: Total de aportes economicos de "Franco Cristaldi"
// ==========================================

print("\nCONSULTA C: Total aportes de Franco Cristaldi");
print("=" .repeat(60));

db.peliculas.aggregate([
  {
    $unwind: "$productores"
  },
  {
    $match: {
      "productores.nombre": "Franco Cristaldi"
    }
  },
  {
    $group: {
      _id: "$productores.nombre",
      "total_aportes": { $sum: "$productores.aportacion_economica" },
      "cantidad_peliculas": { $sum: 1 },
      "peliculas": { $push: "$titulo" }
    }
  },
  {
    $project: {
      _id: 0,
      productor: "$_id",
      total_aportes: { $round: ["$total_aportes", 2] },
      cantidad_peliculas: 1,
      peliculas: 1
    }
  }
]);

// ==========================================
// CONSULTA D: Criticas de "Cinema Paradiso" entre el 15 y 30 de agosto de 1990
// ==========================================

print("\nCONSULTA D: Criticas de Cinema Paradiso (15-30 agosto 1990)");
print("=" .repeat(60));

db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "director.nombre": "Giuseppe Tornatore"
    }
  },
  {
    $unwind: "$criticas"
  },
  {
    $match: {
      "criticas.fecha": {
        $gte: ISODate("1990-08-15T00:00:00.000Z"),
        $lte: ISODate("1990-08-30T23:59:59.999Z")
      }
    }
  },
  {
    $sort: { "criticas.fecha": -1 }
  },
  {
    $project: {
      _id: 0,
      "medio": "$criticas.medio",
      "fecha": {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$criticas.fecha"
        }
      },
      "autor": "$criticas.autor",
      "contenido": "$criticas.contenido",
      "ranking": "$criticas.ranking"
    }
  }
]);

// ==========================================
// CONSULTA E: Todas las personas involucradas en "Cinema Paradiso"
// ==========================================

print("\nCONSULTA E: Personas involucradas en Cinema Paradiso");
print("=" .repeat(60));

// Subconsulta para actores
db.peliculas.aggregate([
  {
    $match: {
      "titulo": "Cinema Paradiso",
      "director.nombre": "Giuseppe Tornatore"
    }
  },
  {
    $project: {
      personas: {
        $concatArrays: [
          // Director
          [{
            nombre: "$director.nombre",
            rol: "Director",
            edad_actual: null,
            estado_civil: null,
            telefono: "$director.telefono"
          }],
          // Actores
          {
            $map: {
              input: "$actores",
              as: "actor",
              in: {
                nombre: "$$actor.nombre",
                rol: "Actor",
                edad_actual: "$$actor.edad_actual",
                estado_civil: "$$actor.estado_civil",
                telefono: "$$actor.telefono"
              }
            }
          },
          // Productores
          {
            $map: {
              input: "$productores",
              as: "productor",
              in: {
                nombre: "$$productor.nombre",
                rol: "Productor",
                edad_actual: null,
                estado_civil: null,
                telefono: "$$productor.telefono"
              }
            }
          }
        ]
      }
    }
  },
  {
    $unwind: "$personas"
  },
  {
    $replaceRoot: { newRoot: "$personas" }
  },
  {
    $sort: { "rol": 1, "nombre": 1 }
  }
]);

// ==========================================
// CONSULTAS ADICIONALES DE ANALISIS
// ==========================================

print("\nCONSULTAS ADICIONALES DE ANALISIS");
print("=" .repeat(60));

// Estadisticas generales de la base de datos
print("\nEstadisticas generales:");
db.peliculas.aggregate([
  {
    $facet: {
      "total_peliculas": [{ $count: "count" }],
      "pelicula_mejor_ranking": [
        { $sort: { "ranking": -1 } },
        { $limit: 1 },
        { $project: { titulo: 1, ranking: 1, "director.nombre": 1 } }
      ],
      "promedio_ranking": [
        { $group: { _id: null, promedio: { $avg: "$ranking" } } }
      ],
      "directores_mas_peliculas": [
        { $group: { _id: "$director.nombre", cantidad: { $sum: 1 } } },
        { $sort: { cantidad: -1 } },
        { $limit: 5 }
      ]
    }
  }
]);

// Analisis de presupuestos
print("\nAnalisis de presupuestos por pelicula:");
db.peliculas.aggregate([
  {
    $project: {
      titulo: 1,
      "director.nombre": 1,
      "presupuesto_total": {
        $add: [
          { $sum: "$actores.salario" },
          { $sum: "$productores.aportacion_economica" }
        ]
      },
      "total_actores": { $size: "$actores" },
      "total_productores": { $size: "$productores" }
    }
  },
  {
    $sort: { presupuesto_total: -1 }
  },
  {
    $limit: 10
  }
]);

print("\nTodas las consultas ejecutadas correctamente");
print("Para ejecutar consultas individuales, copie y pegue cada seccion por separado");
