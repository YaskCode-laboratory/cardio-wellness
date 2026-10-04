# Resultados de Pruebas de Usabilidad — Cardio-Wellness

**Versión del documento:** 1.1
**Fecha de actualización:** 2026-10-03
**Estado:** Pruebas de usabilidad con participantes reales pendientes de ejecución.

---

## 1. Propósito

Este documento registra el estado, la evidencia técnica complementaria y los
resultados que se obtendrán durante las pruebas de usabilidad de
Cardio-Wellness con participantes reales.

El protocolo, las tareas, las métricas y los criterios de aceptación se
encuentran definidos en:

- [`PLAN_PRUEBAS_USABILIDAD.md`](PLAN_PRUEBAS_USABILIDAD.md)

Este documento diferencia explícitamente entre:

- Pruebas técnicas automatizadas.
- Simulaciones automatizadas de flujos.
- Pruebas de usabilidad realizadas con participantes humanos.

Las pruebas automatizadas permiten validar comportamiento técnico, seguridad,
integración, persistencia y rendimiento. Sin embargo, no sustituyen la
evaluación de facilidad de uso, comprensión, satisfacción o recomendación
obtenida mediante personas reales.

---

## 2. Estado actual

Las pruebas de usabilidad con participantes reales están pendientes de
ejecución.

Por tanto, actualmente no existen resultados empíricos de:

- Tasa de completitud de tareas realizada por usuarios reales.
- Tiempo promedio de realización de tareas.
- Errores observados durante sesiones con participantes.
- Solicitudes de ayuda durante las tareas.
- Satisfacción general o satisfacción por módulo.
- NPS obtenido mediante encuestas a participantes reales.
- Defectos de usabilidad detectados durante las fases Alpha o Beta.

No se deben reportar cifras de NPS, satisfacción o completitud como resultados
de usabilidad reales hasta realizar las sesiones, conservar los registros y
consolidar los datos obtenidos.

---

## 3. Preparación completada

Aunque la evaluación humana está pendiente, se completaron las siguientes
actividades de preparación:

| Actividad | Estado |
|---|---|
| Plan de pruebas de usabilidad documentado | ✅ Completado |
| Tareas críticas definidas | ✅ Completado |
| Métricas y criterios de aceptación definidos | ✅ Completado |
| Plantilla de registro por participante | ✅ Completado |
| Escenarios de prueba definidos | ✅ Completado |
| Entorno técnico de pruebas validado | ✅ Completado |
| Simulación automatizada de flujos | ✅ Ejecutada |
| Pruebas de seguridad automatizadas | ✅ Ejecutadas |
| Prueba de estrés PostgreSQL | ✅ Ejecutada |
| Ejecución con participantes reales | ⏳ Pendiente |
| Consolidación de resultados Alpha | ⏳ Pendiente |
| Ejecución de Fase Beta | ⏳ Pendiente |

---
### 3.1 Ejecución de la batería automatizada

La evidencia técnica registrada en este documento fue obtenida mediante la
ejecución del script:

```text
run_all_tests.bat
```

La ejecución incluyó pruebas automatizadas de seguridad, simulación masiva de
flujos, pruebas de estrés PostgreSQL, prueba histórica SQLite y pruebas de
integración.

La fecha de ejecución registrada fue el 2026-10-03.

## 4. Simulación automatizada complementaria

El 2026-10-03 se ejecutó una simulación automatizada de flujos con 100 cuentas
de prueba.

Esta actividad verifica que los flujos programados puedan ejecutarse de forma
automatizada. No equivale a una prueba de usabilidad realizada con personas
reales, ya que las cuentas automatizadas no navegan, interpretan la interfaz,
cometen errores humanos ni responden encuestas reales.

| Métrica técnica | Resultado |
|---|---:|
| Cuentas automatizadas creadas y procesadas | 100 |
| Naturaleza de la prueba | Automatizada |
| Éxito total de flujos automatizados | 93.0% |
| Participantes humanos | 0 |

El reporte automático también generó los siguientes indicadores:

| Indicador generado por simulación | Valor |
|---|---:|
| Satisfacción simulada | 4.65/5.0 |
| Promotores simulados | 98% |
| Detractores simulados | 0% |
| NPS calculado por simulación | 98 |

Los valores de satisfacción, promotores, detractores y NPS anteriores fueron
producidos por el proceso automatizado. Por consiguiente, no representan
opiniones, encuestas ni recomendaciones de personas reales.

No deben utilizarse como resultados de la Fase Alpha, Fase Beta ni como
evidencia de satisfacción humana.

---

## 5. Evidencia técnica relacionada

El 2026-10-03 se ejecutaron pruebas automatizadas de seguridad, simulación de
flujos, estrés de base de datos y pruebas de integración.

La evidencia técnica se conserva como información complementaria al plan de
usabilidad y no reemplaza las pruebas moderadas con participantes humanos.

### 5.1 Pruebas automatizadas de seguridad

| Métrica | Resultado |
|---|---:|
| Pruebas de seguridad ejecutadas | 8 |
| Pruebas aprobadas | 8 |
| Pruebas fallidas | 0 |
| Vulnerabilidades detectadas por el script | 0 |
| Reporte generado | `reporte_seguridad.txt` |

Los controles automatizados evaluaron:

- Validación de contraseñas.
- Generación de hash de contraseñas con salt.
- Uso de consultas parametrizadas para reducir riesgo de inyección SQL.
- Protección frente a payloads de XSS evaluados por el script.
- Validación de datos de entrada.
- Implementación de acceso a datos.
- Protección de contraseñas sin almacenamiento en texto plano.
- Configuración de variables de seguridad y detección de secretos hardcoded.

El resultado indica que los controles evaluados finalizaron correctamente y que
el script no detectó vulnerabilidades en los casos automatizados ejecutados.

Este resultado no constituye una garantía absoluta de seguridad ni sustituye
una auditoría de seguridad independiente, revisión manual de código o prueba de
penetración profesional con mayor alcance.

### 5.2 Prueba de estrés PostgreSQL

| Métrica | Resultado |
|---|---:|
| Base de datos evaluada | PostgreSQL |
| Usuarios concurrentes | 30 |
| Clientes de prueba creados | 100 |
| Duración configurada | 40 segundos |
| Tiempo total de ejecución | 40.26 segundos |
| Operaciones totales | 11,113 |
| Operaciones exitosas | 11,113 |
| Operaciones fallidas | 0 |
| Tasa de éxito | 100.00% |
| Operaciones por segundo | 276.05 |
| Tiempo promedio de respuesta | 22.40 ms |
| Tiempo máximo de respuesta | 345.19 ms |
| Tiempo mínimo de respuesta | 0.37 ms |

Durante la carga evaluada, PostgreSQL procesó 11,113 operaciones sin fallos
registrados. La prueba utilizó 30 usuarios concurrentes y 100 clientes de
prueba durante aproximadamente 40 segundos.

El resultado es válido únicamente para el entorno, duración, volumen de datos y
carga evaluados. No permite garantizar el mismo rendimiento ante mayor número
de usuarios, periodos prolongados, infraestructura distinta o patrones de uso
diferentes.

### 5.3 Prueba histórica SQLite

| Métrica | Resultado |
|---|---:|
| Base de datos evaluada | SQLite |
| Usuarios concurrentes | 20 |
| Duración | 30.01 segundos |
| Operaciones totales | 507 |
| Operaciones exitosas | 499 |
| Operaciones fallidas | 8 |
| Tasa de éxito | 98.42% |
| Operaciones por segundo | 16.90 |
| Tiempo promedio de respuesta | 623.64 ms |
| Tiempo máximo de respuesta | 11,226.94 ms |
| Tiempo mínimo de respuesta | 0.82 ms |
| Errores observados | `database is locked` |

La prueba histórica con SQLite presentó 8 errores de bloqueo de base de datos
bajo concurrencia, identificados como `database is locked`.

Por esta razón, esta prueba no debe utilizarse como evidencia de concurrencia
robusta en SQLite. Se conserva únicamente como antecedente técnico y no
representa la configuración actual basada en PostgreSQL.

### 5.4 Pruebas de integración

Las pruebas de integración fueron iniciadas el 2026-10-03.

El resultado final no se registra todavía en este documento porque se requiere
conservar la salida completa de ejecución, incluyendo:

- Número total de pruebas ejecutadas.
- Pruebas aprobadas.
- Pruebas fallidas.
- Errores detectados.
- Mensaje final de conclusión.
- Reporte o archivo de evidencia generado.

Hasta contar con esa salida completa, el estado de las pruebas de integración
se considera pendiente de consolidación documental.

---

## 6. Resultados Fase Alpha

**Estado:** Pendiente de ejecución con participantes reales.

La Fase Alpha se ejecutará con entre 3 y 5 participantes representativos de los
perfiles administrador, entrenador o cliente.

### 6.1 Resumen de participantes

| Indicador | Resultado |
|---|---|
| Participantes planificados | 3 a 5 |
| Participantes ejecutados | Pendiente |
| Periodo de ejecución | Pendiente |
| Entorno utilizado | Base temporal y datos ficticios |
| Consentimientos registrados | Pendiente |

### 6.2 Resultados por tarea

| Tarea | Participantes que la intentaron | Completitud sin asistencia | Tiempo promedio | Errores promedio | Estado |
|---|---:|---:|---:|---:|---|
| Registrar cliente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Asignar rutina | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Registrar sesión | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Consultar progreso | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

### 6.3 Satisfacción Alpha

| Métrica | Objetivo | Resultado |
|---|---:|---:|
| Satisfacción general | ≥4.0/5 | Pendiente |
| Tasa de completitud | ≥80% | Pendiente |
| Tiempo promedio por tarea | <2 minutos | Pendiente |
| Errores por tarea | ≤2 | Pendiente |

---

## 7. Resultados Fase Beta

**Estado:** Pendiente de ejecución con participantes reales.

La Fase Beta se ejecutará con entre 10 y 15 participantes representativos de
los perfiles definidos en el plan de pruebas.

| Métrica | Objetivo | Resultado |
|---|---:|---:|
| Participantes ejecutados | 10 a 15 | Pendiente |
| NPS | ≥40 | Pendiente |
| Satisfacción por módulo | ≥4.0/5 | Pendiente |
| Completitud de tareas | ≥80% | Pendiente |
| Incidencias críticas | ≤5 | Pendiente |
| Solicitudes de mejora | Registro cualitativo | Pendiente |

El NPS de la Fase Beta se calculará exclusivamente con las respuestas reales a
la pregunta de recomendación definida en el plan de pruebas.

---

## 8. Hallazgos y mejoras

**Estado:** Pendiente de ejecución con participantes reales.

Cuando se ejecuten las sesiones, los hallazgos deberán registrarse con la
siguiente estructura:

| ID | Hallazgo | Tarea afectada | Severidad | Evidencia | Acción propuesta | Estado |
|---|---|---|---|---|---|---|
| U-01 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

### Clasificación de severidad

| Severidad | Descripción |
|---|---|
| Crítica | Impide completar una tarea esencial |
| Alta | Dificulta significativamente una tarea crítica |
| Media | Genera confusión o demora, pero existe una alternativa |
| Baja | Mejora visual, textual o de consistencia |

---

## 9. Limitaciones

- No se han realizado sesiones con usuarios reales.
- No existe una muestra humana real para calcular NPS.
- La simulación automatizada no reemplaza la observación de participantes.
- Los indicadores de satisfacción y NPS generados por scripts no representan
  experiencia de usuario real.
- Las pruebas automatizadas de seguridad cubren únicamente los controles y
  payloads incluidos en el script ejecutado.
- La prueba PostgreSQL representa una carga concreta de 30 usuarios
  concurrentes durante aproximadamente 40 segundos.
- La prueba histórica SQLite presentó bloqueos bajo concurrencia y no
  representa el comportamiento de PostgreSQL.
- El resultado final de las pruebas de integración está pendiente de
  consolidación documental.
- Los resultados futuros dependerán de la disponibilidad y representatividad
  de los participantes seleccionados.

---

## 10. Conclusión actual

Cardio-Wellness cuenta con un protocolo de pruebas de usabilidad documentado,
tareas críticas definidas, métricas de evaluación, una plantilla de registro y
evidencia técnica complementaria de seguridad, simulación automatizada y
rendimiento de PostgreSQL.

La evidencia disponible confirma que, en las pruebas automatizadas ejecutadas,
los controles de seguridad evaluados finalizaron sin fallos, los flujos
automatizados procesaron 100 cuentas con una tasa de éxito de 93.0% y
PostgreSQL procesó 11,113 operaciones sin fallos bajo la carga evaluada.

No obstante, estos resultados no sustituyen una prueba de usabilidad con
personas reales.

La ejecución de pruebas con participantes reales permanece pendiente. Por
consiguiente, no se declara aún que el sistema cumpla los criterios de
usabilidad, satisfacción general o NPS definidos en el plan.
