from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from src.modelos.cliente import Cliente
from src.persistencia.cliente_dao import ClienteDAO
from src.servicios.gestor_seguridad import GestorSeguridad


class ErrorIntegridadSimulado(Exception):
    def __init__(self, pgcode, mensaje="Error de integridad simulado"):
        super().__init__(mensaje)
        self.pgcode = pgcode


@pytest.fixture
def recursos():
    dao = ClienteDAO()

    cursor = MagicMock()
    conexion = MagicMock()

    conexion.cursor.return_value.__enter__.return_value = cursor
    conexion.cursor.return_value.__exit__.return_value = False

    dao._bd = MagicMock()
    dao._bd._conexion = conexion

    return dao, cursor, conexion


def crear_cliente(
    correo="cliente.ramas@example.com",
    id_usuario=1,
    contrasenia_hash=None,
):
    if contrasenia_hash is None:
        contrasenia_hash = GestorSeguridad.generar_hash(
            "ClaveInicial123!"
        )

    return Cliente(
        id_usuario=id_usuario,
        nombre="Laura",
        apellido="Gomez",
        correo_electronico=correo,
        contrasenia_hash=contrasenia_hash,
        edad=32,
        peso=68.5,
        peso_objetivo=64.0,
        altura=1.65,
        objetivo="Mejorar resistencia",
        genero="mujer",
        fecha_registro=date(2026, 1, 1),
        fecha_ingreso=date(2026, 1, 2),
    )


def crear_fila_cliente(
    peso_objetivo=64.0,
    genero="MUJER",
):
    return (
        1,
        "Laura",
        "Gomez",
        "laura@example.com",
        GestorSeguridad.generar_hash("ClaveInicial123!"),
        32,
        "cliente",
        date(2026, 1, 1),
        68.5,
        peso_objetivo,
        1.65,
        "Mejorar resistencia",
        genero,
        date(2026, 1, 2),
    )


@pytest.mark.parametrize(
    "hash_guardado",
    [
        None,
        "",
        123,
    ],
)
def test_validar_hash_rechaza_hash_vacio_o_tipo_invalido(
    hash_guardado,
):
    with pytest.raises(
        ValueError,
        match="El hash de la contraseña no puede estar vacío",
    ):
        ClienteDAO._validar_hash(hash_guardado)


def test_validar_hash_rechaza_prefijo_no_bcrypt():
    with pytest.raises(
        ValueError,
        match="La contraseña debe estar almacenada como hash bcrypt",
    ):
        ClienteDAO._validar_hash("hash-invalido")


def test_validar_hash_rechaza_longitud_incorrecta():
    with pytest.raises(
        ValueError,
        match="El hash bcrypt debe tener 60 caracteres",
    ):
        ClienteDAO._validar_hash("$2b$" + ("a" * 20))


def test_obtener_hash_rechaza_contrasenia_vacia():
    with pytest.raises(
        ValueError,
        match="La contraseña o el hash no puede estar vacío",
    ):
        ClienteDAO._obtener_hash_contrasenia("")


def test_obtener_hash_rechaza_contrasenia_debil():
    with pytest.raises(
        ValueError,
        match="La contraseña debe ser segura",
    ):
        ClienteDAO._obtener_hash_contrasenia("123")


def test_obtener_hash_conserva_hash_bcrypt_existente():
    hash_original = GestorSeguridad.generar_hash("ClaveInicial123!")

    resultado = ClienteDAO._obtener_hash_contrasenia(
        hash_original
    )

    assert resultado == hash_original


def test_obtener_hash_convierte_contrasenia_segura():
    resultado = ClienteDAO._obtener_hash_contrasenia(
        "ClaveSegura456!"
    )

    assert resultado != "ClaveSegura456!"
    assert len(resultado) == 60
    assert GestorSeguridad.verificar_contrasenia(
        "ClaveSegura456!",
        resultado,
    ) is True


@pytest.mark.parametrize("correo", [None, 123, "", "   "])
def test_normalizar_correo_rechaza_valor_invalido(correo):
    with pytest.raises(ValueError):
        ClienteDAO._normalizar_correo(correo)


def test_normalizar_correo_limpia_valor_valido():
    assert ClienteDAO._normalizar_correo(
        "  LAURA@EXAMPLE.COM  "
    ) == "laura@example.com"


@pytest.mark.parametrize("genero", [None, 1, "", "DESCONOCIDO"])
def test_normalizar_genero_rechaza_valor_invalido(genero):
    with pytest.raises(ValueError):
        ClienteDAO._normalizar_genero(genero)


def test_normalizar_genero_normaliza_valor_valido():
    assert ClienteDAO._normalizar_genero(
        " mujer "
    ) == "MUJER"


def test_guardar_rechaza_objeto_que_no_es_cliente(recursos):
    dao, _, _ = recursos

    with pytest.raises(
        TypeError,
        match="Debe proporcionar una instancia de Cliente",
    ):
        dao.guardar(SimpleNamespace())


def test_guardar_falla_si_no_se_recupera_usuario_creado(recursos):
    dao, cursor, conexion = recursos
    cursor.fetchone.return_value = None

    with pytest.raises(
        RuntimeError,
        match="No se pudo obtener el usuario creado",
    ):
        dao.guardar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_guardar_falla_si_no_se_recuperan_datos_cliente(recursos):
    dao, cursor, conexion = recursos
    cursor.fetchone.side_effect = [
        (15, date(2026, 1, 1)),
        None,
    ]

    with pytest.raises(
        RuntimeError,
        match="No se pudieron obtener los datos del cliente creado",
    ):
        dao.guardar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_guardar_convierte_error_integridad_referencia(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = ErrorIntegridadSimulado("23503")

    with patch(
        "src.persistencia.cliente_dao.IntegrityError",
        ErrorIntegridadSimulado,
    ):
        with pytest.raises(
            ValueError,
            match="No existe una referencia relacionada",
        ):
            dao.guardar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_guardar_convierte_error_integridad_generico(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = ErrorIntegridadSimulado(
        "99999",
        "Restricción inesperada",
    )

    with patch(
        "src.persistencia.cliente_dao.IntegrityError",
        ErrorIntegridadSimulado,
    ):
        with pytest.raises(
            RuntimeError,
            match="Error de integridad al guardar el cliente",
        ):
            dao.guardar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_guardar_hace_rollback_en_error_inesperado(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = RuntimeError("Error inesperado")

    with pytest.raises(RuntimeError, match="Error inesperado"):
        dao.guardar(crear_cliente())

    conexion.rollback.assert_called_once()


@pytest.mark.parametrize(
    "metodo,args",
    [
        ("buscar_por_id", (1,)),
        ("buscar_por_correo", ("cliente@example.com",)),
        ("listar", ()),
    ],
)
def test_busquedas_hacen_rollback_si_cursor_falla(
    recursos,
    metodo,
    args,
):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = RuntimeError("Consulta fallida")

    with pytest.raises(RuntimeError, match="Consulta fallida"):
        getattr(dao, metodo)(*args)

    conexion.rollback.assert_called_once()


def test_actualizar_rechaza_objeto_no_cliente(recursos):
    dao, _, _ = recursos

    with pytest.raises(
        TypeError,
        match="Debe proporcionar una instancia de Cliente",
    ):
        dao.actualizar(SimpleNamespace())


def test_actualizar_falla_si_no_existe_usuario_cliente(recursos):
    dao, cursor, conexion = recursos
    cursor.rowcount = 0

    with pytest.raises(
        ValueError,
        match="No se encontró el cliente",
    ):
        dao.actualizar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_actualizar_falla_si_no_existen_datos_cliente(recursos):
    dao, cursor, conexion = recursos
    cursor.rowcount = 1
    llamadas = 0

    def ejecutar_y_cambiar_rowcount(*args, **kwargs):
        nonlocal llamadas
        llamadas += 1

        if llamadas == 2:
            cursor.rowcount = 0

    cursor.execute.side_effect = ejecutar_y_cambiar_rowcount

    with pytest.raises(
        ValueError,
        match="No se encontraron los datos del cliente",
    ):
        dao.actualizar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_actualizar_convierte_correo_duplicado(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = ErrorIntegridadSimulado("23505")

    with patch(
        "src.persistencia.cliente_dao.IntegrityError",
        ErrorIntegridadSimulado,
    ):
        with pytest.raises(
            ValueError,
            match="El correo ya está registrado",
        ):
            dao.actualizar(crear_cliente())

    conexion.rollback.assert_called_once()


def test_actualizar_convierte_error_integridad_generico(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = ErrorIntegridadSimulado("99999")

    with patch(
        "src.persistencia.cliente_dao.IntegrityError",
        ErrorIntegridadSimulado,
    ):
        with pytest.raises(
            RuntimeError,
            match="Error de integridad al actualizar el cliente",
        ):
            dao.actualizar(crear_cliente())

    conexion.rollback.assert_called_once()


@pytest.mark.parametrize("id_usuario", [None, 0, -1, True, "1"])
def test_actualizar_peso_rechaza_id_invalido(recursos, id_usuario):
    dao, _, _ = recursos

    with pytest.raises(ValueError):
        dao.actualizar_peso(id_usuario, 70)


@pytest.mark.parametrize("nuevo_peso", [None, 0, -1])
def test_actualizar_peso_rechaza_peso_invalido(recursos, nuevo_peso):
    dao, _, _ = recursos

    with pytest.raises(
        ValueError,
        match="El nuevo peso debe ser mayor que cero",
    ):
        dao.actualizar_peso(1, nuevo_peso)


@pytest.mark.parametrize(
    ("rowcount", "esperado"),
    [
        (1, True),
        (0, False),
    ],
)
def test_actualizar_peso_retorna_resultado_y_confirma(
    recursos,
    rowcount,
    esperado,
):
    dao, cursor, conexion = recursos
    cursor.rowcount = rowcount

    resultado = dao.actualizar_peso(1, 70.5)

    assert resultado is esperado
    conexion.commit.assert_called_once()


def test_actualizar_peso_hace_rollback_si_falla(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = RuntimeError("No se pudo actualizar")

    with pytest.raises(RuntimeError, match="No se pudo actualizar"):
        dao.actualizar_peso(1, 70.5)

    conexion.rollback.assert_called_once()


def test_actualizar_contrasenia_retorna_false_si_cliente_no_existe(
    recursos,
):
    dao, cursor, _ = recursos
    cursor.fetchone.return_value = None

    assert dao.actualizar_contrasenia(
        1,
        "ClaveInicial123!",
        "ClaveNueva456!",
    ) is False


def test_actualizar_contrasenia_rechaza_contrasenia_nueva_debil(
    recursos,
):
    dao, cursor, conexion = recursos
    cursor.fetchone.return_value = (
        GestorSeguridad.generar_hash("ClaveInicial123!"),
    )

    with pytest.raises(
        ValueError,
        match="La nueva contraseña es muy débil",
    ):
        dao.actualizar_contrasenia(
            1,
            "ClaveInicial123!",
            "123",
        )

    conexion.rollback.assert_called_once()


def test_actualizar_contrasenia_hace_rollback_si_falla(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = RuntimeError("Error contraseña")

    with pytest.raises(RuntimeError, match="Error contraseña"):
        dao.actualizar_contrasenia(
            1,
            "ClaveInicial123!",
            "ClaveNueva456!",
        )

    conexion.rollback.assert_called_once()


def test_eliminar_hace_rollback_si_falla(recursos):
    dao, cursor, conexion = recursos
    cursor.execute.side_effect = RuntimeError("No se pudo eliminar")

    with pytest.raises(RuntimeError, match="No se pudo eliminar"):
        dao.eliminar_por_id(1)

    conexion.rollback.assert_called_once()


def test_crear_cliente_usa_peso_actual_si_objetivo_es_none():
    fila = crear_fila_cliente(peso_objetivo=None)

    cliente = ClienteDAO._crear_cliente_desde_fila(fila)

    assert cliente.peso == cliente.peso_objetivo


@pytest.mark.parametrize("genero", [None, "", "   "])
def test_crear_cliente_usa_genero_por_defecto_si_esta_vacio(genero):
    fila = crear_fila_cliente(genero=genero)

    cliente = ClienteDAO._crear_cliente_desde_fila(fila)

    assert cliente.genero == "PREFIERO NO DECIRLO"


@pytest.mark.parametrize("id_usuario", [None, 0, -1, True, "1"])
def test_validar_id_rechaza_valores_invalidos(id_usuario):
    with pytest.raises(
        ValueError,
        match="El ID de usuario debe ser un entero positivo",
    ):
        ClienteDAO._validar_id(id_usuario)


def test_validar_id_acepta_entero_positivo():
    assert ClienteDAO._validar_id(1) is None

@pytest.mark.parametrize(
    "contrasenia_actual",
    [
        None,
        "",
        123,
    ],
)
def test_actualizar_contrasenia_rechaza_contrasenia_actual_invalida(
    recursos,
    contrasenia_actual,
):
    dao, _, _ = recursos

    with pytest.raises(
        ValueError,
        match="La contraseña actual es obligatoria",
    ):
        dao.actualizar_contrasenia(
            1,
            contrasenia_actual,
            "ClaveNueva456!",
        )

@pytest.mark.parametrize(
    "contrasenia",
    [
        None,
        "",
        123,
        False,
    ],
)
def test_restablecer_contrasenia_rechaza_valor_vacio_o_invalido(
    recursos,
    contrasenia,
):
    dao, _, _ = recursos

    with pytest.raises(
        ValueError,
        match="La nueva contraseña no puede estar vacía",
    ):
        dao.restablecer_contrasenia(
            1,
            contrasenia,
        )


def test_restablecer_contrasenia_rechaza_contrasenia_debil(
    recursos,
):
    dao, _, _ = recursos

    with patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=False,
    ):
        with pytest.raises(
            ValueError,
            match="La nueva contraseña es muy débil",
        ):
            dao.restablecer_contrasenia(
                1,
                "ClaveDebil",
            )


def test_restablecer_contrasenia_lanza_error_si_cliente_no_existe(
    recursos,
):
    dao, cursor, conexion = recursos
    cursor.fetchone.return_value = None

    with patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.generar_hash",
        return_value=GestorSeguridad.generar_hash(
            "NuevaClave123!"
        ),
    ):
        with pytest.raises(
            ValueError,
            match="No se encontró el cliente con ID 1",
        ):
            dao.restablecer_contrasenia(
                1,
                "NuevaClave123!",
            )

    conexion.rollback.assert_called_once()
    conexion.commit.assert_not_called()


def test_restablecer_contrasenia_rechaza_hash_no_verificable(
    recursos,
):
    dao, cursor, conexion = recursos

    hash_generado = GestorSeguridad.generar_hash(
        "NuevaClave123!"
    )

    cursor.fetchone.return_value = (
        1,
        "cliente@example.com",
        hash_generado,
    )

    with patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.generar_hash",
        return_value=hash_generado,
    ), patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.verificar_contrasenia",
        return_value=False,
    ):
        with pytest.raises(
            RuntimeError,
            match=(
                "No se pudo confirmar el hash "
                "actualizado del cliente"
            ),
        ):
            dao.restablecer_contrasenia(
                1,
                "NuevaClave123!",
            )

    conexion.rollback.assert_called_once()
    conexion.commit.assert_not_called()


def test_restablecer_contrasenia_actualiza_y_confirma(
    recursos,
):
    dao, cursor, conexion = recursos

    nueva_contrasenia = "NuevaClave123!"
    hash_generado = GestorSeguridad.generar_hash(
        nueva_contrasenia
    )

    cursor.fetchone.return_value = (
        1,
        "cliente@example.com",
        hash_generado,
    )

    with patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ) as mock_fortaleza, patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.generar_hash",
        return_value=hash_generado,
    ) as mock_generar, patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.verificar_contrasenia",
        return_value=True,
    ) as mock_verificar:
        resultado = dao.restablecer_contrasenia(
            1,
            nueva_contrasenia,
        )

    assert resultado is True

    mock_fortaleza.assert_called_once_with(
        nueva_contrasenia
    )

    mock_generar.assert_called_once_with(
        nueva_contrasenia
    )

    mock_verificar.assert_called_once_with(
        nueva_contrasenia,
        hash_generado,
    )

    cursor.execute.assert_called_once()

    sql, parametros = cursor.execute.call_args.args

    assert "UPDATE usuarios" in sql
    assert "RETURNING" in sql

    assert parametros == (
        hash_generado,
        1,
    )

    conexion.commit.assert_called_once()
    conexion.rollback.assert_not_called()


def test_restablecer_contrasenia_hace_rollback_ante_error_sql(
    recursos,
):
    dao, cursor, conexion = recursos

    cursor.execute.side_effect = RuntimeError(
        "Fallo de base de datos"
    )

    hash_generado = GestorSeguridad.generar_hash(
        "NuevaClave123!"
    )

    with patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.persistencia.cliente_dao."
        "GestorSeguridad.generar_hash",
        return_value=hash_generado,
    ):
        with pytest.raises(
            RuntimeError,
            match="Fallo de base de datos",
        ):
            dao.restablecer_contrasenia(
                1,
                "NuevaClave123!",
            )

    conexion.rollback.assert_called_once()
    conexion.commit.assert_not_called()


@pytest.mark.parametrize(
    "id_usuario",
    [
        None,
        True,
        False,
        0,
        -1,
        "1",
    ],
)
def test_restablecer_contrasenia_valida_id(
    recursos,
    id_usuario,
):
    dao, _, _ = recursos

    with pytest.raises(
        ValueError,
        match="El ID de usuario debe ser un entero positivo",
    ):
        dao.restablecer_contrasenia(
            id_usuario,
            "NuevaClave123!",
        )

def test_listar_retorna_clientes_desde_filas(
    recursos,
):
    dao, cursor, conexion = recursos

    fila_1 = crear_fila_cliente(
        peso_objetivo=64.0,
        genero="MUJER",
    )

    fila_2 = list(
        crear_fila_cliente(
            peso_objetivo=70.0,
            genero="HOMBRE",
        )
    )

    fila_2[0] = 2
    fila_2[1] = "Carlos"
    fila_2[2] = "Lopez"
    fila_2[3] = "carlos@example.com"
    fila_2 = tuple(fila_2)

    cursor.fetchall.return_value = [
        fila_1,
        fila_2,
    ]

    resultado = dao.listar()

    assert len(resultado) == 2

    assert all(
        isinstance(cliente, Cliente)
        for cliente in resultado
    )

    assert resultado[0].id_usuario == 1
    assert resultado[0].nombre == "Laura"
    assert resultado[0].genero == "MUJER"

    assert resultado[1].id_usuario == 2
    assert resultado[1].nombre == "Carlos"
    assert resultado[1].apellido == "Lopez"
    assert resultado[1].correo_electronico == (
        "carlos@example.com"
    )
    assert resultado[1].genero == "HOMBRE"

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()

    sql = cursor.execute.call_args.args[0]

    assert "SELECT" in sql
    assert "FROM usuarios AS u" in sql
    assert "JOIN clientes AS c" in sql
    assert "ORDER BY u.id_usuario" in sql

    conexion.rollback.assert_not_called()