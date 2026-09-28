from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from src.interfaz.interfaz_rutinas_asignadas import (
    InterfazRutinasAsignadas,
)


class WidgetFalso:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.valor = ""
        self.eliminaciones = []
        self.insertados = []
        self.items = {}
        self.seleccion_actual = []
        self.configuraciones = []
        self.children = []
        self.bind_args = None

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def bind(self, *args, **kwargs):
        self.bind_args = (args, kwargs)

    def get(self):
        return self.valor

    def set(self, valor):
        self.valor = valor

    def delete(self, *args, **kwargs):
        self.eliminaciones.append((args, kwargs))
        self.valor = ""

    def insert(self, *args, **kwargs):
        self.insertados.append((args, kwargs))

        if len(args) >= 2 and args[0] == 0:
            self.valor = str(args[1])

    def config(self, *args, **kwargs):
        self.configuraciones.append((args, kwargs))

    def configure(self, *args, **kwargs):
        self.configuraciones.append((args, kwargs))

    def heading(self, *args, **kwargs):
        pass

    def column(self, *args, **kwargs):
        pass

    def get_children(self):
        return list(self.items.keys())

    def selection(self):
        return self.seleccion_actual

    def item(self, item_id, option=None):
        datos = self.items.get(
            item_id,
            {"values": ()},
        )

        if option == "values":
            return datos.get("values", ())

        return datos

    def focus_set(self):
        pass


class EntryFalso(WidgetFalso):
    pass


class LabelFalso(WidgetFalso):
    pass


class TreeviewFalso(WidgetFalso):
    pass


@pytest.fixture
def control_rutinas():
    control = MagicMock()
    control.asignacion_dao = MagicMock()
    return control


@pytest.fixture
def control_sesiones():
    return MagicMock()


@pytest.fixture
def control_ejercicios():
    control = MagicMock()
    control.listar.return_value = []
    return control


@pytest.fixture
def interfaz(
    control_rutinas,
    control_sesiones,
    control_ejercicios,
):
    instancia = object.__new__(
        InterfazRutinasAsignadas
    )

    instancia._controlador = control_rutinas
    instancia._control_rutinas = control_rutinas
    instancia._control_sesiones = control_sesiones
    instancia._control_ejercicios = control_ejercicios
    instancia._control_autenticacion = None

    instancia._id_cliente_actual = None
    instancia._id_asignacion_actual = None
    instancia._id_ejercicio_asignado_seleccionado = None
    instancia._ejercicios_disponibles = []

    instancia._ent_id_cliente = EntryFalso()

    instancia._lbl_cliente = LabelFalso()
    instancia._lbl_asignacion = LabelFalso()
    instancia._lbl_rutina = LabelFalso()
    instancia._lbl_estado = LabelFalso()

    instancia._tree_ejercicios = TreeviewFalso()

    return instancia


def asignacion_activa():
    return SimpleNamespace(
        id_asignacion=50,
        id_rutina=8,
        estado=SimpleNamespace(value="ACTIVA"),
    )


def preparar_asignacion(interfaz):
    interfaz._id_cliente_actual = 10
    interfaz._id_asignacion_actual = 50


def test_buscar_rutina_cliente_rechaza_id_vacio(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.buscar_rutina_cliente()

    mock_error.assert_called_once_with(
        "Ingrese el ID del cliente."
    )


@pytest.mark.parametrize(
    "valor",
    [
        "0",
        "-1",
        "texto",
    ],
)
def test_buscar_rutina_cliente_rechaza_id_invalido(
    interfaz,
    valor,
):
    interfaz._ent_id_cliente.valor = valor

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.buscar_rutina_cliente()

    mock_error.assert_called_once()


def test_buscar_rutina_cliente_rechaza_cliente_sin_rutina_activa(
    interfaz,
    control_rutinas,
):
    interfaz._ent_id_cliente.valor = "10"

    (
        control_rutinas
        .asignacion_dao
        .obtener_activa_por_cliente
        .return_value
    ) = None

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.buscar_rutina_cliente()

    mock_error.assert_called_once_with(
        "El cliente no tiene una rutina activa."
    )


def test_buscar_rutina_cliente_carga_datos_y_progreso(
    interfaz,
    control_rutinas,
):
    interfaz._ent_id_cliente.valor = "10"

    (
        control_rutinas
        .asignacion_dao
        .obtener_activa_por_cliente
        .return_value
    ) = asignacion_activa()

    control_rutinas.buscar_por_id.return_value = (
        SimpleNamespace(
            id_rutina=8,
            nombre="Rutina cardio",
        )
    )

    with patch.object(
        interfaz,
        "_cargar_progreso",
    ) as mock_progreso:
        interfaz.buscar_rutina_cliente()

    assert interfaz._id_cliente_actual == 10
    assert interfaz._id_asignacion_actual == 50

    assert interfaz._lbl_cliente.configuraciones[-1][1] == {
        "text": "Cliente: 10",
    }

    assert interfaz._lbl_asignacion.configuraciones[-1][1] == {
        "text": "Asignación: 50",
    }

    assert interfaz._lbl_rutina.configuraciones[-1][1] == {
        "text": "Rutina: Rutina cardio",
    }

    assert interfaz._lbl_estado.configuraciones[-1][1] == {
        "text": "Estado: ACTIVA",
    }

    mock_progreso.assert_called_once_with()


def test_buscar_rutina_cliente_usa_nombre_por_defecto_si_no_existe(
    interfaz,
    control_rutinas,
):
    interfaz._ent_id_cliente.valor = "10"

    (
        control_rutinas
        .asignacion_dao
        .obtener_activa_por_cliente
        .return_value
    ) = asignacion_activa()

    control_rutinas.buscar_por_id.return_value = None

    with patch.object(
        interfaz,
        "_cargar_progreso",
    ):
        interfaz.buscar_rutina_cliente()

    assert interfaz._lbl_rutina.configuraciones[-1][1] == {
        "text": "Rutina: Rutina #8",
    }


def test_actualizar_vista_rechaza_sin_asignacion(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.actualizar_vista()

    mock_error.assert_called_once_with(
        "Busque primero la rutina activa de un cliente."
    )


def test_actualizar_vista_carga_progreso(
    interfaz,
):
    interfaz._id_asignacion_actual = 50

    with patch.object(
        interfaz,
        "_cargar_progreso",
    ) as mock_progreso:
        interfaz.actualizar_vista()

    mock_progreso.assert_called_once_with()


def test_cargar_progreso_no_hace_nada_sin_asignacion(
    interfaz,
    control_rutinas,
):
    interfaz._cargar_progreso()

    control_rutinas.obtener_progreso_asignacion.assert_not_called()


def test_cargar_progreso_limpia_e_inserta_filas(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    interfaz._tree_ejercicios.items = {
        "fila_anterior": {
            "values": (
                1,
                1,
                "Anterior",
                2,
                0,
                "PENDIENTE",
            ),
        },
    }

    control_rutinas.obtener_progreso_asignacion.return_value = [
        {
            "id_asignacion_ejercicio": 70,
            "orden_ejercicio": 1,
            "nombre_ejercicio": "Caminata",
            "veces_planificadas": 3,
            "veces_realizadas": 1,
            "completado": False,
        },
        {
            "id_asignacion_ejercicio": 71,
            "orden_ejercicio": 2,
            "nombre_ejercicio": "Bicicleta",
            "veces_planificadas": 2,
            "veces_realizadas": 2,
            "completado": True,
        },
    ]

    interfaz._id_ejercicio_asignado_seleccionado = 99

    interfaz._cargar_progreso()

    assert (
        interfaz._tree_ejercicios.eliminaciones[0][0]
        == ("fila_anterior",)
    )

    assert len(interfaz._tree_ejercicios.insertados) == 2

    assert (
        interfaz._tree_ejercicios
        .insertados[0][1]["values"]
    ) == (
        70,
        1,
        "Caminata",
        3,
        1,
        "PENDIENTE",
    )

    assert (
        interfaz._tree_ejercicios
        .insertados[1][1]["values"]
    ) == (
        71,
        2,
        "Bicicleta",
        2,
        2,
        "COMPLETADO",
    )

    assert (
        interfaz._id_ejercicio_asignado_seleccionado
        is None
    )


def test_cargar_progreso_maneja_error(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    control_rutinas.obtener_progreso_asignacion.side_effect = (
        RuntimeError("Error de consulta")
    )

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz._cargar_progreso()

    mock_error.assert_called_once_with(
        (
            "No se pudo cargar el progreso de la "
            "asignación: Error de consulta"
        )
    )


def test_seleccionar_ejercicio_sin_seleccion_limpia_id(
    interfaz,
):
    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._seleccionar_ejercicio()

    assert (
        interfaz._id_ejercicio_asignado_seleccionado
        is None
    )


def test_seleccionar_ejercicio_guarda_id_valido(
    interfaz,
):
    interfaz._tree_ejercicios.seleccion_actual = ["fila1"]

    interfaz._tree_ejercicios.items = {
        "fila1": {
            "values": (
                "70",
                1,
                "Caminata",
                3,
                1,
                "PENDIENTE",
            ),
        },
    }

    interfaz._seleccionar_ejercicio()

    assert (
        interfaz._id_ejercicio_asignado_seleccionado
        == 70
    )


def test_seleccionar_ejercicio_limpia_id_invalido(
    interfaz,
):
    interfaz._tree_ejercicios.seleccion_actual = ["fila1"]

    interfaz._tree_ejercicios.items = {
        "fila1": {
            "values": (
                "invalido",
            ),
        },
    }

    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._seleccionar_ejercicio()

    assert (
        interfaz._id_ejercicio_asignado_seleccionado
        is None
    )


def test_actualizar_ejercicios_no_hace_nada_sin_control(
    interfaz,
):
    interfaz._control_ejercicios = None

    with patch.object(
        interfaz,
        "_cargar_ejercicios_disponibles",
    ) as mock_cargar:
        interfaz._actualizar_ejercicios_disponibles()

    mock_cargar.assert_not_called()


def test_actualizar_ejercicios_recarga_lista(
    interfaz,
):
    with patch.object(
        interfaz,
        "_cargar_ejercicios_disponibles",
    ) as mock_cargar:
        interfaz._actualizar_ejercicios_disponibles()

    mock_cargar.assert_called_once_with()


def test_cargar_ejercicios_disponibles(
    interfaz,
    control_ejercicios,
):
    ejercicios = [
        SimpleNamespace(
            id_ejercicio=1,
            nombre="Caminata",
        ),
        SimpleNamespace(
            id_ejercicio=2,
            nombre="Bicicleta",
        ),
    ]

    control_ejercicios.listar.return_value = ejercicios

    interfaz._cargar_ejercicios_disponibles()

    assert interfaz._ejercicios_disponibles == ejercicios


def test_cargar_ejercicios_disponibles_maneja_error(
    interfaz,
    control_ejercicios,
):
    control_ejercicios.listar.side_effect = RuntimeError(
        "Error al listar"
    )

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz._cargar_ejercicios_disponibles()

    mock_error.assert_called_once_with(
        (
            "No se pudieron cargar los ejercicios "
            "disponibles: Error al listar"
        )
    )


def test_agregar_ejercicio_rechaza_sin_asignacion(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.agregar_ejercicio_cliente()

    mock_error.assert_called_once_with(
        "Busque primero la rutina activa de un cliente."
    )


def test_agregar_ejercicio_rechaza_sin_control(
    interfaz,
):
    interfaz._id_asignacion_actual = 50
    interfaz._control_ejercicios = None

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.agregar_ejercicio_cliente()

    mock_error.assert_called_once_with(
        "No se configuró ControlEjercicios."
    )


def test_agregar_ejercicio_usuario_cancela_primer_dialogo(
    interfaz,
):
    interfaz._id_asignacion_actual = 50

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=None,
    ):
        interfaz.agregar_ejercicio_cliente()


def test_agregar_ejercicio_usuario_cancela_meta(
    interfaz,
):
    interfaz._id_asignacion_actual = 50

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[15, None],
    ):
        interfaz.agregar_ejercicio_cliente()


def test_agregar_ejercicio_correctamente(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    interfaz._ejercicios_disponibles = [
        SimpleNamespace(
            id_ejercicio=15,
            nombre="Caminata",
        ),
    ]

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[15, 3],
    ), patch.object(
        interfaz,
        "mostrar_mensaje",
    ) as mock_mensaje, patch.object(
        interfaz,
        "_cargar_progreso",
    ) as mock_progreso:
        interfaz.agregar_ejercicio_cliente()

    (
        control_rutinas
        .agregar_ejercicio_a_asignacion
        .assert_called_once_with(
            id_asignacion=50,
            id_ejercicio=15,
            veces_planificadas=3,
            usuario_accion=1,
        )
    )

    mock_mensaje.assert_called_once_with(
        "Ejercicio agregado al plan del cliente."
    )

    mock_progreso.assert_called_once_with()


def test_cambiar_meta_rechaza_sin_asignacion(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.cambiar_meta_ejercicio()

    mock_error.assert_called_once_with(
        "Busque primero la rutina activa de un cliente."
    )


def test_cambiar_meta_rechaza_sin_ejercicio_seleccionado(
    interfaz,
):
    interfaz._id_asignacion_actual = 50

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.cambiar_meta_ejercicio()

    mock_error.assert_called_once_with(
        (
            "Seleccione un ejercicio de la tabla "
            "antes de cambiar su meta."
        )
    )


def test_cambiar_meta_usuario_cancela(
    interfaz,
):
    interfaz._id_asignacion_actual = 50
    interfaz._id_ejercicio_asignado_seleccionado = 70

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=None,
    ):
        interfaz.cambiar_meta_ejercicio()


def test_cambiar_meta_correctamente(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50
    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    (
        control_rutinas
        .actualizar_meta_ejercicio_asignado
        .return_value
    ) = True

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=8,
    ), patch.object(
        interfaz,
        "mostrar_mensaje",
    ) as mock_mensaje, patch.object(
        interfaz,
        "_cargar_progreso",
    ) as mock_progreso:
        interfaz.cambiar_meta_ejercicio()

    (
        control_rutinas
        .actualizar_meta_ejercicio_asignado
        .assert_called_once_with(
            id_asignacion_ejercicio=70,
            veces_planificadas=8,
            usuario_accion=1,
        )
    )

    mock_mensaje.assert_called_once_with(
        "Meta actualizada correctamente."
    )

    mock_progreso.assert_called_once_with()


def test_cambiar_meta_muestra_error_si_no_actualiza(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50
    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    (
        control_rutinas
        .actualizar_meta_ejercicio_asignado
        .return_value
    ) = False

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=8,
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.cambiar_meta_ejercicio()

    mock_error.assert_called_once_with(
        "No se pudo cambiar la meta: No se pudo actualizar la meta."
    )


def test_desactivar_ejercicio_rechaza_sin_asignacion(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.desactivar_ejercicio_cliente()

    mock_error.assert_called_once_with(
        "Busque primero la rutina activa de un cliente."
    )


def test_desactivar_ejercicio_rechaza_sin_seleccion(
    interfaz,
):
    interfaz._id_asignacion_actual = 50

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.desactivar_ejercicio_cliente()

    mock_error.assert_called_once_with(
        (
            "Seleccione un ejercicio de la tabla "
            "antes de desactivarlo."
        )
    )


def test_desactivar_ejercicio_usuario_cancela(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50
    interfaz._id_ejercicio_asignado_seleccionado = 70

    with patch.object(
        interfaz,
        "confirmar_accion",
        return_value=False,
    ):
        interfaz.desactivar_ejercicio_cliente()

    (
        control_rutinas
        .desactivar_ejercicio_de_asignacion
        .assert_not_called()
    )


def test_desactivar_ejercicio_correctamente(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50
    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    (
        control_rutinas
        .desactivar_ejercicio_de_asignacion
        .return_value
    ) = True

    with patch.object(
        interfaz,
        "confirmar_accion",
        return_value=True,
    ), patch.object(
        interfaz,
        "mostrar_mensaje",
    ) as mock_mensaje, patch.object(
        interfaz,
        "_cargar_progreso",
    ) as mock_progreso:
        interfaz.desactivar_ejercicio_cliente()

    (
        control_rutinas
        .desactivar_ejercicio_de_asignacion
        .assert_called_once_with(
            id_asignacion_ejercicio=70,
            usuario_accion=1,
        )
    )

    mock_mensaje.assert_called_once_with(
        "Ejercicio desactivado correctamente."
    )

    mock_progreso.assert_called_once_with()


def test_obtener_valores_ejercicio_sin_seleccion(
    interfaz,
):
    assert (
        interfaz._obtener_valores_ejercicio_seleccionado()
        is None
    )


def test_obtener_valores_ejercicio_devuelve_tupla(
    interfaz,
):
    interfaz._tree_ejercicios.seleccion_actual = ["fila1"]

    interfaz._tree_ejercicios.items = {
        "fila1": {
            "values": (
                70,
                1,
                "Caminata",
                3,
                1,
                "PENDIENTE",
            ),
        },
    }

    assert (
        interfaz._obtener_valores_ejercicio_seleccionado()
        == (
            70,
            1,
            "Caminata",
            3,
            1,
            "PENDIENTE",
        )
    )


def test_obtener_rutina_actual_rechaza_sin_asignacion(
    interfaz,
):
    with pytest.raises(
        ValueError,
        match="No existe una asignación activa cargada.",
    ):
        interfaz._obtener_rutina_actual()


def test_obtener_rutina_actual_rechaza_asignacion_inexistente(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    control_rutinas.asignacion_dao.buscar_por_id.return_value = None

    with pytest.raises(
        ValueError,
        match="No se encontró la asignación actual.",
    ):
        interfaz._obtener_rutina_actual()


def test_obtener_rutina_actual_devuelve_id(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    control_rutinas.asignacion_dao.buscar_por_id.return_value = (
        SimpleNamespace(id_rutina="8")
    )

    assert interfaz._obtener_rutina_actual() == 8


def test_registrar_sesion_rechaza_sin_control_sesiones(
    interfaz,
):
    interfaz._control_sesiones = None

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.registrar_sesion_administrador()

    mock_error.assert_called_once_with(
        "No se configuró ControlSesiones."
    )


def test_registrar_sesion_rechaza_sin_cliente(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.registrar_sesion_administrador()

    mock_error.assert_called_once_with(
        "Busque primero la rutina activa de un cliente."
    )


def test_registrar_sesion_rechaza_sin_ejercicio(
    interfaz,
):
    preparar_asignacion(interfaz)

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=None,
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.registrar_sesion_administrador()

    mock_error.assert_called_once_with(
        (
            "Seleccione un ejercicio antes de "
            "registrar una sesión."
        )
    )


def test_registrar_sesion_rechaza_meta_completada(
    interfaz,
):
    preparar_asignacion(interfaz)

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            3,
            3,
            "COMPLETADO",
        ),
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.registrar_sesion_administrador()

    mock_error.assert_called_once_with(
        (
            "El ejercicio ya alcanzó su meta. "
            "No puede registrar más actividad."
        )
    )


def test_registrar_sesion_correctamente_y_recarga_progreso(
    interfaz,
    control_rutinas,
    control_sesiones,
):
    preparar_asignacion(interfaz)

    valores = (
        70,
        1,
        "Caminata",
        3,
        1,
        "PENDIENTE",
    )

    control_rutinas.asignacion_dao.buscar_por_id.return_value = (
        SimpleNamespace(id_rutina=8)
    )

    control_sesiones.registrar_sesion.return_value = (
        SimpleNamespace(
            id_sesion=90,
            calorias_quemadas=200,
        )
    )

    (
        control_rutinas
        .asignacion_dao
        .obtener_activa_por_cliente
        .return_value
    ) = asignacion_activa()

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=valores,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[1, 30],
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askstring",
        side_effect=["media", ""],
    ), patch.object(
        interfaz,
        "mostrar_mensaje",
    ) as mock_mensaje, patch.object(
        interfaz,
        "_cargar_progreso",
    ) as mock_progreso:
        interfaz.registrar_sesion_administrador()

    (
        control_sesiones
        .registrar_sesion
        .assert_called_once_with(
            cliente=10,
            rutina=8,
            duracion_real=30,
            intensidad_real="MEDIA",
            observaciones="",
            nombre_ejercicio="Caminata",
            veces_planificadas=2,
            veces_realizadas=1,
            id_asignacion_ejercicio=70,
        )
    )

    assert mock_mensaje.call_count == 1
    mock_progreso.assert_called_once_with()


def test_registrar_sesion_limpia_vista_si_rutina_finaliza(
    interfaz,
    control_rutinas,
    control_sesiones,
):
    preparar_asignacion(interfaz)

    control_rutinas.asignacion_dao.buscar_por_id.return_value = (
        SimpleNamespace(id_rutina=8)
    )

    control_sesiones.registrar_sesion.return_value = (
        SimpleNamespace(
            id_sesion=90,
            calorias_quemadas=200,
        )
    )

    (
        control_rutinas
        .asignacion_dao
        .obtener_activa_por_cliente
        .return_value
    ) = None

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            2,
            1,
            "PENDIENTE",
        ),
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[1, 30],
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askstring",
        side_effect=["ALTA", None],
    ), patch.object(
        interfaz,
        "mostrar_mensaje",
    ) as mock_mensaje, patch.object(
        interfaz,
        "limpiar_vista",
    ) as mock_limpiar:
        interfaz.registrar_sesion_administrador()

    assert mock_mensaje.call_count == 2
    mock_limpiar.assert_called_once_with()


def test_cambiar_rutina_rechaza_sin_cliente(
    interfaz,
):
    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.cambiar_rutina_cliente()

    mock_error.assert_called_once_with(
        "Busque primero la rutina activa de un cliente."
    )


def test_cambiar_rutina_rechaza_sin_asignacion(
    interfaz,
):
    interfaz._id_cliente_actual = 10

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.cambiar_rutina_cliente()

    mock_error.assert_called_once_with(
        "No existe una asignación activa cargada."
    )


def test_cambiar_rutina_rechaza_si_no_hay_rutinas(
    interfaz,
    control_rutinas,
):
    preparar_asignacion(interfaz)

    control_rutinas.listar.return_value = []

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.cambiar_rutina_cliente()

    mock_error.assert_called_once_with(
        "No se pudo cambiar la rutina: No hay rutinas disponibles."
    )


def test_cambiar_rutina_usuario_cancela(
    interfaz,
    control_rutinas,
):
    preparar_asignacion(interfaz)

    control_rutinas.listar.return_value = [
        SimpleNamespace(
            id_rutina=12,
            nombre="Nueva rutina",
        ),
    ]

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=None,
    ):
        interfaz.cambiar_rutina_cliente()


def test_cambiar_rutina_correctamente(
    interfaz,
    control_rutinas,
):
    preparar_asignacion(interfaz)

    control_rutinas.listar.return_value = [
        SimpleNamespace(
            id_rutina=12,
            nombre="Nueva rutina",
        ),
    ]

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    control_rutinas.cambiar_rutina_asignada.return_value = {
        "id_asignacion": 80,
    }

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=12,
    ), patch.object(
        interfaz,
        "confirmar_accion",
        return_value=True,
    ), patch.object(
        interfaz,
        "mostrar_mensaje",
    ) as mock_mensaje, patch.object(
        interfaz,
        "buscar_rutina_cliente",
    ) as mock_buscar:
        interfaz.cambiar_rutina_cliente()

    (
        control_rutinas
        .cambiar_rutina_asignada
        .assert_called_once_with(
            id_cliente=10,
            id_nueva_rutina=12,
            usuario_accion=1,
            observaciones=(
                "Rutina reemplazada por "
                "un administrador."
            ),
        )
    )

    assert interfaz._id_asignacion_actual == 80

    mock_mensaje.assert_called_once_with(
        (
            "Rutina cambiada correctamente.\n"
            "Nueva asignación: 80"
        )
    )

    mock_buscar.assert_called_once_with()


def test_limpiar_vista_reinicia_estado_y_widgets(
    interfaz,
):
    interfaz._id_cliente_actual = 10
    interfaz._id_asignacion_actual = 50
    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._ent_id_cliente.valor = "10"

    interfaz._tree_ejercicios.items = {
        "fila1": {
            "values": (70,),
        },
    }

    interfaz.limpiar_vista()

    assert interfaz._id_cliente_actual is None
    assert interfaz._id_asignacion_actual is None

    assert (
        interfaz._id_ejercicio_asignado_seleccionado
        is None
    )

    assert interfaz._ent_id_cliente.valor == ""

    assert interfaz._lbl_cliente.configuraciones[-1][1] == {
        "text": "Cliente: -",
    }

    assert interfaz._lbl_asignacion.configuraciones[-1][1] == {
        "text": "Asignación: -",
    }

    assert interfaz._lbl_rutina.configuraciones[-1][1] == {
        "text": "Rutina: -",
    }

    assert interfaz._lbl_estado.configuraciones[-1][1] == {
        "text": "Estado: -",
    }

    assert (
        interfaz._tree_ejercicios.eliminaciones[0][0]
        == ("fila1",)
    )


def test_obtener_id_administrador_desde_control_autenticacion(
    interfaz,
):
    interfaz._control_autenticacion = SimpleNamespace(
        usuario_actual=SimpleNamespace(
            id_usuario="25",
        )
    )

    assert interfaz._obtener_id_administrador() == 25


def test_obtener_id_administrador_desde_ventana_principal(
    interfaz,
):
    interfaz._control_autenticacion = None

    raiz = SimpleNamespace(
        master=None,
        _administrador_actual=SimpleNamespace(
            id_usuario="30",
        ),
    )

    interfaz.master = raiz

    assert interfaz._obtener_id_administrador() == 30


def test_obtener_id_administrador_rechaza_si_no_existe(
    interfaz,
):
    interfaz._control_autenticacion = None
    interfaz.master = None

    with pytest.raises(
        ValueError,
        match=(
            "No se pudo obtener el ID del "
            "administrador autenticado."
        ),
    ):
        interfaz._obtener_id_administrador()

def test_constructor_crea_formulario_tabla_y_botones(
    control_rutinas,
    control_sesiones,
    control_ejercicios,
):
    """
    Cubre el constructor real y la creación de widgets,
    sin abrir una ventana real de Tkinter.
    """
    master = MagicMock()

    tree = TreeviewFalso()

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "InterfazBase.__init__",
        return_value=None,
    ) as mock_base_init, patch.object(
        InterfazRutinasAsignadas,
        "pack",
    ) as mock_pack, patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "ttk.LabelFrame",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "ttk.Frame",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "ttk.Label",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "ttk.Entry",
        side_effect=EntryFalso,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "ttk.Button",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "ttk.Treeview",
        return_value=tree,
    ):
        instancia = InterfazRutinasAsignadas(
            master=master,
            control_rutinas=control_rutinas,
            control_sesiones=control_sesiones,
            control_autenticacion=None,
            control_ejercicios=control_ejercicios,
        )

    mock_base_init.assert_called_once_with(
        master,
        controlador=control_rutinas,
        padding=10,
    )

    mock_pack.assert_called_once_with(
        fill="both",
        expand=True,
    )

    assert instancia._control_rutinas is control_rutinas
    assert instancia._control_sesiones is control_sesiones
    assert instancia._control_ejercicios is control_ejercicios

    assert instancia._id_cliente_actual is None
    assert instancia._id_asignacion_actual is None

    assert (
        instancia._id_ejercicio_asignado_seleccionado
        is None
    )

    assert instancia._ejercicios_disponibles == []

    assert isinstance(
        instancia._ent_id_cliente,
        EntryFalso,
    )

    assert isinstance(
        instancia._lbl_cliente,
        WidgetFalso,
    )

    assert isinstance(
        instancia._lbl_asignacion,
        WidgetFalso,
    )

    assert isinstance(
        instancia._lbl_rutina,
        WidgetFalso,
    )

    assert isinstance(
        instancia._lbl_estado,
        WidgetFalso,
    )

    assert instancia._tree_ejercicios is tree

    control_ejercicios.listar.assert_called_once_with()

def test_buscar_rutina_cliente_maneja_error_inesperado(
    interfaz,
    control_rutinas,
):
    interfaz._ent_id_cliente.valor = "10"

    (
        control_rutinas
        .asignacion_dao
        .obtener_activa_por_cliente
        .side_effect
    ) = RuntimeError("Error de conexión")

    with patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.buscar_rutina_cliente()

    mock_error.assert_called_once_with(
        (
            "No se pudo buscar la rutina del "
            "cliente: Error de conexión"
        )
    )


def test_cargar_ejercicios_disponibles_sin_control_no_hace_nada(
    interfaz,
):
    interfaz._control_ejercicios = None
    interfaz._ejercicios_disponibles = ["ejercicio_anterior"]

    interfaz._cargar_ejercicios_disponibles()

    assert interfaz._ejercicios_disponibles == [
        "ejercicio_anterior",
    ]


def test_agregar_ejercicio_maneja_error_del_controlador(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    interfaz._ejercicios_disponibles = [
        SimpleNamespace(
            id_ejercicio=15,
            nombre="Caminata",
        ),
    ]

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    (
        control_rutinas
        .agregar_ejercicio_a_asignacion
        .side_effect
    ) = RuntimeError("No se pudo guardar")

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[15, 3],
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.agregar_ejercicio_cliente()

    mock_error.assert_called_once_with(
        (
            "No se pudo agregar el ejercicio: "
            "No se pudo guardar"
        )
    )


def test_desactivar_ejercicio_muestra_error_si_ya_esta_desactivado(
    interfaz,
    control_rutinas,
):
    interfaz._id_asignacion_actual = 50

    interfaz._id_ejercicio_asignado_seleccionado = 70

    interfaz._obtener_id_administrador = MagicMock(
        return_value=1
    )

    (
        control_rutinas
        .desactivar_ejercicio_de_asignacion
        .return_value
    ) = False

    with patch.object(
        interfaz,
        "confirmar_accion",
        return_value=True,
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.desactivar_ejercicio_cliente()

    mock_error.assert_called_once_with(
        (
            "No se pudo desactivar el ejercicio: "
            "El ejercicio ya estaba desactivado."
        )
    )


def test_obtener_valores_ejercicio_retorna_none_si_fila_no_tiene_valores(
    interfaz,
):
    interfaz._tree_ejercicios.seleccion_actual = [
        "fila_vacia",
    ]

    interfaz._tree_ejercicios.items = {
        "fila_vacia": {
            "values": (),
        },
    }

    assert (
        interfaz._obtener_valores_ejercicio_seleccionado()
        is None
    )


def test_registrar_sesion_retorna_si_cantidad_es_cancelada(
    interfaz,
):
    preparar_asignacion(interfaz)

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            3,
            1,
            "PENDIENTE",
        ),
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=None,
    ):
        interfaz.registrar_sesion_administrador()


def test_registrar_sesion_retorna_si_duracion_es_cancelada(
    interfaz,
):
    preparar_asignacion(interfaz)

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            3,
            1,
            "PENDIENTE",
        ),
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[1, None],
    ):
        interfaz.registrar_sesion_administrador()


def test_registrar_sesion_retorna_si_intensidad_es_cancelada(
    interfaz,
):
    preparar_asignacion(interfaz)

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            3,
            1,
            "PENDIENTE",
        ),
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[1, 30],
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askstring",
        return_value=None,
    ):
        interfaz.registrar_sesion_administrador()


def test_registrar_sesion_rechaza_intensidad_invalida(
    interfaz,
):
    preparar_asignacion(interfaz)

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            3,
            1,
            "PENDIENTE",
        ),
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[1, 30],
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askstring",
        return_value="MAXIMA",
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.registrar_sesion_administrador()

    mock_error.assert_called_once_with(
        "La intensidad debe ser BAJA, MEDIA o ALTA."
    )


def test_registrar_sesion_maneja_error_inesperado(
    interfaz,
    control_sesiones,
):
    preparar_asignacion(interfaz)

    control_sesiones.registrar_sesion.side_effect = (
        RuntimeError("Fallo de base de datos")
    )

    with patch.object(
        interfaz,
        "_obtener_valores_ejercicio_seleccionado",
        return_value=(
            70,
            1,
            "Caminata",
            3,
            1,
            "PENDIENTE",
        ),
    ), patch.object(
        interfaz,
        "_obtener_rutina_actual",
        return_value=8,
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        side_effect=[1, 30],
    ), patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askstring",
        side_effect=["MEDIA", ""],
    ), patch.object(
        interfaz,
        "mostrar_error",
    ) as mock_error:
        interfaz.registrar_sesion_administrador()

    mock_error.assert_called_once_with(
        (
            "No se pudo registrar la sesión: "
            "Fallo de base de datos"
        )
    )


def test_cambiar_rutina_retorna_si_usuario_no_confirma(
    interfaz,
    control_rutinas,
):
    preparar_asignacion(interfaz)

    control_rutinas.listar.return_value = [
        SimpleNamespace(
            id_rutina=12,
            nombre="Rutina nueva",
        ),
    ]

    with patch(
        "src.interfaz.interfaz_rutinas_asignadas."
        "simpledialog.askinteger",
        return_value=12,
    ), patch.object(
        interfaz,
        "confirmar_accion",
        return_value=False,
    ):
        interfaz.cambiar_rutina_cliente()

    (
        control_rutinas
        .cambiar_rutina_asignada
        .assert_not_called()
    )