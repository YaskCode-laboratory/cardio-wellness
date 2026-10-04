# Documento Final del Proyecto

## 1. Logros Alcanzados

A lo largo del semestre, el equipo desarrolló un sistema funcional de
gestión de rutinas Cardio-Wellness, acompañado de documentación técnica,
diagramas UML, pruebas automatizadas, scripts de base de datos y evidencia
visual de los flujos principales de la aplicación.

### 1.1 Logros técnicos

- **Arquitectura organizada por responsabilidades**: el sistema separa la
  lógica de dominio, persistencia, controladores e interfaz. Además, dispone
  de módulos de servicios y utilidades para funcionalidades transversales,
  como seguridad, generación de reportes, cálculo de calorías y auditoría.

- **Aplicación de patrones y prácticas de diseño**:
  - **Singleton** en `ConexionBD`, utilizado para controlar la instancia de
    conexión a PostgreSQL.
  - **DAO (Data Access Object)** implementado mediante ocho DAOs, aislando el
    acceso a datos de la lógica de negocio.
  - **Fábrica de usuarios** implementada en `FabricaUsuario`, responsable de
    centralizar la creación de instancias `Administrador` y `Cliente`.
  - Separación de responsabilidades entre modelos, controladores, persistencia,
    interfaz, servicios y utilidades.

- **Base de datos PostgreSQL** implementada con:
  - 9 tablas.
  - 4 enums nativos.
  - 3 vistas.
  - 20 índices.
  - Reglas de integridad referencial mediante `ON DELETE CASCADE`,
    `ON DELETE RESTRICT` y `ON DELETE SET NULL`.

- **2.690 pruebas automatizadas aprobadas** mediante `pytest`, incluyendo
  pruebas unitarias, de integración, interfaz, usabilidad, rendimiento y
  carga.

- **Interfaz funcional desarrollada con Tkinter**, con navegación diferenciada
  para los roles de administrador y cliente.

- **Auditoría de actividades relevantes** mediante `ControlBase` y el módulo
  `src.utilidades.logger`. El sistema registra eventos en
  `logs/LOG_CARDIO.txt`, incluyendo autenticación, registro de usuarios,
  creación de rutinas y ejercicios, consultas de progreso, cálculos de
  impacto y generación de reportes.

- **Parámetro META** implementado a partir del peso objetivo del cliente, con
  un indicador visual en verde o rojo según el cumplimiento del objetivo.

- **Seguridad de contraseñas con bcrypt**. El sistema aplica hashing adaptativo
  y utiliza 12 rondas como valor predeterminado, configurable mediante las
  variables de entorno `BCRYPT_ROUNDS` o `ROUNDS`.

- **Generación de reportes PDF** mediante el servicio
  `generador_reportes_pdf.py` y la biblioteca ReportLab.

### 1.2 Logros documentales

- **Diagramas UML versionados** para representar los principales aspectos del
  sistema:
  - Casos de Uso.
  - Diagrama de Objetos.
  - Diagrama de Clases de Diseño (DCD).
  - Diagramas de Secuencia.
  - Diagramas de Colaboración.
  - Diagrama de Componentes.
  - Diagrama de Despliegue.

- **Documentación técnica por componente** mediante archivos de documentación
  en las capas de modelos, persistencia, controladores, interfaz y servicios.

- **Esquema SQL versionado** en `sql/schema.sql`, acompañado por datos de
  demostración, documentación DDL y migraciones de base de datos.

- **Documentación de mantenimiento y operación**, incluyendo bitácora de
  mantenimiento, checklist de producción, configuración de respaldos,
  revisión de seguridad y resultados de pruebas.

- **Capturas de evidencia funcional** para login, gestión de clientes,
  ejercicios, rutinas, sesiones, progreso, META y generación de reportes PDF.

### 1.3 Logros organizacionales

- **Planificación del proyecto** documentada mediante actividades, hitos,
  responsables, cronograma tipo Gantt y análisis de riesgos.

- **Trazabilidad entre documentación e implementación**, mediante la relación
  entre requisitos, diagramas UML, código fuente, scripts de base de datos,
  pruebas y capturas de la aplicación.

- **Distribución de responsabilidades** entre los integrantes del equipo para
  las actividades de análisis, implementación, documentación, pruebas y
  revisión del proyecto.

---

## 2. Dificultades Encontradas y Soluciones

Durante el desarrollo se presentaron desafíos técnicos y de planificación.
Las siguientes dificultades permitieron aplicar prácticas de análisis,
pruebas, documentación y mejora continua.

| # | Dificultad | Solución Adoptada |
|:---:|:---|:---|
| 1 | Curva de aprendizaje de PostgreSQL, especialmente en el uso de enums, vistas, índices y relaciones entre entidades. | Se documentó el esquema SQL, se realizaron pruebas sobre la persistencia y se mantuvieron scripts versionados para facilitar su revisión. |
| 2 | Mantener consistencia entre el DCD, los requisitos y el código fuente. | Se utilizaron los diagramas UML y la documentación técnica como referencia para revisar la estructura de modelos, DAOs, controladores e interfaz. |
| 3 | Manejo de restricciones e integridad de datos en la base de datos. | Se implementaron claves foráneas, restricciones referenciales y validaciones en la capa de persistencia y controladores. |
| 4 | Validación de credenciales y protección de contraseñas. | Se incorporó el uso de bcrypt, validaciones de fortaleza de contraseña y configuración de seguridad mediante variables de entorno. |
| 5 | Control del alcance funcional del sistema. | Se priorizaron los requisitos centrales: autenticación, gestión de clientes, ejercicios, rutinas, sesiones, progreso, META, reportes y auditoría. |
| 6 | Cobertura y tiempo de ejecución de pruebas. | Se construyó una suite automatizada con pytest, incluyendo pruebas unitarias, de integración, de interfaz, usabilidad, carga y rendimiento. |
| 7 | Mantener actualizada la documentación final frente a los cambios de implementación. | Se incorporaron requisitos, planificación, diagramas, resultados de pruebas, scripts SQL, capturas y documentación técnica dentro del repositorio. |

---

## 3. Recomendaciones para Versiones Futuras

El sistema cumple con los requisitos implementados en la versión final, pero
existen oportunidades de evolución técnica y funcional.

### 3.1 Mejoras técnicas sugeridas

- **Migrar la persistencia a una API REST**.

  Beneficio: permitir acceso remoto desde múltiples puestos de trabajo.

  Tecnología sugerida: FastAPI o Flask con PostgreSQL.

- **Implementar el patrón Observer**.

  Beneficio: permitir notificaciones sobre asignación de rutinas, recordatorios
  de entrenamiento o cambios relevantes en el progreso del cliente.

- **Agregar estrategias de negocio configurables**.

  Beneficio: permitir incorporar distintos criterios de recomendación,
  suscripciones, pagos u otros modelos de negocio si el sistema evoluciona.

- **Migrar la interfaz a PyQt o Kivy**.

  Beneficio: ofrecer una experiencia visual más moderna y ampliar las opciones
  de compatibilidad multiplataforma.

- **Autenticación con tokens JWT**.

  Beneficio: reforzar la seguridad en un escenario de API REST, acceso remoto
  o arquitectura distribuida.

- **Pruebas automatizadas de interfaz de usuario**.

  Herramientas sugeridas: PyAutoGUI u otras herramientas compatibles con la
  tecnología de interfaz seleccionada.

  Beneficio: reducir el esfuerzo de pruebas manuales repetitivas.

- **Sistema de respaldo automático**.

  Herramientas sugeridas: `pg_dump`, tareas programadas y políticas de
  conservación de respaldos.

  Beneficio: reducir el riesgo de pérdida de datos ante fallos operativos.

### 3.2 Mejoras de experiencia de usuario

- Modo oscuro o claro configurable.
- Exportación de reportes a Excel además de PDF.
- Búsqueda avanzada con filtros múltiples.
- Dashboard con gráficos de progreso.
- Soporte para múltiples idiomas.
- Mayor personalización de metas, indicadores y recomendaciones de rutina.

### 3.3 Mejoras de arquitectura

- Containerización con Docker para facilitar despliegues reproducibles.
- Separación mediante una API REST si el sistema requiere clientes remotos.
- Integración continua y despliegue continuo mediante GitHub Actions en una
  futura evolución del proyecto.
- Evaluación de una arquitectura distribuida únicamente si el sistema crece
  para atender múltiples estudios, sedes o usuarios concurrentes.

---

## 4. Conclusiones

### 4.1 Síntesis del proyecto

El Sistema de Gestión de Rutinas Cardio-Wellness integra los principales
conceptos abordados durante la asignatura de Ingeniería de Software:
análisis de requisitos, diseño UML, programación orientada a objetos,
persistencia relacional, patrones de diseño, pruebas, documentación,
mantenimiento y trazabilidad.

El proyecto incluye:

- Una estructura de software organizada por responsabilidades.
- Una base de datos PostgreSQL con 9 tablas, 4 enums, 3 vistas, 20 índices y
  reglas de integridad referencial.
- Modelos orientados a objetos para representar usuarios, clientes,
  administradores, ejercicios, rutinas, asignaciones, sesiones y progreso.
- DAOs para encapsular el acceso a PostgreSQL.
- Interfaz Tkinter con flujos diferenciados según el rol.
- Gestión de autenticación y seguridad de contraseñas con bcrypt.
- Auditoría de actividades relevantes mediante archivos de log.
- Cálculo y visualización del progreso respecto al peso objetivo del cliente.
- Generación de reportes PDF.
- 2.690 pruebas automatizadas aprobadas mediante pytest.
- Diagramas UML, scripts SQL, pruebas, documentación técnica y capturas
  versionadas en el repositorio.

### 4.2 Lecciones aprendidas

- Documentar durante el desarrollo facilita la trazabilidad y reduce el
  esfuerzo de consolidación final.
- Los diagramas UML ayudan a mantener coherencia entre análisis, diseño e
  implementación.
- Las pruebas automatizadas permiten detectar regresiones y validar cambios
  antes de la entrega.
- La separación entre modelos, persistencia, controladores e interfaz mejora
  la mantenibilidad del sistema.
- La seguridad debe incorporarse desde el diseño, especialmente en el manejo
  de contraseñas, configuraciones y acceso a la base de datos.
- La documentación de requisitos, planificación, mantenimiento, seguridad y
  pruebas fortalece la calidad y defendibilidad de una entrega académica.

### 4.3 Reflexión final

El proyecto permitió aplicar de forma integrada los conceptos de Ingeniería
de Software: diseñar antes de implementar, estructurar el código por
responsabilidades, persistir datos con reglas de integridad, validar mediante
pruebas, documentar decisiones técnicas y planificar la evolución futura del
sistema.

La entrega final incluye evidencia técnica versionada del proceso de
desarrollo: código fuente, scripts de base de datos, diagramas UML,
documentación, pruebas automatizadas, resultados de validación y capturas de
la aplicación.

---

## 5. Correspondencia con la versión final

Este documento corresponde a la versión final implementada y publicada en la
rama `main` del repositorio. Las funcionalidades, componentes, pruebas,
diagramas, scripts de base de datos y evidencias descritas se fundamentan en
artefactos versionados en dicha rama.

La evidencia técnica del proyecto se sustenta en:

- Código fuente organizado bajo `src/`.
- Scripts y migraciones de base de datos.
- Requisitos y planificación del proyecto.
- Diagramas UML en formato PlantUML y SVG.
- Suite de pruebas automatizadas con pytest.
- Resultados de pruebas de carga, estrés y usabilidad.
- Capturas de los flujos principales de la aplicación.
- Documentación técnica de las capas y componentes del sistema.
- Historial de commits disponible en el repositorio.

No se crearon retrospectivamente Issues, Pull Requests, GitHub Actions ni
otros mecanismos de gestión que no hubieran formado parte del proceso real de
desarrollo. La documentación presenta únicamente funcionalidades, evidencias
y artefactos disponibles en la versión final de `main`.