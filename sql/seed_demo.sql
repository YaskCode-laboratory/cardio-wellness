-- ============================================================================
-- DATOS DE DEMOSTRACIÓN - CARDIO WELLNESS
-- ============================================================================
-- Archivo: sql/seed_demo.sql
--
-- Ejecutar después de sql/schema.sql.
--
-- IMPORTANTE:
-- - Todos los nombres, correos, medidas, sesiones y progresos son ficticios.
-- - No incluir información personal ni datos de usuarios reales.
-- - HASH_SOLO_DEMO_NO_USAR no es una contraseña válida ni un hash utilizable.
-- - Este archivo asume una base de datos nueva, con IDs iniciando desde 1.
-- ============================================================================


-- ============================================================================
-- USUARIO ADMINISTRADOR DEMO
-- ============================================================================

INSERT INTO usuarios (
    nombre,
    apellido,
    correo_electronico,
    contrasenia_hash,
    edad,
    tipo_usuario
)
VALUES (
    'Administrador',
    'Demo',
    'admin.demo@example.com',
    'HASH_SOLO_DEMO_NO_USAR',
    30,
    'administrador'
);


INSERT INTO administradores (id_usuario)
VALUES (1);


-- ============================================================================
-- USUARIOS CLIENTE DEMO
-- ============================================================================

INSERT INTO usuarios (
    nombre,
    apellido,
    correo_electronico,
    contrasenia_hash,
    edad,
    tipo_usuario
)
VALUES
    (
        'Cliente',
        'DemoUno',
        'cliente1.demo@example.com',
        'HASH_SOLO_DEMO_NO_USAR',
        28,
        'cliente'
    ),
    (
        'Cliente',
        'DemoDos',
        'cliente2.demo@example.com',
        'HASH_SOLO_DEMO_NO_USAR',
        25,
        'cliente'
    ),
    (
        'Cliente',
        'DemoTres',
        'cliente3.demo@example.com',
        'HASH_SOLO_DEMO_NO_USAR',
        22,
        'cliente'
    ),
    (
        'Cliente',
        'DemoCuatro',
        'cliente4.demo@example.com',
        'HASH_SOLO_DEMO_NO_USAR',
        21,
        'cliente'
    );


-- ============================================================================
-- CLIENTES DEMO
-- ============================================================================

INSERT INTO clientes (
    id_usuario,
    peso,
    altura,
    objetivo,
    fecha_ingreso
)
VALUES
    (2, 80.0, 1.75, 'Bajar de peso', '2026-01-15'),
    (3, 66.0, 1.65, 'Mejorar resistencia', '2026-02-01'),
    (4, 64.0, 1.70, 'Mejorar resistencia', '2026-03-15'),
    (5, 61.0, 1.72, 'Mantener condicion', '2026-08-15');


-- ============================================================================
-- CATÁLOGO DE EJERCICIOS DEMO
-- ============================================================================

INSERT INTO ejercicios (
    nombre,
    descripcion,
    tipo,
    duracion_minutos,
    intensidad,
    calorias_estimadas,
    creado_por
)
VALUES
    (
        'Caminata Rapida',
        'Marcha rápida al aire libre o en caminadora.',
        'LISS',
        30,
        'BAJA',
        150.0,
        1
    ),
    (
        'Trote Continuo',
        'Trote a ritmo constante.',
        'LISS',
        25,
        'MEDIA',
        250.0,
        1
    ),
    (
        'Bicicleta Estatica',
        'Pedaleo en bicicleta estática.',
        'LISS',
        20,
        'MEDIA',
        190.0,
        1
    ),
    (
        'Saltar la Cuerda',
        'Salto continuo con cuerda.',
        'HIIT',
        15,
        'ALTA',
        280.0,
        1
    ),
    (
        'Circuito Funcional',
        'Circuito de ocho estaciones de cuarenta y cinco segundos cada una.',
        'HIIT',
        25,
        'ALTA',
        350.0,
        1
    ),
    (
        'HIIT de Bajo Impacto',
        'Rutina sin saltos para principiantes: sentadillas, zancadas, planchas y pasos laterales.',
        'HIIT',
        20,
        'MEDIA',
        220.0,
        1
    );


-- ============================================================================
-- RUTINAS DEMO
-- ============================================================================

INSERT INTO rutinas (
    nombre,
    descripcion,
    objetivo,
    nivel,
    duracion_semanas,
    creado_por
)
VALUES
    (
        'Quema Grasa Basica',
        'Rutina suave para comenzar con ejercicios de baja intensidad.',
        'Bajar de peso',
        'BASICO',
        4,
        1
    ),
    (
        'Quema Grasa Intensa',
        'Rutina enfocada en reducción de peso con ejercicios HIIT y LISS.',
        'Bajar de peso',
        'INTERMEDIO',
        4,
        1
    ),
    (
        'Resistencia Cardio',
        'Rutina para mejorar capacidad cardiovascular con ejercicios de intensidad media.',
        'Mejorar resistencia',
        'BASICO',
        6,
        1
    ),
    (
        'Resistencia Intermedia',
        'Rutina para aumentar la capacidad cardiovascular con intensidad media-alta.',
        'Mejorar resistencia',
        'INTERMEDIO',
        6,
        1
    ),
    (
        'Mantenimiento Basico',
        'Rutina ligera para mantener la condición física sin esfuerzo excesivo.',
        'Mantener condicion',
        'BASICO',
        8,
        1
    ),
    (
        'Mantenimiento Activo',
        'Rutina para mantener la condición física con ejercicios variados y de bajo impacto.',
        'Mantener condicion',
        'BASICO',
        8,
        1
    );


-- ============================================================================
-- RELACIÓN ENTRE RUTINAS Y EJERCICIOS
-- ============================================================================

INSERT INTO rutina_ejercicios (
    id_rutina,
    id_ejercicio,
    orden_ejercicio
)
VALUES
    (1, 1, 1),
    (1, 6, 2),
    (1, 3, 3);


INSERT INTO rutina_ejercicios (
    id_rutina,
    id_ejercicio,
    orden_ejercicio
)
VALUES
    (2, 1, 1),
    (2, 2, 2),
    (2, 4, 3),
    (2, 5, 4);


INSERT INTO rutina_ejercicios (
    id_rutina,
    id_ejercicio,
    orden_ejercicio
)
VALUES
    (3, 2, 1),
    (3, 3, 2),
    (3, 6, 3);


INSERT INTO rutina_ejercicios (
    id_rutina,
    id_ejercicio,
    orden_ejercicio
)
VALUES
    (4, 2, 1),
    (4, 5, 2),
    (4, 4, 3),
    (4, 1, 4);


INSERT INTO rutina_ejercicios (
    id_rutina,
    id_ejercicio,
    orden_ejercicio
)
VALUES
    (5, 1, 1),
    (5, 3, 2),
    (5, 6, 3);


INSERT INTO rutina_ejercicios (
    id_rutina,
    id_ejercicio,
    orden_ejercicio
)
VALUES
    (6, 3, 1),
    (6, 6, 2),
    (6, 1, 3),
    (6, 2, 4);


-- ============================================================================
-- ASIGNACIONES DE RUTINAS DEMO
-- ============================================================================

INSERT INTO asignaciones_rutina (
    id_cliente,
    id_rutina,
    fecha_asignacion,
    estado
)
VALUES
    (2, 2, '2026-08-01', 'ACTIVA'), -- Cliente demo 1: Quema Grasa Intensa
    (3, 4, '2026-08-15', 'ACTIVA'), -- Cliente demo 2: Resistencia Intermedia
    (4, 3, '2026-08-20', 'ACTIVA'), -- Cliente demo 3: Resistencia Cardio
    (5, 6, '2026-09-01', 'ACTIVA'); -- Cliente demo 4: Mantenimiento Activo


-- ============================================================================
-- SESIONES DE ENTRENAMIENTO DEMO
-- ============================================================================

INSERT INTO sesiones_entrenamiento (
    id_cliente,
    fecha,
    duracion_real,
    intensidad_real,
    calorias_quemadas,
    observaciones,
    completada
)
VALUES
    -- Cliente demo 1: rutina de quema de grasa
    (2, '2026-08-03', 45, 'ALTA', 380.0, 'Sesión demo completada.', TRUE),
    (2, '2026-08-10', 40, 'MEDIA', 310.0, 'Sesión demo de intensidad media.', TRUE),
    (2, '2026-08-17', 50, 'ALTA', 420.0, 'Sesión demo de alta intensidad.', TRUE),
    (2, '2026-08-24', 35, 'ALTA', 290.0, 'Sesión demo corta.', TRUE),

    -- Cliente demo 2: rutina de resistencia
    (3, '2026-08-18', 45, 'ALTA', 370.0, 'Sesión demo completada.', TRUE),
    (3, '2026-08-25', 40, 'MEDIA', 290.0, 'Sesión demo completada.', TRUE),
    (3, '2026-09-01', 50, 'ALTA', 410.0, 'Sesión demo completada.', TRUE),

    -- Cliente demo 3: rutina de resistencia
    (4, '2026-08-22', 35, 'MEDIA', 250.0, 'Sesión demo completada.', TRUE),
    (4, '2026-08-29', 40, 'MEDIA', 280.0, 'Sesión demo completada.', TRUE),
    (4, '2026-09-05', 30, 'BAJA', 190.0, 'Sesión demo de baja intensidad.', TRUE),

    -- Cliente demo 4: rutina de mantenimiento
    (5, '2026-09-02', 25, 'BAJA', 160.0, 'Sesión demo inicial.', TRUE),
    (5, '2026-09-09', 30, 'MEDIA', 220.0, 'Sesión demo completada.', TRUE),
    (5, '2026-09-16', 20, 'BAJA', 140.0, 'Sesión demo corta.', TRUE);


-- ============================================================================
-- PROGRESO MENSUAL DEMO
-- ============================================================================

INSERT INTO progreso_mensual (
    id_cliente,
    mes,
    peso,
    sesiones_completadas,
    sesiones_planificadas,
    porcentaje_cumplimiento
)
VALUES
    -- Cliente demo 1: objetivo de reducción de peso
    (2, '2026-08-01', 80.0, 4, 4, 100.0),
    (2, '2026-09-01', 79.0, 0, 4, 0.0),

    -- Cliente demo 2: objetivo de resistencia
    (3, '2026-08-01', 66.0, 2, 4, 50.0),
    (3, '2026-09-01', 65.5, 1, 4, 25.0),

    -- Cliente demo 3: objetivo de resistencia
    (4, '2026-08-01', 64.0, 2, 4, 50.0),
    (4, '2026-09-01', 63.5, 1, 4, 25.0),

    -- Cliente demo 4: objetivo de mantenimiento
    (5, '2026-08-01', 61.0, 0, 0, 0.0),
    (5, '2026-09-01', 61.0, 3, 4, 75.0);