"""
Pruebas de integración completas para Cardio-Wellness.

Verifica:
1. Registro de cliente.
2. Inicio de sesión mediante consulta de base de datos.
3. Creación y asignación de rutina.
4. Registro de sesión y progreso mensual.
5. Existencia del archivo de auditoría.
"""

import hashlib
import sys
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tests.integracion.config_db import (
    ejecutar_con_retorno,
    ejecutar_consulta,
    get_connection,
)


class IntegracionWellness:
    """Ejecuta pruebas de integración sin interfaz gráfica."""

    def __init__(self):
        self.resultados = []
        self.id_cliente_prueba = None
        self.id_rutina_prueba = None
        self.id_sesion_prueba = None
        self.correo_prueba = None
        self.contrasena_prueba = "Password123!"
        self.prefijo = f"integracion.{uuid4().hex}"

    def _registrar_resultado(
        self,
        nombre_prueba: str,
        exito: bool,
        mensaje: str = "",
    ):
        self.resultados.append(
            {
                "prueba": nombre_prueba,
                "exito": exito,
                "mensaje": mensaje,
            }
        )

        estado = "✅" if exito else "❌"
        print(f"{estado} {nombre_prueba}: {mensaje}")

    @staticmethod
    def _hash_contrasena(
        contrasena: str,
    ) -> str:
        return hashlib.sha256(
            contrasena.encode("utf-8")
        ).hexdigest()

    def test_01_registro_cliente(self):
        """Crea un usuario y su registro relacionado de cliente."""
        print("\n" + "=" * 70)
        print("CASO 1: Registro completo de cliente")
        print("=" * 70)

        try:
            self.correo_prueba = (
                f"{self.prefijo}@wellness.com"
            )

            hash_contrasena = self._hash_contrasena(
                self.contrasena_prueba
            )

            print("Creando usuario de integración...")

            self.id_cliente_prueba = ejecutar_con_retorno(
                """
                INSERT INTO usuarios (
                    nombre,
                    apellido,
                    correo_electronico,
                    contrasenia_hash,
                    "contraseña_hash",
                    edad,
                    tipo_usuario
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario
                """,
                (
                    "Test",
                    "Integracion",
                    self.correo_prueba,
                    hash_contrasena,
                    hash_contrasena,
                    25,
                    "cliente",
                ),
            )

            conn = get_connection()
            conn.abrir_conexion()

            try:
                with conn._obtener_cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO clientes (
                            id_usuario,
                            peso,
                            altura,
                            objetivo
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            self.id_cliente_prueba,
                            75.5,
                            1.75,
                            "Mejorar resistencia",
                        ),
                    )

                conn._conexion.commit()

            finally:
                conn.cerrar_conexion()

            self._registrar_resultado(
                "Registro de cliente",
                True,
                (
                    "Cliente registrado con ID: "
                    f"{self.id_cliente_prueba}"
                ),
            )

            resultados = ejecutar_consulta(
                """
                SELECT
                    id_usuario,
                    correo_electronico,
                    contrasenia_hash
                FROM usuarios
                WHERE correo_electronico = %s
                  AND contrasenia_hash = %s
                """,
                (
                    self.correo_prueba,
                    hash_contrasena,
                ),
            )

            if resultados:
                self._registrar_resultado(
                    "Verificación de hash",
                    True,
                    "Hash almacenado correctamente",
                )
                return True

            self._registrar_resultado(
                "Verificación de hash",
                False,
                "No se pudo verificar el hash",
            )
            return False

        except Exception as error:
            self._registrar_resultado(
                "Registro de cliente",
                False,
                f"Excepción: {error}",
            )
            return False

    def test_02_inicio_sesion(self):
        """Valida credenciales correctas e incorrectas."""
        print("\n" + "=" * 70)
        print("CASO 2: Inicio de sesión")
        print("=" * 70)

        if not self.correo_prueba:
            self._registrar_resultado(
                "Inicio de sesión",
                False,
                "No existe un cliente de prueba registrado.",
            )
            return False

        try:
            hash_correcto = self._hash_contrasena(
                self.contrasena_prueba
            )

            resultados = ejecutar_consulta(
                """
                SELECT id_usuario, correo_electronico
                FROM usuarios
                WHERE correo_electronico = %s
                  AND contrasenia_hash = %s
                """,
                (
                    self.correo_prueba,
                    hash_correcto,
                ),
            )

            self._registrar_resultado(
                "Login correcto",
                bool(resultados),
                (
                    "Usuario autenticado correctamente"
                    if resultados
                    else "No se autenticó al usuario."
                ),
            )

            hash_incorrecto = self._hash_contrasena(
                "ContrasenaIncorrecta123!"
            )

            resultados_incorrectos = ejecutar_consulta(
                """
                SELECT id_usuario
                FROM usuarios
                WHERE correo_electronico = %s
                  AND contrasenia_hash = %s
                """,
                (
                    self.correo_prueba,
                    hash_incorrecto,
                ),
            )

            self._registrar_resultado(
                "Login incorrecto",
                not bool(resultados_incorrectos),
                "Contraseña incorrecta rechazada",
            )

            return bool(resultados) and not bool(
                resultados_incorrectos
            )

        except Exception as error:
            self._registrar_resultado(
                "Inicio de sesión",
                False,
                f"Excepción: {error}",
            )
            return False

    def test_03_asignacion_rutina(self):
        """Crea una rutina y la asigna al cliente temporal."""
        print("\n" + "=" * 70)
        print("CASO 3: Asignación de rutina")
        print("=" * 70)

        if self.id_cliente_prueba is None:
            self._registrar_resultado(
                "Asignación de rutina",
                False,
                "No existe cliente válido para asignar rutina.",
            )
            return False

        try:
            self.id_rutina_prueba = ejecutar_con_retorno(
                """
                INSERT INTO rutinas (
                    nombre,
                    descripcion,
                    objetivo,
                    nivel,
                    duracion_semanas,
                    creado_por
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_rutina
                """,
                (
                    f"Rutina {self.prefijo}",
                    "Rutina temporal de integración",
                    "Mejorar resistencia",
                    "INTERMEDIO",
                    4,
                    self.id_cliente_prueba,
                ),
            )

            ejecutar_consulta(
                """
                UPDATE asignaciones_rutina
                SET
                    estado = 'FINALIZADA',
                    fecha_finalizacion = CURRENT_DATE
                WHERE id_cliente = %s
                  AND estado = 'ACTIVA'
                """,
                (self.id_cliente_prueba,),
            )

            id_asignacion = ejecutar_con_retorno(
                """
                INSERT INTO asignaciones_rutina (
                    id_cliente,
                    id_rutina,
                    estado,
                    observaciones
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_asignacion
                """,
                (
                    self.id_cliente_prueba,
                    self.id_rutina_prueba,
                    "ACTIVA",
                    "Asignación de prueba de integración",
                ),
            )

            resultados = ejecutar_consulta(
                """
                SELECT id_asignacion
                FROM asignaciones_rutina
                WHERE id_asignacion = %s
                  AND estado = 'ACTIVA'
                """,
                (id_asignacion,),
            )

            self._registrar_resultado(
                "Asignación de rutina",
                bool(resultados),
                (
                    f"Rutina asignada con ID: "
                    f"{id_asignacion}"
                ),
            )

            return bool(resultados)

        except Exception as error:
            self._registrar_resultado(
                "Asignación de rutina",
                False,
                f"Excepción: {error}",
            )
            return False

    def test_04_registro_sesion_progreso(self):
        """Registra una sesión y comprueba su persistencia."""
        print("\n" + "=" * 70)
        print("CASO 4: Registro de sesión y progreso")
        print("=" * 70)

        if self.id_cliente_prueba is None:
            self._registrar_resultado(
                "Registro de sesión y progreso",
                False,
                "No existe cliente válido para registrar sesión.",
            )
            return False

        try:
            self.id_sesion_prueba = ejecutar_con_retorno(
                """
                INSERT INTO sesiones_entrenamiento (
                    id_cliente,
                    fecha,
                    duracion_real,
                    intensidad_real,
                    calorias_quemadas,
                    observaciones,
                    completada
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_sesion
                """,
                (
                    self.id_cliente_prueba,
                    date.today(),
                    45,
                    "ALTA",
                    450.5,
                    "Sesión de prueba de integración",
                    True,
                ),
            )

            resultados = ejecutar_consulta(
                """
                SELECT
                    id_sesion,
                    duracion_real,
                    calorias_quemadas
                FROM sesiones_entrenamiento
                WHERE id_sesion = %s
                """,
                (self.id_sesion_prueba,),
            )

            exito_sesion = bool(resultados)

            self._registrar_resultado(
                "Registro de sesión",
                exito_sesion,
                (
                    f"Sesión registrada con ID: "
                    f"{self.id_sesion_prueba}"
                ),
            )

            resultado_progreso = ejecutar_consulta(
                """
                SELECT COUNT(*) AS sesiones
                FROM sesiones_entrenamiento
                WHERE id_cliente = %s
                  AND completada = TRUE
                  AND EXTRACT(
                      MONTH FROM fecha
                  ) = EXTRACT(
                      MONTH FROM CURRENT_DATE
                  )
                  AND EXTRACT(
                      YEAR FROM fecha
                  ) = EXTRACT(
                      YEAR FROM CURRENT_DATE
                  )
                """,
                (self.id_cliente_prueba,),
            )

            sesiones = (
                resultado_progreso[0]["sesiones"]
                if resultado_progreso
                else 0
            )

            self._registrar_resultado(
                "Cálculo de progreso",
                sesiones >= 1,
                (
                    "Sesiones completadas este mes: "
                    f"{sesiones}"
                ),
            )

            return exito_sesion and sesiones >= 1

        except Exception as error:
            self._registrar_resultado(
                "Registro de sesión y progreso",
                False,
                f"Excepción: {error}",
            )
            return False

    def test_05_verificacion_log(self):
        """Comprueba que exista el archivo global de auditoría."""
        print("\n" + "=" * 70)
        print("CASO 5: Verificación de LOG_CARDIO.txt")
        print("=" * 70)

        rutas_posibles = [
            ROOT_DIR / "LOG_CARDIO.txt",
            ROOT_DIR / "logs" / "LOG_CARDIO.txt",
        ]

        log_path = next(
            (
                ruta
                for ruta in rutas_posibles
                if ruta.exists()
            ),
            None,
        )

        if log_path is None:
            self._registrar_resultado(
                "Existencia de LOG_CARDIO.txt",
                False,
                "No se encontró el archivo de auditoría.",
            )
            return False

        lineas = log_path.read_text(
            encoding="utf-8",
        ).splitlines()

        self._registrar_resultado(
            "Verificación de LOG_CARDIO.txt",
            True,
            (
                f"Archivo encontrado: {log_path.name}; "
                f"entradas: {len(lineas)}"
            ),
        )

        return True

    def _limpiar_datos(self):
        """Elimina registros creados en esta ejecución."""
        if self.id_cliente_prueba is None:
            return

        conn = get_connection()
        conn.abrir_conexion()

        try:
            with conn._obtener_cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM sesiones_entrenamiento
                    WHERE id_cliente = %s
                    """,
                    (self.id_cliente_prueba,),
                )

                cursor.execute(
                    """
                    DELETE FROM asignaciones_rutina
                    WHERE id_cliente = %s
                    """,
                    (self.id_cliente_prueba,),
                )

                if self.id_rutina_prueba is not None:
                    cursor.execute(
                        """
                        DELETE FROM rutinas
                        WHERE id_rutina = %s
                        """,
                        (self.id_rutina_prueba,),
                    )

                cursor.execute(
                    """
                    DELETE FROM clientes
                    WHERE id_usuario = %s
                    """,
                    (self.id_cliente_prueba,),
                )

                cursor.execute(
                    """
                    DELETE FROM usuarios
                    WHERE id_usuario = %s
                    """,
                    (self.id_cliente_prueba,),
                )

            conn._conexion.commit()

        except Exception as error:
            conn._conexion.rollback()
            print(f"⚠️ Error limpiando datos: {error}")

        finally:
            conn.cerrar_conexion()

    def _guardar_resumen(self):
        """Guarda el resumen de ejecución en un archivo."""
        ruta = (
            ROOT_DIR
            / "tests"
            / "integracion"
            / "resumen_pruebas_integracion.txt"
        )

        total = len(self.resultados)
        exitosas = sum(
            1
            for resultado in self.resultados
            if resultado["exito"]
        )

        with ruta.open(
            "w",
            encoding="utf-8",
        ) as archivo:
            archivo.write(
                "RESUMEN DE PRUEBAS DE INTEGRACIÓN\n"
            )
            archivo.write("=" * 70 + "\n")
            archivo.write(
                f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            )
            archivo.write(f"Total: {total}\n")
            archivo.write(f"Exitosas: {exitosas}\n")
            archivo.write(
                f"Fallidas: {total - exitosas}\n\n"
            )

            for resultado in self.resultados:
                estado = (
                    "✅"
                    if resultado["exito"]
                    else "❌"
                )

                archivo.write(
                    f"{estado} "
                    f"{resultado['prueba']}: "
                    f"{resultado['mensaje']}\n"
                )

        print(f"\nResumen guardado en: {ruta}")

    def ejecutar_todas_las_pruebas(self) -> bool:
        """Ejecuta los casos de integración y devuelve éxito global."""
        print("\n" + "=" * 70)
        print("PRUEBAS DE INTEGRACIÓN - CARDIO-WELLNESS")
        print("=" * 70)
        print(
            f"Fecha de ejecución: "
            f"{datetime.now():%Y-%m-%d %H:%M:%S}"
        )
        print("=" * 70)

        try:
            self.test_01_registro_cliente()
            self.test_02_inicio_sesion()
            self.test_03_asignacion_rutina()
            self.test_04_registro_sesion_progreso()
            self.test_05_verificacion_log()

        finally:
            self._guardar_resumen()
            self._limpiar_datos()

        total = len(self.resultados)
        exitosas = sum(
            1
            for resultado in self.resultados
            if resultado["exito"]
        )
        fallidas = total - exitosas

        print("\n" + "=" * 70)
        print("RESUMEN DE PRUEBAS DE INTEGRACIÓN")
        print("=" * 70)
        print(f"Total de pruebas: {total}")
        print(
            f"Exitosas: {exitosas} "
            f"({exitosas / total * 100:.1f}%)"
        )
        print(
            f"Fallidas: {fallidas} "
            f"({fallidas / total * 100:.1f}%)"
        )
        print("=" * 70)

        return fallidas == 0


def main():
    """Punto de entrada del script."""
    tester = IntegracionWellness()
    exito = tester.ejecutar_todas_las_pruebas()

    raise SystemExit(0 if exito else 1)


if __name__ == "__main__":
    main()