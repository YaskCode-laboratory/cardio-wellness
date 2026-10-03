-- ============================================================
-- SCRIPT DDL DEFINITIVO: Cardio Wellness Manager (PostgreSQL)
-- BASADO EN: DCD
-- PROPIEDADES: Normalizado (3FN), ACID, buenas prácticas
-- ============================================================

-- ============================================================
-- CREACIÓN DE TIPOS ENUM
-- ============================================================
CREATE TYPE tipo_usuario AS ENUM ('cliente', 'administrador');

CREATE TYPE nivel_rutina AS ENUM ('BASICO', 'INTERMEDIO', 'AVANZADO');

CREATE TYPE intensidad AS ENUM ('BAJA', 'MEDIA', 'ALTA');

CREATE TYPE estado_asignacion AS ENUM ('ACTIVA', 'FINALIZADA', 'CANCELADA');

-- ============================================================
-- TABLA: usuarios (Clase abstracta Usuario)
-- ============================================================
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(150) UNIQUE NOT NULL,
    contrasenia_hash VARCHAR(255) NOT NULL,  -- bcrypt
    edad INTEGER NOT NULL CHECK (edad > 0),
    tipo_usuario tipo_usuario NOT NULL DEFAULT 'cliente',
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE
);

COMMENT ON TABLE usuarios IS 'Base de la herencia: Usuario (abstracta en Python)';
COMMENT ON COLUMN usuarios.contrasenia_hash IS 'Almacena el hash de la contraseña';

-- Indices criticos
CREATE INDEX idx_usuarios_correo ON usuarios(correo_electronico);
CREATE INDEX idx_usuarios_tipo ON usuarios(tipo_usuario);
CREATE INDEX idx_usuarios_nombre ON usuarios(nombre, apellido);

-- ============================================================
-- TABLA: clientes (Especializacion de Usuario - Herencia 1:1)
-- Representa la clase Cliente del DCD
-- ============================================================
CREATE TABLE clientes (
    id_usuario INTEGER PRIMARY KEY REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    peso DECIMAL(5,2) NOT NULL CHECK (peso > 0),
    altura DECIMAL(5,2) NOT NULL CHECK (altura > 0),
    objetivo VARCHAR(255) NOT NULL,
    fecha_ingreso DATE NOT NULL DEFAULT CURRENT_DATE
);

COMMENT ON TABLE clientes IS 'Especializacion de Usuario: Cliente (hereda de Usuario)';
COMMENT ON COLUMN clientes.objetivo IS 'Ej: Bajar de peso, Mejorar resistencia, Mantener condicion';

-- Indice para consultas de progreso por fecha de ingreso
CREATE INDEX idx_clientes_ingreso ON clientes(fecha_ingreso);

-- ============================================================
-- TABLA: administradores (Especializacion de Usuario)
-- Representa la clase Administrador del DCD
-- ============================================================
CREATE TABLE administradores (
    id_usuario INTEGER PRIMARY KEY REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    -- Sin atributos adicionales (igual que en el DCD)
);

COMMENT ON TABLE administradores IS 'Especializacion de Usuario: Administrador (sin atributos propios)';

-- ============================================================
-- TABLA: ejercicios (Catalogo de ejercicios - Entidad fuerte)
-- Representa la clase EjercicioCardio del DCD
-- ============================================================
CREATE TABLE ejercicios (
    id_ejercicio SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50) NOT NULL,  -- Ej. "Aeróbico", "HIIT", "Cardio funcional"
    duracion_minutos INTEGER NOT NULL CHECK (duracion_minutos > 0),
    intensidad intensidad NOT NULL,
    calorias_estimadas DECIMAL(6,2) NOT NULL CHECK (calorias_estimadas >= 0),
    creado_por INTEGER NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL  -- Asociacion con Administrador
);

COMMENT ON TABLE ejercicios IS 'Catalogo de ejercicios (Clase EjercicioCardio)';
COMMENT ON COLUMN ejercicios.creado_por IS 'Administrador que creo el ejercicio (asociacion)';

-- Indices para búsquedas rápidas
CREATE INDEX idx_ejercicios_nombre ON ejercicios(nombre);
CREATE INDEX idx_ejercicios_tipo ON ejercicios(tipo);
CREATE INDEX idx_ejercicios_intensidad ON ejercicios(intensidad);

-- ============================================================
-- TABLA: rutinas (Planes de entrenamiento - Entidad fuerte)
-- Representa la clase Rutina del DCD
-- ============================================================
CREATE TABLE rutinas (
    id_rutina SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    objetivo VARCHAR(255) NOT NULL,
    nivel nivel_rutina NOT NULL,
    duracion_semanas INTEGER NOT NULL CHECK (duracion_semanas > 0),
    creado_por INTEGER NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,  -- Asociacion con Administrador
    fecha_creacion DATE NOT NULL DEFAULT CURRENT_DATE
);

COMMENT ON TABLE rutinas IS 'Planes de entrenamiento (Clase Rutina)';
COMMENT ON COLUMN rutinas.creado_por IS 'Administrador que gestiona/crea la rutina (asociacion)';

-- Indices para filtrar rutinas
CREATE INDEX idx_rutinas_objetivo ON rutinas(objetivo);
CREATE INDEX idx_rutinas_nivel ON rutinas(nivel);

-- ============================================================
-- TABLA PUENTE: rutina_ejercicios (Agregación N:M)
-- Representa: Rutina "1" o-- "1..*" EjercicioCardio
-- ============================================================
CREATE TABLE rutina_ejercicios (
    id_rutina INTEGER NOT NULL REFERENCES rutinas(id_rutina) ON DELETE CASCADE,
    id_ejercicio INTEGER NOT NULL REFERENCES ejercicios(id_ejercicio) ON DELETE CASCADE,
    orden_ejercicio INTEGER NOT NULL CHECK (orden_ejercicio > 0),  -- Para mantener el orden en la rutina
    PRIMARY KEY (id_rutina, id_ejercicio)
);

COMMENT ON TABLE rutina_ejercicios IS 'Relacion N:M: una rutina contiene varios ejercicios (agregacion)';

-- Indices para consultas eficientes
CREATE INDEX idx_rutina_ejercicios_rutina ON rutina_ejercicios(id_rutina);
CREATE INDEX idx_rutina_ejercicios_ejercicio ON rutina_ejercicios(id_ejercicio);

-- ============================================================
-- TABLA: asignaciones_rutina (Composicion con Cliente)
-- Representa: Cliente "1" *-- "0..*" AsignacionRutina
-- ============================================================
CREATE TABLE asignaciones_rutina (
    id_asignacion SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_usuario) ON DELETE CASCADE,
    id_rutina INTEGER NOT NULL REFERENCES rutinas(id_rutina) ON DELETE RESTRICT,  -- No borrar rutina si está asignada
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_finalizacion DATE,
    estado estado_asignacion NOT NULL DEFAULT 'ACTIVA',
    observaciones TEXT,
    CONSTRAINT chk_fechas CHECK (fecha_finalizacion IS NULL OR fecha_finalizacion >= fecha_asignacion)
);

COMMENT ON TABLE asignaciones_rutina IS 'Historial de asignaciones (Clase AsignacionRutina)';
COMMENT ON CONSTRAINT chk_fechas ON asignaciones_rutina IS 'La fecha de finalizacion debe ser posterior a la asignacion';

-- Indices criticos para consultas frecuentes
CREATE INDEX idx_asignaciones_cliente ON asignaciones_rutina(id_cliente);
CREATE INDEX idx_asignaciones_estado ON asignaciones_rutina(estado);
CREATE INDEX idx_asignaciones_fechas ON asignaciones_rutina(fecha_asignacion, fecha_finalizacion);

-- Indice parcial para búsquedas de rutina activa (muy rapido)
CREATE INDEX idx_asignaciones_activa ON asignaciones_rutina(id_cliente) WHERE estado = 'ACTIVA';

-- ============================================================
-- TABLA: sesiones_entrenamiento (Composicion con Cliente)
-- Representa: Cliente "1" *-- "0..*" SesionEntrenamiento
-- ============================================================
CREATE TABLE sesiones_entrenamiento (
    id_sesion SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_usuario) ON DELETE CASCADE,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    duracion_real INTEGER NOT NULL CHECK (duracion_real > 0),
    intensidad_real intensidad NOT NULL,
    calorias_quemadas DECIMAL(6,2) NOT NULL CHECK (calorias_quemadas >= 0),
    observaciones TEXT,
    completada BOOLEAN NOT NULL DEFAULT FALSE
);

COMMENT ON TABLE sesiones_entrenamiento IS 'Registro de entrenamientos (Clase SesionEntrenamiento)';

-- Indices para consultar sesiones por cliente y fechas
CREATE INDEX idx_sesiones_cliente ON sesiones_entrenamiento(id_cliente);
CREATE INDEX idx_sesiones_fecha ON sesiones_entrenamiento(fecha);
CREATE INDEX idx_sesiones_completada ON sesiones_entrenamiento(completada);

-- ============================================================
-- TABLA: progreso_mensual (Composicion con Cliente)
-- Representa: Cliente "1" *-- "0..*" ProgresoMensual
-- ============================================================
CREATE TABLE progreso_mensual (
    id_progreso SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_usuario) ON DELETE CASCADE,
    mes DATE NOT NULL,  -- Se recomienda guardar el primer día del mes (ej. 2026-08-01)
    peso DECIMAL(5,2) NOT NULL CHECK (peso > 0),
    sesiones_completadas INTEGER NOT NULL DEFAULT 0 CHECK (sesiones_completadas >= 0),
    sesiones_planificadas INTEGER NOT NULL DEFAULT 0 CHECK (sesiones_planificadas >= 0),
    porcentaje_cumplimiento DECIMAL(5,2) NOT NULL DEFAULT 0.0 CHECK (porcentaje_cumplimiento BETWEEN 0 AND 100),
    CONSTRAINT unq_cliente_mes UNIQUE (id_cliente, mes)  -- Solo un registro por cliente y mes
);

COMMENT ON TABLE progreso_mensual IS 'Resumen mensual de progreso (Clase ProgresoMensual)';
COMMENT ON COLUMN progreso_mensual.mes IS 'Primer día del mes (ej. 2026-08-01)';

-- Indices para consultar progreso
CREATE INDEX idx_progreso_cliente ON progreso_mensual(id_cliente);
CREATE INDEX idx_progreso_mes ON progreso_mensual(mes);

-- ============================================================
-- 12. VISTAS UTILES (para simplificar las consultas en Python)
-- ============================================================
-- Vista: Datos completos del cliente (union de usuario + cliente)
CREATE VIEW vw_clientes_completo AS
SELECT 
    u.id_usuario,
    u.nombre,
    u.apellido,
    u.correo_electronico,
    u.contrasenia_hash,
    u.edad,
    u.fecha_registro,
    c.peso,
    c.altura,
    c.objetivo,
    c.fecha_ingreso
FROM usuarios u
JOIN clientes c ON u.id_usuario = c.id_usuario
WHERE u.tipo_usuario = 'cliente';

COMMENT ON VIEW vw_clientes_completo IS 'Vista para obtener todos los datos de un cliente en una sola consulta (incluye hash)';

-- Vista: Rutina activa por cliente (para el panel del cliente)
CREATE VIEW vw_rutina_activa_cliente AS
SELECT 
    a.id_cliente,
    a.id_asignacion,
    r.id_rutina,
    r.nombre AS nombre_rutina,
    r.objetivo,
    r.nivel,
    r.duracion_semanas,
    a.fecha_asignacion,
    a.fecha_finalizacion,
    a.observaciones
FROM asignaciones_rutina a
JOIN rutinas r ON a.id_rutina = r.id_rutina
WHERE a.estado = 'ACTIVA';

COMMENT ON VIEW vw_rutina_activa_cliente IS 'Vista para obtener la rutina activa de un cliente (filtro por id_cliente)';

-- Vista: Resumen de progreso con cumplimiento
CREATE VIEW vw_progreso_cliente AS
SELECT 
    p.id_cliente,
    u.nombre,
    u.apellido,
    p.mes,
    p.peso,
    p.sesiones_completadas,
    p.sesiones_planificadas,
    p.porcentaje_cumplimiento,
    CASE 
        WHEN p.porcentaje_cumplimiento >= 80 THEN 'ALTO'
        WHEN p.porcentaje_cumplimiento >= 50 THEN 'MEDIO'
        ELSE 'BAJO'
    END AS nivel_cumplimiento
FROM progreso_mensual p
JOIN clientes c ON p.id_cliente = c.id_usuario
JOIN usuarios u ON c.id_usuario = u.id_usuario
ORDER BY p.mes DESC;

COMMENT ON VIEW vw_progreso_cliente IS 'Vista para mostrar el progreso con niveles de cumplimiento';

-- ============================================================
-- DATOS DE PRUEBA MÍNIMOS
-- Descomentar para insertar datos de ejemplo
-- ============================================================

-- Insertar un administrador (id_usuario = 1)
-- Insertar un administrador en la tabla específica
-- Insertar clientes
-- ============================================================
-- Datos de Prueba: Insertar ejercicios (Calorias sin verificar, solo ejemplo)
-- ============================================================
-- ============================================================
-- Datos de Prueba: Insertar rutinas
-- ============================================================
-- ============================================================
-- Datos de prueba: Asignacion de ejercicios a rutinas (Agregacion)
-- ============================================================

-- Quema Grasa Básica (1)
-- Quema Grasa Intensa (2)
-- Resistencia Cardio (3)
-- Resistencia Intermedia (4)
-- Mantenimiento Básico (5)
-- Mantenimiento Activo (6)
-- Asignar rutinas a clientes (composicion)
-- Héctor con Mantenimiento Activo

-- ============================================================
-- Datos de prueba: Insertar sesiones de entrenamiento
-- ============================================================
-- ============================================================
-- Datos de Prueba: Insertar progreso mensual
-- ============================================================
-- Septiembre: 3 de 4 sesiones

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================
