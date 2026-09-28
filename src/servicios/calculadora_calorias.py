"""
Servicio para calcular calorías estimadas de sesiones de
entrenamiento según peso, duración, tipo e intensidad.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Union

from src.modelos.enums import Intensidad


class CalculadoraCalorias:
    """
    Calcula calorías estimadas usando valores MET de
    referencia según el tipo e intensidad del ejercicio.
    """

    MET_POR_TIPO_E_INTENSIDAD = {
        "CARDIO": {
            Intensidad.BAJA: Decimal("3.5"),
            Intensidad.MEDIA: Decimal("5.5"),
            Intensidad.ALTA: Decimal("8.0"),
        },
        "FUERZA": {
            Intensidad.BAJA: Decimal("3.0"),
            Intensidad.MEDIA: Decimal("4.5"),
            Intensidad.ALTA: Decimal("6.0"),
        },
        "FLEXIBILIDAD": {
            Intensidad.BAJA: Decimal("2.3"),
            Intensidad.MEDIA: Decimal("2.8"),
            Intensidad.ALTA: Decimal("3.5"),
        },
        "HIIT": {
            Intensidad.BAJA: Decimal("5.0"),
            Intensidad.MEDIA: Decimal("7.0"),
            Intensidad.ALTA: Decimal("9.0"),
        },
    }

    ALIAS_TIPOS = {
        "CARDIOVASCULAR": "CARDIO",
        "AEROBICO": "CARDIO",
        "AERÓBICO": "CARDIO",
        "LISS": "CARDIO",
        "CARDIO FUNCIONAL": "CARDIO",
        "FUERZAS": "FUERZA",
        "PESAS": "FUERZA",
        "MUSCULACION": "FUERZA",
        "MUSCULACIÓN": "FUERZA",
        "ESTIRAMIENTO": "FLEXIBILIDAD",
        "ESTIRAMIENTOS": "FLEXIBILIDAD",
        "MOVILIDAD": "FLEXIBILIDAD",
        "CIRCUITO": "HIIT",
        "INTERVALOS": "HIIT",
    }

    @classmethod
    def calcular_calorias(
        cls,
        peso_kg: Union[
            int,
            float,
            Decimal,
        ],
        duracion_minutos: int,
        tipo_ejercicio: str,
        intensidad: Union[
            Intensidad,
            str,
        ],
    ) -> Decimal:
        """
        Calcula calorías estimadas.

        Fórmula:
        MET × 3.5 × peso_kg × duración_minutos / 200
        """
        peso = cls._normalizar_peso(
            peso_kg
        )

        duracion = cls._normalizar_duracion(
            duracion_minutos
        )

        tipo = cls._normalizar_tipo(
            tipo_ejercicio
        )

        intensidad_normalizada = (
            cls._normalizar_intensidad(
                intensidad
            )
        )

        met = cls.MET_POR_TIPO_E_INTENSIDAD[
            tipo
        ][intensidad_normalizada]

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
        Alias compatible para cálculos de cardio.
        """
        return cls.calcular_calorias(
            peso_kg=peso_kg,
            duracion_minutos=duracion_minutos,
            tipo_ejercicio="CARDIO",
            intensidad=intensidad,
        )

    @classmethod
    def obtener_met(
        cls,
        tipo_ejercicio: str,
        intensidad: Union[
            Intensidad,
            str,
        ],
    ) -> Decimal:
        """
        Devuelve el MET asignado al tipo e intensidad.
        """
        tipo = cls._normalizar_tipo(
            tipo_ejercicio
        )

        intensidad_normalizada = (
            cls._normalizar_intensidad(
                intensidad
            )
        )

        return cls.MET_POR_TIPO_E_INTENSIDAD[
            tipo
        ][intensidad_normalizada]

    @classmethod
    def _normalizar_tipo(
        cls,
        tipo_ejercicio: str,
    ) -> str:
        """
        Normaliza el tipo de ejercicio.
        """
        if not isinstance(
            tipo_ejercicio,
            str,
        ):
            raise ValueError(
                "El tipo de ejercicio debe ser texto."
            )

        tipo = tipo_ejercicio.strip().upper()

        if not tipo:
            raise ValueError(
                "El tipo de ejercicio es obligatorio."
            )

        tipo = cls.ALIAS_TIPOS.get(
            tipo,
            tipo,
        )

        if tipo not in cls.MET_POR_TIPO_E_INTENSIDAD:
            tipos_validos = ", ".join(
                cls.MET_POR_TIPO_E_INTENSIDAD.keys()
            )

            raise ValueError(
                "Tipo de ejercicio no soportado para "
                f"el cálculo de calorías: {tipo}. "
                f"Tipos válidos: {tipos_validos}."
            )

        return tipo

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