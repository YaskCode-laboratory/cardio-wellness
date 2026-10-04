# Plan de Pruebas de Usabilidad â€” Cardio-Wellness

**VersiÃ³n del documento:** 1.1
**Fecha de actualizaciÃ³n:** 2026-10-03
**Estado:** Protocolo documentado; ejecuciÃ³n con usuarios reales pendiente.

---

## 1. PropÃ³sito

Este documento define el protocolo para evaluar la usabilidad de
Cardio-Wellness con participantes reales que representen los perfiles de uso
del sistema.

La evaluaciÃ³n busca determinar si los usuarios pueden completar las tareas
crÃ­ticas sin asistencia excesiva, identificar problemas de navegaciÃ³n o
comprensiÃ³n y recopilar sugerencias de mejora antes de una futura adopciÃ³n en
un gimnasio.

Este plan no presenta resultados de usabilidad reales. Las mÃ©tricas de
completitud, satisfacciÃ³n, tiempos y NPS solo podrÃ¡n informarse despuÃ©s de
ejecutar las sesiones con participantes y registrar la evidencia
correspondiente.

---

## 2. Alcance

Las pruebas cubren los flujos principales del sistema:

- Registro de clientes.
- AsignaciÃ³n de rutinas de entrenamiento.
- Consulta de rutinas activas.
- Registro de sesiones de entrenamiento.
- Consulta de progreso mensual.

La prueba se realizarÃ¡ en un entorno de datos ficticios. No se utilizarÃ¡n
datos reales de clientes, contraseÃ±as reales ni informaciÃ³n mÃ©dica
identificable.

---

## 3. Objetivos

### Objetivo general

Validar que los usuarios representativos de Cardio-Wellness puedan realizar
las tareas crÃ­ticas del sistema con claridad, eficiencia y mÃ­nima asistencia.

### Objetivos especÃ­ficos

- Medir la tasa de finalizaciÃ³n de las tareas crÃ­ticas.
- Registrar el tiempo empleado por los participantes.
- Identificar errores, dudas y puntos de fricciÃ³n.
- Recoger la percepciÃ³n de facilidad de uso y satisfacciÃ³n.
- Obtener observaciones cualitativas para priorizar mejoras.
- Medir NPS Ãºnicamente en la Fase Beta, con participantes reales.

---

## 4. Perfiles evaluados

| Perfil | DescripciÃ³n | Tareas principales |
|---|---|---|
| Administrador o entrenador | Persona encargada de registrar clientes y asignar rutinas | Registro de cliente y asignaciÃ³n de rutina |
| Cliente | Persona que consulta y registra su actividad fÃ­sica | Consulta de rutina, registro de sesiÃ³n y progreso |

Los participantes se identificarÃ¡n de forma anÃ³nima mediante cÃ³digos como
`P1`, `P2`, `P3` y no mediante nombres completos.

---

## 5. Fase Alpha

### 5.1 PropÃ³sito

La Fase Alpha permite detectar problemas iniciales en flujos crÃ­ticos antes de
una evaluaciÃ³n piloto mÃ¡s amplia.

### 5.2 Participantes

- Entre 3 y 5 participantes.
- Personas que representen los perfiles de administrador, entrenador o cliente.
- Participantes que no conozcan en detalle la implementaciÃ³n interna de la
  interfaz.
- DuraciÃ³n estimada de la fase: 2 semanas.

### 5.3 Entorno

- AplicaciÃ³n ejecutada en un entorno local de pruebas.
- Base de datos temporal: `cardio_wellness_prueba_limpieza`.
- Cuentas, clientes, rutinas y sesiones ficticias.
- Sin uso de informaciÃ³n personal real.

### 5.4 Tareas crÃ­ticas

#### Tarea 1: Registrar un nuevo cliente

**Escenario para el participante:**

> Eres responsable de la gestiÃ³n del gimnasio. Necesitas registrar a un nuevo
> cliente para que pueda comenzar a usar el sistema. Completa la informaciÃ³n
> solicitada y guarda el registro.

**Datos de prueba sugeridos:**

| Campo | Valor de ejemplo |
|---|---|
| Nombre | Cliente |
| Apellido | Prueba |
| Correo | cliente.prueba@example.com |
| Edad | 30 |
| Peso | 70 kg |
| Altura | 1.70 m |
| Objetivo | Mantener condiciÃ³n |

**Criterios de Ã©xito:**

- El participante registra el cliente correctamente.
- No requiere indicaciones sobre la ubicaciÃ³n de botones o menÃºs.
- Tiempo objetivo: menos de 2 minutos.
- No se producen errores crÃ­ticos.

---

#### Tarea 2: Asignar una rutina a un cliente

**Escenario para el participante:**

> El cliente registrado necesita comenzar un plan de entrenamiento. Localiza al
> cliente y asÃ­gnale una rutina disponible.

**Criterios de Ã©xito:**

- El participante encuentra al cliente.
- Selecciona y confirma una rutina vÃ¡lida.
- La asignaciÃ³n queda registrada correctamente.
- Tiempo objetivo: menos de 1 minuto.

---

#### Tarea 3: Registrar una sesiÃ³n de entrenamiento

**Escenario para el participante:**

> Ahora actÃºa como cliente. Consulta tu rutina activa y registra una sesiÃ³n de
> entrenamiento realizada, incluyendo fecha, duraciÃ³n, intensidad y calorÃ­as.

**Criterios de Ã©xito:**

- El participante encuentra su rutina activa.
- Registra una sesiÃ³n vÃ¡lida.
- El sistema confirma el registro.
- Tiempo objetivo: menos de 2 minutos.
- No requiere asistencia.

---

#### Tarea 4: Consultar progreso mensual

**Escenario para el participante:**

> Revisa el progreso mensual del cliente para identificar las sesiones
> registradas y la evoluciÃ³n disponible en el sistema.

**Criterios de Ã©xito:**

- El participante encuentra el mÃ³dulo de progreso.
- Interpreta la informaciÃ³n principal mostrada.
- Identifica al menos una mÃ©trica de progreso.
- Tiempo objetivo: menos de 2 minutos.

---

### 5.5 MÃ©tricas Alpha

| MÃ©trica | Objetivo | MÃ©todo de registro |
|---|---:|---|
| Completitud de tareas | â‰¥80% | Tareas completadas sin asistencia / tareas intentadas |
| Tiempo promedio por tarea | <2 minutos | CronÃ³metro desde el inicio hasta la finalizaciÃ³n |
| Errores por participante | â‰¤2 por tarea | ObservaciÃ³n del moderador |
| Solicitudes de ayuda | â‰¤1 por tarea | Registro del moderador |
| SatisfacciÃ³n general | â‰¥4.0/5 | Encuesta posterior |
| Hallazgos cualitativos | Identificar patrones | Comentarios y observaciones |

La tasa de completitud se calcularÃ¡ mediante:

\[
\text{Tasa de completitud} =
\frac{\text{tareas completadas sin asistencia}}
{\text{tareas intentadas}}
\times 100
\]

---

## 6. Fase Beta

### 6.1 PropÃ³sito

La Fase Beta permite validar los flujos con una muestra mÃ¡s amplia de personas
representativas y recoger indicadores de satisfacciÃ³n y recomendaciÃ³n.

### 6.2 Participantes

- Entre 10 y 15 entrenadores, administradores o clientes representativos.
- DuraciÃ³n estimada: 4 semanas.
- Uso de identificadores anÃ³nimos para los registros de prueba.

### 6.3 MÃ©tricas Beta

| MÃ©trica | Objetivo | MÃ©todo de mediciÃ³n |
|---|---:|---|
| NPS | â‰¥40 | Encuesta final con escala de 0 a 10 |
| SatisfacciÃ³n por mÃ³dulo | â‰¥4.0/5 | Encuesta por mÃ³dulo |
| Completitud de tareas | â‰¥80% | Registro de tareas completadas |
| Incidencias crÃ­ticas | â‰¤5 | Registro de incidencias |
| Solicitudes de mejora | Sin lÃ­mite | Lista priorizada de sugerencias |

### 6.4 Pregunta NPS

La pregunta se realizarÃ¡ Ãºnicamente a participantes reales al finalizar la
prueba:

> En una escala de 0 a 10, Â¿quÃ© tan probable es que recomiendes
> Cardio-Wellness a un colega?

| ClasificaciÃ³n | PuntuaciÃ³n |
|---|---:|
| Promotores | 9 a 10 |
| Neutros | 7 a 8 |
| Detractores | 0 a 6 |

El NPS se calcularÃ¡ mediante:

\[
\text{NPS} =
\% \text{ de promotores}
-
\% \text{ de detractores}
\]

Los participantes neutros no se incluyen directamente en el cÃ¡lculo.

---

## 7. Fase posterior

Si el sistema se utiliza en un contexto real, se recomienda realizar
seguimiento periÃ³dico de las siguientes mÃ©tricas:

| MÃ©trica | Frecuencia | Fuente |
|---|---|---|
| Incidencias de soporte | Semanal | Registro de soporte |
| Frecuencia de uso | Semanal | Logs y reportes de actividad |
| Usuarios activos | Mensual | Reporte de usuarios |
| RetenciÃ³n | Mensual | Reporte de actividad |
| Feedback cualitativo | Continuo | Encuestas y entrevistas |
| Solicitudes de mejora | Continuo | Registro de mejoras |

---

## 8. Criterios de aceptaciÃ³n

El sistema podrÃ¡ considerarse usable para el alcance evaluado cuando, despuÃ©s
de ejecutar pruebas con participantes reales, se cumplan los siguientes
criterios:

| Criterio | Meta |
|---|---:|
| Completitud de tareas crÃ­ticas sin asistencia | â‰¥80% |
| Tiempo promedio por tarea | <2 minutos |
| SatisfacciÃ³n general | â‰¥4.0/5 |
| NPS en Fase Beta | â‰¥40 |
| Defectos crÃ­ticos en Fase Beta | â‰¤5 |

El cumplimiento de estos criterios deberÃ¡ sustentarse con registros de sesiones,
encuestas y resultados consolidados.

---

## 9. Protocolo de ejecuciÃ³n

### 9.1 PreparaciÃ³n

1. Preparar la aplicaciÃ³n y la base de datos temporal.
2. Crear cuentas, clientes, rutinas y sesiones ficticias.
3. Verificar que los flujos a evaluar estÃ©n disponibles.
4. Preparar la plantilla de registro.
5. Solicitar consentimiento para registrar tiempos, observaciones y comentarios.
6. Informar que se evalÃºa el sistema, no el desempeÃ±o de la persona.

### 9.2 SesiÃ³n por participante

1. Realizar un briefing inicial de aproximadamente 5 minutos.
2. Presentar cada tarea como escenario, sin explicar botones o rutas de
   navegaciÃ³n.
3. Observar la ejecuciÃ³n sin intervenir, salvo ante un bloqueo crÃ­tico.
4. Registrar tiempo, errores, solicitudes de ayuda y comentarios.
5. Aplicar la encuesta posterior.
6. Agradecer al participante y proteger su identidad en el reporte.

### 9.3 AnÃ¡lisis

1. Consolidar los registros de todos los participantes.
2. Calcular completitud, tiempos, errores y satisfacciÃ³n.
3. Clasificar los hallazgos por severidad.
4. Identificar problemas recurrentes.
5. Proponer acciones de mejora.
6. Documentar resultados y limitaciones.

---

## 10. Plantilla de registro

### IdentificaciÃ³n anÃ³nima

**Participante:** P_____
**Fecha:** __________________
**Perfil:** Administrador / Entrenador / Cliente
**Moderador:** __________________

### Registro de tareas

| Tarea | Completada sin asistencia | Tiempo en segundos | Errores | Ayuda solicitada | Comentarios |
|---|---|---:|---:|---:|---|
| Registrar cliente | SÃ­ / No | | | | |
| Asignar rutina | SÃ­ / No | | | | |
| Registrar sesiÃ³n | SÃ­ / No | | | | |
| Consultar progreso | SÃ­ / No | | | | |

### Encuesta posterior

| Pregunta | Respuesta |
|---|---|
| Facilidad general de uso, de 1 a 5 | |
| MÃ³dulo mÃ¡s claro o Ãºtil | |
| Parte mÃ¡s confusa o difÃ­cil | |
| Mejora prioritaria sugerida | |
| Probabilidad de recomendar el sistema, de 0 a 10 | |

### Observaciones adicionales

```text
______________________________________________________________________________

______________________________________________________________________________

______________________________________________________________________________
```

---

## 11. Cronograma propuesto

| Semana | Actividad |
|---|---|
| 1 | PreparaciÃ³n de cuentas ficticias, consentimiento y material de prueba |
| 2 | EjecuciÃ³n de Fase Alpha con 3 a 5 participantes |
| 3 | AnÃ¡lisis de hallazgos Alpha y aplicaciÃ³n de mejoras prioritarias |
| 4 a 7 | Fase Beta con 10 a 15 participantes |
| 8 | ConsolidaciÃ³n de mÃ©tricas, hallazgos y recomendaciones |
| Posterior | Seguimiento periÃ³dico de uso, soporte y feedback |

---

## 12. Estado actual y limitaciones

- Las pruebas de usabilidad con participantes reales estÃ¡n pendientes de
  ejecuciÃ³n.
- Este documento describe el protocolo que se utilizarÃ¡ cuando se realicen las
  sesiones.
- La simulaciÃ³n automatizada de flujos con 100 cuentas es una prueba tÃ©cnica y
  no equivale a una evaluaciÃ³n de usabilidad humana.
- Los indicadores de satisfacciÃ³n, NPS, tiempos observados y completitud real
  no deben declararse hasta contar con registros de participantes.
- Los resultados futuros se documentarÃ¡n en
  [`RESULTADOS_PRUEBAS_USABILIDAD.md`](RESULTADOS_PRUEBAS_USABILIDAD.md).

---

## 13. Evidencia tÃ©cnica relacionada

La validaciÃ³n tÃ©cnica automatizada del proyecto se documenta por separado y no
sustituye esta prueba de usabilidad:

| Evidencia | Resultado |
|---|---|
| Suite automatizada | 2,690 pruebas aprobadas, 0 fallos y 0 errores |
| Reporte JUnit | `docs/resultado_suite_actual.xml` |
| Stress PostgreSQL | 30 usuarios concurrentes, 10,792 operaciones y 100% de Ã©xito |
| SimulaciÃ³n de flujos | 100 cuentas automatizadas; 93.6% de Ã©xito |
| Prueba con personas reales | Pendiente |

La evidencia tÃ©cnica confirma comportamiento automatizado del sistema, mientras
que la evaluaciÃ³n de usabilidad debe obtenerse directamente de participantes
representativos.
