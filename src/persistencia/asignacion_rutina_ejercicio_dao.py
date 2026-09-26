from typing import Dict, List, Optional

from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor

from src.modelos.asignacion_rutina_ejercicio import (
    AsignacionRutinaEjercicio,
)
from src.persistencia.conexion_bd import ConexionBD


class AsignacionRutinaEjercicioDAO:
    """
    DAO para ejercicios personalizados dentro de una
    asignación de rutina.

    Gestiona los ejercicios pertenecientes a una
    asignación concreta de un cliente, sin modificar
    la plantilla global de la rutina.
    """

    COLUMNAS = (
        "id_asignacion_ejercicio",
        "id_asignacion",
        "id_ejercicio",
        "orden_ejercicio",
        "veces_planificadas",
        "activo",
        "fecha_agregado",
    )

    def __init__(self) -> None:
        self._bd = ConexionBD.obtener_instancia()

    def guardar(
        self,
        ejercicio_asignado: AsignacionRutinaEjercicio,
    ) -> AsignacionRutinaEjercicio:
        """
        Guarda un ejercicio dentro de una asignación.
        """
        self._validar_entidad(ejercicio_asignado)

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:
                cursor.execute(
                    """
                    INSERT INTO asignacion_rutina_ejercicios (
                        id_asignacion,
                        id_ejercicio,
                        orden_ejercicio,
                        veces_planificadas,
                        activo,
                        fecha_agregado
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING
                        id_asignacion_ejercicio,
                        id_asignacion,
                        id_ejercicio,
                        orden_ejercicio,
                        veces_planificadas,
                        activo,
                        fecha_agregado
                    """,
                    (
                        ejercicio_asignado.id_asignacion,
                        ejercicio_asignado.id_ejercicio,
                        ejercicio_asignado.orden_ejercicio,
                        ejercicio_asignado.veces_planificadas,
                        ejercicio_asignado.activo,
                        ejercicio_asignado.fecha_agregado,
                    ),
                )

                fila = cursor.fetchone()

            if fila is None:
                raise RuntimeError(
                    "No se pudo recuperar el ejercicio "
                    "asignado guardado."
                )

            self._bd._conexion.commit()

            return self._crear_desde_fila(fila)

        except IntegrityError as error:
            self._bd._conexion.rollback()
            raise self._convertir_error_integridad(
                error
            ) from error

        except Exception:
            self._bd._conexion.rollback()
            raise

    def buscar_por_id(
        self,
        id_asignacion_ejercicio: int,
    ) -> Optional[AsignacionRutinaEjercicio]:
        """
        Busca un ejercicio asignado por su ID.
        """
        identificador = self._validar_id(
            id_asignacion_ejercicio,
            "El ID del ejercicio asignado",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:
                cursor.execute(
                    """
                    SELECT
                        id_asignacion_ejercicio,
                        id_asignacion,
                        id_ejercicio,
                        orden_ejercicio,
                        veces_planificadas,
                        activo,
                        fecha_agregado
                    FROM asignacion_rutina_ejercicios
                    WHERE id_asignacion_ejercicio = %s
                    """,
                    (identificador,),
                )

                fila = cursor.fetchone()

            if fila is None:
                return None

            return self._crear_desde_fila(fila)

        except Exception:
            self._bd._conexion.rollback()
            raise

    def listar_por_asignacion(
        self,
        id_asignacion: int,
        solo_activos: bool = False,
    ) -> List[AsignacionRutinaEjercicio]:
        """
        Lista los ejercicios de una asignación.

        Si solo_activos es True, devuelve únicamente los
        ejercicios que continúan activos en el plan.
        """
        asignacion_id = self._validar_id(
            id_asignacion,
            "El ID de la asignación",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:
                consulta = """
                    SELECT
                        id_asignacion_ejercicio,
                        id_asignacion,
                        id_ejercicio,
                        orden_ejercicio,
                        veces_planificadas,
                        activo,
                        fecha_agregado
                    FROM asignacion_rutina_ejercicios
                    WHERE id_asignacion = %s
                """

                parametros = [asignacion_id]

                if solo_activos:
                    consulta += """
                        AND activo = TRUE
                    """

                consulta += """
                    ORDER BY
                        orden_ejercicio,
                        id_asignacion_ejercicio
                """

                cursor.execute(
                    consulta,
                    tuple(parametros),
                )

                filas = cursor.fetchall()

            return [
                self._crear_desde_fila(fila)
                for fila in filas
            ]

        except Exception:
            self._bd._conexion.rollback()
            raise

    def obtener_siguiente_orden(
        self,
        id_asignacion: int,
    ) -> int:
        """
        Obtiene el siguiente orden disponible dentro de
        una asignación.
        """
        asignacion_id = self._validar_id(
            id_asignacion,
            "El ID de la asignación",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COALESCE(
                        MAX(orden_ejercicio),
                        0
                    ) + 1
                    FROM asignacion_rutina_ejercicios
                    WHERE id_asignacion = %s
                    """,
                    (asignacion_id,),
                )

                fila = cursor.fetchone()

            if fila is None:
                return 1

            return int(fila[0])

        except Exception:
            self._bd._conexion.rollback()
            raise

    def actualizar(
        self,
        ejercicio_asignado: AsignacionRutinaEjercicio,
    ) -> AsignacionRutinaEjercicio:
        """
        Actualiza los datos de un ejercicio asignado.
        """
        self._validar_entidad(ejercicio_asignado)

        if ejercicio_asignado.id_asignacion_ejercicio is None:
            raise ValueError(
                "El ejercicio asignado debe tener un ID "
                "para actualizarse."
            )

        identificador = self._validar_id(
            ejercicio_asignado.id_asignacion_ejercicio,
            "El ID del ejercicio asignado",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:
                cursor.execute(
                    """
                    UPDATE asignacion_rutina_ejercicios
                    SET
                        id_ejercicio = %s,
                        orden_ejercicio = %s,
                        veces_planificadas = %s,
                        activo = %s
                    WHERE id_asignacion_ejercicio = %s
                      AND id_asignacion = %s
                    RETURNING
                        id_asignacion_ejercicio,
                        id_asignacion,
                        id_ejercicio,
                        orden_ejercicio,
                        veces_planificadas,
                        activo,
                        fecha_agregado
                    """,
                    (
                        ejercicio_asignado.id_ejercicio,
                        ejercicio_asignado.orden_ejercicio,
                        ejercicio_asignado.veces_planificadas,
                        ejercicio_asignado.activo,
                        identificador,
                        ejercicio_asignado.id_asignacion,
                    ),
                )

                fila = cursor.fetchone()

            if fila is None:
                raise ValueError(
                    "No se encontró el ejercicio asignado."
                )

            self._bd._conexion.commit()

            return self._crear_desde_fila(fila)

        except IntegrityError as error:
            self._bd._conexion.rollback()
            raise self._convertir_error_integridad(
                error
            ) from error

        except Exception:
            self._bd._conexion.rollback()
            raise

    def actualizar_meta(
        self,
        id_asignacion_ejercicio: int,
        veces_planificadas: int,
    ) -> bool:
        """
        Actualiza la meta total de un ejercicio asignado.
        """
        identificador = self._validar_id(
            id_asignacion_ejercicio,
            "El ID del ejercicio asignado",
        )

        if (
            isinstance(veces_planificadas, bool)
            or not isinstance(
                veces_planificadas,
                int,
            )
            or veces_planificadas <= 0
        ):
            raise ValueError(
                "Las veces planificadas deben ser un "
                "entero mayor que cero."
            )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE asignacion_rutina_ejercicios
                    SET veces_planificadas = %s
                    WHERE id_asignacion_ejercicio = %s
                    """,
                    (
                        veces_planificadas,
                        identificador,
                    ),
                )

                actualizado = cursor.rowcount > 0

            self._bd._conexion.commit()

            return actualizado

        except Exception:
            self._bd._conexion.rollback()
            raise

    def desactivar(
        self,
        id_asignacion_ejercicio: int,
    ) -> bool:
        """
        Retira un ejercicio del plan sin borrar su historial.
        """
        identificador = self._validar_id(
            id_asignacion_ejercicio,
            "El ID del ejercicio asignado",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE asignacion_rutina_ejercicios
                    SET activo = FALSE
                    WHERE id_asignacion_ejercicio = %s
                      AND activo = TRUE
                    """,
                    (identificador,),
                )

                actualizado = cursor.rowcount > 0

            self._bd._conexion.commit()

            return actualizado

        except Exception:
            self._bd._conexion.rollback()
            raise

    def activar(
        self,
        id_asignacion_ejercicio: int,
    ) -> bool:
        """
        Reactiva un ejercicio retirado del plan.
        """
        identificador = self._validar_id(
            id_asignacion_ejercicio,
            "El ID del ejercicio asignado",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE asignacion_rutina_ejercicios
                    SET activo = TRUE
                    WHERE id_asignacion_ejercicio = %s
                      AND activo = FALSE
                    """,
                    (identificador,),
                )

                actualizado = cursor.rowcount > 0

            self._bd._conexion.commit()

            return actualizado

        except Exception:
            self._bd._conexion.rollback()
            raise

    def copiar_desde_rutina(
        self,
        id_asignacion: int,
        id_rutina: int,
        veces_planificadas: int = 1,
    ) -> int:
        """
        Copia los ejercicios de una plantilla global hacia
        una asignación individual.

        Devuelve el número de ejercicios insertados.
        """
        asignacion_id = self._validar_id(
            id_asignacion,
            "El ID de la asignación",
        )

        rutina_id = self._validar_id(
            id_rutina,
            "El ID de la rutina",
        )

        if (
            isinstance(veces_planificadas, bool)
            or not isinstance(
                veces_planificadas,
                int,
            )
            or veces_planificadas <= 0
        ):
            raise ValueError(
                "Las veces planificadas deben ser un "
                "entero mayor que cero."
            )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO asignacion_rutina_ejercicios (
                        id_asignacion,
                        id_ejercicio,
                        orden_ejercicio,
                        veces_planificadas,
                        activo
                    )
                    SELECT
                        %s,
                        re.id_ejercicio,
                        re.orden_ejercicio,
                        %s,
                        TRUE
                    FROM rutina_ejercicios AS re
                    WHERE re.id_rutina = %s
                    ORDER BY
                        re.orden_ejercicio,
                        re.id_ejercicio
                    ON CONFLICT (
                        id_asignacion,
                        id_ejercicio
                    ) DO NOTHING
                    """,
                    (
                        asignacion_id,
                        veces_planificadas,
                        rutina_id,
                    ),
                )

                insertados = cursor.rowcount

            self._bd._conexion.commit()

            return insertados

        except IntegrityError as error:
            self._bd._conexion.rollback()
            raise self._convertir_error_integridad(
                error
            ) from error

        except Exception:
            self._bd._conexion.rollback()
            raise

    def obtener_progreso(
        self,
        id_asignacion: int,
        solo_activos: bool = True,
    ) -> List[Dict]:
        """
        Devuelve el progreso acumulado de cada ejercicio de
        una asignación.

        El progreso se calcula sumando las veces realizadas
        en las sesiones vinculadas a cada ejercicio asignado.
        """
        asignacion_id = self._validar_id(
            id_asignacion,
            "El ID de la asignación",
        )

        self._bd.abrir_conexion()

        try:
            with self._bd._conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:
                consulta = """
                    SELECT
                        are.id_asignacion_ejercicio,
                        are.id_asignacion,
                        are.id_ejercicio,
                        e.nombre AS nombre_ejercicio,
                        are.orden_ejercicio,
                        are.veces_planificadas,
                        are.activo,
                        COALESCE(
                            SUM(se.veces_realizadas),
                            0
                        ) AS veces_realizadas,
                        (
                            COALESCE(
                                SUM(se.veces_realizadas),
                                0
                            ) >= are.veces_planificadas
                        ) AS completado
                    FROM asignacion_rutina_ejercicios AS are
                    INNER JOIN ejercicios AS e
                        ON e.id_ejercicio =
                           are.id_ejercicio
                    LEFT JOIN sesiones_entrenamiento AS se
                        ON se.id_asignacion_ejercicio =
                           are.id_asignacion_ejercicio
                    WHERE are.id_asignacion = %s
                """

                parametros = [asignacion_id]

                if solo_activos:
                    consulta += """
                        AND are.activo = TRUE
                    """

                consulta += """
                    GROUP BY
                        are.id_asignacion_ejercicio,
                        are.id_asignacion,
                        are.id_ejercicio,
                        e.nombre,
                        are.orden_ejercicio,
                        are.veces_planificadas,
                        are.activo
                    ORDER BY
                        are.orden_ejercicio,
                        are.id_asignacion_ejercicio
                """

                cursor.execute(
                    consulta,
                    tuple(parametros),
                )

                filas = cursor.fetchall()

            return [dict(fila) for fila in filas]

        except Exception:
            self._bd._conexion.rollback()
            raise

    def asignacion_esta_completada(
        self,
        id_asignacion: int,
    ) -> bool:
        """
        Indica si todos los ejercicios activos de una
        asignación alcanzaron su meta.

        Una asignación sin ejercicios activos no se
        considera completada.
        """
        progreso = self.obtener_progreso(
            id_asignacion=id_asignacion,
            solo_activos=True,
        )

        if not progreso:
            return False

        return all(
            bool(fila["completado"])
            for fila in progreso
        )

    @staticmethod
    def _crear_desde_fila(
        fila,
    ) -> AsignacionRutinaEjercicio:
        """
        Convierte una fila de PostgreSQL en una entidad.
        """
        datos = dict(fila)

        return AsignacionRutinaEjercicio(
            id_asignacion_ejercicio=datos.get(
                "id_asignacion_ejercicio"
            ),
            id_asignacion=datos["id_asignacion"],
            id_ejercicio=datos["id_ejercicio"],
            orden_ejercicio=datos["orden_ejercicio"],
            veces_planificadas=datos[
                "veces_planificadas"
            ],
            activo=datos["activo"],
            fecha_agregado=datos["fecha_agregado"],
        )

    @staticmethod
    def _validar_entidad(
        ejercicio_asignado: AsignacionRutinaEjercicio,
    ) -> None:
        """
        Valida una instancia antes de persistirla.
        """
        if not isinstance(
            ejercicio_asignado,
            AsignacionRutinaEjercicio,
        ):
            raise TypeError(
                "Debe proporcionar una instancia de "
                "AsignacionRutinaEjercicio."
            )

        AsignacionRutinaEjercicioDAO._validar_id(
            ejercicio_asignado.id_asignacion,
            "El ID de la asignación",
        )

        AsignacionRutinaEjercicioDAO._validar_id(
            ejercicio_asignado.id_ejercicio,
            "El ID del ejercicio",
        )

        if (
            isinstance(
                ejercicio_asignado.orden_ejercicio,
                bool,
            )
            or not isinstance(
                ejercicio_asignado.orden_ejercicio,
                int,
            )
            or ejercicio_asignado.orden_ejercicio <= 0
        ):
            raise ValueError(
                "El orden del ejercicio debe ser "
                "un entero mayor que cero."
            )

        if (
            isinstance(
                ejercicio_asignado.veces_planificadas,
                bool,
            )
            or not isinstance(
                ejercicio_asignado.veces_planificadas,
                int,
            )
            or ejercicio_asignado.veces_planificadas <= 0
        ):
            raise ValueError(
                "Las veces planificadas deben ser un "
                "entero mayor que cero."
            )

        if not isinstance(
            ejercicio_asignado.activo,
            bool,
        ):
            raise ValueError(
                "El campo activo debe ser booleano."
            )

    @staticmethod
    def _validar_id(
        valor: object,
        nombre: str,
    ) -> int:
        """
        Valida un identificador entero positivo.
        """
        if (
            valor is None
            or isinstance(valor, bool)
        ):
            raise ValueError(
                f"{nombre} debe ser un entero positivo."
            )

        try:
            identificador = int(valor)

        except (
            TypeError,
            ValueError,
        ) as error:
            raise ValueError(
                f"{nombre} debe ser un entero positivo."
            ) from error

        if identificador <= 0:
            raise ValueError(
                f"{nombre} debe ser un entero positivo."
            )

        return identificador

    @staticmethod
    def _convertir_error_integridad(
        error: IntegrityError,
    ) -> ValueError:
        """
        Convierte errores de PostgreSQL a mensajes de
        dominio comprensibles.
        """
        codigo = getattr(
            error,
            "pgcode",
            None,
        )

        if codigo == "23503":
            return ValueError(
                "La asignación o el ejercicio indicado "
                "no existe."
            )

        if codigo == "23505":
            return ValueError(
                "El ejercicio ya pertenece a esta "
                "asignación o el orden ya está ocupado."
            )

        if codigo == "23514":
            return ValueError(
                "Los datos no cumplen las restricciones "
                "del ejercicio asignado."
            )

        if codigo == "23502":
            return ValueError(
                "Falta un dato obligatorio."
            )

        return ValueError(
            "No se pudo guardar el ejercicio asignado."
        )