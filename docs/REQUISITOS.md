# Especificación Final de Requisitos

## Sistema de Gestión de Rutinas Cardio-Wellness

**Asignatura:** Ingeniería de Software<br>
**Período:** 2026-I<br>
**Equipo:** Emiro Rincón, Juan Perea, Eliam Rodríguez<br>
**Área de Wellness:** Cardio / Salud / Fitness<br>
**Última actualización:** Octubre 2026<br>

---

## Índice

1. [Análisis de Necesidades](#1-análisis-de-necesidades)
2. [Actores del Sistema](#2-actores-del-sistema)
3. [Requisitos Funcionales](#3-requisitos-funcionales)
4. [Requisitos No Funcionales](#4-requisitos-no-funcionales)
5. [Requisitos de Datos y Base de Datos](#5-requisitos-de-datos-y-base-de-datos)
6. [Trazabilidad con la Implementación](#6-trazabilidad-con-la-implementación)
7. [Estado de Validación](#7-estado-de-validación)

---

## 1. Análisis de Necesidades

### 1.1 Contexto del problema

Durante el análisis comparativo de aplicaciones de wellness, el equipo identificó
las siguientes necesidades:

- Aplicaciones como MyFitnessPal, Strava y Kinetiq se orientan principalmente
  al usuario individual y no cubren necesariamente la gestión local de rutinas
  desde un panel administrativo para un estudio pequeño.
- Plataformas como Virtuagym están orientadas a organizaciones de mayor escala y
  pueden resultar complejas para pequeños estudios de wellness.
- En el análisis comparativo realizado por el equipo, no se identificó una
  solución orientada específicamente a pequeños estudios de wellness que
  integrara gestión de rutinas cardio personalizadas, seguimiento mensual del
  progreso, parámetro META con indicador visual y funcionamiento local sin
  dependencia de internet.

### 1.2 Necesidades identificadas

| # | Necesidad | Descripción | Prioridad |
|:---:|:---|:---|:---:|
| N1 | **Gestión de usuarios con roles** | El sistema debe distinguir entre Administrador y Cliente, con permisos diferenciados. | Alta |
| N2 | **Registro de datos biométricos** | Al registrar un cliente se deben almacenar peso, altura, edad, objetivo de salud y peso objetivo. | Alta |
| N3 | **Catálogo de ejercicios cardio** | El Administrador debe poder crear, editar y eliminar ejercicios clasificados por tipo. | Alta |
| N4 | **Gestión de rutinas** | El Administrador debe poder crear rutinas compuestas por múltiples ejercicios. | Alta |
| N5 | **Asignación de rutinas a clientes** | El Administrador debe poder asignar rutinas a clientes con una duración estimada. | Alta |
| N6 | **Registro de sesiones de entrenamiento** | El Cliente debe poder registrar las sesiones realizadas. | Alta |
| N7 | **Cálculo de progreso mensual** | El sistema debe calcular porcentaje de cumplimiento y variación de peso mensual. | Alta |
| N8 | **Parámetro META con colores** | El sistema debe mostrar visualmente si el cliente alcanzó su objetivo de salud. | Alta |
| N9 | **LOG de auditoría** | Las acciones críticas deben registrarse en un archivo de auditoría. | Alta |
| N10 | **Exportación de reportes a PDF** | El Cliente debe poder generar un reporte consolidado de progreso. | Media |
| N11 | **Funcionamiento offline** | El sistema debe operar sin requerir conexión a internet. | Alta |

### 1.3 Alcance del sistema

**El sistema incluye:**

- Gestión de usuarios con los roles Administrador y Cliente.
- Catálogo de ejercicios cardio, incluyendo LISS, HIIT y Cardio Funcional.
- Gestión de rutinas con agregación de ejercicios.
- Asignación de rutinas con historial y estados.
- Registro de sesiones de entrenamiento.
- Cálculo de progreso mensual y Parámetro META.
- Registro de auditoría de acciones críticas.
- Exportación de reportes de progreso a PDF para el Cliente.
- Uso local de PostgreSQL mediante variables de entorno.

**El sistema no incluye:**

- Pagos o suscripciones.
- Notificaciones en tiempo real.
- Sensores biométricos externos.
- Acceso remoto o despliegue en nube.
- Múltiples idiomas.
- Aplicación móvil.
- API REST pública.

---

## 2. Actores del Sistema

El sistema cuenta con dos actores principales.

### 2.1 Administrador

**Descripción:** Responsable de gestionar los clientes, ejercicios, rutinas y
asignaciones dentro del estudio de wellness.

**Responsabilidades:**

- Gestionar clientes: crear, editar, eliminar y listar.
- Gestionar el catálogo de ejercicios cardio.
- Gestionar rutinas: crear, editar y eliminar.
- Asignar rutinas a clientes.
- Consultar el progreso de los clientes.
- Administrar información operativa del sistema según sus permisos.

**Casos de uso asociados:**

- CU01 — Iniciar Sesión.
- CU02 — Cerrar Sesión.
- CU03 — Registrar Cliente.
- CU04 — Gestionar Rutinas.
- CU05 — Gestionar Ejercicios.
- CU06 — Asignar Rutina.
- CU07 — Ver Progreso de Clientes.

### 2.2 Cliente

**Descripción:** Usuario final que consulta su rutina, registra entrenamientos y
visualiza su progreso.

**Responsabilidades:**

- Consultar su rutina activa.
- Registrar sesiones de entrenamiento.
- Consultar su progreso personal.
- Visualizar el Parámetro META.
- Exportar su reporte de progreso a PDF.

**Casos de uso asociados:**

- CU01 — Iniciar Sesión.
- CU02 — Cerrar Sesión.
- CU08 — Consultar Rutina Activa.
- CU09 — Registrar Sesión de Entrenamiento.
- CU10 — Consultar Progreso Personal.
- CU11 — Ver Parámetro META.
- CU12 — Exportar Reporte PDF.

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
| RF-02 | El sistema debe validar que las credenciales coincidan con las almacenadas mediante bcrypt. | Alta |
| RF-03 | El sistema debe redirigir al panel correspondiente según el rol del usuario. | Alta |
| RF-04 | El sistema debe registrar cada intento de login exitoso o fallido en el LOG. | Alta |
| RF-05 | El sistema debe permitir cerrar sesión. | Alta |

### 3.2 Módulo de Gestión de Clientes

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-06 | El Administrador debe poder registrar un cliente con nombre, apellido, correo, contraseña, edad, peso, altura, objetivo y peso objetivo. | Alta |
| RF-07 | El sistema debe validar que edad, peso y altura tengan valores mayores que cero. | Alta |
| RF-08 | El sistema debe hashear la contraseña antes de almacenarla. | Alta |
| RF-09 | El Administrador debe poder editar los datos de un cliente. | Media |
| RF-10 | El Administrador debe poder eliminar un cliente. | Media |
| RF-11 | El Administrador debe poder listar todos los clientes. | Media |
| RF-12 | El Administrador debe poder buscar un cliente por correo o identificador. | Media |

### 3.3 Módulo de Gestión de Ejercicios

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-13 | El Administrador debe poder crear ejercicios con nombre, descripción, tipo, duración, intensidad y calorías estimadas. | Alta |
| RF-14 | El sistema debe validar que la duración sea mayor que cero y las calorías sean iguales o mayores que cero. | Alta |
| RF-15 | El Administrador debe poder clasificar ejercicios por tipo: LISS, HIIT o Cardio Funcional. | Alta |
| RF-16 | El Administrador debe poder editar ejercicios existentes. | Media |
| RF-17 | El Administrador debe poder eliminar ejercicios que no estén en uso dentro de una rutina. | Media |
| RF-18 | El Administrador debe poder listar y buscar ejercicios. | Media |

### 3.4 Módulo de Gestión de Rutinas

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-19 | El Administrador debe poder crear rutinas con nombre, descripción, objetivo, nivel y duración en semanas. | Alta |
| RF-20 | El Administrador debe poder agregar ejercicios del catálogo a una rutina. | Alta |
| RF-21 | El Administrador debe poder eliminar ejercicios de una rutina. | Media |
| RF-22 | El sistema debe calcular la duración total de una rutina sumando las duraciones de sus ejercicios. | Media |
| RF-23 | El Administrador debe poder asignar una rutina a un cliente con duración estimada. | Alta |
| RF-24 | El sistema debe finalizar la asignación activa anterior antes de crear una nueva asignación. | Alta |

### 3.5 Módulo de Sesiones de Entrenamiento

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-25 | El Cliente debe poder registrar una sesión con duración real, intensidad real y calorías quemadas. | Alta |
| RF-26 | El sistema debe validar que la duración real sea mayor que cero. | Alta |
| RF-27 | El sistema debe asociar la sesión al cliente autenticado y a su fecha de registro. | Alta |
| RF-28 | El Cliente debe poder consultar el historial de sus sesiones. | Media |
| RF-29 | El Administrador debe poder eliminar una sesión cuando sea necesario. | Baja |

### 3.6 Módulo de Progreso y META

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-30 | El sistema debe calcular el porcentaje de cumplimiento mensual mediante `(sesiones_completadas / sesiones_planificadas) × 100`. | Alta |
| RF-31 | El sistema debe calcular la variación de peso comparando el mes actual con el anterior. | Alta |
| RF-32 | El sistema debe mostrar el alcance del peso objetivo con colores: verde para alcanzado y rojo para no alcanzado. | Alta |
| RF-33 | El Cliente debe poder consultar su progreso personal. | Alta |
| RF-34 | El Administrador debe poder consultar el progreso de los clientes. | Alta |

### 3.7 Módulo de Reportes

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-35 | El Cliente debe poder exportar su reporte de progreso a PDF. | Media |
| RF-36 | El reporte debe incluir datos del cliente, resumen de actividad, historial mensual y Parámetro META. | Alta |

### 3.8 Módulo de Auditoría

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RF-37 | El sistema debe registrar acciones críticas en el archivo de auditoría configurado por la aplicación. | Alta |
| RF-38 | Cada registro debe conservar fecha, usuario y actividad realizada. | Alta |
| RF-39 | Las actividades de auditoría deben incluir, como mínimo, LOGIN, CONSULTA, REGISTRO, ELIMINACIÓN y LOGOUT. | Alta |

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

Los requisitos no funcionales se clasifican según el atributo de calidad que
impactan.

### 4.1 Usabilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-01 | La interfaz debe ser intuitiva y no requerir capacitación previa para operaciones básicas. | Media |
| RNF-02 | Los mensajes de error deben ser claros y estar en español. | Media |
| RNF-03 | La navegación debe ser consistente en todas las ventanas. | Media |
| RNF-04 | La interfaz debe ser funcional con teclado y ratón. | Baja |

### 4.2 Rendimiento

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-05 | El login debe ejecutarse en menos de 2 segundos en el entorno objetivo. | Media |
| RNF-06 | Las consultas de listado deben ejecutarse en menos de 1 segundo en el entorno objetivo. | Media |
| RNF-07 | La generación de reportes PDF debe completarse en menos de 5 segundos en condiciones normales de uso. | Baja |

### 4.3 Seguridad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-08 | Las contraseñas deben almacenarse con bcrypt de 12 rounds y nunca en texto plano. | Alta |
| RNF-09 | El sistema debe usar roles para controlar el acceso a funcionalidades. | Alta |
| RNF-10 | Las credenciales de base de datos deben gestionarse mediante variables de entorno en `.env`. | Alta |
| RNF-11 | El sistema debe validar las entradas de usuario antes de procesarlas. | Alta |
| RNF-12 | El LOG de auditoría debe permitir rastrear acciones relevantes del sistema. | Alta |

### 4.4 Mantenibilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-13 | El código debe seguir una arquitectura por capas: Dominio, Persistencia, Control e Interfaz. | Alta |
| RNF-14 | El código debe usar type hints y docstrings cuando corresponda. | Media |
| RNF-15 | El diseño debe aplicar principios SOLID cuando sean pertinentes. | Media |
| RNF-16 | El código debe contar con documentación técnica por capa. | Media |
| RNF-17 | Debe existir una suite de pruebas automatizadas con `pytest`. | Alta |

### 4.5 Portabilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-18 | El sistema debe funcionar localmente sin dependencia de internet. | Alta |
| RNF-19 | El sistema debe ejecutarse en equipos modestos con al menos 4 GB de RAM y 500 MB de espacio disponible. | Alta |
| RNF-20 | El sistema debe diseñarse para ser portable a Windows, Linux y macOS, sujeto a la disponibilidad de Python, Tkinter y PostgreSQL. | Media |
| RNF-21 | El sistema debe utilizar PostgreSQL como motor de base de datos. | Alta |

### 4.6 Escalabilidad

| ID | Requisito | Prioridad |
|:---:|:---|:---:|
| RNF-22 | El sistema debe soportar al menos 100 clientes. | Media |
| RNF-23 | La arquitectura debe permitir una futura migración a un servicio web. | Baja |
| RNF-24 | Los enums de PostgreSQL deben permitir agregar nuevos valores sin rediseñar las tablas existentes. | Baja |

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

### 5.1 Entidades y estructuras del dominio

El sistema maneja **7 entidades principales de dominio** y una tabla puente que
representa la relación de muchos a muchos entre rutinas y ejercicios.

| # | Entidad o estructura | Descripción |
|:---:|:---|:---|
| 1 | **Usuario** | Datos comunes de cualquier usuario, administrador o cliente. |
| 2 | **Cliente** | Extiende la información de Usuario con datos biométricos y objetivos. |
| 3 | **EjercicioCardio** | Catálogo de ejercicios reutilizables. |
| 4 | **Rutina** | Plan de entrenamiento compuesto por ejercicios. |
| 5 | **RutinaEjercicio** | Tabla puente que relaciona ejercicios con rutinas. |
| 6 | **AsignacionRutina** | Historial de asignaciones de rutinas a clientes. |
| 7 | **SesionEntrenamiento** | Registro de cada sesión realizada. |
| 8 | **ProgresoMensual** | Resumen mensual de progreso por cliente. |

### 5.2 Requisitos de datos por entidad

| Entidad | Atributos clave | Restricciones |
|:---|:---|:---|
| **Usuario** | id, nombre, apellido, correo, contraseña_hash, edad, tipo_usuario, fecha_registro | correo único; edad mayor que cero; contraseña hasheada |
| **Cliente** | id_usuario, peso, altura, objetivo, fecha_ingreso, peso_objetivo, genero | peso, altura y peso objetivo mayores que cero |
| **EjercicioCardio** | id, nombre, descripción, tipo, duración_minutos, intensidad, calorías_estimadas, creado_por | duración mayor que cero; calorías mayores o iguales a cero |
| **Rutina** | id, nombre, descripción, objetivo, nivel, duración_semanas, creado_por, fecha_creacion | duración mayor que cero; nivel definido por enum |
| **RutinaEjercicio** | id_rutina, id_ejercicio, orden, repeticiones u observaciones según configuración | relación única entre rutina y ejercicio según reglas de negocio |
| **AsignacionRutina** | id, id_cliente, id_rutina, fecha_asignacion, fecha_finalizacion, estado, observaciones | fecha final mayor o igual a fecha inicial; estado definido por enum |
| **SesionEntrenamiento** | id, id_cliente, id_rutina, fecha, duración_real, intensidad_real, calorías_quemadas, observaciones, completada | duración mayor que cero; calorías mayores o iguales a cero |
| **ProgresoMensual** | id, id_cliente, mes, peso, sesiones_completadas, sesiones_planificadas, porcentaje_cumplimiento | único por cliente y mes; porcentaje entre 0 y 100 |

### 5.3 Enums de PostgreSQL

| Enum | Valores | Aplica a |
|:---|:---|:---|
| `tipo_usuario` | cliente, administrador | usuarios.tipo_usuario |
| `nivel_rutina` | BASICO, INTERMEDIO, AVANZADO | rutinas.nivel |
| `intensidad` | BAJA, MEDIA, ALTA | ejercicios.intensidad y sesiones.intensidad_real |
| `estado_asignacion` | ACTIVA, FINALIZADA, CANCELADA | asignaciones_rutina.estado |

### 5.4 Relaciones entre entidades

| Relación | Tipo | Implementación en base de datos |
|:---|:---|:---|
| Usuario ↔ Cliente | Herencia o extensión 1:1 | `clientes.id_usuario` como FK hacia `usuarios.id_usuario` |
| Cliente → AsignacionRutina | Composición 1:N | `ON DELETE CASCADE` |
| Cliente → SesionEntrenamiento | Composición 1:N | `ON DELETE CASCADE` |
| Cliente → ProgresoMensual | Composición 1:N | `ON DELETE CASCADE` |
| Rutina → EjercicioCardio | Agregación N:M | Tabla puente `rutina_ejercicios` |
| AsignacionRutina → Rutina | Asociación N:1 | `ON DELETE RESTRICT` |
| Usuario Administrador → Rutina | Asociación 1:N | `rutinas.creado_por` con `SET NULL` |
| Usuario Administrador → Ejercicio | Asociación 1:N | `ejercicios.creado_por` con `SET NULL` |

### 5.5 Requisitos de integridad referencial

| Regla | Aplicación | Justificación |
|:---|:---|:---|
| **CASCADE** | Cliente hacia sesiones, progreso y asignaciones | Los registros dependen del cliente propietario |
| **RESTRICT** | Asignación hacia rutina | No se elimina una rutina mientras exista una asignación relacionada |
| **SET NULL** | Administrador hacia rutinas y ejercicios | Los recursos se conservan aunque se elimine el creador |
| **UNIQUE** | Correo de usuario y progreso mensual por cliente y mes | Evitar registros duplicados |
| **CHECK** | Edad, peso, altura y porcentaje de cumplimiento | Validar rangos de valores en la base de datos |

### 5.6 Requisitos de rendimiento de base de datos

| Requisito | Estrategia |
|:---|:---|
| Búsqueda rápida por correo | Índice en `usuarios.correo_electronico` |
| Búsqueda de rutina activa | Índice parcial para asignaciones activas |
| Listado de sesiones por cliente | Índice en identificador de cliente |
| Búsqueda de progreso por cliente y mes | Índice compuesto en cliente y mes |
| Optimización de consultas complejas | Vistas para clientes y rutinas activas |

### 5.7 Requisitos de seguridad de datos

| Requisito | Implementación |
|:---|:---|
| Contraseñas hasheadas | bcrypt con 12 rounds |
| Credenciales no expuestas | Variables de entorno en `.env` y plantilla `.env.example` |
| LOG de auditoría | Registro de acciones críticas mediante logger del sistema |
| Ausencia de credenciales hardcoded | Uso de variables de entorno, incluyendo `DB_PASSWORD` |

### 5.8 Volumen esperado de datos

| Entidad | Volumen estimado | Justificación |
|:---|:---:|:---|
| Usuarios | 100 – 1.000 | Pequeños estudios de wellness |
| Clientes | 100 – 500 | Clientes activos e históricos |
| Ejercicios | 20 – 100 | Catálogo base del estudio |
| Rutinas | 10 – 50 | Planes de entrenamiento disponibles |
| Asignaciones | 100 – 500 | Historial de rutinas asignadas |
| Sesiones | 10.000+ | Registro continuo de actividad |
| Progreso mensual | 1.000+ | Historial por clientes y meses |

---

## 6. Trazabilidad con la Implementación

### 6.1 Requisitos, casos de uso y clases

| Requisito | Caso de Uso | Clases o componentes relacionados |
|:---|:---|:---|
| RF-01 a RF-05 | CU01, CU02 | `ControlAutenticacion`, `InterfazLogin`, `UsuarioDAO` |
| RF-06 a RF-12 | CU03 | `ControlClientes`, `InterfazGestionClientes`, `ClienteDAO` |
| RF-13 a RF-18 | CU05 | `ControlEjercicios`, `InterfazGestionEjercicios`, `EjercicioDAO` |
| RF-19 a RF-24 | CU04, CU06 | `ControlRutinas`, `InterfazGestionRutinas`, `RutinaDAO`, `AsignacionRutinaDAO` |
| RF-25 a RF-29 | CU09 | `ControlSesiones`, `InterfazRegistroSesion`, `SesionEntrenamientoDAO` |
| RF-30 a RF-34 | CU07, CU10, CU11 | `ControlProgreso`, `InterfazProgreso`, `ProgresoMensualDAO` |
| RF-35 a RF-36 | CU12 | `GeneradorReportesPDF`, `InterfazCliente` |
| RF-37 a RF-39 | — | `ControlBase._registrar_log()` o componente equivalente de auditoría |

### 6.2 Correspondencia de documentos

| Documento | Ubicación relativa | Contenido |
|:---|:---|:---|
| Especificación de requisitos | `REQUISITOS.md` | Este documento |
| Índice UML | `DIAGRAMAS_UML.md` | Descripción y acceso a diagramas UML |
| Casos de Uso | `diagramas/plantuml/01_casos_de_uso.puml` | Casos de uso del sistema |
| DCD | `diagramas/plantuml/03_DCD.puml` | Diagrama de clases de diseño |
| Migración PostgreSQL reciente | `../database/migrations/20261003_agregar_peso_objetivo_y_genero_clientes.sql` | Campos de peso objetivo y género para clientes |
| Documentación por capa | `DOC_*_FINAL.txt` | Documentación técnica de capas y principios POO |
| Plan de usabilidad | `PLAN_PRUEBAS_USABILIDAD.md` | Protocolo, tareas y métricas de usabilidad |
| Resultados de usabilidad | `RESULTADOS_PRUEBAS_USABILIDAD.md` | Estado y evidencia técnica complementaria |

---

## 7. Estado de Validación

| Elemento | Estado |
|:---|:---|
| Requisitos funcionales | 39 requisitos identificados y trazados con la implementación |
| Requisitos no funcionales | 24 requisitos definidos; validados parcialmente mediante pruebas técnicas y documentación |
| Seguridad | bcrypt, variables de entorno y controles automatizados documentados |
| Rendimiento PostgreSQL | Evidencia de prueba de estrés disponible en la documentación técnica |
| Diagramas UML | Disponibles en `docs/diagramas/` y documentados en `docs/DIAGRAMAS_UML.md` |
| Configuración de entorno | Plantilla `.env.example` disponible sin credenciales reales |
| Usabilidad con participantes reales | Protocolo documentado; ejecución pendiente |
| Actores principales | 2: Administrador y Cliente |
| Trazabilidad | Documentada entre requisitos, casos de uso, clases y persistencia |

> La implementación de los requisitos se respalda mediante código fuente,
> diagramas UML, pruebas automatizadas y documentación técnica disponible en el
> repositorio. Los indicadores de satisfacción, NPS, tiempos observados y
> completitud de tareas con usuarios reales no se presentan como validados hasta
> ejecutar el protocolo de usabilidad con participantes reales.

---

**Última actualización:** Octubre 2026<br>
**Estado:** Requisitos documentados y trazados con la implementación actual.