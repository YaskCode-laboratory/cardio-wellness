# Resultados de Pruebas de Usabilidad â€” Cardio-Wellness

**VersiÃ³n del documento:** 1.1
**Fecha de actualizaciÃ³n:** 2026-10-03
**Estado:** Pruebas de usabilidad con participantes reales pendientes de ejecuciÃ³n.

---

## 1. PropÃ³sito

Este documento registra el estado, la evidencia tÃ©cnica complementaria y los
resultados que se obtendrÃ¡n durante las pruebas de usabilidad de
Cardio-Wellness con participantes reales.

El protocolo, las tareas, las mÃ©tricas y los criterios de aceptaciÃ³n se
encuentran definidos en:

- [`PLAN_PRUEBAS_USABILIDAD.md`](PLAN_PRUEBAS_USABILIDAD.md)

Este documento diferencia explÃ­citamente entre:

- Pruebas tÃ©cnicas automatizadas.
- Simulaciones automatizadas de flujos.
- Pruebas de usabilidad realizadas con participantes humanos.

Las pruebas automatizadas permiten validar comportamiento tÃ©cnico, seguridad,
integraciÃ³n, persistencia y rendimiento. Sin embargo, no sustituyen la
evaluaciÃ³n de facilidad de uso, comprensiÃ³n, satisfacciÃ³n o recomendaciÃ³n
obtenida mediante personas reales.

---

## 2. Estado actual

Las pruebas de usabilidad con participantes reales estÃ¡n pendientes de
ejecuciÃ³n.

Por tanto, actualmente no existen resultados empÃ­ricos de:

- Tasa de completitud de tareas realizada por usuarios reales.
- Tiempo promedio de realizaciÃ³n de tareas.
- Errores observados durante sesiones con participantes.
- Solicitudes de ayuda durante las tareas.
- SatisfacciÃ³n general o satisfacciÃ³n por mÃ³dulo.
- NPS obtenido mediante encuestas a participantes reales.
- Defectos de usabilidad detectados durante las fases Alpha o Beta.

No se deben reportar cifras de NPS, satisfacciÃ³n o completitud como resultados
de usabilidad reales hasta realizar las sesiones, conservar los registros y
consolidar los datos obtenidos.

---

## 3. PreparaciÃ³n completada

Aunque la evaluaciÃ³n humana estÃ¡ pendiente, se completaron las siguientes
actividades de preparaciÃ³n:

| Actividad | Estado |
|---|---|
| Plan de pruebas de usabilidad documentado | âœ… Completado |
| Tareas crÃ­ticas definidas | âœ… Completado |
| MÃ©tricas y criterios de aceptaciÃ³n definidos | âœ… Completado |
| Plantilla de registro por participante | âœ… Completado |
| Escenarios de prueba definidos | âœ… Completado |
| Entorno tÃ©cnico de pruebas validado | âœ… Completado |
| SimulaciÃ³n automatizada de flujos | âœ… Ejecutada |
| Pruebas de seguridad automatizadas | âœ… Ejecutadas |
| Prueba de estrÃ©s PostgreSQL | âœ… Ejecutada |
| EjecuciÃ³n con participantes reales | â³ Pendiente |
| ConsolidaciÃ³n de resultados Alpha | â³ Pendiente |
| EjecuciÃ³n de Fase Beta | â³ Pendiente |

---
### 3.1 EjecuciÃ³n de la baterÃ­a automatizada

La evidencia tÃ©cnica registrada en este documento fue obtenida mediante la
ejecuciÃ³n del script:

```text
run_all_tests.bat
```

La ejecuciÃ³n incluyÃ³ pruebas automatizadas de seguridad, simulaciÃ³n masiva de
flujos, pruebas de estrÃ©s PostgreSQL, prueba histÃ³rica SQLite y pruebas de
integraciÃ³n.

La fecha de ejecuciÃ³n registrada fue el 2026-10-03.

## 4. SimulaciÃ³n automatizada complementaria

El 2026-10-03 se ejecutÃ³ una simulaciÃ³n automatizada de flujos con 100 cuentas
de prueba.

Esta actividad verifica que los flujos programados puedan ejecutarse de forma
automatizada. No equivale a una prueba de usabilidad realizada con personas
reales, ya que las cuentas automatizadas no navegan, interpretan la interfaz,
cometen errores humanos ni responden encuestas reales.

| MÃ©trica tÃ©cnica | Resultado |
|---|---:|
| Cuentas automatizadas creadas y procesadas | 100 |
| Naturaleza de la prueba | Automatizada |
| Ã‰xito total de flujos automatizados | 93.0% |
| Participantes humanos | 0 |

El reporte automÃ¡tico tambiÃ©n generÃ³ los siguientes indicadores:

| Indicador generado por simulaciÃ³n | Valor |
|---|---:|
| SatisfacciÃ³n simulada | 4.65/5.0 |
| Promotores simulados | 98% |
| Detractores simulados | 0% |
| NPS calculado por simulaciÃ³n | 98 |

Los valores de satisfacciÃ³n, promotores, detractores y NPS anteriores fueron
producidos por el proceso automatizado. Por consiguiente, no representan
opiniones, encuestas ni recomendaciones de personas reales.

No deben utilizarse como resultados de la Fase Alpha, Fase Beta ni como
evidencia de satisfacciÃ³n humana.

---

## 5. Evidencia tÃ©cnica relacionada

El 2026-10-03 se ejecutaron pruebas automatizadas de seguridad, simulaciÃ³n de
flujos, estrÃ©s de base de datos y pruebas de integraciÃ³n.

La evidencia tÃ©cnica se conserva como informaciÃ³n complementaria al plan de
usabilidad y no reemplaza las pruebas moderadas con participantes humanos.

### 5.1 Pruebas automatizadas de seguridad

| MÃ©trica | Resultado |
|---|---:|
| Pruebas de seguridad ejecutadas | 8 |
| Pruebas aprobadas | 8 |
| Pruebas fallidas | 0 |
| Vulnerabilidades detectadas por el script | 0 |
| Reporte generado | `reporte_seguridad.txt` |

Los controles automatizados evaluaron:

- ValidaciÃ³n de contraseÃ±as.
- GeneraciÃ³n de hash de contraseÃ±as con salt.
- Uso de consultas parametrizadas para reducir riesgo de inyecciÃ³n SQL.
- ProtecciÃ³n frente a payloads de XSS evaluados por el script.
- ValidaciÃ³n de datos de entrada.
- ImplementaciÃ³n de acceso a datos.
- ProtecciÃ³n de contraseÃ±as sin almacenamiento en texto plano.
- ConfiguraciÃ³n de variables de seguridad y detecciÃ³n de secretos hardcoded.

El resultado indica que los controles evaluados finalizaron correctamente y que
el script no detectÃ³ vulnerabilidades en los casos automatizados ejecutados.

Este resultado no constituye una garantÃ­a absoluta de seguridad ni sustituye
una auditorÃ­a de seguridad independiente, revisiÃ³n manual de cÃ³digo o prueba de
penetraciÃ³n profesional con mayor alcance.

### 5.2 Prueba de estrÃ©s PostgreSQL

| MÃ©trica | Resultado |
|---|---:|
| Base de datos evaluada | PostgreSQL |
| Usuarios concurrentes | 30 |
| Clientes de prueba creados | 100 |
| DuraciÃ³n configurada | 40 segundos |
| Tiempo total de ejecuciÃ³n | 40.26 segundos |
| Operaciones totales | 11,113 |
| Operaciones exitosas | 11,113 |
| Operaciones fallidas | 0 |
| Tasa de Ã©xito | 100.00% |
| Operaciones por segundo | 276.05 |
| Tiempo promedio de respuesta | 22.40 ms |
| Tiempo mÃ¡ximo de respuesta | 345.19 ms |
| Tiempo mÃ­nimo de respuesta | 0.37 ms |

Durante la carga evaluada, PostgreSQL procesÃ³ 11,113 operaciones sin fallos
registrados. La prueba utilizÃ³ 30 usuarios concurrentes y 100 clientes de
prueba durante aproximadamente 40 segundos.

El resultado es vÃ¡lido Ãºnicamente para el entorno, duraciÃ³n, volumen de datos y
carga evaluados. No permite garantizar el mismo rendimiento ante mayor nÃºmero
de usuarios, periodos prolongados, infraestructura distinta o patrones de uso
diferentes.

### 5.3 Prueba histÃ³rica SQLite

| MÃ©trica | Resultado |
|---|---:|
| Base de datos evaluada | SQLite |
| Usuarios concurrentes | 20 |
| DuraciÃ³n | 30.01 segundos |
| Operaciones totales | 507 |
| Operaciones exitosas | 499 |
| Operaciones fallidas | 8 |
| Tasa de Ã©xito | 98.42% |
| Operaciones por segundo | 16.90 |
| Tiempo promedio de respuesta | 623.64 ms |
| Tiempo mÃ¡ximo de respuesta | 11,226.94 ms |
| Tiempo mÃ­nimo de respuesta | 0.82 ms |
| Errores observados | `database is locked` |

La prueba histÃ³rica con SQLite presentÃ³ 8 errores de bloqueo de base de datos
bajo concurrencia, identificados como `database is locked`.

Por esta razÃ³n, esta prueba no debe utilizarse como evidencia de concurrencia
robusta en SQLite. Se conserva Ãºnicamente como antecedente tÃ©cnico y no
representa la configuraciÃ³n actual basada en PostgreSQL.

### 5.4 Pruebas de integraciÃ³n

Las pruebas de integraciÃ³n fueron iniciadas el 2026-10-03.

El resultado final no se registra todavÃ­a en este documento porque se requiere
conservar la salida completa de ejecuciÃ³n, incluyendo:

- NÃºmero total de pruebas ejecutadas.
- Pruebas aprobadas.
- Pruebas fallidas.
- Errores detectados.
- Mensaje final de conclusiÃ³n.
- Reporte o archivo de evidencia generado.

Hasta contar con esa salida completa, el estado de las pruebas de integraciÃ³n
se considera pendiente de consolidaciÃ³n documental.

---

## 6. Resultados Fase Alpha

**Estado:** Pendiente de ejecuciÃ³n con participantes reales.

La Fase Alpha se ejecutarÃ¡ con entre 3 y 5 participantes representativos de los
perfiles administrador, entrenador o cliente.

### 6.1 Resumen de participantes

| Indicador | Resultado |
|---|---|
| Participantes planificados | 3 a 5 |
| Participantes ejecutados | Pendiente |
| Periodo de ejecuciÃ³n | Pendiente |
| Entorno utilizado | Base temporal y datos ficticios |
| Consentimientos registrados | Pendiente |

### 6.2 Resultados por tarea

| Tarea | Participantes que la intentaron | Completitud sin asistencia | Tiempo promedio | Errores promedio | Estado |
|---|---:|---:|---:|---:|---|
| Registrar cliente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Asignar rutina | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Registrar sesiÃ³n | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Consultar progreso | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

### 6.3 SatisfacciÃ³n Alpha

| MÃ©trica | Objetivo | Resultado |
|---|---:|---:|
| SatisfacciÃ³n general | â‰¥4.0/5 | Pendiente |
| Tasa de completitud | â‰¥80% | Pendiente |
| Tiempo promedio por tarea | <2 minutos | Pendiente |
| Errores por tarea | â‰¤2 | Pendiente |

---

## 7. Resultados Fase Beta

**Estado:** Pendiente de ejecuciÃ³n con participantes reales.

La Fase Beta se ejecutarÃ¡ con entre 10 y 15 participantes representativos de
los perfiles definidos en el plan de pruebas.

| MÃ©trica | Objetivo | Resultado |
|---|---:|---:|
| Participantes ejecutados | 10 a 15 | Pendiente |
| NPS | â‰¥40 | Pendiente |
| SatisfacciÃ³n por mÃ³dulo | â‰¥4.0/5 | Pendiente |
| Completitud de tareas | â‰¥80% | Pendiente |
| Incidencias crÃ­ticas | â‰¤5 | Pendiente |
| Solicitudes de mejora | Registro cualitativo | Pendiente |

El NPS de la Fase Beta se calcularÃ¡ exclusivamente con las respuestas reales a
la pregunta de recomendaciÃ³n definida en el plan de pruebas.

---

## 8. Hallazgos y mejoras

**Estado:** Pendiente de ejecuciÃ³n con participantes reales.

Cuando se ejecuten las sesiones, los hallazgos deberÃ¡n registrarse con la
siguiente estructura:

| ID | Hallazgo | Tarea afectada | Severidad | Evidencia | AcciÃ³n propuesta | Estado |
|---|---|---|---|---|---|---|
| U-01 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

### ClasificaciÃ³n de severidad

| Severidad | DescripciÃ³n |
|---|---|
| CrÃ­tica | Impide completar una tarea esencial |
| Alta | Dificulta significativamente una tarea crÃ­tica |
| Media | Genera confusiÃ³n o demora, pero existe una alternativa |
| Baja | Mejora visual, textual o de consistencia |

---

## 9. Limitaciones

- No se han realizado sesiones con usuarios reales.
- No existe una muestra humana real para calcular NPS.
- La simulaciÃ³n automatizada no reemplaza la observaciÃ³n de participantes.
- Los indicadores de satisfacciÃ³n y NPS generados por scripts no representan
  experiencia de usuario real.
- Las pruebas automatizadas de seguridad cubren Ãºnicamente los controles y
  payloads incluidos en el script ejecutado.
- La prueba PostgreSQL representa una carga concreta de 30 usuarios
  concurrentes durante aproximadamente 40 segundos.
- La prueba histÃ³rica SQLite presentÃ³ bloqueos bajo concurrencia y no
  representa el comportamiento de PostgreSQL.
- El resultado final de las pruebas de integraciÃ³n estÃ¡ pendiente de
  consolidaciÃ³n documental.
- Los resultados futuros dependerÃ¡n de la disponibilidad y representatividad
  de los participantes seleccionados.

---

## 10. ConclusiÃ³n actual

Cardio-Wellness cuenta con un protocolo de pruebas de usabilidad documentado,
tareas crÃ­ticas definidas, mÃ©tricas de evaluaciÃ³n, una plantilla de registro y
evidencia tÃ©cnica complementaria de seguridad, simulaciÃ³n automatizada y
rendimiento de PostgreSQL.

La evidencia disponible confirma que, en las pruebas automatizadas ejecutadas,
los controles de seguridad evaluados finalizaron sin fallos, los flujos
automatizados procesaron 100 cuentas con una tasa de Ã©xito de 93.0% y
PostgreSQL procesÃ³ 11,113 operaciones sin fallos bajo la carga evaluada.

No obstante, estos resultados no sustituyen una prueba de usabilidad con
personas reales.

La ejecuciÃ³n de pruebas con participantes reales permanece pendiente. Por
consiguiente, no se declara aÃºn que el sistema cumpla los criterios de
usabilidad, satisfacciÃ³n general o NPS definidos en el plan.
