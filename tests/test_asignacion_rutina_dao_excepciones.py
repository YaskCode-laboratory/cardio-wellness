"""Pruebas de excepciones para AsignacionRutinaDAO."""


from datetime import date
from unittest.mock import MagicMock, patch


import pytest


import src.persistencia.asignacion_rutina_dao as modulo_dao


from src.modelos.enums import EstadoAsignacion
from src.persistencia.asignacion_rutina_dao import (
    AsignacionRutinaDAO,
)


@pytest.fixture
def bd_mock():
    """
    Simula ConexionBD y su conexión PostgreSQL.
    """
    bd = MagicMock()

    conexion = MagicMock()
    conexion.closed = False

    bd._conexion = conexion

    return bd


@pytest.fixture
def dao(
    bd_mock,
):
    """
    Crea un DAO con una conexión simulada.
    """
    with patch.object(
        modulo_dao.ConexionBD,
        "obtener_instancia",
        return_value=bd_mock,
    ):
        return AsignacionRutinaDAO()


def crear_cursor(
    rowcount=1,
):
    """
    Crea un cursor compatible con el bloque with.
    """
    cursor = MagicMock()

    cursor.rowcount = rowcount
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = False

    return cursor


def configurar_cursor(
    dao,
    cursor,
):
    """
    Configura el cursor simulado de la conexión del DAO.
    """
    dao._bd._conexion.cursor.return_value = cursor


@pytest.mark.parametrize(
    "id_asignacion",
    [
        None,
        True,
        False,
        0,
        -1,
        "10",
        10.5,
    ],
)
def test_cancelar_asignacion_rechaza_id_invalido(
    dao,
    id_asignacion,
):
    """
    Verifica que cancelar_asignacion rechace IDs que no
    sean enteros positivos.
    """
    with pytest.raises(ValueError):
        dao.cancelar_asignacion(id_asignacion)

    dao._bd.abrir_conexion.assert_not_called()


@pytest.mark.parametrize(
    ("rowcount", "esperado"),
    [
        (1, True),
        (0, False),
    ],
)
def test_cancelar_asignacion_retorna_resultado_segun_rowcount(
    dao,
    rowcount,
    esperado,
):
    """
    Verifica el resultado según la cantidad de filas
    actualizadas por la sentencia SQL.
    """
    cursor = crear_cursor(
        rowcount=rowcount,
    )

    configurar_cursor(
        dao,
        cursor,
    )

    resultado = dao.cancelar_asignacion(22)

    assert resultado is esperado

    dao._bd.abrir_conexion.assert_called_once_with()

    cursor.execute.assert_called_once()

    consulta, parametros = cursor.execute.call_args.args

    assert "UPDATE asignaciones_rutina" in consulta

    assert parametros[0] == EstadoAsignacion.CANCELADA.value
    assert parametros[1] == date.today()
    assert parametros[2] == 22
    assert parametros[3] == EstadoAsignacion.ACTIVA.value

    dao._bd._conexion.commit.assert_called_once_with()

    dao._bd._conexion.rollback.assert_not_called()


def test_cancelar_asignacion_hace_rollback_en_error(
    dao,
):
    """
    Verifica rollback y relanzamiento si falla la consulta.
    """
    cursor = crear_cursor()

    cursor.execute.side_effect = RuntimeError(
        "fallo al cancelar asignación",
    )

    configurar_cursor(
        dao,
        cursor,
    )

    with pytest.raises(
        RuntimeError,
        match="fallo al cancelar",
    ):
        dao.cancelar_asignacion(22)

    dao._bd.abrir_conexion.assert_called_once_with()

    dao._bd._conexion.rollback.assert_called_once_with()

    dao._bd._conexion.commit.assert_not_called()