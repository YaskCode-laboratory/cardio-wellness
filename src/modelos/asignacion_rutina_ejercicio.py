from datetime import date
from typing import Optional


class AsignacionRutinaEjercicio:
    """
    Representa un ejercicio individual dentro de una
    asignación de rutina.

    A diferencia de Rutina/EjercicioCardio, esta entidad
    pertenece a una asignación concreta de un cliente y
    permite establecer orden y meta propios.
    """

    def __init__(
        self,
        id_asignacion: int,
        id_ejercicio: int,
        orden_ejercicio: int,
        veces_planificadas: int = 1,
        activo: bool = True,
        fecha_agregado: Optional[date] = None,
        id_asignacion_ejercicio: Optional[int] = None,
    ) -> None:
        self.id_asignacion_ejercicio = (
            id_asignacion_ejercicio
        )
        self.id_asignacion = id_asignacion
        self.id_ejercicio = id_ejercicio
        self.orden_ejercicio = orden_ejercicio
        self.veces_planificadas = veces_planificadas
        self.activo = activo
        self.fecha_agregado = fecha_agregado

    @property
    def id_asignacion_ejercicio(self) -> Optional[int]:
        return self._id_asignacion_ejercicio

    @id_asignacion_ejercicio.setter
    def id_asignacion_ejercicio(
        self,
        valor: Optional[int],
    ) -> None:
        if valor is not None:
            self._validar_id(
                valor,
                "El ID del ejercicio asignado",
            )

        self._id_asignacion_ejercicio = valor

    @property
    def id_asignacion(self) -> int:
        return self._id_asignacion

    @id_asignacion.setter
    def id_asignacion(
        self,
        valor: int,
    ) -> None:
        self._validar_id(
            valor,
            "El ID de la asignación",
        )

        self._id_asignacion = valor

    @property
    def id_ejercicio(self) -> int:
        return self._id_ejercicio

    @id_ejercicio.setter
    def id_ejercicio(
        self,
        valor: int,
    ) -> None:
        self._validar_id(
            valor,
            "El ID del ejercicio",
        )

        self._id_ejercicio = valor

    @property
    def orden_ejercicio(self) -> int:
        return self._orden_ejercicio

    @orden_ejercicio.setter
    def orden_ejercicio(
        self,
        valor: int,
    ) -> None:
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
            or valor <= 0
        ):
            raise ValueError(
                "El orden del ejercicio debe ser "
                "un entero mayor que cero."
            )

        self._orden_ejercicio = valor

    @property
    def veces_planificadas(self) -> int:
        return self._veces_planificadas

    @veces_planificadas.setter
    def veces_planificadas(
        self,
        valor: int,
    ) -> None:
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
            or valor <= 0
        ):
            raise ValueError(
                "Las veces planificadas deben ser "
                "un entero mayor que cero."
            )

        self._veces_planificadas = valor

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(
        self,
        valor: bool,
    ) -> None:
        if not isinstance(valor, bool):
            raise ValueError(
                "El estado activo debe ser booleano."
            )

        self._activo = valor

    @property
    def fecha_agregado(self) -> date:
        return self._fecha_agregado

    @fecha_agregado.setter
    def fecha_agregado(
        self,
        valor: Optional[date],
    ) -> None:
        if valor is not None and not isinstance(
            valor,
            date,
        ):
            raise ValueError(
                "La fecha de agregado no es válida."
            )

        self._fecha_agregado = (
            valor
            if valor is not None
            else date.today()
        )

    def actualizar_meta(
        self,
        veces_planificadas: int,
    ) -> None:
        """
        Cambia la meta total del ejercicio para esta
        asignación específica.
        """
        self.veces_planificadas = veces_planificadas

    def cambiar_orden(
        self,
        orden_ejercicio: int,
    ) -> None:
        """
        Cambia la posición del ejercicio dentro del plan.
        """
        self.orden_ejercicio = orden_ejercicio

    def desactivar(self) -> None:
        """
        Retira el ejercicio del plan activo sin borrar
        su registro histórico.
        """
        self.activo = False

    def activar(self) -> None:
        """
        Reactiva un ejercicio previamente retirado.
        """
        self.activo = True

    @staticmethod
    def _validar_id(
        valor: int,
        nombre: str,
    ) -> None:
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
            or valor <= 0
        ):
            raise ValueError(
                f"{nombre} debe ser un entero positivo."
            )

    def __repr__(self) -> str:
        return (
            "AsignacionRutinaEjercicio("
            "id_asignacion_ejercicio="
            f"{self.id_asignacion_ejercicio}, "
            f"id_asignacion={self.id_asignacion}, "
            f"id_ejercicio={self.id_ejercicio}, "
            f"orden_ejercicio={self.orden_ejercicio}, "
            "veces_planificadas="
            f"{self.veces_planificadas}, "
            f"activo={self.activo}, "
            f"fecha_agregado={self.fecha_agregado}"
            ")"
        )