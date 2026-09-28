"""
Tests para cubrir excepciones y casos edge en ProgresoMensualDAO.
"""

import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from src.modelos.progreso_mensual import ProgresoMensual
from src.persistencia.progreso_mensual_dao import ProgresoMensualDAO
from src.persistencia.conexion_bd import ConexionBD
from src.servicios.gestor_seguridad import GestorSeguridad


@pytest.fixture
def dao():
    return ProgresoMensualDAO()


@pytest.fixture
def datos_prueba():
    """Crea cliente real para pruebas."""
    bd = ConexionBD.obtener_instancia()
    bd.abrir_conexion()

    correo = f"test.progreso.{uuid4().hex}@example.com"
    contrasenia_hash = GestorSeguridad.generar_hash("Clave123!")

    with bd._conexion.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO usuarios (
                nombre, apellido, correo_electronico, contrasenia_hash, edad, tipo_usuario
            )
            VALUES (%s, %s, %s, %s, %s, 'cliente')
            RETURNING id_usuario
            """,
            ("Test", "Progreso", correo, contrasenia_hash, 30),
        )
        id_cliente = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO clientes (id_usuario, peso, altura, objetivo)
            VALUES (%s, %s, %s, %s)
            """,
            (id_cliente, 70.0, 1.75, "Pruebas excepciones"),
        )

    bd._conexion.commit()
    yield {"id_cliente": id_cliente}

    try:
        with bd._conexion.cursor() as cursor:
            cursor.execute("DELETE FROM progreso_mensual WHERE id_cliente = %s", (id_cliente,))
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_cliente,))
        bd._conexion.commit()
    except Exception:
        bd._conexion.rollback()
        raise


def test_dao_guardar_con_cliente_inexistente(dao):
    """Prueba que guarda con cliente inexistente lanza ValueError."""
    progreso = ProgresoMensual(
        id_progreso=None,
        id_cliente=999999,  # Cliente inexistente
        mes=date(2026, 9, 1),
        peso=70.0,
        sesiones_completadas=0,
        sesiones_planificadas=12,
        porcentaje_cumplimiento=0.0,
    )

    with pytest.raises(ValueError, match="El cliente referenciado no existe"):
        dao.guardar(progreso)


def test_dao_guardar_duplicado_mes(dao, datos_prueba):
    """Prueba que guarda progreso duplicado para mismo mes lanza ValueError."""
    # Crear primer progreso
    progreso1 = ProgresoMensual(
        id_progreso=None,
        id_cliente=datos_prueba["id_cliente"],
        mes=date(2026, 9, 1),
        peso=70.0,
        sesiones_completadas=5,
        sesiones_planificadas=12,
        porcentaje_cumplimiento=41.67,
    )
    dao.guardar(progreso1)

    # Intentar crear segundo progreso para el mismo mes
    progreso2 = ProgresoMensual(
        id_progreso=None,
        id_cliente=datos_prueba["id_cliente"],
        mes=date(2026, 9, 1),  # Mismo mes
        peso=69.5,
        sesiones_completadas=8,
        sesiones_planificadas=12,
        porcentaje_cumplimiento=66.67,
    )

    with pytest.raises(ValueError, match="Ya existe un registro de progreso"):
        dao.guardar(progreso2)


def test_dao_buscar_por_id_inexistente(dao):
    """Prueba que buscar ID inexistente retorna None."""
    resultado = dao.buscar_por_id(999999)
    assert resultado is None


def test_dao_actualizar_sin_id(dao, datos_prueba):
    """Prueba que actualizar sin ID lanza ValueError."""
    progreso = ProgresoMensual(
        id_progreso=None,  # Sin ID
        id_cliente=datos_prueba["id_cliente"],
        mes=date(2026, 9, 1),
        peso=70.0,
        sesiones_completadas=0,
        sesiones_planificadas=12,
        porcentaje_cumplimiento=0.0,
    )

    with pytest.raises(ValueError, match="El progreso debe tener un ID"):
        dao.actualizar(progreso)


def test_dao_actualizar_id_inexistente(dao):
    """Prueba que actualizar ID inexistente lanza ValueError."""
    progreso = ProgresoMensual(
        id_progreso=999999,  # ID inexistente
        id_cliente=1,
        mes=date(2026, 9, 1),
        peso=70.0,
        sesiones_completadas=0,
        sesiones_planificadas=12,
        porcentaje_cumplimiento=0.0,
    )

    with pytest.raises(ValueError, match="No se encontró el registro"):
        dao.actualizar(progreso)


def test_dao_eliminar_id_inexistente(dao):
    """Prueba que eliminar ID inexistente retorna False."""
    resultado = dao.eliminar_por_id(999999)
    assert resultado is False


def test_dao_listar_cliente_sin_progreso(dao, datos_prueba):
    """Prueba que listar cliente sin progreso retorna lista vacía."""
    resultado = dao.listar_por_cliente(datos_prueba["id_cliente"])
    assert isinstance(resultado, list)
    assert len(resultado) == 0


def test_dao_buscar_cliente_sin_progreso(dao, datos_prueba):
    """Prueba que buscar cliente sin progreso retorna lista vacía."""
    resultado = dao.buscar_por_cliente(datos_prueba["id_cliente"])
    assert isinstance(resultado, list)
    assert len(resultado) == 0

def test_dao_buscar_por_cliente_y_mes_exitoso_normaliza_mes(
    dao,
    datos_prueba,
):
    progreso = ProgresoMensual(
        id_progreso=None,
        id_cliente=datos_prueba["id_cliente"],
        mes=date(2026, 10, 18),
        peso=71.25,
        sesiones_completadas=6,
        sesiones_planificadas=10,
        porcentaje_cumplimiento=60.0,
    )

    guardado = dao.guardar(progreso)

    encontrado = dao.buscar_por_cliente_y_mes(
        datos_prueba["id_cliente"],
        date(2026, 10, 29),
    )

    assert encontrado is not None
    assert encontrado.id_progreso == guardado.id_progreso
    assert encontrado.id_cliente == datos_prueba["id_cliente"]
    assert encontrado.mes == date(2026, 10, 1)
    assert encontrado.peso == Decimal("71.25")
    assert encontrado.sesiones_completadas == 6
    assert encontrado.sesiones_planificadas == 10
    assert encontrado.porcentaje_cumplimiento == 60.0

def test_dao_buscar_por_cliente_y_mes_exitoso_normaliza_mes(
    dao,
    datos_prueba,
):
    progreso = ProgresoMensual(
        id_progreso=None,
        id_cliente=datos_prueba["id_cliente"],
        mes=date(2026, 10, 18),
        peso=71.25,
        sesiones_completadas=6,
        sesiones_planificadas=10,
        porcentaje_cumplimiento=60.0,
    )

    guardado = dao.guardar(progreso)

    encontrado = dao.buscar_por_cliente_y_mes(
        datos_prueba["id_cliente"],
        date(2026, 10, 29),
    )

    assert encontrado is not None
    assert encontrado.id_progreso == guardado.id_progreso
    assert encontrado.id_cliente == datos_prueba["id_cliente"]
    assert encontrado.mes == date(2026, 10, 1)
    assert encontrado.peso == Decimal("71.25")
    assert encontrado.sesiones_completadas == 6
    assert encontrado.sesiones_planificadas == 10
    assert encontrado.porcentaje_cumplimiento == 60.0


def test_dao_buscar_por_cliente_y_mes_inexistente_retorna_none(
    dao,
    datos_prueba,
):
    resultado = dao.buscar_por_cliente_y_mes(
        datos_prueba["id_cliente"],
        date(2026, 11, 15),
    )

    assert resultado is None


@pytest.mark.parametrize(
    "id_cliente, mes, mensaje",
    [
        (
            0,
            date(2026, 10, 1),
            "El ID del cliente debe ser positivo",
        ),
        (
            -1,
            date(2026, 10, 1),
            "El ID del cliente debe ser positivo",
        ),
        (
            True,
            date(2026, 10, 1),
            "El ID del cliente debe ser positivo",
        ),
        (
            1,
            "2026-10-01",
            "El mes debe ser una fecha válida",
        ),
    ],
)
def test_dao_buscar_por_cliente_y_mes_valida_datos(
    dao,
    id_cliente,
    mes,
    mensaje,
):
    with pytest.raises(ValueError, match=mensaje):
        dao.buscar_por_cliente_y_mes(
            id_cliente,
            mes,
        )

def test_dao_buscar_por_cliente_y_mes_relanza_error(
    dao,
    monkeypatch,
):
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = False
    cursor.execute.side_effect = RuntimeError(
        "fallo al buscar progreso por cliente y mes",
    )

    conexion = MagicMock()
    conexion.cursor.return_value = cursor

    monkeypatch.setattr(
        dao._bd,
        "_conexion",
        conexion,
    )

    monkeypatch.setattr(
        dao._bd,
        "abrir_conexion",
        MagicMock(),
    )

    with pytest.raises(
        RuntimeError,
        match="fallo al buscar progreso por cliente y mes",
    ):
        dao.buscar_por_cliente_y_mes(
            10,
            date(2026, 10, 1),
        )

    cursor.execute.assert_called_once()