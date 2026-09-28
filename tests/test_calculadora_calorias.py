from decimal import Decimal

import pytest

from src.modelos.enums import Intensidad
from src.servicios.calculadora_calorias import (
    CalculadoraCalorias,
)


@pytest.mark.parametrize(
    "tipo, intensidad, met_esperado",
    [
        ("CARDIO", "BAJA", Decimal("3.5")),
        ("cardio", "MEDIA", Decimal("5.5")),
        ("FUERZA", Intensidad.ALTA, Decimal("6.0")),
        ("FLEXIBILIDAD", "MEDIA", Decimal("2.8")),
        ("HIIT", "ALTA", Decimal("9.0")),
        ("LISS", "MEDIA", Decimal("5.5")),
        ("Cardio funcional", "ALTA", Decimal("8.0")),
        ("pesas", "BAJA", Decimal("3.0")),
        ("MUSCULACIÓN", "MEDIA", Decimal("4.5")),
        ("estiramientos", "ALTA", Decimal("3.5")),
        ("movilidad", "BAJA", Decimal("2.3")),
        ("circuito", "MEDIA", Decimal("7.0")),
        ("intervalos", "ALTA", Decimal("9.0")),
    ],
)
def test_obtener_met_para_tipos_intensidades_y_alias(
    tipo,
    intensidad,
    met_esperado,
):
    resultado = CalculadoraCalorias.obtener_met(
        tipo,
        intensidad,
    )

    assert resultado == met_esperado


def test_calcular_calorias_calcula_y_redondea_a_dos_decimales():
    resultado = CalculadoraCalorias.calcular_calorias(
        peso_kg=70,
        duracion_minutos=30,
        tipo_ejercicio="CARDIO",
        intensidad="MEDIA",
    )

    assert resultado == Decimal("202.13")


@pytest.mark.parametrize(
    "peso",
    [
        70,
        70.5,
        Decimal("70.5"),
        "70.5",
    ],
)
def test_calcular_calorias_acepta_pesos_numericos_validos(
    peso,
):
    resultado = CalculadoraCalorias.calcular_calorias(
        peso_kg=peso,
        duracion_minutos=20,
        tipo_ejercicio="HIIT",
        intensidad=Intensidad.ALTA,
    )

    assert isinstance(resultado, Decimal)
    assert resultado > Decimal("0")


def test_calcular_calorias_cardio_delega_en_calculo_general():
    resultado = CalculadoraCalorias.calcular_calorias_cardio(
        peso_kg=70,
        duracion_minutos=30,
        intensidad="MEDIA",
    )

    esperado = CalculadoraCalorias.calcular_calorias(
        peso_kg=70,
        duracion_minutos=30,
        tipo_ejercicio="CARDIO",
        intensidad="MEDIA",
    )

    assert resultado == esperado
    assert resultado == Decimal("202.13")


@pytest.mark.parametrize(
    "tipo, mensaje",
    [
        (None, "El tipo de ejercicio debe ser texto"),
        (123, "El tipo de ejercicio debe ser texto"),
        (True, "El tipo de ejercicio debe ser texto"),
        ("", "El tipo de ejercicio es obligatorio"),
        ("   ", "El tipo de ejercicio es obligatorio"),
        (
            "DESCONOCIDO",
            "Tipo de ejercicio no soportado para el cálculo",
        ),
    ],
)
def test_normalizar_tipo_rechaza_entradas_invalidas(
    tipo,
    mensaje,
):
    with pytest.raises(ValueError, match=mensaje):
        CalculadoraCalorias._normalizar_tipo(tipo)


@pytest.mark.parametrize(
    "tipo, esperado",
    [
        (" cardio ", "CARDIO"),
        ("aerobico", "CARDIO"),
        ("aeróbico", "CARDIO"),
        ("liss", "CARDIO"),
        ("fuerzas", "FUERZA"),
        ("pesas", "FUERZA"),
        ("musculacion", "FUERZA"),
        ("estiramiento", "FLEXIBILIDAD"),
        ("movilidad", "FLEXIBILIDAD"),
        ("circuito", "HIIT"),
    ],
)
def test_normalizar_tipo_aplica_aliases(
    tipo,
    esperado,
):
    assert (
        CalculadoraCalorias._normalizar_tipo(tipo)
        == esperado
    )


@pytest.mark.parametrize(
    "peso, mensaje",
    [
        (True, "El peso debe ser numérico"),
        (False, "El peso debe ser numérico"),
        (None, "El peso no es válido"),
        ("peso-invalido", "El peso no es válido"),
        (object(), "El peso no es válido"),
        (0, "El peso debe ser mayor que cero"),
        (0.0, "El peso debe ser mayor que cero"),
        (-1, "El peso debe ser mayor que cero"),
        (Decimal("-0.01"), "El peso debe ser mayor que cero"),
    ],
)
def test_normalizar_peso_rechaza_valores_invalidos(
    peso,
    mensaje,
):
    with pytest.raises(ValueError, match=mensaje):
        CalculadoraCalorias._normalizar_peso(peso)


@pytest.mark.parametrize(
    "peso, esperado",
    [
        (70, Decimal("70")),
        (70.5, Decimal("70.5")),
        ("70.50", Decimal("70.50")),
        (Decimal("80.25"), Decimal("80.25")),
    ],
)
def test_normalizar_peso_convierte_a_decimal(
    peso,
    esperado,
):
    assert (
        CalculadoraCalorias._normalizar_peso(peso)
        == esperado
    )


@pytest.mark.parametrize(
    "duracion",
    [
        None,
        True,
        False,
        "30",
        30.0,
        0,
        -1,
    ],
)
def test_normalizar_duracion_rechaza_valores_invalidos(
    duracion,
):
    with pytest.raises(
        ValueError,
        match="La duración debe ser un entero mayor que cero",
    ):
        CalculadoraCalorias._normalizar_duracion(duracion)


@pytest.mark.parametrize(
    "duracion",
    [
        1,
        30,
        120,
    ],
)
def test_normalizar_duracion_acepta_enteros_positivos(
    duracion,
):
    assert (
        CalculadoraCalorias._normalizar_duracion(duracion)
        == duracion
    )


@pytest.mark.parametrize(
    "intensidad, esperado",
    [
        (Intensidad.BAJA, Intensidad.BAJA),
        (Intensidad.MEDIA, Intensidad.MEDIA),
        (Intensidad.ALTA, Intensidad.ALTA),
        ("BAJA", Intensidad.BAJA),
        (" media ", Intensidad.MEDIA),
        ("alta", Intensidad.ALTA),
    ],
)
def test_normalizar_intensidad_acepta_enum_y_texto(
    intensidad,
    esperado,
):
    assert (
        CalculadoraCalorias._normalizar_intensidad(
            intensidad
        )
        == esperado
    )


@pytest.mark.parametrize(
    "intensidad",
    [
        None,
        1,
        True,
        "",
        "MEDIA-ALTA",
        "INVALIDA",
    ],
)
def test_normalizar_intensidad_rechaza_valores_invalidos(
    intensidad,
):
    with pytest.raises(
        ValueError,
        match="La intensidad debe ser BAJA, MEDIA o ALTA",
    ):
        CalculadoraCalorias._normalizar_intensidad(
            intensidad
        )


def test_calcular_calorias_propaga_validaciones_de_entrada():
    with pytest.raises(
        ValueError,
        match="El peso debe ser mayor que cero",
    ):
        CalculadoraCalorias.calcular_calorias(
            peso_kg=0,
            duracion_minutos=30,
            tipo_ejercicio="CARDIO",
            intensidad="MEDIA",
        )

    with pytest.raises(
        ValueError,
        match="La duración debe ser un entero mayor que cero",
    ):
        CalculadoraCalorias.calcular_calorias(
            peso_kg=70,
            duracion_minutos=0,
            tipo_ejercicio="CARDIO",
            intensidad="MEDIA",
        )

    with pytest.raises(
        ValueError,
        match="Tipo de ejercicio no soportado",
    ):
        CalculadoraCalorias.calcular_calorias(
            peso_kg=70,
            duracion_minutos=30,
            tipo_ejercicio="NATACION",
            intensidad="MEDIA",
        )