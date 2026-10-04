# Planificación del Proyecto

## Sistema de Gestión de Rutinas Cardio-Wellness

**Asignatura:** Ingeniería de Software<br>
**Período:** 2026-I<br>
**Equipo:** Emiro Rincón, Juan Perea, Eliam Rodríguez<br>
**Metodología:** Scrum + Kanban (híbrida)<br>
**Última actualización:** Octubre 2026<br>

---

## Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Actividades e Hitos por Fase](#2-actividades-e-hitos-por-fase)
3. [Asignación de Responsabilidades](#3-asignación-de-responsabilidades)
4. [Diagrama de Gantt](#4-diagrama-de-gantt)
5. [Análisis y Gestión de Riesgos](#5-análisis-y-gestión-de-riesgos)
6. [Estados del Tablero Kanban](#6-estados-del-tablero-kanban)
7. [Definition of Done](#7-definition-of-done)
8. [Herramientas de Planificación](#8-herramientas-de-planificación)

---

## 1. Resumen Ejecutivo

El proyecto se desarrolló en **6 fases iterativas** durante un período de
aproximadamente **cinco meses**, aplicando una metodología híbrida
**Scrum + Kanban**.

Cada fase contó con entregables, responsables y fechas de referencia. La
planificación se gestionó mediante un tablero Kanban y una vista Gantt en
Trello, complementada con revisión de código por pares, documentación técnica y
evidencia de pruebas automatizadas.

| Aspecto | Detalle |
|:---|:---|
| **Duración total** | Mayo – Octubre 2026 |
| **Fases** | 6 fases: Fase 0 a Fase 5 |
| **Equipo** | 3 integrantes |
| **Herramienta de planificación** | Trello, Kanban y vista Gantt |
| **Metodología** | Scrum con sprints semanales + Kanban de flujo continuo |
| **Estado general** | Planificación documentada y ejecutada; pruebas de usabilidad humana pendientes |

---

## 2. Actividades e Hitos por Fase

### Fase 0: Estado del Arte y Metodología

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 0.1 | Elaboración de tabla comparativa sobre aplicaciones existentes | Equipo | 07/05 – 10/05 | Identificación de vacíos | Tabla comparativa |
| 0.2 | Definición de requisitos | Equipo | 10/05 – 14/05 | Análisis de necesidades | Requisitos funcionales y no funcionales |
| 0.3 | Planificación del proyecto de software | Equipo; Gantt: Emiro | 14/05 – 26/05 | Análisis de riesgos | Gantt en Trello y análisis de riesgos |
| 0.4 | Selección de metodología | Eliam | 09/06 – 18/06 | Elección de metodología | Documento Scrum + Kanban |

**Entregable de fase:** Documento del Sprint 1 con estado del arte, requisitos y
metodología de trabajo.

---

### Fase 1: Diseño UML y Arquitectura

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 1.1 | Diagrama de Casos de Uso | Juan | 03/06 – 05/07 | Casos de uso definidos | Diagrama de Casos de Uso |
| 1.2 | Diagrama de Clases de Diseño (DCD) | Emiro | 01/07 – 07/07 | Estructura estática definida | DCD en PlantUML |
| 1.3 | Diagramas de Secuencia y Colaboración | Eliam | 08/07 – 15/07 | Comportamiento dinámico definido | Diagramas de interacción |
| 1.4 | Diagrama de Componentes y Despliegue | Juan | 06/07 – 10/07 | Arquitectura física definida | Diagramas de arquitectura |

**Entregable de fase:** Diagramas UML documentados en
[`docs/DIAGRAMAS_UML.md`](docs/DIAGRAMAS_UML.md), con archivos fuente PlantUML
para Casos de Uso, Objetos, Clases de Diseño, Secuencia, Colaboración,
Componentes y Despliegue.

---

### Fase 2: Persistencia y Seguridad

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 2.1 | Diseño y ejecución de base de datos | Emiro | 07/08 – 12/08 | Base de datos funcional | Esquema PostgreSQL ejecutado |
| 2.2 | Implementación de clases DAO | Emiro + Juan | 12/08 – 06/09 | DAOs implementados | DAOs con consultas SQL |
| 2.3 | Revisión de código | Emiro | 12/08 – 07/09 | Cumplimiento POO | Documentación y revisión técnica |
| 2.4 | Configuración de seguridad | Equipo | 13/09 – 03/10 | Hash de contraseñas y variables de entorno | bcrypt, `.env.example` y revisión de seguridad |

**Entregable de fase:** Base de datos PostgreSQL, DAOs funcionales, migraciones,
configuración de credenciales por variables de entorno y documentación de
seguridad con bcrypt.

---

### Fase 3: Motor de Lógica de Rutinas

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 3.1 | Implementación de clases de dominio | Juan | 13/08 – 07/09 | Modelos implementados | Modelos en `src/modelos/` |
| 3.2 | Implementación de clases de control | Juan | 17/08 – 07/09 | Controladores y auditoría | Controladores con LOG |
| 3.3 | Revisión de código | Emiro | 13/08 – 09/09 | Cumplimiento POO | Documentación y revisión |

**Entregable de fase:** Modelos de dominio, controladores, reglas de negocio y
registro de auditoría de acciones críticas.

---

### Fase 4: Interfaz, Progreso y Reportes

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 4.1 | Implementación de clases de interfaz | Eliam | 31/08 – 12/09 | Interfaces Tkinter implementadas | `src/interfaz/` |
| 4.2 | Revisión de código | Emiro | 31/08 – 12/09 | Trazabilidad con DCD | Documentación |
| 4.3 | Integración interfaz-controladores | Eliam + Juan | 13/09 – 19/09 | Sistema integrado | Flujos principales disponibles |
| 4.4 | Progreso y reportes | Equipo | 13/09 – 26/09 | Indicador META y reportes | Progreso visual y reportes PDF |

**Entregable de fase:** Interfaz Tkinter, integración con controladores,
parámetro META con indicadores visuales y reportes disponibles en el sistema.

---

### Fase 5: Calidad y Cierre

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 5.1 | Corrección de pruebas unitarias | Juan | 25/08 – 03/10 | Suite estabilizada | Ejecución de `pytest` y reporte de suite |
| 5.2 | Pruebas de integración | Juan | 09/09 – 24/09 | Integración de DAOs, BD y controladores | Reporte de integración |
| 5.3 | Pruebas funcionales | Juan | 11/09 – 26/09 | Escenarios de usuario automatizados | Documento funcional |
| 5.4 | Pruebas de seguridad | Equipo | 13/09 – 03/10 | Validación de bcrypt, roles e inputs | `docs/REVISION_SEGURIDAD_2026_09.md` |
| 5.5 | Diseño del protocolo de pruebas de usabilidad y aceptación | Equipo | 13/09 – 03/10 | Protocolo documentado | `docs/PLAN_PRUEBAS_USABILIDAD.md` y `docs/RESULTADOS_PRUEBAS_USABILIDAD.md` |
| 5.6 | Documentación del proceso de validación | Juan | 25/08 – 24/09 | Evidencia técnica consolidada | Documentación de validación |
| 5.7 | Redacción del Plan de Mantenimiento | Juan | 01/09 – 03/09 | Plan completo | `docs/BITACORA_MANTENIMIENTO.md` |
| 5.8 | Redacción de conclusiones | Emiro | 18/09 – 20/09 | Documento final | `DOCUMENTACION_FINAL.md` |
| 5.9 | Actualización documental final | Equipo | 03/10 | Consistencia entre código y documentación | Changelog, seguridad, usabilidad, UML y configuración |

**Entregable de fase:** Suite de pruebas, evidencia técnica, plan de
mantenimiento, documentación final, migraciones, configuración de entorno y
protocolo de pruebas de usabilidad.

> **Nota sobre usabilidad:** El protocolo y las métricas de evaluación se
> encuentran documentados. La ejecución con participantes reales permanece
> pendiente y no se presenta como una prueba de aceptación ya completada.

---

## 3. Asignación de Responsabilidades

| Integrante | Rol principal | Áreas de responsabilidad |
|:---|:---|:---|
| **Emiro Rincón** | Arquitecto y Coordinador | DCD, base de datos, DAOs, revisión de código, documentación y conclusiones |
| **Juan Perea** | Backend y QA | Modelos, controladores, pruebas unitarias e integración, plan de mantenimiento |
| **Eliam Rodríguez** | Frontend y Diagramas | Interfaz Tkinter, diagramas de secuencia y colaboración, metodología |

### Distribución de esfuerzo

| Integrante | Fases en las que participó | Peso relativo |
|:---|:---|:---:|
| **Emiro** | 0, 1, 2, 3, 4 y 5 | ~35% |
| **Juan** | 0, 1, 2, 3, 4 y 5 | ~35% |
| **Eliam** | 0, 1, 4 y 5 | ~30% |

La distribución representa una estimación relativa de participación y no
sustituye los registros de tareas individuales gestionados en el tablero.

---

## 4. Diagrama de Gantt

El cronograma se gestionó internamente mediante Trello y una vista Gantt.
La siguiente tabla permite consultar la planificación sin requerir acceso al
tablero externo.

| Fase | Semanas aproximadas | Mayo | Junio | Julio | Agosto | Septiembre | Octubre |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Fase 0** – Estado del Arte y Metodología | 4 | ███ | █ | | | | |
| **Fase 1** – Diseño UML y Arquitectura | 6 | | ███ | ███ | | | |
| **Fase 2** – Persistencia y Seguridad | 4 | | | | ███ | █ | |
| **Fase 3** – Motor Lógico | 4 | | | | ███ | █ | |
| **Fase 4** – Interfaz, Progreso y Reportes | 3 | | | | ███ | ███ | |
| **Fase 5** – Calidad y Cierre | 5 | | | | █ | ███ | █ |

**Evidencia de planificación:** El tablero Kanban y la vista Gantt fueron
gestionados internamente en Trello mediante Placker. La representación tabular
de este documento permite consultar el cronograma sin requerir acceso externo.

---

## 5. Análisis y Gestión de Riesgos

Se identificaron **8 riesgos** clasificados por tipo, con probabilidad, impacto,
estrategia de mitigación y mecanismo de monitoreo.

### 5.1 Matriz de Riesgos

| # | Tipo | Riesgo | Probabilidad | Impacto | Estrategia de Mitigación | Monitoreo |
|:---:|:---|:---|:---:|:---:|:---|:---|
| 1 | **Tecnología** | Se elige una tecnología que el equipo no domina | Media | Alta | Elegir tecnología conocida por al menos un integrante y decidir temprano | Confirmación formal del stack |
| 2 | **Personas** | Cortes de electricidad de un integrante | Alta | Media | Dividir tareas en entregas pequeñas y asignar trabajo asíncrono | Revisión en clase online |
| 3 | **Personas** | Integrante con conocimientos básicos de base de datos | Alta | Media | Aprendizaje guiado y code review obligatorio | Revisión por pares antes de subir cambios |
| 4 | **Organizacional** | El proyecto no avanza más allá del estado del arte | Alta | Alta | Plan de trabajo inmediato y responsables definidos | Monitoreo de hitos semanales |
| 5 | **Organizacional** | Trabajo asíncrono desordenado en WhatsApp | Media | Media | Centralizar decisiones y acuerdos en Trello | Verificación de acuerdos en tarjetas |
| 6 | **Herramientas** | Expiración de Trello Premium | Alta | Media | Copia de seguridad en CSV y rotación de cuentas | Revisión semanal de días restantes |
| 7 | **Requisitos** | Scope creep o funciones no previstas | Media | Media | Aplicar YAGNI y controlar requisitos | Revisión semanal contra Sprint 1 |
| 8 | **Estimación** | Tiempo del semestre insuficiente | Media | Alta | Cronograma realista, trabajo temprano y margen para correcciones | Control de línea de tiempo |

### 5.2 Resumen de Riesgos por Tipo

| Tipo | Cantidad | Riesgos identificados |
|:---|:---:|:---|
| Tecnología | 1 | Dominio de la tecnología |
| Personas | 2 | Cortes de luz y curva de aprendizaje de BD |
| Organizacional | 2 | Estancamiento y comunicación asíncrona |
| Herramientas | 1 | Expiración de Trello Premium |
| Requisitos | 1 | Scope creep |
| Estimación | 1 | Tiempo insuficiente |
| **Total** | **8** | |

### 5.3 Riesgos Materializados y Soluciones Aplicadas

| Riesgo | ¿Se materializó? | Solución aplicada |
|:---|:---:|:---|
| Cortes de electricidad | Sí | Se aplicó Kanban con tareas atómicas y trabajo asíncrono documentado |
| Curva de aprendizaje de PostgreSQL | Sí | Investigación autónoma, code review y documentación progresiva |
| Scope creep | Parcial | Se aplicó YAGNI y se controló el alcance semanalmente |
| Expiración de Trello Premium | Sí | Copia de seguridad en CSV y rotación de cuentas |

---

## 6. Estados del Tablero Kanban

El tablero Kanban utilizó cinco estados de flujo:

| Estado | Descripción | Regla |
|:---|:---|:---|
| **1. Backlog** | Tareas priorizadas | Priorización según hito del sprint |
| **2. En Progreso** | Tareas en desarrollo | WIP máximo de 2 tarjetas por persona |
| **3. En Revisión / QA** | Tareas codificadas | Code review obligatorio |
| **4. Bloqueado** | Tareas con impedimentos | Mover la tarjeta y documentar el bloqueo |
| **5. Terminado** | Tareas finalizadas | Cumplir la Definition of Done |

---

## 7. Definition of Done

Los siguientes criterios definen las condiciones mínimas para considerar una
tarea terminada. Las casillas representan criterios de evaluación y no un
registro global de cumplimiento de todo el proyecto.

- [ ] **Funcionamiento offline:** El código se ejecuta sin requerir conexión a internet
- [ ] **Validación de datos:** Los formularios validan rangos lógicos, como peso mayor que cero y edad mayor que cero
- [ ] **Seguridad básica:** Contraseñas almacenadas con bcrypt
- [ ] **Calidad del código:** Nombres claros, comentarios pertinentes y estructura organizada
- [ ] **Pruebas unitarias:** Al menos el flujo principal se verifica con `pytest`
- [ ] **Revisión por pares:** La tarea es revisada por otro integrante del equipo
- [ ] **Documentación:** El cambio relevante cuenta con documentación o actualización correspondiente

---

## 8. Herramientas de Planificación

| Herramienta | Uso |
|:---|:---|
| **Trello** | Tablero Kanban y planificación de actividades |
| **Placker** | Extensión de vista Gantt para Trello |
| **Google Drive** | Respaldo de CSV y documentos |
| **WhatsApp** | Comunicación asíncrona complementaria |
| **GitHub** | Control de versiones, revisión de cambios y evidencia de implementación |

---

**Última actualización:** Octubre 2026<br>
**Estado:** Planificación documentada y ejecutada. La validación de usabilidad
con participantes reales permanece pendiente, conforme al protocolo registrado
en [`docs/PLAN_PRUEBAS_USABILIDAD.md`](docs/PLAN_PRUEBAS_USABILIDAD.md).