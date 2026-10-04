# Diagramas UML del Sistema Cardio-Wellness

Este directorio contiene los diagramas UML del sistema en dos formatos:

- Código fuente editable en PlantUML (`.puml`).
- Diagramas renderizados en formato SVG (`.svg`).

Los diagramas representan la implementación final de Cardio-Wellness,
incluyendo entidades del dominio, interfaces, controladores, DAO y
componentes de infraestructura.

---

## Índice de diagramas

| # | Diagrama | Código fuente | Imagen SVG |
|:---:|:---|:---|:---|
| 1 | Casos de uso | [01_casos_de_uso.puml](plantuml/01_casos_de_uso.puml) | [01_casos_de_uso.svg](svg/01_casos_de_uso.svg) |
| 2 | Diagrama de objetos | [02_diagrama_de_objetos.puml](plantuml/02_diagrama_de_objetos.puml) | [02_diagrama_de_objetos.svg](svg/02_diagrama_de_objetos.svg) |
| 3 | Diagrama de clases de diseño (DCD) | [03_DCD.puml](plantuml/03_DCD.puml) | [03_DCD.svg](svg/03_DCD.svg) |
| 4 | Secuencia: registrar sesión | [04a_secuencia_registrar_sesion.puml](plantuml/04a_secuencia_registrar_sesion.puml) | [04a_secuencia_registrar_sesion.svg](svg/04a_secuencia_registrar_sesion.svg) |
| 5 | Secuencia: iniciar sesión | [04b_secuencia_login.puml](plantuml/04b_secuencia_login.puml) | [04b_secuencia_login.svg](svg/04b_secuencia_login.svg) |
| 6 | Secuencia: asignar rutina | [04c_secuencia_asignar_rutina.puml](plantuml/04c_secuencia_asignar_rutina.puml) | [04c_secuencia_asignar_rutina.svg](svg/04c_secuencia_asignar_rutina.svg) |
| 7 | Colaboración: registrar sesión | [05a_colaboracion_registrar_sesion.puml](plantuml/05a_colaboracion_registrar_sesion.puml) | [05a_colaboracion_registrar_sesion.svg](svg/05a_colaboracion_registrar_sesion.svg) |
| 8 | Colaboración: iniciar sesión | [05b_colaboracion_login.puml](plantuml/05b_colaboracion_login.puml) | [05b_colaboracion_login.svg](svg/05b_colaboracion_login.svg) |
| 9 | Colaboración: asignar rutina | [05c_colaboracion_asignar_rutina.puml](plantuml/05c_colaboracion_asignar_rutina.puml) | [05c_colaboracion_asignar_rutina.svg](svg/05c_colaboracion_asignar_rutina.svg) |
| 10 | Diagrama de componentes | [06_componentes.puml](plantuml/06_componentes.puml) | [06_componentes.svg](svg/06_componentes.svg) |
| 11 | Diagrama de despliegue | [07_despliegue.puml](plantuml/07_despliegue.puml) | [07_despliegue.svg](svg/07_despliegue.svg) |

---

## Cobertura UML

El repositorio contiene 11 diagramas correspondientes a siete tipos principales
de diagramas UML:

1. Casos de uso.
2. Objetos.
3. Clases de diseño.
4. Secuencia.
5. Colaboración.
6. Componentes.
7. Despliegue.

Los diagramas de secuencia y colaboración incluyen tres escenarios funcionales:
registro de sesión, inicio de sesión y asignación de rutina.

Los requisitos mínimos de diagramación se encuentran disponibles en:

- [Diagrama de casos de uso](svg/01_casos_de_uso.svg).
- [Diagrama de clases de diseño](svg/03_DCD.svg).

---

## Visualización y regeneración

Los archivos `.svg` pueden abrirse directamente en cualquier navegador web.

Para modificar o regenerar un diagrama, utiliza el archivo fuente `.puml`
correspondiente con PlantUML.

- [PlantUML Web Server](https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000)

---

## Herramienta utilizada

- PlantUML para definir y generar los diagramas.
