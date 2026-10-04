# Changelog

Todos los cambios importantes en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [1.0.1] - 2026-10-03

### Corregido

- Se actualizó la documentación de seguridad para reflejar el uso de bcrypt en
  el almacenamiento de contraseñas.
- Se corrigió la referencia documental del mecanismo de hash de contraseñas.
- Se actualizó la documentación de resultados de pruebas de usabilidad.
- Se documentó la separación entre simulaciones automatizadas y pruebas de
  usabilidad con participantes reales.

### Seguridad

- Se confirmó el uso de bcrypt para el almacenamiento de contraseñas.
- Se documentó la generación de hashes únicos mediante salt.
- Se documentó la validación automatizada de hashes de 60 caracteres.
- Se registraron 8 pruebas automatizadas de seguridad aprobadas mediante
  `run_all_tests.bat`.

---

## [1.0.0] - 2026-09-13

### Agregado

- Sistema completo de gestión de rutinas Cardio-Wellness (backend).
- CRUD de clientes, rutinas, ejercicios y sesiones.
- Autenticación de usuarios con hash de contraseñas mediante bcrypt.
- Sistema de backups automáticos.
- 279 pruebas unitarias y de integración.
- Documentación técnica completa por capa.
- Scripts de utilidad para backup, seed, depuración y mantenimiento.

### Cambiado

- Migración de SQLite a PostgreSQL como alternativa de persistencia.
- Mejora en validaciones de datos.
- Optimización de consultas a base de datos.

### Corregido

- Errores de integridad referencial en asignación de rutinas.
- Problemas de concurrencia en escrituras simultáneas.
- Validaciones de edad e IMC en clientes.

### Seguridad

- Almacenamiento de contraseñas con bcrypt.
- Validación de permisos por tipo de usuario.
- Protección contra inyección SQL mediante consultas parametrizadas.

---

## [0.2.0] - 2026-09-10

### Agregado

- Módulo de progreso de clientes.
- Reportes de sesiones completadas.

### Corregido

- Errores en cálculo de calorías.
- Problemas de persistencia en SQLite.

---

## [0.1.0] - 2026-09-01

### Agregado

- Estructura base del proyecto.
- Modelos de dominio.
- Conexión a base de datos.
- Primeras pruebas unitarias.