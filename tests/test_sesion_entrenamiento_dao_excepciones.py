"""
Tests para cubrir excepciones y casos edge en SesionEntrenamientoDAO.
"""

from datetime import date
from uuid import uuid4

import pytest

from src.modelos.enums import Intensidad
from src.modelos.sesion_entrenamiento import SesionEntrenamiento
from src.persistencia.conexion_bd import ConexionBD
from src.persistencia.sesion_entrenamiento_dao import (
    SesionEntrenamientoDAO,
)
from src.servicios.gestor_seguridad import GestorSeguridad


@pytest.fixture
def dao():
    return SesionEntrenamientoDAO()


@pytest.fixture
def datos_prueba():
    """Crea un cliente temporal para pruebas de integración."""
    bd = ConexionBD.obtener_instancia()
    bd.abrir_conexion()

    correo = f"test.sesion.{uuid4().hex}@example.com"
    contrasenia_hash = GestorSeguridad.generar_hash(
        "Clave123!",
    )

    id_cliente = None

    try:
        with bd._conexion.cursor() as cursor:
            cursor.execute(
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
                    "Sesion",
                    correo,
                    contrasenia_hash,
                    contrasenia_hash,
                    30,
                    "cliente",
                ),
            )

            id_cliente = cursor.fetchone()[0]

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
                    id_cliente,
                    70.0,
                    1.75,
                    "Pruebas excepciones",
                ),
            )

        bd._conexion.commit()

        yield {
            "id_cliente": id_cliente,
        }

    except Exception:
        bd._conexion.rollback()
        raise

    finally:
        if id_cliente is not None:
            try:
                with bd._conexion.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM sesiones_entrenamiento
                        WHERE id_cliente = %s
                        """,
                        (id_cliente,),
                    )

                    cursor.execute(
                        """
                        DELETE FROM clientes
                        WHERE id_usuario = %s
                        """,
                        (id_cliente,),
                    )

                    cursor.execute(
                        """
                        DELETE FROM usuarios
                        WHERE id_usuario = %s
                        """,
                        (id_cliente,),
                    )

                bd._conexion.commit()

            except Exception:
                bd._conexion.rollback()


def crear_sesion(
    id_cliente,
    id_sesion=None,
):
    """Construye una sesión válida para las pruebas."""
    return SesionEntrenamiento(
        id_sesion=id_sesion,
        id_cliente=id_cliente,
        fecha=date(2026, 9, 11),
        duracion_real=30,
        intensidad_real=Intensidad.MEDIA,
        calorias_quemadas=200.0,
        observaciones="Test",
        completada=True,
    )


def test_dao_guardar_con_cliente_inexistente(dao):
    """Guardar una sesión para un cliente inexistente debe fallar."""
    sesion = crear_sesion(id_cliente=999999)

    with pytest.raises(
        ValueError,
        match="El cliente referenciado no existe",
    ):
        dao.guardar(sesion)


def test_dao_buscar_por_id_inexistente(dao):
    """Buscar una sesión inexistente debe retornar None."""
    resultado = dao.buscar_por_id(999999)

    assert resultado is None


def test_dao_actualizar_sin_id(
    dao,
    datos_prueba,
):
    """Actualizar una sesión sin ID debe fallar."""
    sesion = crear_sesion(
        id_cliente=datos_prueba["id_cliente"],
    )

    with pytest.raises(
        ValueError,
        match="La sesión debe tener un ID",
    ):
        dao.actualizar(sesion)


def test_dao_actualizar_id_inexistente(dao):
    """Actualizar una sesión inexistente debe fallar."""
    sesion = crear_sesion(
        id_cliente=1,
        id_sesion=999999,
    )

    with pytest.raises(
        ValueError,
        match="No se encontró la sesión",
    ):
        dao.actualizar(sesion)


def test_dao_eliminar_id_inexistente(dao):
    """Eliminar una sesión inexistente debe retornar False."""
    resultado = dao.eliminar_por_id(999999)

    assert resultado is False


def test_dao_listar_cliente_sin_sesiones(
    dao,
    datos_prueba,
):
    """Un cliente nuevo no debe tener sesiones registradas."""
    resultado = dao.listar_por_cliente(
        datos_prueba["id_cliente"],
    )

    assert isinstance(resultado, list)
    assert resultado == []

def test_validar_sesion_rechaza_asignacion_sin_ejercicio_asignado():
    sesion = crear_sesion(
        id_cliente=1,
    )

    sesion._id_asignacion = 10
    sesion._id_asignacion_ejercicio = None

    with pytest.raises(
        ValueError,
        match=(
            "La sesión debe indicar tanto la asignación "
            "como el ejercicio asignado"
        ),
    ):
        SesionEntrenamientoDAO._validar_sesion(sesion)


@pytest.mark.parametrize(
    "pgcode, mensaje",
    [
        (
            "23503",
            (
                "El cliente, la rutina, la asignación "
                "o el ejercicio asignado no existe."
            ),
        ),
        (
            "23514",
            (
                "Las veces realizadas deben ser mayores "
                "o iguales a cero y no pueden superar "
                "las planificadas."
            ),
        ),
        (
            "23502",
            "Falta un dato obligatorio para guardar la sesión.",
        ),
        (
            "99999",
            (
                "No se pudo guardar o actualizar la sesión "
                "por una restricción de integridad."
            ),
        ),
    ],
)
def test_convertir_error_integridad(
    pgcode,
    mensaje,
):
    class ErrorIntegridadPrueba:
        def __init__(self, codigo):
            self.pgcode = codigo

    error = ErrorIntegridadPrueba(pgcode)

    resultado = SesionEntrenamientoDAO._convertir_error_integridad(
        error,
    )

    assert isinstance(resultado, ValueError)
    assert str(resultado) == mensaje