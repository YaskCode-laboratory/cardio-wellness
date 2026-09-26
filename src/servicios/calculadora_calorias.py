"""
Servicio para calcular calorías estimadas de sesiones
cardiovasculares.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Union

from src.modelos.enums import Intensidad


class CalculadoraCalorias:
    """
    Calcula calorías estimadas con peso, duración e
    intensidad real de ejercicios cardiovasculares.
    """

    MET_POR_INTENSIDAD = {
        Intensidad.BAJA: Decimal("3.5"),
        Intensidad.MEDIA: Decimal("5.5"),
        Intensidad.ALTA: Decimal("8.0"),
    }

    @classmethod
    def calcular_calorias_cardio(
        cls,
        peso_kg: Union[
            int,
            float,
            Decimal,
        ],
        duracion_minutos: int,
        intensidad: Union[
            Intensidad,
            str,
        ],
    ) -> Decimal:
        """
        Calcula calorías estimadas para una actividad cardio.

        Fórmula:
        MET × 3.5 × peso_kg × minutos / 200
        """
        peso = cls._normalizar_peso(
            peso_kg
        )

        duracion = cls._normalizar_duracion(
            duracion_minutos
        )

        intensidad_normalizada = (
            cls._normalizar_intensidad(
                intensidad
            )
        )

        met = cls.MET_POR_INTENSIDAD[
            intensidad_normalizada
        ]

        calorias = (
            met
            * Decimal("3.5")
            * peso
            * Decimal(duracion)
            / Decimal("200")
        )

        return calorias.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @staticmethod
    def _normalizar_peso(
        peso_kg: Union[
            int,
            float,
            Decimal,
        ],
    ) -> Decimal:
        """
        Valida y convierte el peso a Decimal.
        """
        if isinstance(peso_kg, bool):
            raise ValueError(
                "El peso debe ser numérico."
            )

        try:
            peso = Decimal(
                str(peso_kg)
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError,
        ) as error:
            raise ValueError(
                "El peso no es válido."
            ) from error

        if peso <= Decimal("0"):
            raise ValueError(
                "El peso debe ser mayor que cero."
            )

        return peso

    @staticmethod
    def _normalizar_duracion(
        duracion_minutos: int,
    ) -> int:
        """
        Valida la duración de la sesión.
        """
        if (
            isinstance(duracion_minutos, bool)
            or not isinstance(
                duracion_minutos,
                int,
            )
            or duracion_minutos <= 0
        ):
            raise ValueError(
                "La duración debe ser un entero "
                "mayor que cero."
            )

        return duracion_minutos

    @staticmethod
    def _normalizar_intensidad(
        intensidad: Union[
            Intensidad,
            str,
        ],
    ) -> Intensidad:
        """
        Convierte texto o enum a Intensidad.
        """
        if isinstance(
            intensidad,
            Intensidad,
        ):
            return intensidad

        if not isinstance(
            intensidad,
            str,
        ):
            raise ValueError(
                "La intensidad debe ser BAJA, "
                "MEDIA o ALTA."
            )

        texto = intensidad.strip().upper()

        try:
            return Intensidad[texto]

        except KeyError:
            try:
                return Intensidad(texto)

            except ValueError as error:
                raise ValueError(
                    "La intensidad debe ser BAJA, "
                    "MEDIA o ALTA."
                ) from error