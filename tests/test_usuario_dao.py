from uuid import uuid4

import pytest

from src.modelos.administrador import Administrador
from src.persistencia.usuario_dao import UsuarioDAO


@pytest.fixture
def dao():
    return UsuarioDAO()


@pytest.fixture
def usuario_temporal(dao):
    """
    Crea y limpia administradores temporales.

    La limpieza se ejecuta incluso si falla una aserción de la prueba.
    """
    usuarios_creados = []

    def crear(
        correo=None,
        nombre="Usuario",
        apellido="Prueba",
    ):
        if correo is None:
            correo = f"usuario.dao.{uuid4().hex}@example.com"

        usuario = Administrador(
            nombre=nombre,
            apellido=apellido,
            correo_electronico=correo,
            contrasenia_hash="Clave123!",
            edad=30,
        )

        usuario_guardado = dao.guardar(
            usuario,
            contrasenia_plana="Clave123!",
        )

        usuarios_creados.append(usuario_guardado.id_usuario)

        return usuario_guardado

    yield crear

    for id_usuario in usuarios_creados:
        try:
            dao.eliminar_por_id(id_usuario)
        except Exception:
            pass


def crear_usuario(
    correo: str,
) -> Administrador:
    """Crea un usuario administrador sin guardarlo."""
    return Administrador(
        nombre="Usuario",
        apellido="Prueba",
        correo_electronico=correo,
        contrasenia_hash="Clave123!",
        edad=30,
    )


def test_usuario_dao_guardar(
    usuario_temporal,
):
    usuario_guardado = usuario_temporal()

    assert usuario_guardado.id_usuario is not None
    assert usuario_guardado.fecha_registro is not None
    assert usuario_guardado.tipo_usuario == "administrador"


def test_usuario_dao_buscar_por_correo(
    dao,
    usuario_temporal,
):
    usuario_guardado = usuario_temporal()

    usuario_encontrado = dao.buscar_por_correo(
        usuario_guardado.correo_electronico,
    )

    assert usuario_encontrado is not None

    assert (
        usuario_encontrado.id_usuario
        == usuario_guardado.id_usuario
    )

    assert (
        usuario_encontrado.correo_electronico
        == usuario_guardado.correo_electronico
    )


def test_usuario_dao_actualizar(
    dao,
    usuario_temporal,
):
    usuario_guardado = usuario_temporal()
    usuario_guardado.nombre = "NombreActualizado"

    usuario_actualizado = dao.actualizar(
        usuario_guardado,
    )

    assert usuario_actualizado.nombre == "NombreActualizado"

    usuario_encontrado = dao.buscar_por_correo(
        usuario_guardado.correo_electronico,
    )

    assert usuario_encontrado.nombre == "NombreActualizado"


def test_usuario_dao_actualizar_correo(
    dao,
    usuario_temporal,
):
    usuario_guardado = usuario_temporal()

    correo_nuevo = (
        f"usuario.correo.nuevo.{uuid4().hex}@example.com"
    )

    usuario_guardado.correo_electronico = correo_nuevo

    dao.actualizar(usuario_guardado)

    usuario_encontrado = dao.buscar_por_correo(
        correo_nuevo,
    )

    assert usuario_encontrado is not None
    assert usuario_encontrado.correo_electronico == correo_nuevo


def test_usuario_dao_actualizar_preserva_hash(
    dao,
    usuario_temporal,
):
    usuario_guardado = usuario_temporal()

    usuario_fresh = dao.buscar_por_correo(
        usuario_guardado.correo_electronico,
    )

    hash_original = usuario_fresh.contrasenia_hash

    usuario_guardado.nombre = "NombreActualizado"

    dao.actualizar(usuario_guardado)

    usuario_encontrado = dao.buscar_por_correo(
        usuario_guardado.correo_electronico,
    )