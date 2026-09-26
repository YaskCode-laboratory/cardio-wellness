"""
Controlador para la gestión de sesiones de entrenamiento.
"""

from src.persistencia.cliente_dao import ClienteDAO
from src.persistencia.ejercicio_dao import EjercicioDAO
from src.servicios.calculadora_calorias import (
    CalculadoraCalorias,
)
from datetime import date, datetime
from decimal import Decimal
from typing import Any, List, Optional, Union


from src.controladores.control_base import ControlBase
from src.modelos.enums import Intensidad
from src.modelos.sesion_entrenamiento import (
    SesionEntrenamiento,
)
from src.persistencia.asignacion_rutina_dao import (
    AsignacionRutinaDAO,
)
from src.persistencia.asignacion_rutina_ejercicio_dao import (
    AsignacionRutinaEjercicioDAO,
)
from src.persistencia.sesion_entrenamiento_dao import (
    SesionEntrenamientoDAO,
)



class ControlSesiones(ControlBase):
    """
    Controlador para registrar, consultar y eliminar
    sesiones de entrenamiento.
    """

    def __init__(
        self,
        sesion_dao: Optional[
            SesionEntrenamientoDAO
        ] = None,
        ruta_log: str = "logs/LOG_CARDIO.txt",
        asignacion_dao: Optional[
            AsignacionRutinaDAO
        ] = None,
        asignacion_ejercicio_dao: Optional[
            AsignacionRutinaEjercicioDAO
        ] = None,
        cliente_dao: Optional[ClienteDAO] = None,
        ejercicio_dao: Optional[EjercicioDAO] = None,
    ) -> None:
        super().__init__(
            ruta_log=ruta_log,
        )

        self.sesion_dao = (
            sesion_dao
            if sesion_dao is not None
            else SesionEntrenamientoDAO()
        )

        self.asignacion_dao = (
            asignacion_dao
            if asignacion_dao is not None
            else AsignacionRutinaDAO()
        )

        self.asignacion_ejercicio_dao = (
            asignacion_ejercicio_dao
            if asignacion_ejercicio_dao is not None
            else AsignacionRutinaEjercicioDAO()
        )

        self.cliente_dao = (
            cliente_dao
            if cliente_dao is not None
            else ClienteDAO()
        )

        self.ejercicio_dao = (
            ejercicio_dao
            if ejercicio_dao is not None
            else EjercicioDAO()
        )

    def registrar_sesion(
        self,
        cliente: Any,
        rutina: Any,
        duracion_real: int,
        intensidad_real: Union[
            Intensidad,
            str,
        ],
        calorias_quemadas: Optional[
            Union[
                int,
                float,
                Decimal,
            ]
        ] = None,
        observaciones: str = "",
        fecha: Optional[
            Union[
                date,
                datetime,
            ]
        ] = None,
        nombre_ejercicio: str = "",
        veces_planificadas: int = 1,
        veces_realizadas: int = 0,
        id_asignacion_ejercicio: Optional[int] = None,
    ) -> SesionEntrenamiento:
        """
        Registra una sesión diaria.

        Si se recibe id_asignacion_ejercicio, la sesión se
        vincula al plan individual activo del cliente. Luego
        se recalcula el progreso y se finaliza la asignación
        automáticamente si todos sus ejercicios activos
        alcanzaron la meta.
        """
        id_cliente = self._extraer_id(
            cliente,
            "id_usuario",
            "id_cliente",
            "id",
        )

        id_rutina = self._extraer_id(
            rutina,
            "id_rutina",
            "id",
        )

        if id_cliente is None or id_cliente <= 0:
            raise ValueError(
                "El ID del cliente debe ser un entero "
                "positivo."
            )

        if id_rutina is None or id_rutina <= 0:
            raise ValueError(
                "El ID de rutina debe ser un entero "
                "positivo."
            )

        if not isinstance(
            nombre_ejercicio,
            str,
        ):
            raise ValueError(
                "El nombre del ejercicio debe ser texto."
            )

        nombre_ejercicio = nombre_ejercicio.strip()

        if not nombre_ejercicio:
            raise ValueError(
                "El nombre del ejercicio es obligatorio."
            )

        if len(nombre_ejercicio) > 100:
            raise ValueError(
                "El nombre del ejercicio no puede "
                "superar 100 caracteres."
            )

        if (
            isinstance(duracion_real, bool)
            or not isinstance(duracion_real, int)
            or duracion_real <= 0
        ):
            raise ValueError(
                "La duración real debe ser un entero "
                "positivo."
            )

        cliente_actual = self.cliente_dao.buscar_por_id(
            id_cliente
        )

        if cliente_actual is None:
            raise ValueError(
                "No se encontró el cliente para calcular "
                "las calorías estimadas."
            )

        peso_cliente = getattr(
            cliente_actual,
            "peso",
            None,
        )

        if peso_cliente is None:
            raise ValueError(
                "El cliente no tiene un peso registrado. "
                "Actualice el peso antes de registrar "
                "una sesión."
            )


        veces_planificadas = self._validar_cantidad(
            veces_planificadas,
            "Las veces planificadas",
            minimo=1,
        )

        veces_realizadas = self._validar_cantidad(
            veces_realizadas,
            "Las veces realizadas",
            minimo=0,
        )

        if veces_realizadas > veces_planificadas:
            raise ValueError(
                "Las veces realizadas no pueden "
                "superar las planificadas."
            )


        fecha_sesion = (
            fecha
            if fecha is not None
            else date.today()
        )

        if isinstance(fecha_sesion, datetime):
            fecha_sesion = fecha_sesion.date()

        if not isinstance(fecha_sesion, date):
            raise ValueError(
                "La fecha debe ser un objeto date."
            )

        id_asignacion: Optional[int] = None

        if id_asignacion_ejercicio is not None:
            id_asignacion_ejercicio = self._validar_id(
                id_asignacion_ejercicio,
                "ejercicio asignado",
            )

            asignacion = (
                self.asignacion_dao.buscar_activa(
                    id_cliente
                )
            )

            if asignacion is None:
                raise ValueError(
                    "El cliente no tiene una rutina activa."
                )

            if asignacion.id_rutina != id_rutina:
                raise ValueError(
                    "La rutina indicada no coincide con "
                    "la rutina activa del cliente."
                )

            ejercicio_asignado = (
                self.asignacion_ejercicio_dao.buscar_por_id(
                    id_asignacion_ejercicio
                )
            )

            if ejercicio_asignado is None:
                raise ValueError(
                    "El ejercicio asignado no existe."
                )

            if not ejercicio_asignado.activo:
                raise ValueError(
                    "El ejercicio asignado está inactivo."
                )

            if (
                ejercicio_asignado.id_asignacion
                != asignacion.id_asignacion
            ):
                raise ValueError(
                    "El ejercicio no pertenece a la "
                    "rutina activa del cliente."
                )

            ejercicio = self.ejercicio_dao.buscar_por_id(
                ejercicio_asignado.id_ejercicio
            )

            if ejercicio is None:
                raise ValueError(
                    "No se encontró el ejercicio asociado "
                    "a la rutina activa."
                )

            tipo_ejercicio = getattr(
                ejercicio,
                "tipo",
                None,
            )

            if (
                not isinstance(tipo_ejercicio, str)
                or not tipo_ejercicio.strip()
            ):
                raise ValueError(
                    "El ejercicio no tiene un tipo válido "
                    "para calcular las calorías."
                )

            id_asignacion = asignacion.id_asignacion

        if id_asignacion_ejercicio is None:
            tipo_ejercicio = "CARDIO"

        intensidad = self._normalizar_intensidad(
            intensidad_real
        )

        calorias = CalculadoraCalorias.calcular_calorias(
            peso_kg=peso_cliente,
            duracion_minutos=duracion_real,
            tipo_ejercicio=tipo_ejercicio,
            intensidad=intensidad,
        )

        sesion = SesionEntrenamiento(
            id_cliente=id_cliente,
            id_rutina=id_rutina,
            id_asignacion=id_asignacion,
            id_asignacion_ejercicio=(
                id_asignacion_ejercicio
            ),
            fecha=fecha_sesion,
            nombre_ejercicio=nombre_ejercicio,
            duracion_real=duracion_real,
            intensidad_real=intensidad,
            calorias_quemadas=calorias,
            observaciones=observaciones or "",
            veces_planificadas=veces_planificadas,
            veces_realizadas=veces_realizadas,
        )

        try:
            sesion_guardada = self.sesion_dao.guardar(
                sesion
            )

            rutina_finalizada = False

            if id_asignacion is not None:
                rutina_completada = (
                    self.asignacion_ejercicio_dao
                    .asignacion_esta_completada(
                        id_asignacion
                    )
                )

                if rutina_completada:
                    rutina_finalizada = (
                        self.asignacion_dao
                        .finalizar_asignacion(
                            id_asignacion
                        )
                    )

                    if rutina_finalizada:
                        self._registrar_log(
                            f"CLIENTE_{id_cliente}",
                            (
                                "FINALIZACION_AUTOMATICA_RUTINA "
                                f"Asignacion: {id_asignacion}, "
                                f"Rutina: {id_rutina}"
                            ),
                        )

            mensaje_log = (
                f"Rutina: {id_rutina}, "
                f"Ejercicio: {nombre_ejercicio}, "
                f"Duración: {duracion_real} min, "
                f"Intensidad: {intensidad.value}, "
                f"Calorías estimadas: "
                f"{calorias:.2f} kcal, "
                f"Realizadas: "
                f"{veces_realizadas}/"
                f"{veces_planificadas}"
            )

            if id_asignacion is not None:
                mensaje_log += (
                    f", Asignacion: {id_asignacion}, "
                    "EjercicioAsignado: "
                    f"{id_asignacion_ejercicio}"
                )

            if rutina_finalizada:
                mensaje_log += (
                    ", RutinaFinalizada: True"
                )

            self._registrar_log(
                f"CLIENTE_{id_cliente}",
                "REGISTRO_SESION",
                mensaje_log,
            )

            return sesion_guardada

        except ValueError as error:
            raise ValueError(
                f"Error al registrar la sesión: {error}"
            ) from error

        except Exception as error:
            raise RuntimeError(
                "Error inesperado al registrar "
                f"la sesión: {error}"
            ) from error

    def actualizar_sesion(
        self,
        sesion: SesionEntrenamiento,
        usuario_accion: Optional[str] = None,
    ) -> SesionEntrenamiento:
        """
        Actualiza una sesión existente.
        """
        if not isinstance(
            sesion,
            SesionEntrenamiento,
        ):
            raise TypeError(
                "Debe proporcionar una instancia "
                "de SesionEntrenamiento."
            )

        if sesion.id_sesion is None:
            raise ValueError(
                "La sesión debe tener un ID."
            )

        self._validar_cantidad(
            sesion.veces_planificadas,
            "Las veces planificadas",
            minimo=1,
        )

        self._validar_cantidad(
            sesion.veces_realizadas,
            "Las veces realizadas",
            minimo=0,
        )

        if (
            sesion.veces_realizadas
            > sesion.veces_planificadas
        ):
            raise ValueError(
                "Las veces realizadas no pueden "
                "superar las planificadas."
            )

        try:
            resultado = self.sesion_dao.actualizar(
                sesion
            )

            self._registrar_log(
                usuario_accion
                or f"SESION_{sesion.id_sesion}",
                "ACTUALIZACION_SESION",
            )

            return resultado

        except ValueError as error:
            raise ValueError(
                f"Error al actualizar la sesión: {error}"
            ) from error

        except Exception as error:
            raise RuntimeError(
                "Error inesperado al actualizar "
                f"la sesión: {error}"
            ) from error

    def obtener_sesiones_cliente(
        self,
        id_cliente: int,
    ) -> List[SesionEntrenamiento]:
        """
        Obtiene las sesiones de un cliente.
        """
        id_cliente_validado = self._validar_id(
            id_cliente,
            "cliente",
        )

        self._registrar_log(
            f"CLIENTE_{id_cliente_validado}",
            "CONSULTA_SESIONES",
        )

        try:
            sesiones = self.sesion_dao.listar_por_cliente(
                id_cliente_validado
            )

            return sesiones or []

        except Exception as error:
            raise RuntimeError(
                "Error al consultar las sesiones: "
                f"{error}"
            ) from error

    def listar_por_cliente(
        self,
        id_cliente: int,
    ) -> List[SesionEntrenamiento]:
        """
        Alias de obtener_sesiones_cliente().
        """
        return self.obtener_sesiones_cliente(
            id_cliente
        )

    def buscar_por_id(
        self,
        id_sesion: int,
    ) -> Optional[SesionEntrenamiento]:
        """
        Busca una sesión por ID.
        """
        id_validado = self._validar_id(
            id_sesion,
            "sesión",
        )

        try:
            return self.sesion_dao.buscar_por_id(
                id_validado
            )

        except Exception as error:
            raise RuntimeError(
                "Error al buscar la sesión: "
                f"{error}"
            ) from error

    def obtener_por_id(
        self,
        id_sesion: int,
    ) -> Optional[SesionEntrenamiento]:
        """
        Alias para buscar por ID.
        """
        return self.buscar_por_id(id_sesion)

    def eliminar_sesion(
        self,
        id_sesion: int,
        usuario_accion: Optional[str] = None,
    ) -> bool:
        """
        Elimina una sesión por ID.
        """
        id_validado = self._validar_id(
            id_sesion,
            "sesión",
        )

        try:
            resultado = self.sesion_dao.eliminar_por_id(
                id_validado
            )

            if resultado:
                self._registrar_log(
                    usuario_accion
                    or f"SESION_{id_validado}",
                    "ELIMINACION_SESION",
                )

            return resultado

        except ValueError as error:
            raise ValueError(
                f"Error al eliminar la sesión: {error}"
            ) from error

        except Exception as error:
            raise RuntimeError(
                "Error inesperado al eliminar "
                f"la sesión: {error}"
            ) from error

    def contar_sesiones_completadas(
        self,
        id_cliente: int,
        fecha: Optional[date] = None,
    ) -> int:
        """
        Cuenta sesiones completadas de un cliente.
        """
        cliente_id = self._validar_id(
            id_cliente,
            "cliente",
        )

        sesiones = self.sesion_dao.listar_por_cliente(
            cliente_id
        )

        if fecha is None:
            fecha = date.today()

        return sum(
            1
            for sesion in sesiones
            if sesion.fecha == fecha
            and sesion.completada
        )

    def porcentaje_cumplimiento_sesion(
        self,
        sesion: SesionEntrenamiento,
    ) -> float:
        """
        Calcula el porcentaje de cumplimiento de una sesión.
        """
        if not isinstance(
            sesion,
            SesionEntrenamiento,
        ):
            raise TypeError(
                "La sesión no es válida."
            )

        porcentaje = sesion.porcentaje_cumplimiento

        if callable(porcentaje):
            porcentaje = porcentaje()

        return float(porcentaje)

    @staticmethod
    def _extraer_id(
        objeto: Any,
        *campos: str,
    ) -> Optional[int]:
        """
        Extrae un ID desde un entero, diccionario
        u objeto.
        """
        if isinstance(
            objeto,
            bool,
        ):
            return None

        if isinstance(
            objeto,
            int,
        ):
            return objeto

        if isinstance(
            objeto,
            dict,
        ):
            for campo in campos:
                if campo in objeto:
                    return ControlSesiones._convertir_id(
                        objeto[campo]
                    )

            return None

        for campo in campos:
            if hasattr(
                objeto,
                campo,
            ):
                return ControlSesiones._convertir_id(
                    getattr(
                        objeto,
                        campo,
                    )
                )

        return None

    @staticmethod
    def _convertir_id(
        valor: Any,
    ) -> Optional[int]:
        """
        Convierte un valor a ID entero.
        """
        if valor is None or isinstance(
            valor,
            bool,
        ):
            return None

        try:
            return int(valor)

        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _validar_id(
        valor: Any,
        nombre: str,
    ) -> int:
        """
        Valida un ID positivo.
        """
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
            or valor <= 0
        ):
            raise ValueError(
                f"El ID de {nombre} debe ser un "
                "entero positivo."
            )

        return valor

    @staticmethod
    def _validar_cantidad(
        valor: Any,
        nombre: str,
        minimo: int,
    ) -> int:
        """
        Valida una cantidad entera.
        """
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
        ):
            raise ValueError(
                f"{nombre} debe ser un entero."
            )

        if valor < minimo:
            raise ValueError(
                f"{nombre} debe ser mayor o igual "
                f"a {minimo}."
            )

        return valor

    @staticmethod
    def _normalizar_intensidad(
        valor: Union[
            Intensidad,
            str,
        ],
    ) -> Intensidad:
        """
        Convierte texto o enum a Intensidad.
        """
        if isinstance(
            valor,
            Intensidad,
        ):
            return valor

        if not isinstance(
            valor,
            str,
        ):
            raise ValueError(
                "La intensidad debe ser BAJA, "
                "MEDIA o ALTA."
            )

        texto = valor.strip().upper()

        try:
            return Intensidad[texto]

        except KeyError:
            try:
                return Intensidad(texto)

            except ValueError as error:
                raise ValueError(
                    "Intensidad inválida. Debe ser "
                    "BAJA, MEDIA o ALTA."
                ) from error