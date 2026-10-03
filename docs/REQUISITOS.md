# Especificación Final de Requisitos

## Sistema de Gestión de Rutinas Cardio-Wellness

**Asignatura:** Ingeniería de Software
**Período:** 2026-I  
**Equipo:** Emiro Rincón, Juan Perea, Eliam Rodríguez  
**Área de Wellness:** Cardio / Salud / Fitness

---

## Índice

1. [Análisis de Necesidades](#1-análisis-de-necesidades)
2. [Actores del Sistema](#2-actores-del-sistema)
3. [Requisitos Funcionales](#3-requisitos-funcionales)
4. [Requisitos No Funcionales](#4-requisitos-no-funcionales)
5. [Requisitos de Datos y Base de Datos](#5-requisitos-de-datos-y-base-de-datos)
6. [Trazabilidad con la Implementación](#6-trazabilidad-con-la-implementación)

---

## 1. Análisis de Necesidades

### 1.1 Contexto del problema

Al analizar el mercado de aplicaciones de wellness, se identificó que:

- **Aplicaciones como MyFitnessPal, Strava y Kinetiq** están orientadas al **usuario individual** y no permiten que un entrenador gestione rutinas desde un panel de administración.
- **Plataformas como Virtuagym** están diseñadas para **grandes cadenas de gimnasios** y resultan costosas y complejas para pequeños estudios locales.
- **Ninguna solución existente** combina: gestión de rutinas cardio personalizadas, seguimiento mensual del progreso, parámetro META con indicador visual, y funcionamiento offline.

### 1.2 Necesidades identificadas

| # | Necesidad | Descripción | Prioridad |
|:---:|:---|:---|:---:|
| N1 | **Gestión de usuarios con roles** | El sistema debe distinguir entre Administrador (entrenador) y Cliente, con permisos diferenciados. | Alta |
| N2 | **Registro de datos biométricos** | Al dar de alta a un cliente, se deben registrar peso, altura, edad y objetivo de salud. | Alta |
| N3 | **Catálogo de ejercicios cardio** | El Administrador debe poder crear, editar y eliminar ejercicios clasificados por tipo (LISS, HIIT, Cardio Funcional). | Alta |
| N4 | **Gestión de rutinas** | El Administrador debe poder crear rutinas compuestas por múltiples ejercicios del catálogo. | Alta |
| N5 | **Asignación de rutinas a clientes** | El Administrador debe asignar rutinas a clientes específicos con duración estimada. | Alta |
| N6 | **Registro de sesiones de entrenamiento** | El Cliente debe registrar cada sesión realizada (duración, intensidad). | Alta |
| N7 | **Cálculo de progreso mensual** | El sistema debe calcular el porcentaje de cumplimiento y la variación de peso mensual. | Alta |
| N8 | **Parámetro META con colores** | El sistema debe mostrar visualmente si el cliente alcanzó su objetivo de salud (verde/rojo). | Alta |
| N9 | **LOG de auditoría** | Todas las acciones críticas deben registrarse en un archivo de texto plano. | Alta |
| N10 | **Exportación de reportes a PDF** | El Cliente debe poder generar un reporte consolidado de su progreso. | Media |
| N11 | **Funcionamiento 100% offline** | El sistema no debe depender de conexión a internet. | Alta |

### 1.3 Alcance del sistema

**El sistema SÍ incluye:**
- Gestión completa de usuarios (Administrador y Cliente).
- Catálogo de ejercicios cardio (LISS, HIIT, Cardio Funcional).
- Gestión de rutinas con agregación de ejercicios.
- Asignación de rutinas con historial y estados.
- Registro de sesiones de entrenamiento.
- Cálculo de progreso mensual y Parámetro META.
- LOG de auditoría.
- Exportación de reportes a PDF.

**El sistema NO incluye:**
- Pagos o suscripciones (patrón Strategy no aplica).
- Notificaciones en tiempo real (patrón Observer no aplica).
- Sensores biométricos externos.
- Acceso remoto o en la nube.
- Múltiples idiomas (por ahora, solo español).

---

## 2. Actores del Sistema

El sistema tiene **2 actores principales**:

### 2.1 Administrador (Entrenador)

**Descripción:** Responsable de la gestión completa del estudio de wellness.

**Responsabilidades:**
- Gestionar clientes (crear, editar, eliminar, listar).
- Gestionar el catálogo de ejercicios cardio.
- Gestionar rutinas (crear, editar, eliminar).
- Asignar rutinas a clientes.
- Consultar el progreso de todos los clientes.
- Exportar reportes consolidados.

**Casos de uso asociados:**
- CU01 – Iniciar Sesión
- CU02 – Cerrar Sesión
- CU03 – Registrar Cliente
- CU04 – Gestionar Rutinas
- CU05 – Gestionar Ejercicios
- CU06 – Asignar Rutina
- CU07 – Ver Progreso de Clientes

### 2.2 Cliente

**Descripción:** Usuario final que realiza entrenamientos y registra su progreso.

**Responsabilidades:**
- Consultar su rutina activa.
- Registrar sesiones de entrenamiento.
- Consultar su progreso personal.
- Ver su Parámetro META.
- Exportar su reporte de progreso a PDF.

**Casos de uso asociados:**
- CU01 – Iniciar Sesión
- CU02 – Cerrar Sesión
- CU08 – Consultar Rutina Activa
- CU09 – Registrar Sesión de Entrenamiento
- CU10 – Consultar Progreso Personal
- CU11 – Ver Parámetro META
- CU12 – Exportar Reporte PDF

### 2.3 Matriz de permisos por actor

| Funcionalidad | Administrador | Cliente |
|:---|:---:|:---:|
| Iniciar / Cerrar Sesión | ✅ | ✅ |
| Registrar Cliente | ✅ | ❌ |
| Gestionar Rutinas | ✅ | ❌ |
| Gestionar Ejercicios | ✅ | ❌ |
| Asignar Rutina | ✅ | ❌ |
| Ver Progreso de Clientes | ✅ | ❌ |
| Consultar Rutina Activa | ❌ | ✅ |
| Registrar Sesión | ❌ | ✅ |
| Consultar Progreso Personal | ❌ | ✅ |
| Ver Parámetro META | ❌ | ✅ |
| Exportar Reporte PDF | ❌ | ✅ |

---

## 3. Requisitos Funcionales

Los requisitos funcionales se organizan por módulo.

### 3.1 Módulo de Autenticación

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-01 | El sistema debe permitir el inicio de sesión con correo electrónico y contraseña. | Alta |
| RF-02 | El sistema debe validar que las credenciales coincidan con las almacenadas (hash bcrypt). | Alta |
| RF-03 | El sistema debe redirigir al panel correspondiente según el rol del usuario. | Alta |
| RF-04 | El sistema debe registrar cada intento de login (exitoso o fallido) en el LOG. | Alta |
| RF-05 | El sistema debe permitir cerrar sesión. | Alta |

### 3.2 Módulo de Gestión de Clientes

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-06 | El Administrador debe poder registrar un cliente con: nombre, apellido, correo, contraseña, edad, peso, altura, objetivo y peso objetivo (META). | Alta |
| RF-07 | El sistema debe validar que la edad > 0, peso > 0 y altura > 0. | Alta |
| RF-08 | El sistema debe hashear la contraseña antes de almacenarla. | Alta |
| RF-09 | El Administrador debe poder editar los datos de un cliente. | Media |
| RF-10 | El Administrador debe poder eliminar un cliente. | Media |
| RF-11 | El Administrador debe poder listar todos los clientes. | Media |
| RF-12 | El Administrador debe poder buscar un cliente por correo o ID. | Media |

### 3.3 Módulo de Gestión de Ejercicios

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-13 | El Administrador debe poder crear ejercicios con: nombre, descripción, tipo, duración, intensidad y calorías estimadas. | Alta |
| RF-14 | El sistema debe validar que la duración > 0 y las calorías >= 0. | Alta |
| RF-15 | El Administrador debe poder clasificar ejercicios por tipo: LISS, HIIT, Cardio Funcional. | Alta |
| RF-16 | El Administrador debe poder editar ejercicios existentes. | Media |
| RF-17 | El Administrador debe poder eliminar ejercicios (si no están en uso en alguna rutina). | Media |
| RF-18 | El Administrador debe poder listar y buscar ejercicios. | Media |

### 3.4 Módulo de Gestión de Rutinas

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-19 | El Administrador debe poder crear rutinas con: nombre, descripción, objetivo, nivel y duración en semanas. | Alta |
| RF-20 | El Administrador debe poder agregar ejercicios del catálogo a una rutina. | Alta |
| RF-21 | El Administrador debe poder eliminar ejercicios de una rutina. | Media |
| RF-22 | El sistema debe calcular la duración total de una rutina sumando las duraciones de sus ejercicios. | Media |
| RF-23 | El Administrador debe poder asignar una rutina a un cliente con duración estimada. | Alta |
| RF-24 | El sistema debe finalizar la asignación activa anterior antes de crear una nueva. | Alta |

### 3.5 Módulo de Sesiones de Entrenamiento

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-25 | El Cliente debe poder registrar una sesión de entrenamiento con: duración real, intensidad real y calorías quemadas. | Alta |
| RF-26 | El sistema debe validar que la duración real > 0. | Alta |
| RF-27 | El sistema debe asociar la sesión al cliente autenticado y a la fecha actual. | Alta |
| RF-28 | El Cliente debe poder consultar el historial de sus sesiones. | Media |
| RF-29 | El Administrador debe poder eliminar una sesión si es necesario. | Baja |

### 3.6 Módulo de Progreso y META

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-30 | El sistema debe calcular el porcentaje de cumplimiento mensual: `(sesiones_completadas / sesiones_planificadas) * 100`. | Alta |
| RF-31 | El sistema debe calcular la variación de peso comparando el mes actual con el anterior. | Alta |
| RF-32 | El sistema debe mostrar si el cliente alcanzó su peso objetivo (Parámetro META) con colores: verde (alcanzado) o rojo (no alcanzado). | Alta |
| RF-33 | El Cliente debe poder consultar su progreso personal. | Alta |
| RF-34 | El Administrador debe poder consultar el progreso de todos sus clientes. | Alta |

### 3.7 Módulo de Reportes

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-35 | El Cliente debe poder exportar su reporte de progreso a PDF. | Media |
| RF-36 | El reporte debe incluir: datos del cliente, resumen de actividad, historial mensual y Parámetro META. | Alta |

### 3.8 Módulo de Auditoría

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-37 | El sistema debe registrar todas las acciones críticas en `logs/LOG_CARDIO.txt`. | Alta |
| RF-38 | El formato de cada línea debe ser: `FECHA, USUARIO, ACTIVIDAD`. | Alta |
| RF-39 | Las actividades a registrar son: LOGIN, CONSULTA, REGISTRO, ELIMINACIÓN, LOGOUT. | Alta |

### 3.9 Resumen de requisitos funcionales

| Módulo | Cantidad de RF | IDs |
|:---|:---:|:---|
| Autenticación | 5 | RF-01 a RF-05 |
| Gestión de Clientes | 7 | RF-06 a RF-12 |
| Gestión de Ejercicios | 6 | RF-13 a RF-18 |
| Gestión de Rutinas | 6 | RF-19 a RF-24 |
| Sesiones de Entrenamiento | 5 | RF-25 a RF-29 |
| Progreso y META | 5 | RF-30 a RF-34 |
| Reportes | 2 | RF-35 a RF-36 |
| Auditoría | 3 | RF-37 a RF-39 |
| **Total** | **39** | |

---

## 4. Requisitos No Funcionales

Los requisitos no funcionales se clasifican según el atributo de calidad que impactan.

### 4.1 Usabilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-01 | La interfaz debe ser intuitiva y no requerir capacitación previa para operaciones básicas. | Media |
| RNF-02 | Los mensajes de error deben ser claros y en español. | Media |
| RNF-03 | La navegación debe ser consistente en todas las ventanas. | Media |
| RNF-04 | La interfaz debe ser funcional con teclado y ratón. | Baja |

### 4.2 Rendimiento

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-05 | El login debe ejecutarse en menos de 2 segundos. | Media |
| RNF-06 | Las consultas de listado deben ejecutarse en menos de 1 segundo. | Media |
| RNF-07 | La generación de reportes PDF debe completarse en menos de 5 segundos. | Baja |

### 4.3 Seguridad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-08 | Las contraseñas deben almacenarse con hash bcrypt (12 rounds), nunca en texto plano. | Alta |
| RNF-09 | El sistema debe usar roles para controlar el acceso a funcionalidades. | Alta |
| RNF-10 | Las credenciales de la BD deben gestionarse mediante variables de entorno (`.env`). | Alta |
| RNF-11 | El sistema debe validar todas las entradas de usuario antes de procesarlas. | Alta |
| RNF-12 | El LOG de auditoría debe permitir rastrear cualquier acción del sistema. | Alta |

### 4.4 Mantenibilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-13 | El código debe seguir la arquitectura en capas (Dominio, Persistencia, Control, Interfaz). | Alta |
| RNF-14 | El código debe usar type hints y docstrings. | Media |
| RNF-15 | El código debe aplicar los principios SOLID. | Media |
| RNF-16 | El código debe estar documentado por capa (`DOC_*_FINAL.txt`). | Media |
| RNF-17 | Debe existir una suite de pruebas unitarias con `pytest`. | Alta |

### 4.5 Portabilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-18 | El sistema debe funcionar 100% offline, sin dependencia de internet. | Alta |
| RNF-19 | El sistema debe ejecutarse en equipos modestos (4 GB RAM, 500 MB disco). | Alta |
| RNF-20 | El sistema debe ser compatible con Windows, Linux y macOS. | Media |
| RNF-21 | El sistema debe usar PostgreSQL como motor de base de datos. | Alta |

### 4.6 Escalabilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-22 | El sistema debe soportar múltiples clientes (al menos 100). | Media |
| RNF-23 | La arquitectura debe permitir migrar a un servicio web en el futuro. | Baja |
| RNF-24 | Los enums de PostgreSQL deben permitir agregar nuevos valores sin modificar tablas. | Baja |

### 4.7 Resumen de requisitos no funcionales

| Atributo | Cantidad de RNF | IDs |
|:---|:---:|:---|
| Usabilidad | 4 | RNF-01 a RNF-04 |
| Rendimiento | 3 | RNF-05 a RNF-07 |
| Seguridad | 5 | RNF-08 a RNF-12 |
| Mantenibilidad | 5 | RNF-13 a RNF-17 |
| Portabilidad | 4 | RNF-18 a RNF-21 |
| Escalabilidad | 3 | RNF-22 a RNF-24 |
| **Total** | **24** | |

---

## 5. Requisitos de Datos y Base de Datos

### 5.1 Entidades del dominio

El sistema maneja **8 entidades principales**:

| # | Entidad | Descripción |
|:---:|:---|:---|
| 1 | **Usuario** | Datos comunes de cualquier usuario (admin o cliente). |
| 2 | **Cliente** | Extiende Usuario con datos biométricos. |
| 3 | **EjercicioCardio** | Catálogo de ejercicios reutilizables. |
| 4 | **Rutina** | Plan de entrenamiento compuesto por ejercicios. |
| 5 | **AsignacionRutina** | Historial de asignaciones de rutinas a clientes. |
| 6 | **SesionEntrenamiento** | Registro de cada sesión realizada. |
| 7 | **ProgresoMensual** | Resumen mensual del progreso. |

### 5.2 Requisitos de datos por entidad

| Entidad | Atributos clave | Restricciones |
|:---|:---|:---|
| **Usuario** | id, nombre, apellido, correo, contraseña_hash, edad, tipo_usuario, fecha_registro | correo único; edad > 0; contraseña hasheada |
| **Cliente** | id_usuario (FK), peso, altura, objetivo, fecha_ingreso, peso_objetivo, genero | peso > 0; altura > 0; peso_objetivo > 0 |
| **EjercicioCardio** | id, nombre, descripción, tipo, duración_minutos, intensidad, calorías_estimadas, creado_por | duración > 0; calorías >= 0; intensidad ∈ enum |
| **Rutina** | id, nombre, descripción, objetivo, nivel, duración_semanas, creado_por, fecha_creacion | duración_semanas > 0; nivel ∈ enum |
| **AsignacionRutina** | id, id_cliente, id_rutina, fecha_asignacion, fecha_finalizacion, estado, observaciones | fecha_finalizacion >= fecha_asignacion; estado ∈ enum |
| **SesionEntrenamiento** | id, id_cliente, id_rutina, fecha, duración_real, intensidad_real, calorías_quemadas, observaciones, completada | duración_real > 0; calorías >= 0 |
| **ProgresoMensual** | id, id_cliente, mes, peso, sesiones_completadas, sesiones_planificadas, porcentaje_cumplimiento | UNIQUE (id_cliente, mes); porcentaje ∈ [0, 100] |

### 5.3 Enums de PostgreSQL

| Enum | Valores | Aplica a |
|:---|:---|:---|
| `tipo_usuario` | cliente, administrador | usuarios.tipo_usuario |
| `nivel_rutina` | BASICO, INTERMEDIO, AVANZADO | rutinas.nivel |
| `intensidad` | BAJA, MEDIA, ALTA | ejercicios.intensidad, sesiones.intensidad_real |
| `estado_asignacion` | ACTIVA, FINALIZADA, CANCELADA | asignaciones_rutina.estado |

### 5.4 Relaciones entre entidades

| Relación | Tipo | Implementación en BD |
|:---|:---|:---|
| Usuario ↔ Cliente | Herencia 1:1 | `clientes.id_usuario` FK a `usuarios.id_usuario` |
| Cliente → AsignacionRutina | Composición 1:N | `ON DELETE CASCADE` |
| Cliente → SesionEntrenamiento | Composición 1:N | `ON DELETE CASCADE` |
| Cliente → ProgresoMensual | Composición 1:N | `ON DELETE CASCADE` |
| Rutina → EjercicioCardio | Agregación N:M | Tabla puente `rutina_ejercicios` |
| AsignacionRutina → Rutina | Asociación N:1 | `ON DELETE RESTRICT` |
| Usuario (Admin) → Rutina | Asociación 1:N | `rutinas.creado_por` con `SET NULL` |
| Usuario (Admin) → Ejercicio | Asociación 1:N | `ejercicios.creado_por` con `SET NULL` |

### 5.5 Requisitos de integridad referencial

| Regla | Aplicación | Justificación |
|:---|:---|:---|
| **CASCADE** | Composición (Cliente → Sesiones, Progreso, Asignaciones) | El cliente es dueño de esos datos; sin él, no existen. |
| **RESTRICT** | Asignación → Rutina | No se puede eliminar una rutina que está asignada. |
| **SET NULL** | Admin → Recursos (Rutinas, Ejercicios) | Los recursos sobreviven al admin que los creó. |
| **UNIQUE** | `usuarios.correo_electronico`, `(progreso_mensual.id_cliente, mes)` | Evitar duplicados. |
| **CHECK** | edad > 0, peso > 0, porcentaje ∈ [0, 100] | Validaciones automáticas. |

### 5.6 Requisitos de rendimiento de la BD

| Requisito | Estrategia |
|:---|:---|
| Búsqueda rápida por correo | Índice en `usuarios.correo_electronico` |
| Búsqueda de rutina activa | Índice parcial `WHERE estado = 'ACTIVA'` |
| Listado de sesiones por cliente | Índice en `sesiones.id_cliente` |
| Búsqueda de progreso por cliente y mes | Índice compuesto en `(id_cliente, mes)` |
| Optimización de consultas complejas | Vistas `vw_clientes_completo` y `vw_rutina_activa_cliente` |

### 5.7 Requisitos de seguridad de datos

| Requisito | Implementación |
|:---|:---|
| Contraseñas hasheadas | `bcrypt` con 12 rounds |
| Credenciales no expuestas | Variables de entorno en `.env` |
| LOG de auditoría | Archivo `logs/LOG_CARDIO.txt` |
| Ausencia de credenciales en el código | `os.getenv()` para todas las credenciales |

### 5.8 Volumen esperado de datos

| Entidad | Volumen estimado | Justificación |
|:---|:---:|:---|
| Usuarios | 100 – 1.000 | Pequeño estudio local |
| Clientes | 100 – 500 | Clientes activos |
| Ejercicios | 20 – 100 | Catálogo del estudio |
| Rutinas | 10 – 50 | Planes de entrenamiento |
| Asignaciones | 100 – 500 | Historial de asignaciones |
| Sesiones | 10.000+ | Registro diario |
| Progreso mensual | 1.000+ | 12 meses × clientes |

---

## 6. Trazabilidad con la Implementación

### 6.1 Requisitos → Casos de Uso → Clases

| Requisito | Caso de Uso | Clase que lo implementa |
|:---|:---|:---|
| RF-01 a RF-05 | CU01, CU02 | `ControlAutenticacion`, `InterfazLogin`, `UsuarioDAO` |
| RF-06 a RF-12 | CU03 | `ControlClientes`, `InterfazGestionClientes`, `ClienteDAO` |
| RF-13 a RF-18 | CU05 | `ControlEjercicios`, `InterfazGestionEjercicios`, `EjercicioDAO` |
| RF-19 a RF-24 | CU04, CU06 | `ControlRutinas`, `InterfazGestionRutinas`, `RutinaDAO`, `AsignacionRutinaDAO` |
| RF-25 a RF-29 | CU09 | `ControlSesiones`, `InterfazRegistroSesion`, `SesionEntrenamientoDAO` |
| RF-30 a RF-34 | CU07, CU10, CU11 | `ControlProgreso`, `InterfazProgreso`, `ProgresoMensualDAO` |
| RF-35 a RF-36 | CU12 | `GeneradorReportesPDF`, `InterfazCliente` |
| RF-37 a RF-39 | — | `ControlBase._registrar_log()` |

### 6.2 Correspondencia de documentos

| Documento | Ubicación | Contenido |
|:---|:---|:---|
| Especificación de requisitos | `docs/REQUISITOS.md` | Este documento |
| Casos de Uso | `docs/diagramas/plantuml/01_casos_de_uso.puml` | 12 casos de uso |
| DCD | `docs/diagramas/plantuml/03_DCD.puml` | Todas las clases |
| Base de Datos | `sql/schema.sql` | 8 tablas + enums |
| Documentación por capa | `docs/DOC_*.txt` | Documentación técnica |

---

## Estado

- **Requisitos funcionales:** 39 identificados e implementados
- **Requisitos no funcionales:** 24 identificados e implementados
- **Necesidades:** 12 identificadas
- **Actores:** 2 (Administrador, Cliente)
- **Correspondencia con la implementación:** Verificada

---

**Última actualización:** Octubre 2026
