from datetime import date
from unittest.mock import patch

import pytest

from src.modelos.asignacion_rutina_ejercicio import (
    AsignacionRutinaEjercicio,
)


@pytest.fixture
def asignacion():
    return AsignacionRutinaEjercicio(
        id_asignacion=1,
        id_ejercicio=2,
        orden_ejercicio=3,
        veces_planificadas=4,
        activo=True,
        fecha_agregado=date(2026, 1, 15),
        id_asignacion_ejercicio=10,
    )


def test_crear_asignacion_con_datos_completos():
    fecha = date(2026, 1, 15)

    asignacion = AsignacionRutinaEjercicio(
        id_asignacion=1,
        id_ejercicio=2,
        orden_ejercicio=3,
        veces_planificadas=4,
        activo=True,
        fecha_agregado=fecha,
        id_asignacion_ejercicio=10,
    )

    assert asignacion.id_asignacion_ejercicio == 10
    assert asignacion.id_asignacion == 1
    assert asignacion.id_ejercicio == 2
    assert asignacion.orden_ejercicio == 3
    assert asignacion.veces_planificadas == 4
    assert asignacion.activo is True
    assert asignacion.fecha_agregado == fecha


def test_crear_asignacion_sin_id_y_con_fecha_actual():
    fecha_hoy = date(2026, 9, 27)

    with patch(
        "src.modelos.asignacion_rutina_ejercicio.date"
    ) as mock_date:
        mock_date.today.return_value = fecha_hoy

        asignacion = AsignacionRutinaEjercicio(
            id_asignacion=1,
            id_ejercicio=2,
            orden_ejercicio=1,
        )

    assert asignacion.id_asignacion_ejercicio is None
    assert asignacion.veces_planificadas == 1
    assert asignacion.activo is True
    assert asignacion.fecha_agregado == fecha_hoy


@pytest.mark.parametrize(
    "atributo, valor, mensaje",
    [
        (
            "id_asignacion_ejercicio",
            0,
            "El ID del ejercicio asignado debe ser un entero positivo.",
        ),
        (
            "id_asignacion_ejercicio",
            -1,
            "El ID del ejercicio asignado debe ser un entero positivo.",
        ),
        (
            "id_asignacion_ejercicio",
            "10",
            "El ID del ejercicio asignado debe ser un entero positivo.",
        ),
        (
            "id_asignacion",
            0,
            "El ID de la asignación debe ser un entero positivo.",
        ),
        (
            "id_asignacion",
            False,
            "El ID de la asignación debe ser un entero positivo.",
        ),
        (
            "id_ejercicio",
            -5,
            "El ID del ejercicio debe ser un entero positivo.",
        ),
        (
            "id_ejercicio",
            True,
            "El ID del ejercicio debe ser un entero positivo.",
        ),
    ],
)
def test_validar_ids_invalidos(
    asignacion,
    atributo,
    valor,
    mensaje,
):
    with pytest.raises(
        ValueError,
        match=mensaje,
    ):
        setattr(
            asignacion,
            atributo,
            valor,
        )


@pytest.mark.parametrize(
    "valor",
    [
        0,
        -1,
        "1",
        1.5,
        True,
        False,
    ],
)
def test_orden_ejercicio_rechaza_valores_invalidos(
    asignacion,
    valor,
):
    with pytest.raises(
        ValueError,
        match=(
            "El orden del ejercicio debe ser "
            "un entero mayor que cero."
        ),
    ):
        asignacion.orden_ejercicio = valor


@pytest.mark.parametrize(
    "valor",
    [
        0,
        -1,
        "2",
        2.5,
        True,
        False,
    ],
)
def test_veces_planificadas_rechaza_valores_invalidos(
    asignacion,
    valor,
):
    with pytest.raises(
        ValueError,
        match=(
            "Las veces planificadas deben ser "
            "un entero mayor que cero."
        ),
    ):
        asignacion.veces_planificadas = valor


@pytest.mark.parametrize(
    "valor",
    [
        1,
        0,
        "True",
        None,
        [],
    ],
)
def test_activo_rechaza_valores_no_booleanos(
    asignacion,
    valor,
):
    with pytest.raises(
        ValueError,
        match="El estado activo debe ser booleano.",
    ):
        asignacion.activo = valor


@pytest.mark.parametrize(
    "valor",
    [
        "2026-01-15",
        123,
        10.5,
        [],
        {},
    ],
)
def test_fecha_agregado_rechaza_valores_invalidos(
    asignacion,
    valor,
):
    with pytest.raises(
        ValueError,
        match="La fecha de agregado no es válida.",
    ):
        asignacion.fecha_agregado = valor


def test_fecha_agregado_acepta_fecha_valida(
    asignacion,
):
    fecha = date(2026, 5, 20)

    asignacion.fecha_agregado = fecha

    assert asignacion.fecha_agregado == fecha


def test_actualizar_meta_modifica_veces_planificadas(
    asignacion,
):
    asignacion.actualizar_meta(8)

    assert asignacion.veces_planificadas == 8


def test_actualizar_meta_rechaza_valor_invalido(
    asignacion,
):
    with pytest.raises(
        ValueError,
        match=(
            "Las veces planificadas deben ser "
            "un entero mayor que cero."
        ),
    ):
        asignacion.actualizar_meta(0)


def test_cambiar_orden_modifica_orden(
    asignacion,
):
    asignacion.cambiar_orden(8)

    assert asignacion.orden_ejercicio == 8


def test_cambiar_orden_rechaza_valor_invalido(
    asignacion,
):
    with pytest.raises(
        ValueError,
        match=(
            "El orden del ejercicio debe ser "
            "un entero mayor que cero."
        ),
    ):
        asignacion.cambiar_orden(-1)


def test_desactivar_cambia_estado_a_falso(
    asignacion,
):
    asignacion.desactivar()

    assert asignacion.activo is False


def test_activar_cambia_estado_a_verdadero(
    asignacion,
):
    asignacion.desactivar()
    asignacion.activar()

    assert asignacion.activo is True


def test_repr_muestra_todos_los_datos(
    asignacion,
):
    representacion = repr(asignacion)

    assert "AsignacionRutinaEjercicio(" in representacion
    assert "id_asignacion_ejercicio=10" in representacion
    assert "id_asignacion=1" in representacion
    assert "id_ejercicio=2" in representacion
    assert "orden_ejercicio=3" in representacion
    assert "veces_planificadas=4" in representacion
    assert "activo=True" in representacion
    assert "fecha_agregado=2026-01-15" in representacion


def test_validar_id_acepta_entero_positivo():
    AsignacionRutinaEjercicio._validar_id(
        1,
        "ID de prueba",
    )