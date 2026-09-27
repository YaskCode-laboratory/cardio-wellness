"""
Script para limpiar datos temporales creados por pruebas de integración.

El orden de eliminación respeta las claves foráneas:
1. Sesiones de entrenamiento.
2. Asignaciones de rutinas.
3. Rutinas temporales.
4. Clientes temporales.
5. Usuarios temporales.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tests.integracion.config_db import get_connection


def limpiar_datos_prueba():
    """Elimina de forma segura los datos temporales de pruebas."""
    print("Limpiando datos de prueba...")

    conn = get_connection()
    conn.abrir_conexion()

    try:
        with conn._obtener_cursor() as cur:
            cur.execute(
                """
                DELETE FROM sesiones_entrenamiento
                WHERE observaciones ILIKE %s
                   OR id_cliente IN (
                       SELECT id_usuario
                       FROM usuarios
                       WHERE correo_electronico = %s
                          OR correo_electronico ILIKE %s
                   )
                   OR id_asignacion IN (
                       SELECT id_asignacion
                       FROM asignaciones_rutina
                       WHERE observaciones ILIKE %s
                          OR id_cliente IN (
                              SELECT id_usuario
                              FROM usuarios
                              WHERE correo_electronico = %s
                                 OR correo_electronico ILIKE %s
                          )
                          OR id_rutina IN (
                              SELECT id_rutina
                              FROM rutinas
                              WHERE nombre ILIKE %s
                                 OR nombre ILIKE %s
                                 OR descripcion ILIKE %s
                          )
                   )
                """,
                (
                    "%prueba de integración%",
                    "test.integracion@wellness.com",
                    "integracion.%@wellness.com",
                    "%prueba de integración%",
                    "test.integracion@wellness.com",
                    "integracion.%@wellness.com",
                    "%Rutina Test Integración%",
                    "Rutina integracion.%",
                    "%Rutina temporal de integración%",
                ),
            )

            print(f"✅ {cur.rowcount} sesiones eliminadas")


            cur.execute(
                """
                DELETE FROM asignaciones_rutina
                WHERE observaciones ILIKE %s
                   OR id_cliente IN (
                       SELECT id_usuario
                       FROM usuarios
                       WHERE correo_electronico = %s
                          OR correo_electronico ILIKE %s
                   )
                   OR id_rutina IN (
                       SELECT id_rutina
                       FROM rutinas
                       WHERE nombre ILIKE %s
                          OR nombre ILIKE %s
                          OR descripcion ILIKE %s
                   )
                """,
                (
                    "%prueba de integración%",
                    "test.integracion@wellness.com",
                    "integracion.%@wellness.com",
                    "%Rutina Test Integración%",
                    "Rutina integracion.%",
                    "%Rutina temporal de integración%",
                ),
            )

            print(f"✅ {cur.rowcount} asignaciones eliminadas")

            cur.execute(
                """
                DELETE FROM rutinas
                WHERE nombre ILIKE %s
                   OR nombre ILIKE %s
                   OR descripcion ILIKE %s
                """,
                (
                    "%Rutina Test Integración%",
                    "Rutina integracion.%",
                    "%Rutina temporal de integración%",
                ),
            )

            print(f"✅ {cur.rowcount} rutinas eliminadas")

            cur.execute(
                """
                DELETE FROM clientes
                WHERE id_usuario IN (
                    SELECT id_usuario
                    FROM usuarios
                    WHERE correo_electronico = %s
                       OR correo_electronico ILIKE %s
                )
                """,
                (
                    "test.integracion@wellness.com",
                    "integracion.%@wellness.com",
                ),
            )

            print(f"✅ {cur.rowcount} clientes eliminados")

            cur.execute(
                """
                DELETE FROM usuarios
                WHERE correo_electronico = %s
                   OR correo_electronico ILIKE %s
                """,
                (
                    "test.integracion@wellness.com",
                    "integracion.%@wellness.com",
                ),
            )

            print(f"✅ {cur.rowcount} usuarios eliminados")

        conn._conexion.commit()

        print(
            "\n✅ Datos de prueba eliminados correctamente"
        )

        return True

    except Exception as error:
        conn._conexion.rollback()

        print(f"❌ Error: {error}")

        return False

    finally:
        conn.cerrar_conexion()


if __name__ == "__main__":
    exito = limpiar_datos_prueba()
    raise SystemExit(0 if exito else 1)