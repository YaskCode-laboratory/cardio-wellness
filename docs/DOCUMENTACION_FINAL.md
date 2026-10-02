## 1. Logros Alcanzados

A lo largo del semestre, el equipo cumplió con los objetivos planteados en la asignatura, entregando un sistema funcional, documentado y probado.

### 1.1 Logros técnicos

- **Arquitectura en 4 capas** implementada: Dominio, Persistencia, Control e Interfaz. Cada capa con responsabilidad única y bajo acoplamiento.
- **Aplicación de patrones de diseño**:
  - **Singleton** en `ConexionBD` para garantizar una única conexión a PostgreSQL.
  - **DAO (Data Access Object)** en los 8 DAOs, aislando el acceso a datos.
  - **Inyección de Dependencias** en todos los controladores.
  - **Factory Method** implícito en la jerarquía de usuarios (Cliente/Administrador).
- **Base de datos PostgreSQL normalizada** hasta 3FN, con:
  - 8 tablas, 4 enums nativos, 2 vistas, más de 25 índices.
  - Triggers y reglas de integridad referencial (CASCADE, RESTRICT, SET NULL).
- **2000+ pruebas unitarias pasando** con `pytest`.
- **Interfaz funcional en Tkinter** con navegación completa por roles.
- **LOG de auditoría** registrando todas las acciones críticas del sistema (login, registro, consulta, eliminación, logout).
- **Parámetro META** implementado con indicador visual en colores (verde/rojo) según cumplimiento del objetivo de salud.
- **Seguridad con bcrypt** (12 rounds) para hashing de contraseñas.

### 1.2 Logros documentales

- **7 diagramas UML** completos: Casos de Uso, Objetos, Clases de Diseño (DCD), Secuencia, Colaboración, Componentes y Despliegue.
- **Documentación por capas** (archivos `DOC_*_FINAL.txt` en `docs/`). Archivos que contienen los principios POO presentes.
- **Plan de Mantenimiento** con los 4 tipos: correctivo, adaptativo, perfectivo, preventivo.

### 1.3 Logros organizacionales

- **Gestión de riesgos** con riesgos identificados y mitigados.
- **Trazabilidad completa** entre DCD y código fuente.
- **Trabajo en equipo efectivo** con roles claros y colaboración asíncrona.

---

## 2. Dificultades Encontradas y Soluciones

A lo largo del desarrollo enfrentamos múltiples desafíos técnicos y organizacionales. Estos fueron los más relevantes:

| # | Dificultad | Solución Adoptada |
|:---:|:---|:---|
| 1 | **Curva de aprendizaje de PostgreSQL.** Ningún integrante había trabajado con enums nativos, vistas o índices parciales. | Se dividió el aprendizaje en tareas pequeñas. Investigación autónoma + code review por pares. Documentación progresiva en `docs/`. |
| 2 | **Mantener coherencia entre DCD y código.** Con más de 30 clases, el código tendía a desviarse del diseño. | Revisiones semanales obligatorias. Refactorización continua cuando había desviaciones. Uso del DCD como contrato. |
| 3 | **Cortes de electricidad de un integrante.** Rompían la sincronía del equipo y frenaban el avance. | Aplicación de Kanban con tareas atómicas. Redistribución de cargas. Trabajo asíncrono documentado en Trello. |
| 4 | **Manejo de errores de integridad en la BD.** Un correo duplicado rompía la aplicación con excepciones no controladas. | Captura de `IntegrityError` con códigos `pgcode` específicos (23505, 23503). Transformación a mensajes amigables (`ValueError`). |
| 5 | **Scope creep (agregar funcionalidades no pedidas).** La tentación de agregar features extra retrasaba el alcance base. | Aplicación del principio **YAGNI** ("You Aren't Gonna Need It"). Control semanal estricto de requisitos contra el Sprint 1. |
| 6 | **Subestimación del tiempo de pruebas.** Al inicio se asignó poco tiempo; las pruebas consumieron más de lo previsto. | Se reservó 2 semanas exclusivas para pruebas. Priorización por criticidad (primero unitarias, luego integración, luego funcionales). ||
| 7 | **Trello Premium expiraba.** Se perdía la vista de Gantt. | Copia de seguridad en CSV cada semana. Rotación de cuentas entre integrantes para mantener visibilidad del cronograma. |

---

## 3. Recomendaciones para Versiones Futuras

El sistema cumple con los requisitos actuales, pero existen oportunidades de mejora identificadas por el equipo.

### 3.1 Mejoras técnicas sugeridas

- Migrar la persistencia a una API REST.

        Beneficio: Permitir acceso remoto desde múltiples puestos de trabajo.

        Tecnología: FastAPI o Flask + PostgreSQL.

- Implementar el patrón Observer.

        Beneficio: Notificaciones en tiempo real al cliente (recordatorios de entrenamiento).

        Aplicación: Cuando el entrenador asigne una rutina, el cliente recibe una alerta.

- Agregar el patrón Strategy.

        Beneficio: Soportar diferentes estrategias de negocio (ej. pagos, suscripciones).

        Aplicación: Si el sistema se comercializa.

- Migrar la interfaz a PyQt o Kivy.

        Beneficio: Experiencia visual más moderna y multiplataforma (móvil incluido).

- Autenticación con tokens JWT.

        Beneficio: Mayor seguridad en entornos remotos o distribuidos.

- Pruebas automatizadas de UI.

        Herramientas: pyautogui, selenium.

        Beneficio: Reducir el esfuerzo de pruebas manuales.

- Sistema de respaldo automático.

        Herramientas: pg_dump + cron.

        Beneficio: Evitar pérdida de datos ante fallos.

### 3.2 Mejoras de experiencia de usuario

    Modo oscuro/claro configurable.

    Exportación de reportes a Excel además de PDF.

    Búsqueda avanzada con filtros múltiples.

    Dashboard con gráficos de progreso.

    Soporte para múltiples idiomas.

### 3.3 Mejoras de arquitectura

    Migrar a microservicios si el sistema crece para múltiples estudios.

    Containerización con Docker para despliegue reproducible.

    CI/CD con GitHub Actions para automatizar pruebas y despliegue.

---
  
## 4. Conclusiones
### 4.1 Síntesis del proyecto

El Sistema de Gestión de Rutinas Cardio-Wellness es el resultado de 4 meses de trabajo continuo aplicando los conceptos de Ingeniería de Software enseñados durante el semestre.

El proyecto cumple con:

    Una arquitectura en 4 capas claramente diferenciadas.

    Una base de datos normalizada hasta 3FN con integridad referencial.

    POO aplicada rigurosamente: encapsulamiento, herencia, polimorfismo, composición y agregación.

    Patrones de diseño aplicados y documentados.

    2000+ pruebas unitarias validando cada componente.

    Interfaz funcional con navegación completa.

    LOG de auditoría y Parámetro META cumpliendo requisitos específicos.

    Documentación completa de cada capa y decisión arquitectónica.

### 4.2 Lecciones aprendidas

    Documentar mientras se desarrolla ahorra tiempo a largo plazo.

    El DCD es un contrato: si se desvía el código, hay que corregir uno u otro.

    La comunicación asíncrona es clave en equipos con horarios diversos.

    No subestimar el tiempo de pruebas: es una inversión, no un gasto.

    Aplicar YAGNI mantiene el alcance bajo control.

    Los patrones de diseño resuelven problemas reales, no son adornos teóricos.

    La trazabilidad (DCD → código → BD) demuestra calidad del proceso.

### 4.3 Reflexión final

    "Este proyecto nos permitió comprender que la Ingeniería de Software no se limita a escribir código funcional: es la disciplina de diseñar con criterio, documentar con rigor, validar con evidencia y mantener con visión de futuro. Cada decisión arquitectónica, cada patrón aplicado y cada prueba escrita reflejan el aprendizaje de un semestre completo."

El equipo entrega no solo un sistema funcional, sino la evidencia completa del proceso: diseño, planificación, implementación, pruebas, documentación y mejora continua.
