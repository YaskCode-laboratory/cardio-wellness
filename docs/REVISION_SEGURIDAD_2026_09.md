# RevisiÃ³n de Seguridad y Backups â€” Cardio-Wellness

**VersiÃ³n del documento:** 1.1
**Fecha de revisiÃ³n inicial:** 2026-09-13
**Ãšltima actualizaciÃ³n:** 2026-10-03
**Responsable:** Equipo de desarrollo
**Evidencia tÃ©cnica:** EjecuciÃ³n de `run_all_tests.bat`

---

## 1. PropÃ³sito

Este documento registra las verificaciones de seguridad, credenciales, acceso,
backups y restauraciÃ³n realizadas sobre Cardio-Wellness.

La evidencia tÃ©cnica de seguridad fue obtenida mediante la ejecuciÃ³n de:

```text
run_all_tests.bat
```

La revisiÃ³n documenta controles bÃ¡sicos evaluados por pruebas automatizadas.
No sustituye una auditorÃ­a de seguridad profesional, una prueba de penetraciÃ³n
de alcance completo ni una certificaciÃ³n formal de seguridad.

---

## 2. ValidaciÃ³n de acceso y credenciales

### 2.1 Verificaciones realizadas

| Control | Estado | Evidencia o detalle |
|---|---|---|
| Hash de contraseÃ±as con bcrypt | âœ… Verificado | La implementaciÃ³n utiliza bcrypt |
| Salt Ãºnico por generaciÃ³n | âœ… Verificado | El test confirmÃ³ hash Ãºnico por generaciÃ³n |
| Longitud de hash bcrypt | âœ… Verificado | Hash de 60 caracteres |
| ValidaciÃ³n de contraseÃ±as | âœ… Verificado | Prueba automatizada aprobada |
| ProtecciÃ³n contra inyecciÃ³n SQL | âœ… Verificado | Uso de consultas parametrizadas con `psycopg2` |
| ProtecciÃ³n frente a XSS | âœ… Verificado | Se evaluaron 4 payloads automatizados |
| ValidaciÃ³n de datos de entrada | âœ… Verificado | ValidaciÃ³n de datos de cliente aprobada |
| Control de acceso a datos | âœ… Verificado | DAOs y controles de acceso evaluados |
| ContraseÃ±as en texto plano | âœ… No detectadas | El script verificÃ³ que no existen contraseÃ±as en texto plano |
| Variable de seguridad | âœ… Detectada | Variable `DB_PASSWORD` configurada |
| Secretos hardcoded | âœ… No detectados por el script | El test no encontrÃ³ secretos hardcoded |
| Archivo `.env` incluido en `.gitignore` | â³ Pendiente de validar | Requiere comprobaciÃ³n con Git |

### 2.2 ProtecciÃ³n de contraseÃ±as

Las contraseÃ±as se almacenan utilizando **bcrypt**, un algoritmo destinado al
almacenamiento seguro de contraseÃ±as. La prueba automatizada confirmÃ³ que los hashes generados
son Ãºnicos por generaciÃ³n mediante salt y que tienen una longitud de 60
caracteres.

No deben almacenarse contraseÃ±as en texto plano ni reemplazarse bcrypt por otro
mecanismo sin una revisiÃ³n tÃ©cnica y de seguridad formal.

### 2.3 Resultado de pruebas automatizadas de seguridad

La ejecuciÃ³n de `run_all_tests.bat` registrÃ³ los siguientes resultados:

| MÃ©trica | Resultado |
|---|---:|
| Pruebas de seguridad ejecutadas | 8 |
| Pruebas aprobadas | 8 |
| Pruebas fallidas | 0 |
| Vulnerabilidades detectadas por el script | 0 |
| Reporte generado | `reporte_seguridad.txt` |

Los controles evaluados incluyeron:

- ValidaciÃ³n de contraseÃ±as.
- GeneraciÃ³n de hashes bcrypt con salt.
- Uso de consultas parametrizadas frente a inyecciÃ³n SQL.
- Pruebas automatizadas frente a payloads XSS.
- ValidaciÃ³n de datos de entrada.
- Controles de acceso a datos.
- ProtecciÃ³n de datos sensibles.
- ConfiguraciÃ³n de seguridad y detecciÃ³n de secretos hardcoded.

### 2.4 Estado

âœ… **Los controles bÃ¡sicos de seguridad evaluados finalizaron correctamente en
las pruebas automatizadas ejecutadas.**

El resultado indica que no se detectaron vulnerabilidades en los casos incluidos
en el script. No garantiza la ausencia total de vulnerabilidades fuera de los
escenarios evaluados.

---

## 3. ValidaciÃ³n de backups

### 3.1 Verificaciones realizadas

| Control | Estado | Detalle |
|---|---|---|
| Script de backup automÃ¡tico | âœ… Verificado | Existe `scripts/backup_automatico.py` |
| DocumentaciÃ³n de programaciÃ³n de backups | âœ… Verificada | Existe `docs/PROGRAMAR_BACKUPS.md` |
| DocumentaciÃ³n de rollback | âœ… Verificada | Existe `docs/CHECKLIST_PRODUCCION.md` |
| Historial de cambios | âœ… Verificado | Existe `CHANGELOG.md` |
| Directorio actual de backups | â³ Pendiente de validar | La carpeta `backups/` no estaba presente durante la verificaciÃ³n |
| Existencia de backups recientes | â³ Pendiente de validar | No se encontraron archivos en `backups/` porque la carpeta no existe |
| RetenciÃ³n de los Ãºltimos 7 backups | â³ Pendiente de validar | Debe confirmarse mediante revisiÃ³n del script o ejecuciÃ³n real |
| ExportaciÃ³n de tablas PostgreSQL | â³ Pendiente de validar | Debe confirmarse mediante un archivo de backup generado |
| RestauraciÃ³n de backup | â³ Pendiente de validar | Debe probarse en una base de datos temporal |

### 3.2 Estado actual

El proyecto dispone de un script de backup automÃ¡tico y documentaciÃ³n de apoyo
para programaciÃ³n de backups y rollback.

Durante la verificaciÃ³n realizada el 2026-10-03, no se encontrÃ³ la carpeta:

```text
backups/
```

en la raÃ­z del proyecto.

Por tanto, no se declara todavÃ­a la existencia actual de archivos de respaldo,
la conservaciÃ³n efectiva de siete backups ni la restauraciÃ³n validada de una
copia de seguridad.

La ausencia de la carpeta puede deberse a que el script no se ha ejecutado
recientemente, que crea la carpeta Ãºnicamente durante su ejecuciÃ³n o que utiliza
una ruta de salida distinta. Esto debe comprobarse antes de declarar el control
como completamente validado.

### 3.3 Acciones pendientes

- Ejecutar `scripts/backup_automatico.py`.
- Identificar la ruta de salida configurada por el script.
- Confirmar la creaciÃ³n de un archivo de backup.
- Validar el formato generado.
- Confirmar cuÃ¡ntos backups conserva el mecanismo.
- Probar una restauraciÃ³n controlada en una base de datos temporal.
- Registrar la fecha, archivo y resultado de la restauraciÃ³n.

### 3.4 Estado

âœ… **El script y la documentaciÃ³n de backup existen.**

â³ **La generaciÃ³n actual de archivos, la ubicaciÃ³n de salida, la retenciÃ³n y la
restauraciÃ³n requieren validaciÃ³n mediante ejecuciÃ³n real.**

---

## 4. Procedimiento de restauraciÃ³n

### 4.1 DocumentaciÃ³n disponible

| Documento o archivo | Estado | PropÃ³sito |
|---|---|---|
| `scripts/backup_automatico.py` | âœ… Existe | GeneraciÃ³n de backups |
| `docs/PROGRAMAR_BACKUPS.md` | âœ… Existe | Instrucciones de programaciÃ³n de backups |
| `docs/CHECKLIST_PRODUCCION.md` | âœ… Existe | Procedimiento de rollback en producciÃ³n |
| `CHANGELOG.md` | âœ… Existe | Historial de cambios y versiones |

### 4.2 Procedimiento pendiente de validaciÃ³n

Antes de registrar un procedimiento definitivo, se debe identificar el formato
real generado por `scripts/backup_automatico.py`.

Si el script genera un archivo SQL plano con extensiÃ³n `.sql`, el procedimiento
de restauraciÃ³n deberÃ¡ documentarse utilizando el comando correspondiente para
ejecutar dicho script SQL en PostgreSQL.

Si el script genera un backup en formato archivo de PostgreSQL, se deberÃ¡
documentar el procedimiento compatible con ese formato.

La restauraciÃ³n debe realizarse primero en una base de datos temporal, nunca
directamente sobre una base de datos productiva.

### 4.3 Verificaciones posteriores a una restauraciÃ³n

DespuÃ©s de realizar una restauraciÃ³n de prueba, se deberÃ¡ comprobar:

- Que la base de datos acepta conexiones.
- Que las tablas requeridas existen.
- Que los datos esperados estÃ¡n disponibles.
- Que las contraseÃ±as continÃºan almacenadas como hashes bcrypt.
- Que las pruebas de conexiÃ³n a base de datos finalizan correctamente.
- Que no se ha modificado la base de datos productiva.
- Que se registra evidencia de la restauraciÃ³n realizada.

### 4.4 Estado

â³ **Procedimiento documentado parcialmente; restauraciÃ³n real pendiente de
ejecuciÃ³n y validaciÃ³n.**

---

## 5. Recomendaciones

### 5.1 Corto plazo

- [ ] Ejecutar `scripts/backup_automatico.py` y comprobar la ruta de salida.
- [ ] Verificar la creaciÃ³n de la carpeta de backups si corresponde.
- [ ] Registrar un backup real generado por el script.
- [ ] Confirmar la polÃ­tica de retenciÃ³n de backups.
- [ ] Probar la restauraciÃ³n en una base de datos temporal.
- [ ] Verificar que `.env` estÃ© excluido del repositorio mediante `.gitignore`.
- [ ] Mantener los archivos de backup fuera del repositorio Git.
- [ ] Configurar alertas o notificaciones ante fallos de backup.
- [ ] Cifrar las copias de seguridad antes de almacenarlas en servicios externos.

### 5.2 Mediano y largo plazo

- [ ] Implementar autenticaciÃ³n de dos factores para perfiles administrativos.
- [ ] Registrar auditorÃ­a de accesos y acciones sensibles.
- [ ] Definir una polÃ­tica de rotaciÃ³n de credenciales.
- [ ] Revisar los permisos mÃ­nimos de usuarios de base de datos.
- [ ] Mantener actualizadas las dependencias del proyecto.
- [ ] Realizar una revisiÃ³n de seguridad manual de mayor alcance.
- [ ] Definir una polÃ­tica de retenciÃ³n y eliminaciÃ³n segura de backups.
- [ ] Ejecutar revisiones de seguridad despuÃ©s de cambios relevantes en
  autenticaciÃ³n, base de datos o despliegue.

---

## 6. Limitaciones de la revisiÃ³n

Esta revisiÃ³n presenta las siguientes limitaciones:

- Las pruebas automatizadas de seguridad cubren Ãºnicamente los 8 escenarios
  implementados en el script ejecutado.
- La ausencia de vulnerabilidades detectadas por un script no garantiza la
  ausencia total de vulnerabilidades.
- La protecciÃ³n contra XSS se evaluÃ³ con 4 payloads automatizados, no con todos
  los vectores posibles.
- La protecciÃ³n contra inyecciÃ³n SQL depende de que futuras modificaciones
  mantengan el uso de consultas parametrizadas.
- La detecciÃ³n de secretos hardcoded depende de la cobertura del script.
- La exclusiÃ³n de `.env` mediante `.gitignore` estÃ¡ pendiente de verificaciÃ³n.
- La carpeta `backups/` no se encontrÃ³ durante la verificaciÃ³n del 2026-10-03.
- La generaciÃ³n de archivos de backup, su retenciÃ³n y su restauraciÃ³n no han
  sido confirmadas durante esta revisiÃ³n.
- La configuraciÃ³n de seguridad tambiÃ©n depende del servidor, PostgreSQL,
  sistema operativo, red, permisos y proceso de despliegue.

---

## 7. ConclusiÃ³n

**Estado general:** âœ… **Controles bÃ¡sicos de seguridad automatizados evaluados
correctamente.**

Cardio-Wellness utiliza bcrypt para el almacenamiento de contraseÃ±as. Las
pruebas automatizadas verificaron la generaciÃ³n de hashes Ãºnicos con salt y una
longitud de hash de 60 caracteres.

La ejecuciÃ³n de `run_all_tests.bat` registrÃ³ 8 pruebas automatizadas de
seguridad aprobadas, 0 pruebas fallidas y 0 vulnerabilidades detectadas por el
script en los escenarios evaluados.

El proyecto cuenta con un script de backup y documentaciÃ³n relacionada. Sin
embargo, durante la verificaciÃ³n actual no se encontrÃ³ la carpeta `backups/`,
por lo que la generaciÃ³n de backups, la retenciÃ³n de archivos y la restauraciÃ³n
controlada se mantienen como aspectos pendientes de validaciÃ³n.

**PrÃ³xima revisiÃ³n recomendada:** 2027-03-13
**Periodicidad recomendada:** Semestral o despuÃ©s de cambios relevantes de
seguridad, autenticaciÃ³n, base de datos o despliegue.

---

**Firma:** _________________________
**Fecha:** _________________________
