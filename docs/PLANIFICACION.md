# Planificación del Proyecto

## Sistema de Gestión de Rutinas Cardio-Wellness

**Asignatura:** Ingeniería de Software
**Período:** 2026-I  
**Equipo:** Emiro Rincón, Juan Perea, Eliam Rodríguez  
**Metodología:** Scrum + Kanban (híbrida)

---

## Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Actividades e Hitos por Fase](#2-actividades-e-hitos-por-fase)
3. [Asignación de Responsabilidades](#3-asignación-de-responsabilidades)
4. [Diagrama de Gantt](#4-diagrama-de-gantt)
5. [Análisis y Gestión de Riesgos](#5-análisis-y-gestión-de-riesgos)
6. [Estados del Tablero Kanban](#6-estados-del-tablero-kanban)
7. [Definition of Done](#7-definition-of-done)

---

## 1. Resumen Ejecutivo

El proyecto se desarrolló en **6 fases iterativas** durante un período de aproximadamente **4 meses**, aplicando una metodología híbrida **Scrum + Kanban**. Cada fase tuvo entregables concretos, responsables definidos y fechas específicas, gestionados a través de **Trello** y validados con **code review** por pares.

| Aspecto | Detalle |
|:---|:---|
| **Duración total** | Mayo – Septiembre 2026 |
| **Fases** | 6 (Fase 0 a Fase 5) |
| **Equipo** | 3 integrantes |
| **Herramienta de planificación** | Trello (Gantt + Kanban) |
| **Metodología** | Scrum (sprints semanales) + Kanban (flujo continuo) |

---

## 2. Actividades e Hitos por Fase

### FASE 0: Estado del Arte y Metodología

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 0.1 | Elaboración de tabla comparativa sobre aplicaciones existentes | Equipo | 07/05 – 10/05 | Identificación de vacíos | Tabla comparativa |
| 0.2 | Definición de requisitos | Equipo | 10/05 – 14/05 | Análisis de necesidades | Requisitos funcionales y no funcionales |
| 0.3 | Planificación del proyecto de software | Equipo (Gantt: Emiro) | 14/05 – 26/05 | Análisis de riesgos | Gantt en Trello + Análisis de riesgos |
| 0.4 | Selección de metodología | Eliam | 09/06 – 18/06 | Elección de metodología | Documento Scrum + Kanban |

**Entregable de fase:** Documento del Sprint 1 (Estado del Arte, Requisitos, Metodología).

---

### FASE 1: Diseño UML y Arquitectura

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 1.1 | Diagrama de Casos de Uso | Juan | 03/06 – 05/07 | Casos de uso | Diagrama de Casos de Uso |
| 1.2 | Diagrama de Clases de Diseño (DCD) | Emiro | 01/07 – 07/07 | Estructura estática definida | DCD en PlantUML |
| 1.3 | Diagramas de Secuencia y Colaboración | Eliam | 08/07 – 15/07 | Comportamiento dinámico | Diagramas de interacción |
| 1.4 | Diagrama de Componentes y Despliegue | Juan | 06/07 – 10/07 | Arquitectura física | Diagramas de arquitectura |

**Entregable de fase:** Todos los diagramas UML (Sprints 4, 5, 6, 7).

---

### FASE 2: Persistencia y Seguridad

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 2.1 | Diseño y ejecución de base de datos | Emiro | 07/08 – 12/08 | BD funcional | `schema.sql` ejecutado |
| 2.2 | Implementación de Clases DAO | Emiro + Juan | 12/08 – 06/09 | 8 DAOs completos | DAOs con SQL real |
| 2.3 | Revisión de código | Emiro | 12/08 – 07/09 | Cumplimiento POO | Documentación y revisión |

**Entregable de fase:** Base de datos PostgreSQL + 8 DAOs funcionales + Gestor de seguridad con bcrypt.

---

### FASE 3: Motor de Lógica de Rutinas

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 3.1 | Implementación de Clases de Dominio | Juan | 13/08 – 07/09 | 8 modelos completos | Modelos en `src/modelos/` |
| 3.2 | Implementación de Clases de Control | Juan | 17/08 – 07/09 | 6 controladores + LOG | Controladores con auditoría |
| 3.3 | Revisión de código | Emiro | 13/08 – 09/09 | Cumplimiento POO | Documentación y revisión |

**Entregable de fase:** Modelos + Controladores + Reglas de negocio + LOG de auditoría.

---

### FASE 4: Interfaz, Progreso y Reportes

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 4.1 | Implementación de Clases de Interfaz | Eliam | 31/08 – 12/09 | 9 interfaces Tkinter | `src/interfaz/` completo |
| 4.2 | Revisión de código | Emiro | 31/08 – 12/09 | Trazabilidad con DCD | Documentación |
| 4.3 | Integración Interfaz-Controladores | Eliam + Juan | 13/09 – 19/09 | Sistema funcional | Sistema integrado |

**Entregable de fase:** Interfaz Tkinter completa + Parámetro META con colores + Reportes PDF.

---

### FASE 5: Calidad y Cierre

| ID | Actividad | Responsable(s) | Fecha | Hito | Entregable |
|:---:|:---|:---|:---:|:---|:---|
| 5.1 | Corrección de pruebas unitarias | Juan | 25/08 – 03/10 | Suite estable | `pytest` ejecutado |
| 5.2 | Pruebas de integración | Juan | 09/09 – 24/09 | DAOs + BD + Controladores | Reporte de integración |
| 5.3 | Pruebas funcionales | Juan | 11/09 – 26/09 | Escenarios de usuario | Documento funcional |
| 5.4 | Pruebas de seguridad | Equipo | 13/09 – 26/09 | bcrypt + roles | Documento de seguridad |
| 5.5 | Pruebas de usabilidad y aceptación | Equipo | 13/09 – 26/09 | Usuario externo | `PLAN_PRUEBAS_USABILIDAD.md` |
| 5.6 | Documentar proceso de validación | Juan | 25/08 – 24/09 | Documentación| Documento de validación |
| 5.7 | Redacción del Plan de Mantenimiento | Juan | 01/09 – 03/09 | Plan completo | `docs/BITACORA_MANTENIMIENTO.md` |
| 5.8 | Redacción de Conclusiones | Emiro | 18/09 – 20/09 | Documento final | `DOCUMENTACION_FINAL.md` |

**Entregable de fase:** Suite de pruebas + Plan de Mantenimiento + Documentación final.

---

## 3. Asignación de Responsabilidades

| Integrante | Rol principal | Áreas de responsabilidad |
|:---|:---|:---|
| **Emiro Rincón** | Arquitecto y Coordinador | DCD, Base de Datos, DAOs, Revisión de código, Documentación, Conclusiones |
| **Juan Perea** | Backend y QA | Modelos, Controladores, Pruebas unitarias/integración, Plan de Mantenimiento |
| **Eliam Rodríguez** | Frontend y Diagramas | Interfaz Tkinter, Diagramas de Secuencia/Colaboración, Metodología |

### Distribución de esfuerzo

| Integrante | Fases en las que participó | Peso relativo |
|:---|:---|:---:|
| **Emiro** | 0, 1, 2, 3, 4, 5 | ~35% |
| **Juan** | 0, 1, 2, 3, 4, 5 | ~35% |
| **Eliam** | 0, 1, 4, 5 | ~30% |

---

## 4. Diagrama de Gantt

El diagrama de Gantt se gestionó en **Trello** mediante la extensión Placker. A continuación, la representación tabular del cronograma:

| Fase | Semanas | Mayo | Junio | Julio | Agosto | Septiembre |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Fase 0** – Estado del Arte | 4 | ███ | | | | |
| **Fase 1** – Diseño UML | 6 | | ███ | ███ | | |
| **Fase 2** – Persistencia | 4 | | | | ███ | |
| **Fase 3** – Motor Lógico | 4 | | | | ███ | |
| **Fase 4** – Interfaz | 3 | | | | ███ | ███ |
| **Fase 5** – Calidad y Cierre | 5 | | | | | ███ |

**Enlace al Gantt:** [Trello – Gantt Cardio-Wellness](https://trello.com/b/6ab2fb58081962ee609885fc)

---

# 5. Análisis y Gestión de Riesgos

Se identificaron **8 riesgos** clasificados por tipo, con su probabilidad, impacto, estrategia de mitigación y plan de monitoreo.

### 5.1 Matriz de Riesgos

| # | Tipo | Riesgo | Probabilidad | Impacto | Estrategia de Mitigación | Monitoreo |
|:---:|:---|:---|:---:|:---:|:---|:---|
| 1 | **Tecnología** | Se elige una tecnología que el equipo no domina | Media | Alta | Elegir tecnología conocida por al menos un integrante. Decidir temprano. | Confirmación formal del stack |
| 2 | **Personas** | Cortes de electricidad de un integrante | Alta | Media | Asignar tareas que pueda adelantar de día. Dividir en entregas pequeñas. | Revisión en clase online (miércoles y viernes) |
| 3 | **Personas** | Integrante con conocimientos básicos de BD | Alta | Media | Tareas de aprendizaje guiado. Code review obligatorio. | Revisión por pares antes de subir al repo |
| 4 | **Organizacional** | El proyecto no avanza más allá del estado del arte | Alta | Alta | Plan de trabajo inmediato. Asignar responsables. | Monitoreo de hitos semanales en Trello |
| 5 | **Organizacional** | Trabajo asíncrono desordenado en WhatsApp | Media | Media | Centralizar decisiones en Trello. Registrar acuerdos por escrito. | Verificación de acuerdos en tarjetas |
| 6 | **Herramientas** | Expiración de Trello Premium | Alta | Media | Copia de seguridad en CSV. Rotación de cuentas. | Revisión semanal de días restantes |
| 7 | **Requisitos** | Scope creep (agregar funciones no previstas) | Media | Media | Apegarse estrictamente a los requisitos. Aplicar YAGNI. | Revisión semanal contra el Sprint 1 |
| 8 | **Estimación** | Tiempo del semestre insuficiente | Media | Alta | Cronograma realista. Repartir tareas temprano. Dejar margen para correcciones. | Control de línea de tiempo en Gantt |

### 5.2 Resumen de Riesgos por Tipo

| Tipo | Cantidad | Riesgos identificados |
|:---|:---:|:---|
| Tecnología | 1 | Dominio de la tecnología |
| Personas | 2 | Cortes de luz, curva de aprendizaje de BD |
| Organizacional | 2 | Estancamiento, comunicación asíncrona |
| Herramientas | 1 | Expiración de Trello Premium |
| Requisitos | 1 | Scope creep |
| Estimación | 1 | Tiempo insuficiente |
| **Total** | **8** | |

### 5.3 Riesgos Materializados y Soluciones Aplicadas

| Riesgo | ¿Se materializó? | Solución aplicada |
|:---|:---:|:---|
| Cortes de electricidad | Sí | Se aplicó Kanban con tareas atómicas. Trabajo asíncrono documentado. |
| Curva de aprendizaje de PostgreSQL | Sí | Investigación autónoma + code review. Documentación progresiva. |
| Scope creep | Parcial | Se aplicó YAGNI. Se controló el alcance semanalmente. |
| Expiración de Trello Premium | Sí | Copia de seguridad en CSV + rotación de cuentas. |

---

## 6. Estados del Tablero Kanban

El tablero Kanban en Trello tuvo **5 estados** con reglas de flujo:

| Estado | Descripción | Regla |
|:---|:---|:---|
| **1. Backlog** | Tareas priorizadas | Priorización según hito del Sprint |
| **2. En Progreso** | Tareas en desarrollo | WIP: máximo 2 tarjetas por persona |
| **3. En Revisión / QA** | Tareas codificadas | Code review obligatorio |
| **4. Bloqueado** | Tareas con impedimentos | Protocolo: mover y comentar el bloqueo |
| **5. Terminado** | Tareas finalizadas | Cumplir con la Definition of Done |

---

## 7. Definition of Done

Una tarea se considera completada solo si cumple **todos** estos criterios:

- [ ] **Funcionamiento offline:** El código se ejecuta sin requerir conexión a internet.
- [ ] **Validación de datos:** Los formularios validan rangos lógicos (peso > 0, edad > 0, etc.).
- [ ] **Seguridad básica:** Contraseñas almacenadas con hash bcrypt.
- [ ] **Calidad del código:** Nombres claros, comentarios, estructura organizada.
- [ ] **Pruebas unitarias:** Al menos el flujo principal verificado con `pytest`.
- [ ] **Revisión por pares:** Aprobada por otro integrante del equipo.

---

## Herramientas utilizadas para la planificación

| Herramienta | Uso |
|:---|:---|
| **Trello** | Tablero Kanban y vista Gantt |
| **Placker** | Extensión para Gantt en Trello |
| **Google Drive** | Respaldo de CSV y documentos |
| **WhatsApp** | Comunicación asíncrona (complementaria) |

---

**Última actualización:** Octubre 2026  
**Estado:** Planificación completa y ejecutada
