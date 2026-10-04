# Revisión de Seguridad y Backups — Cardio-Wellness

**Versión del documento:** 1.1
**Fecha de revisión inicial:** 2026-09-13
**Última actualización:** 2026-10-03
**Responsable:** Equipo de desarrollo
**Evidencia técnica:** Ejecución de `run_all_tests.bat`

---

## 1. Propósito

Este documento registra las verificaciones de seguridad, credenciales, acceso,
backups y restauración realizadas sobre Cardio-Wellness.

La evidencia técnica de seguridad fue obtenida mediante la ejecución de:

```text
run_all_tests.bat
```

La revisión documenta controles básicos evaluados por pruebas automatizadas.
No sustituye una auditoría de seguridad profesional, una prueba de penetración
de alcance completo ni una certificación formal de seguridad.

---

## 2. Validación de acceso y credenciales

### 2.1 Verificaciones realizadas

| Control | Estado | Evidencia o detalle |
|---|---|---|
| Hash de contraseñas con bcrypt | ✅ Verificado | La implementación utiliza bcrypt |
| Salt único por generación | ✅ Verificado | El test confirmó hash único por generación |
| Longitud de hash bcrypt | ✅ Verificado | Hash de 60 caracteres |
| Validación de contraseñas | ✅ Verificado | Prueba automatizada aprobada |
| Protección contra inyección SQL | ✅ Verificado | Uso de consultas parametrizadas con `psycopg2` |
| Protección frente a XSS | ✅ Verificado | Se evaluaron 4 payloads automatizados |
| Validación de datos de entrada | ✅ Verificado | Validación de datos de cliente aprobada |
| Control de acceso a datos | ✅ Verificado | DAOs y controles de acceso evaluados |
| Contraseñas en texto plano | ✅ No detectadas | El script verificó que no existen contraseñas en texto plano |
| Variable de seguridad | ✅ Detectada | Variable `DB_PASSWORD` configurada |
| Secretos hardcoded | ✅ No detectados por el script | El test no encontró secretos hardcoded |
| Archivo `.env` incluido en `.gitignore` | ⏳ Pendiente de validar | Requiere comprobación con Git |

### 2.2 Protección de contraseñas

Las contraseñas se almacenan utilizando **bcrypt**, un algoritmo destinado al
almacenamiento seguro de contraseñas. La prueba automatizada confirmó que los hashes generados
son únicos por generación mediante salt y que tienen una longitud de 60
caracteres.

No deben almacenarse contraseñas en texto plano ni reemplazarse bcrypt por otro
mecanismo sin una revisión técnica y de seguridad formal.

### 2.3 Resultado de pruebas automatizadas de seguridad

La ejecución de `run_all_tests.bat` registró los siguientes resultados:

| Métrica | Resultado |
|---|---:|
| Pruebas de seguridad ejecutadas | 8 |
| Pruebas aprobadas | 8 |
| Pruebas fallidas | 0 |
| Vulnerabilidades detectadas por el script | 0 |
| Reporte generado | `reporte_seguridad.txt` |

Los controles evaluados incluyeron:

- Validación de contraseñas.
- Generación de hashes bcrypt con salt.
- Uso de consultas parametrizadas frente a inyección SQL.
- Pruebas automatizadas frente a payloads XSS.
- Validación de datos de entrada.
- Controles de acceso a datos.
- Protección de datos sensibles.
- Configuración de seguridad y detección de secretos hardcoded.

### 2.4 Estado

✅ **Los controles básicos de seguridad evaluados finalizaron correctamente en
las pruebas automatizadas ejecutadas.**

El resultado indica que no se detectaron vulnerabilidades en los casos incluidos
en el script. No garantiza la ausencia total de vulnerabilidades fuera de los
escenarios evaluados.

---

## 3. Validación de backups

### 3.1 Verificaciones realizadas

| Control | Estado | Detalle |
|---|---|---|
| Script de backup automático | ✅ Verificado | Existe `scripts/backup_automatico.py` |
| Documentación de programación de backups | ✅ Verificada | Existe `docs/PROGRAMAR_BACKUPS.md` |
| Documentación de rollback | ✅ Verificada | Existe `docs/CHECKLIST_PRODUCCION.md` |
| Historial de cambios | ✅ Verificado | Existe `CHANGELOG.md` |
| Directorio actual de backups | ⏳ Pendiente de validar | La carpeta `backups/` no estaba presente durante la verificación |
| Existencia de backups recientes | ⏳ Pendiente de validar | No se encontraron archivos en `backups/` porque la carpeta no existe |
| Retención de los últimos 7 backups | ⏳ Pendiente de validar | Debe confirmarse mediante revisión del script o ejecución real |
| Exportación de tablas PostgreSQL | ⏳ Pendiente de validar | Debe confirmarse mediante un archivo de backup generado |
| Restauración de backup | ⏳ Pendiente de validar | Debe probarse en una base de datos temporal |

### 3.2 Estado actual

El proyecto dispone de un script de backup automático y documentación de apoyo
para programación de backups y rollback.

Durante la verificación realizada el 2026-10-03, no se encontró la carpeta:

```text
backups/
```

en la raíz del proyecto.

Por tanto, no se declara todavía la existencia actual de archivos de respaldo,
la conservación efectiva de siete backups ni la restauración validada de una
copia de seguridad.

La ausencia de la carpeta puede deberse a que el script no se ha ejecutado
recientemente, que crea la carpeta únicamente durante su ejecución o que utiliza
una ruta de salida distinta. Esto debe comprobarse antes de declarar el control
como completamente validado.

### 3.3 Acciones pendientes

- Ejecutar `scripts/backup_automatico.py`.
- Identificar la ruta de salida configurada por el script.
- Confirmar la creación de un archivo de backup.
- Validar el formato generado.
- Confirmar cuántos backups conserva el mecanismo.
- Probar una restauración controlada en una base de datos temporal.
- Registrar la fecha, archivo y resultado de la restauración.

### 3.4 Estado

✅ **El script y la documentación de backup existen.**

⏳ **La generación actual de archivos, la ubicación de salida, la retención y la
restauración requieren validación mediante ejecución real.**

---

## 4. Procedimiento de restauración

### 4.1 Documentación disponible

| Documento o archivo | Estado | Propósito |
|---|---|---|
| `scripts/backup_automatico.py` | ✅ Existe | Generación de backups |
| `docs/PROGRAMAR_BACKUPS.md` | ✅ Existe | Instrucciones de programación de backups |
| `docs/CHECKLIST_PRODUCCION.md` | ✅ Existe | Procedimiento de rollback en producción |
| `CHANGELOG.md` | ✅ Existe | Historial de cambios y versiones |

### 4.2 Procedimiento pendiente de validación

Antes de registrar un procedimiento definitivo, se debe identificar el formato
real generado por `scripts/backup_automatico.py`.

Si el script genera un archivo SQL plano con extensión `.sql`, el procedimiento
de restauración deberá documentarse utilizando el comando correspondiente para
ejecutar dicho script SQL en PostgreSQL.

Si el script genera un backup en formato archivo de PostgreSQL, se deberá
documentar el procedimiento compatible con ese formato.

La restauración debe realizarse primero en una base de datos temporal, nunca
directamente sobre una base de datos productiva.

### 4.3 Verificaciones posteriores a una restauración

Después de realizar una restauración de prueba, se deberá comprobar:

- Que la base de datos acepta conexiones.
- Que las tablas requeridas existen.
- Que los datos esperados están disponibles.
- Que las contraseñas continúan almacenadas como hashes bcrypt.
- Que las pruebas de conexión a base de datos finalizan correctamente.
- Que no se ha modificado la base de datos productiva.
- Que se registra evidencia de la restauración realizada.

### 4.4 Estado

⏳ **Procedimiento documentado parcialmente; restauración real pendiente de
ejecución y validación.**

---

## 5. Recomendaciones

### 5.1 Corto plazo

- [ ] Ejecutar `scripts/backup_automatico.py` y comprobar la ruta de salida.
- [ ] Verificar la creación de la carpeta de backups si corresponde.
- [ ] Registrar un backup real generado por el script.
- [ ] Confirmar la política de retención de backups.
- [ ] Probar la restauración en una base de datos temporal.
- [ ] Verificar que `.env` esté excluido del repositorio mediante `.gitignore`.
- [ ] Mantener los archivos de backup fuera del repositorio Git.
- [ ] Configurar alertas o notificaciones ante fallos de backup.
- [ ] Cifrar las copias de seguridad antes de almacenarlas en servicios externos.

### 5.2 Mediano y largo plazo

- [ ] Implementar autenticación de dos factores para perfiles administrativos.
- [ ] Registrar auditoría de accesos y acciones sensibles.
- [ ] Definir una política de rotación de credenciales.
- [ ] Revisar los permisos mínimos de usuarios de base de datos.
- [ ] Mantener actualizadas las dependencias del proyecto.
- [ ] Realizar una revisión de seguridad manual de mayor alcance.
- [ ] Definir una política de retención y eliminación segura de backups.
- [ ] Ejecutar revisiones de seguridad después de cambios relevantes en
  autenticación, base de datos o despliegue.

---

## 6. Limitaciones de la revisión

Esta revisión presenta las siguientes limitaciones:

- Las pruebas automatizadas de seguridad cubren únicamente los 8 escenarios
  implementados en el script ejecutado.
- La ausencia de vulnerabilidades detectadas por un script no garantiza la
  ausencia total de vulnerabilidades.
- La protección contra XSS se evaluó con 4 payloads automatizados, no con todos
  los vectores posibles.
- La protección contra inyección SQL depende de que futuras modificaciones
  mantengan el uso de consultas parametrizadas.
- La detección de secretos hardcoded depende de la cobertura del script.
- La exclusión de `.env` mediante `.gitignore` está pendiente de verificación.
- La carpeta `backups/` no se encontró durante la verificación del 2026-10-03.
- La generación de archivos de backup, su retención y su restauración no han
  sido confirmadas durante esta revisión.
- La configuración de seguridad también depende del servidor, PostgreSQL,
  sistema operativo, red, permisos y proceso de despliegue.

---

## 7. Conclusión

**Estado general:** ✅ **Controles básicos de seguridad automatizados evaluados
correctamente.**

Cardio-Wellness utiliza bcrypt para el almacenamiento de contraseñas. Las
pruebas automatizadas verificaron la generación de hashes únicos con salt y una
longitud de hash de 60 caracteres.

La ejecución de `run_all_tests.bat` registró 8 pruebas automatizadas de
seguridad aprobadas, 0 pruebas fallidas y 0 vulnerabilidades detectadas por el
script en los escenarios evaluados.

El proyecto cuenta con un script de backup y documentación relacionada. Sin
embargo, durante la verificación actual no se encontró la carpeta `backups/`,
por lo que la generación de backups, la retención de archivos y la restauración
controlada se mantienen como aspectos pendientes de validación.

**Próxima revisión recomendada:** 2027-03-13
**Periodicidad recomendada:** Semestral o después de cambios relevantes de
seguridad, autenticación, base de datos o despliegue.

---

**Firma:** _________________________
**Fecha:** _________________________
