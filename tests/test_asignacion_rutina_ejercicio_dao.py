from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from psycopg2 import IntegrityError

from src.modelos.asignacion_rutina_ejercicio import (
    AsignacionRutinaEjercicio,
)
from src.persistencia.asignacion_rutina_ejercicio_dao import (
    AsignacionRutinaEjercicioDAO,
)


@pytest.fixture
def fila():
    return {
        "id_asignacion_ejercicio": 10,
        "id_asignacion": 1,
        "id_ejercicio": 2,
        "orden_ejercicio": 3,
        "veces_planificadas": 4,
        "activo": True,
        "fecha_agregado": date(2026, 1, 10),
    }


@pytest.fixture
def ejercicio():
    return AsignacionRutinaEjercicio(
        id_asignacion=1,
        id_ejercicio=2,
        orden_ejercicio=3,
        veces_planificadas=4,
        activo=True,
        fecha_agregado=date(2026, 1, 10),
        id_asignacion_ejercicio=10,
    )


@pytest.fixture
def entorno_dao():
    bd = MagicMock()
    conexion = MagicMock()
    administrador_cursor = MagicMock()
    cursor = MagicMock()

    bd._conexion = conexion
    conexion.cursor.return_value = administrador_cursor
    administrador_cursor.__enter__.return_value = cursor
    administrador_cursor.__exit__.return_value = False

    with patch(
        "src.persistencia.asignacion_rutina_ejercicio_dao."
        "ConexionBD.obtener_instancia",
        return_value=bd,
    ):
        dao = AsignacionRutinaEjercicioDAO()

    return dao, bd, conexion, cursor


def test_constructor_obtiene_instancia_de_base_de_datos():
    bd = MagicMock()

    with patch(
        "src.persistencia.asignacion_rutina_ejercicio_dao."
        "ConexionBD.obtener_instancia",
        return_value=bd,
    ) as obtener_instancia:
        dao = AsignacionRutinaEjercicioDAO()

    assert dao._bd is bd
    obtener_instancia.assert_called_once_with()


def test_guardar_retorna_entidad_y_confirma_transaccion(
    entorno_dao,
    ejercicio,
    fila,
):
    dao, bd, conexion, cursor = entorno_dao
    ejercicio.id_asignacion_ejercicio = None
    cursor.fetchone.return_value = fila

    resultado = dao.guardar(ejercicio)

    assert isinstance(resultado, AsignacionRutinaEjercicio)
    assert resultado.id_asignacion_ejercicio == 10
    assert resultado.id_asignacion == 1
    assert resultado.id_ejercicio == 2
    assert resultado.orden_ejercicio == 3
    assert resultado.veces_planificadas == 4
    assert resultado.activo is True
    assert resultado.fecha_agregado == date(2026, 1, 10)
    bd.abrir_conexion.assert_called_once_with()
    cursor.execute.assert_called_once()
    conexion.commit.assert_called_once_with()
    conexion.rollback.assert_not_called()


def test_guardar_lanza_error_si_insert_no_devuelve_fila(
    entorno_dao,
    ejercicio,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.fetchone.return_value = None

    with pytest.raises(
        RuntimeError,
        match="No se pudo recuperar el ejercicio asignado guardado",
    ):
        dao.guardar(ejercicio)

    conexion.rollback.assert_called_once_with()


def test_guardar_hace_rollback_ante_error_general(
    entorno_dao,
    ejercicio,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo SQL")

    with pytest.raises(RuntimeError, match="fallo SQL"):
        dao.guardar(ejercicio)

    conexion.rollback.assert_called_once_with()


def test_guardar_convierte_error_de_integridad(
    entorno_dao,
    ejercicio,
):
    dao, _, conexion, cursor = entorno_dao
    error = IntegrityError("violación de restricción")
    cursor.execute.side_effect = error

    with patch.object(
        dao,
        "_convertir_error_integridad",
        return_value=ValueError("error de dominio"),
    ) as convertir:
        with pytest.raises(ValueError, match="error de dominio"):
            dao.guardar(ejercicio)

    conexion.rollback.assert_called_once_with()
    convertir.assert_called_once_with(error)


def test_buscar_por_id_retorna_entidad_si_existe(entorno_dao, fila):
    dao, bd, conexion, cursor = entorno_dao
    cursor.fetchone.return_value = fila

    resultado = dao.buscar_por_id("10")

    assert isinstance(resultado, AsignacionRutinaEjercicio)
    assert resultado.id_asignacion_ejercicio == 10
    assert resultado.id_ejercicio == 2
    bd.abrir_conexion.assert_called_once_with()
    conexion.rollback.assert_not_called()
    cursor.execute.assert_called_once()


def test_buscar_por_id_retorna_none_si_no_existe(entorno_dao):
    dao, _, _, cursor = entorno_dao
    cursor.fetchone.return_value = None

    assert dao.buscar_por_id(99) is None


def test_buscar_por_id_hace_rollback_ante_error(entorno_dao):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("consulta fallida")

    with pytest.raises(RuntimeError, match="consulta fallida"):
        dao.buscar_por_id(10)

    conexion.rollback.assert_called_once_with()


@pytest.mark.parametrize("valor", [None, True, False, 0, -1, "texto"])
def test_buscar_por_id_valida_identificador(entorno_dao, valor):
    dao, bd, _, _ = entorno_dao

    with pytest.raises(ValueError, match="entero positivo"):
        dao.buscar_por_id(valor)

    bd.abrir_conexion.assert_not_called()


def test_listar_por_asignacion_retorna_entidades(entorno_dao, fila):
    dao, _, _, cursor = entorno_dao
    segunda_fila = dict(fila)
    segunda_fila["id_asignacion_ejercicio"] = 11
    segunda_fila["id_ejercicio"] = 8
    cursor.fetchall.return_value = [fila, segunda_fila]

    resultado = dao.listar_por_asignacion(1)

    assert len(resultado) == 2
    assert all(
        isinstance(elemento, AsignacionRutinaEjercicio)
        for elemento in resultado
    )
    assert resultado[1].id_ejercicio == 8

    consulta = cursor.execute.call_args.args[0]
    assert "AND activo = TRUE" not in consulta


def test_listar_por_asignacion_solo_activos_agrega_filtro(
    entorno_dao,
    fila,
):
    dao, _, _, cursor = entorno_dao
    cursor.fetchall.return_value = [fila]

    resultado = dao.listar_por_asignacion(1, solo_activos=True)

    assert len(resultado) == 1
    consulta = cursor.execute.call_args.args[0]
    assert "AND activo = TRUE" in consulta


def test_listar_por_asignacion_hace_rollback_ante_error(entorno_dao):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("error al listar")

    with pytest.raises(RuntimeError, match="error al listar"):
        dao.listar_por_asignacion(1)

    conexion.rollback.assert_called_once_with()


@pytest.mark.parametrize("fila_db, esperado", [(None, 1), ((7,), 7)])
def test_obtener_siguiente_orden(entorno_dao, fila_db, esperado):
    dao, _, _, cursor = entorno_dao
    cursor.fetchone.return_value = fila_db

    assert dao.obtener_siguiente_orden(1) == esperado


def test_obtener_siguiente_orden_hace_rollback_ante_error(entorno_dao):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo orden")

    with pytest.raises(RuntimeError, match="fallo orden"):
        dao.obtener_siguiente_orden(1)

    conexion.rollback.assert_called_once_with()


def test_actualizar_retorna_entidad_actualizada(
    entorno_dao,
    ejercicio,
    fila,
):
    dao, _, conexion, cursor = entorno_dao
    fila_actualizada = dict(fila)
    fila_actualizada["veces_planificadas"] = 8
    cursor.fetchone.return_value = fila_actualizada
    ejercicio.veces_planificadas = 8

    resultado = dao.actualizar(ejercicio)

    assert resultado.veces_planificadas == 8
    conexion.commit.assert_called_once_with()


def test_actualizar_exige_identificador(entorno_dao, ejercicio):
    dao, bd, _, _ = entorno_dao
    ejercicio.id_asignacion_ejercicio = None

    with pytest.raises(ValueError, match="debe tener un ID"):
        dao.actualizar(ejercicio)

    bd.abrir_conexion.assert_not_called()


def test_actualizar_lanza_error_si_no_encuentra_registro(
    entorno_dao,
    ejercicio,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="No se encontró el ejercicio asignado"):
        dao.actualizar(ejercicio)

    conexion.rollback.assert_called_once_with()


def test_actualizar_hace_rollback_ante_error_general(
    entorno_dao,
    ejercicio,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo actualización")

    with pytest.raises(RuntimeError, match="fallo actualización"):
        dao.actualizar(ejercicio)

    conexion.rollback.assert_called_once_with()


def test_actualizar_convierte_error_integridad(
    entorno_dao,
    ejercicio,
):
    dao, _, conexion, cursor = entorno_dao
    error = IntegrityError("duplicado")
    cursor.execute.side_effect = error

    with patch.object(
        dao,
        "_convertir_error_integridad",
        return_value=ValueError("registro duplicado"),
    ):
        with pytest.raises(ValueError, match="registro duplicado"):
            dao.actualizar(ejercicio)

    conexion.rollback.assert_called_once_with()


@pytest.mark.parametrize(
    "rowcount, esperado",
    [
        (1, True),
        (0, False),
    ],
)
def test_actualizar_meta_retorna_estado(
    entorno_dao,
    rowcount,
    esperado,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.rowcount = rowcount

    resultado = dao.actualizar_meta(10, 5)

    assert resultado is esperado
    conexion.commit.assert_called_once_with()


@pytest.mark.parametrize("veces", [None, True, False, 0, -1, "5"])
def test_actualizar_meta_valida_veces_planificadas(
    entorno_dao,
    veces,
):
    dao, bd, _, _ = entorno_dao

    with pytest.raises(ValueError, match="entero mayor que cero"):
        dao.actualizar_meta(10, veces)

    bd.abrir_conexion.assert_not_called()


def test_actualizar_meta_hace_rollback_ante_error(entorno_dao):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo meta")

    with pytest.raises(RuntimeError, match="fallo meta"):
        dao.actualizar_meta(10, 3)

    conexion.rollback.assert_called_once_with()


@pytest.mark.parametrize(
    "metodo",
    [
        "desactivar",
        "activar",
    ],
)
@pytest.mark.parametrize(
    "rowcount, esperado",
    [
        (1, True),
        (0, False),
    ],
)
def test_activar_y_desactivar_retorna_estado(
    entorno_dao,
    metodo,
    rowcount,
    esperado,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.rowcount = rowcount

    resultado = getattr(dao, metodo)(10)

    assert resultado is esperado
    conexion.commit.assert_called_once_with()


@pytest.mark.parametrize(
    "metodo",
    [
        "desactivar",
        "activar",
    ],
)
def test_activar_y_desactivar_hacen_rollback_ante_error(
    entorno_dao,
    metodo,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo de estado")

    with pytest.raises(RuntimeError, match="fallo de estado"):
        getattr(dao, metodo)(10)

    conexion.rollback.assert_called_once_with()


def test_copiar_desde_rutina_retorna_cantidad_insertada(entorno_dao):
    dao, _, conexion, cursor = entorno_dao
    cursor.rowcount = 3

    resultado = dao.copiar_desde_rutina(1, 2, 4)

    assert resultado == 3
    conexion.commit.assert_called_once_with()

    parametros = cursor.execute.call_args.args[1]
    assert parametros == (1, 4, 2)


@pytest.mark.parametrize("veces", [None, True, False, 0, -2, "3"])
def test_copiar_desde_rutina_valida_veces_planificadas(
    entorno_dao,
    veces,
):
    dao, bd, _, _ = entorno_dao

    with pytest.raises(ValueError, match="entero mayor que cero"):
        dao.copiar_desde_rutina(1, 2, veces)

    bd.abrir_conexion.assert_not_called()


def test_copiar_desde_rutina_hace_rollback_ante_error_general(
    entorno_dao,
):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo al copiar")

    with pytest.raises(RuntimeError, match="fallo al copiar"):
        dao.copiar_desde_rutina(1, 2)

    conexion.rollback.assert_called_once_with()


def test_copiar_desde_rutina_convierte_error_integridad(
    entorno_dao,
):
    dao, _, conexion, cursor = entorno_dao
    error = IntegrityError("referencia inexistente")
    cursor.execute.side_effect = error

    with patch.object(
        dao,
        "_convertir_error_integridad",
        return_value=ValueError("referencia inválida"),
    ):
        with pytest.raises(ValueError, match="referencia inválida"):
            dao.copiar_desde_rutina(1, 2)

    conexion.rollback.assert_called_once_with()


def test_obtener_progreso_retorna_diccionarios(entorno_dao):
    dao, _, _, cursor = entorno_dao
    progreso = {
        "id_asignacion_ejercicio": 10,
        "id_asignacion": 1,
        "id_ejercicio": 2,
        "nombre_ejercicio": "Caminata",
        "tipo_ejercicio": "Cardio",
        "duracion_minutos": 30,
        "intensidad_ejercicio": "Media",
        "orden_ejercicio": 1,
        "veces_planificadas": 3,
        "activo": True,
        "veces_realizadas": 2,
        "completado": False,
    }
    cursor.fetchall.return_value = [progreso]

    resultado = dao.obtener_progreso(1)

    assert resultado == [progreso]
    consulta = cursor.execute.call_args.args[0]
    assert "AND are.activo = TRUE" in consulta


def test_obtener_progreso_incluye_inactivos_si_se_indica(
    entorno_dao,
):
    dao, _, _, cursor = entorno_dao
    cursor.fetchall.return_value = []

    resultado = dao.obtener_progreso(1, solo_activos=False)

    assert resultado == []
    consulta = cursor.execute.call_args.args[0]
    assert "AND are.activo = TRUE" not in consulta


def test_obtener_progreso_hace_rollback_ante_error(entorno_dao):
    dao, _, conexion, cursor = entorno_dao
    cursor.execute.side_effect = RuntimeError("fallo progreso")

    with pytest.raises(RuntimeError, match="fallo progreso"):
        dao.obtener_progreso(1)

    conexion.rollback.assert_called_once_with()


def test_asignacion_esta_completada_es_falsa_si_no_hay_progreso(
    entorno_dao,
):
    dao, _, _, _ = entorno_dao

    with patch.object(dao, "obtener_progreso", return_value=[]):
        assert dao.asignacion_esta_completada(1) is False


def test_asignacion_esta_completada_es_verdadera_si_todo_completo(
    entorno_dao,
):
    dao, _, _, _ = entorno_dao
    progreso = [
        {"completado": True},
        {"completado": 1},
    ]

    with patch.object(
        dao,
        "obtener_progreso",
        return_value=progreso,
    ) as obtener_progreso:
        assert dao.asignacion_esta_completada(1) is True

    obtener_progreso.assert_called_once_with(
        id_asignacion=1,
        solo_activos=True,
    )


def test_asignacion_esta_completada_es_falsa_si_hay_pendientes(
    entorno_dao,
):
    dao, _, _, _ = entorno_dao

    with patch.object(
        dao,
        "obtener_progreso",
        return_value=[
            {"completado": True},
            {"completado": False},
        ],
    ):
        assert dao.asignacion_esta_completada(1) is False


def test_crear_desde_fila_convierte_fila_en_entidad(fila):
    resultado = AsignacionRutinaEjercicioDAO._crear_desde_fila(fila)

    assert isinstance(resultado, AsignacionRutinaEjercicio)
    assert resultado.id_asignacion_ejercicio == 10
    assert resultado.id_asignacion == 1
    assert resultado.id_ejercicio == 2


def test_crear_desde_fila_acepta_fila_sin_id(fila):
    fila.pop("id_asignacion_ejercicio")

    resultado = AsignacionRutinaEjercicioDAO._crear_desde_fila(fila)

    assert resultado.id_asignacion_ejercicio is None


def test_validar_entidad_acepta_entidad_valida(ejercicio):
    assert AsignacionRutinaEjercicioDAO._validar_entidad(ejercicio) is None


def test_validar_entidad_rechaza_objeto_de_otro_tipo():
    with pytest.raises(TypeError, match="AsignacionRutinaEjercicio"):
        AsignacionRutinaEjercicioDAO._validar_entidad(object())


@pytest.mark.parametrize(
    "atributo, valor, mensaje",
    [
        ("id_asignacion", 0, "ID de la asignación"),
        ("id_ejercicio", 0, "ID del ejercicio"),
        ("orden_ejercicio", 0, "orden del ejercicio"),
        ("veces_planificadas", 0, "veces planificadas"),
        ("activo", "sí", "campo activo"),
    ],
)
def test_validar_entidad_rechaza_campos_invalidos(
    ejercicio,
    atributo,
    valor,
    mensaje,
):
    object.__setattr__(ejercicio, f"_{atributo}", valor)

    with pytest.raises(ValueError, match=mensaje):
        AsignacionRutinaEjercicioDAO._validar_entidad(ejercicio)


@pytest.mark.parametrize(
    "valor, esperado",
    [
        (1, 1),
        ("7", 7),
        (3.8, 3),
    ],
)
def test_validar_id_convierte_valores_validos(valor, esperado):
    assert (
        AsignacionRutinaEjercicioDAO._validar_id(
            valor,
            "El identificador",
        )
        == esperado
    )


@pytest.mark.parametrize(
    "valor",
    [
        None,
        True,
        False,
        0,
        -1,
        "abc",
        [],
    ],
)
def test_validar_id_rechaza_valores_invalidos(valor):
    with pytest.raises(ValueError, match="entero positivo"):
        AsignacionRutinaEjercicioDAO._validar_id(
            valor,
            "El identificador",
        )


@pytest.mark.parametrize(
    "codigo, mensaje",
    [
        (
            "23503",
            "La asignación o el ejercicio indicado no existe",
        ),
        (
            "23505",
            "El ejercicio ya pertenece a esta asignación",
        ),
        (
            "23514",
            "Los datos no cumplen las restricciones",
        ),
        (
            "23502",
            "Falta un dato obligatorio",
        ),
        (
            None,
            "No se pudo guardar el ejercicio asignado",
        ),
        (
            "99999",
            "No se pudo guardar el ejercicio asignado",
        ),
    ],
)
def test_convertir_error_integridad(codigo, mensaje):
    error = SimpleNamespace(pgcode=codigo)

    resultado = AsignacionRutinaEjercicioDAO._convertir_error_integridad(
        error
    )

    assert isinstance(resultado, ValueError)
    assert mensaje in str(resultado)