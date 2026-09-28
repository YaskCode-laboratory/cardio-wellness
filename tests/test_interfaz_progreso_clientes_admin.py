from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
from unittest.mock import Mock

from src.interfaz.interfaz_progreso import InterfazProgreso
import pytest

from src.interfaz.interfaz_progreso_clientes_admin import (
    InterfazProgresoClientesAdmin,
)


class WidgetFalso:
    """
    Widget genérico para pruebas de ttk sin iniciar Tkinter.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.valor = ""
        self.valores = []
        self.configuraciones = []
        self.grid_args = []
        self.pack_args = []
        self.insertados = []
        self.eliminaciones = []
        self.items = {}
        self.children = []

    def pack(self, *args, **kwargs):
        self.pack_args.append((args, kwargs))

    def grid(self, *args, **kwargs):
        self.grid_args.append((args, kwargs))

    def config(self, *args, **kwargs):
        self.configuraciones.append((args, kwargs))

    def set(self, valor):
        self.valor = valor

    def get(self):
        return self.valor

    def __setitem__(self, clave, valor):
        if clave == "values":
            self.valores = list(valor)

    def __getitem__(self, clave):
        if clave == "values":
            return self.valores

        raise KeyError(clave)

    def heading(self, *args, **kwargs):
        pass

    def column(self, *args, **kwargs):
        pass

    def get_children(self):
        return list(self.children)

    def delete(self, item):
        self.eliminaciones.append(item)

        if item in self.children:
            self.children.remove(item)

    def insert(self, *args, **kwargs):
        self.insertados.append((args, kwargs))

        identificador = f"item_{len(self.insertados)}"
        self.children.append(identificador)

        self.items[identificador] = {
            "values": kwargs.get("values", ()),
        }

        return identificador


class FrameFalso(WidgetFalso):
    """Frame falso."""


class LabelFalso(WidgetFalso):
    """Label falso."""


class LabelFrameFalso(WidgetFalso):
    """LabelFrame falso."""


class ComboboxFalso(WidgetFalso):
    """Combobox falso."""


class ButtonFalso(WidgetFalso):
    """Button falso."""


class TreeviewFalso(WidgetFalso):
    """Treeview falso."""


class TestInterfazProgresoClientesAdmin:
    @pytest.fixture
    def control_clientes(self):
        """
        Crea controlador de clientes simulado.
        """
        return MagicMock()

    @pytest.fixture
    def control_progreso(self):
        """
        Crea controlador de progreso simulado.
        """
        return MagicMock()

    @pytest.fixture
    def cliente(self):
        """
        Crea cliente de ejemplo.
        """
        cliente = MagicMock()

        cliente.id_usuario = 10
        cliente.nombre = "Ana"
        cliente.apellido = "Pérez"
        cliente.obtener_nombre_completo.return_value = (
            "Ana Pérez"
        )

        return cliente

    @pytest.fixture
    def interfaz(
        self,
        control_clientes,
        control_progreso,
    ):
        """
        Crea interfaz sin ejecutar ttk.Frame.__init__.
        """
        interfaz = object.__new__(
            InterfazProgresoClientesAdmin
        )

        interfaz._control_clientes = control_clientes
        interfaz._control_progreso = control_progreso
        interfaz._clientes_por_id = {}
        interfaz._ids_por_texto = {}

        interfaz._cb_clientes = ComboboxFalso()
        interfaz._lbl_estado = LabelFalso()

        interfaz._labels_resumen = {
            "sesiones": LabelFalso(),
            "completadas": LabelFalso(),
            "minutos": LabelFalso(),
            "calorias": LabelFalso(),
            "planificadas": LabelFalso(),
            "realizadas": LabelFalso(),
            "cumplimiento": LabelFalso(),
        }

        interfaz._tree_sesiones = TreeviewFalso()
        interfaz._tree_progreso_mensual = TreeviewFalso()

        return interfaz

    def test_constructor_inicializa_componentes(
        self,
        control_clientes,
        control_progreso,
    ):
        """
        Verifica constructor, widgets y carga inicial de clientes.
        """
        master = MagicMock()

        with patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Frame.__init__",
            return_value=None,
        ) as mock_frame_init, patch.object(
            InterfazProgresoClientesAdmin,
            "pack",
        ) as mock_pack, patch.object(
            InterfazProgresoClientesAdmin,
            "_crear_selector_cliente",
        ) as mock_selector, patch.object(
            InterfazProgresoClientesAdmin,
            "_crear_resumen",
        ) as mock_resumen, patch.object(
            InterfazProgresoClientesAdmin,
            "_crear_tabla_sesiones",
        ) as mock_sesiones, patch.object(
            InterfazProgresoClientesAdmin,
            "_crear_tabla_progreso_mensual",
        ) as mock_progreso, patch.object(
            InterfazProgresoClientesAdmin,
            "cargar_clientes",
        ) as mock_cargar:
            interfaz = InterfazProgresoClientesAdmin(
                master,
                control_clientes,
                control_progreso,
            )

        mock_frame_init.assert_called_once_with(
            master,
            padding=10,
        )

        mock_pack.assert_called_once_with(
            fill="both",
            expand=True,
        )

        mock_selector.assert_called_once_with()
        mock_resumen.assert_called_once_with()
        mock_sesiones.assert_called_once_with()
        mock_progreso.assert_called_once_with()
        mock_cargar.assert_called_once_with()

        assert interfaz.control_clientes is control_clientes
        assert interfaz.control_progreso is control_progreso
        assert interfaz._clientes_por_id == {}
        assert interfaz._ids_por_texto == {}

    @pytest.mark.parametrize(
        ("control_clientes", "control_progreso", "mensaje"),
        [
            (
                None,
                MagicMock(),
                "Se requiere un ControlClientes inicializado.",
            ),
            (
                MagicMock(),
                None,
                "Se requiere un ControlProgreso inicializado.",
            ),
        ],
    )
    def test_constructor_valida_controladores(
        self,
        control_clientes,
        control_progreso,
        mensaje,
    ):
        """
        Verifica validación de dependencias obligatorias.
        """
        with patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Frame.__init__",
            return_value=None,
        ):
            with pytest.raises(ValueError) as error:
                InterfazProgresoClientesAdmin(
                    MagicMock(),
                    control_clientes,
                    control_progreso,
                )

        assert str(error.value) == mensaje

    def test_crear_selector_cliente(
        self,
        interfaz,
    ):
        """
        Verifica creación de controles de selección.
        """
        with patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.LabelFrame",
            side_effect=LabelFrameFalso,
        ), patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Label",
            side_effect=LabelFalso,
        ), patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Combobox",
            side_effect=ComboboxFalso,
        ), patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Button",
            side_effect=ButtonFalso,
        ):
            interfaz._crear_selector_cliente()

        assert isinstance(
            interfaz._cb_clientes,
            ComboboxFalso,
        )

        assert isinstance(
            interfaz._lbl_estado,
            LabelFalso,
        )

    def test_crear_resumen(
        self,
        interfaz,
    ):
        """
        Verifica creación de etiquetas de resumen.
        """
        with patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.LabelFrame",
            side_effect=LabelFrameFalso,
        ), patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Label",
            side_effect=LabelFalso,
        ):
            interfaz._crear_resumen()

        assert set(
            interfaz._labels_resumen.keys()
        ) == {
            "sesiones",
            "completadas",
            "minutos",
            "calorias",
            "planificadas",
            "realizadas",
            "cumplimiento",
        }

    def test_crear_tabla_sesiones(
        self,
        interfaz,
    ):
        """
        Verifica creación de tabla de sesiones.
        """
        tree = TreeviewFalso()

        with patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.LabelFrame",
            side_effect=LabelFrameFalso,
        ), patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Treeview",
            return_value=tree,
        ):
            interfaz._crear_tabla_sesiones()

        assert interfaz._tree_sesiones is tree

    def test_crear_tabla_progreso_mensual(
        self,
        interfaz,
    ):
        """
        Verifica creación de tabla de progreso mensual.
        """
        tree = TreeviewFalso()

        with patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.LabelFrame",
            side_effect=LabelFrameFalso,
        ), patch(
            "src.interfaz.interfaz_progreso_clientes_admin."
            "ttk.Treeview",
            return_value=tree,
        ):
            interfaz._crear_tabla_progreso_mensual()

        assert interfaz._tree_progreso_mensual is tree

    def test_cargar_clientes_correctamente(
        self,
        interfaz,
        control_clientes,
        cliente,
    ):
        """
        Verifica carga de clientes al Combobox.
        """
        control_clientes.listar.return_value = [cliente]

        interfaz.cargar_clientes()

        control_clientes.listar.assert_called_once_with()

        assert interfaz._cb_clientes.valores == [
            "10 - Ana Pérez",
        ]

        assert interfaz._cb_clientes.valor == (
            "10 - Ana Pérez"
        )

        assert interfaz._clientes_por_id == {
            10: cliente,
        }

        assert interfaz._ids_por_texto == {
            "10 - Ana Pérez": 10,
        }

    def test_cargar_clientes_omite_cliente_sin_id(
        self,
        interfaz,
        control_clientes,
        cliente,
    ):
        """
        Verifica omisión de clientes sin ID entero válido.
        """
        cliente_invalido = MagicMock()
        cliente_invalido.id_usuario = "sin-id"

        control_clientes.listar.return_value = [
            cliente,
            cliente_invalido,
        ]

        interfaz.cargar_clientes()

        assert interfaz._cb_clientes.valores == [
            "10 - Ana Pérez",
        ]

    def test_cargar_clientes_sin_resultados(
        self,
        interfaz,
        control_clientes,
    ):
        """
        Verifica estado de lista vacía.
        """
        control_clientes.listar.return_value = []

        interfaz.cargar_clientes()

        assert interfaz._cb_clientes.valores == []
        assert interfaz._cb_clientes.valor == ""

        assert interfaz._lbl_estado.configuraciones[-1][1] == {
            "text": "No hay clientes registrados.",
            "foreground": "#b71c1c",
        }

    def test_cargar_clientes_maneja_error(
        self,
        interfaz,
        control_clientes,
    ):
        """
        Verifica error al consultar clientes.
        """
        control_clientes.listar.side_effect = RuntimeError(
            "Error de base de datos"
        )

        interfaz.cargar_clientes()

        assert interfaz._cb_clientes.valores == []
        assert interfaz._cb_clientes.valor == ""

        assert interfaz._lbl_estado.configuraciones[-1][1] == {
            "text": (
                "No se pudieron cargar los clientes: "
                "Error de base de datos"
            ),
            "foreground": "#b71c1c",
        }

    def test_cargar_progreso_sin_cliente_seleccionado(
        self,
        interfaz,
    ):
        """
        Verifica validación de selección inexistente.
        """
        interfaz._cb_clientes.valor = ""

        interfaz.cargar_progreso_cliente()

        assert interfaz._lbl_estado.configuraciones[-1][1] == {
            "text": "Seleccione un cliente válido.",
            "foreground": "#b71c1c",
        }

    def test_cargar_progreso_cliente_no_encontrado(
        self,
        interfaz,
    ):
        """
        Verifica cliente seleccionado no disponible.
        """
        interfaz._cb_clientes.valor = "10 - Ana Pérez"
        interfaz._ids_por_texto = {
            "10 - Ana Pérez": 10,
        }

        interfaz._clientes_por_id = {}

        interfaz.cargar_progreso_cliente()

        assert interfaz._lbl_estado.configuraciones[-1][1] == {
            "text": (
                "No se encontró el cliente seleccionado."
            ),
            "foreground": "#b71c1c",
        }

    def test_cargar_progreso_cliente_correctamente(
        self,
        interfaz,
        control_progreso,
        cliente,
    ):
        """
        Verifica carga exitosa de resumen, sesiones y progreso.
        """
        sesion = SimpleNamespace(
            fecha=date(2026, 9, 25),
            nombre_ejercicio="Caminata",
            duracion_real=45,
            intensidad_real=SimpleNamespace(value="MEDIA"),
            calorias_quemadas=Decimal("320.50"),
            veces_planificadas=3,
            veces_realizadas=3,
            porcentaje_cumplimiento=100.0,
            completada=True,
            observaciones="Buen ritmo",
        )

        progreso = SimpleNamespace(
            mes=date(2026, 9, 1),
            peso=Decimal("68.50"),
            sesiones_completadas=8,
            sesiones_planificadas=10,
            porcentaje_cumplimiento=80.0,
        )

        resumen = {
            "total_sesiones": 1,
            "sesiones_completadas": 1,
            "total_minutos": 45,
            "total_calorias": Decimal("320.50"),
            "total_veces_planificadas": 3,
            "total_veces_realizadas": 3,
            "porcentaje_cumplimiento": 100.0,
            "sesiones": [sesion],
        }

        interfaz._cb_clientes.valor = "10 - Ana Pérez"

        interfaz._ids_por_texto = {
            "10 - Ana Pérez": 10,
        }

        interfaz._clientes_por_id = {
            10: cliente,
        }

        control_progreso.calcular_resumen_cliente.return_value = (
            resumen
        )

        control_progreso.consultar_progreso.return_value = [
            progreso,
        ]

        interfaz.cargar_progreso_cliente()

        control_progreso.calcular_resumen_cliente.assert_called_once_with(
            cliente
        )

        control_progreso.consultar_progreso.assert_called_once_with(
            cliente
        )

        assert interfaz._labels_resumen[
            "sesiones"
        ].configuraciones[-1][1] == {
            "text": "1",
        }

        assert interfaz._labels_resumen[
            "minutos"
        ].configuraciones[-1][1] == {
            "text": "45 min",
        }

        assert interfaz._labels_resumen[
            "calorias"
        ].configuraciones[-1][1] == {
            "text": "320.50 kcal",
        }

        assert interfaz._tree_sesiones.insertados[-1][1][
            "values"
        ] == (
            "2026-09-25",
            "Caminata",
            "45 min",
            "MEDIA",
            "320.50 kcal",
            "3/3",
            "100.00%",
            "COMPLETADA",
            "Buen ritmo",
        )

        assert interfaz._tree_progreso_mensual.insertados[-1][1][
            "values"
        ] == (
            "September 2026",
            "68.50 kg",
            "8",
            "10",
            "80.00%",
        )

    def test_cargar_progreso_maneja_error_y_limpia_datos(
        self,
        interfaz,
        control_progreso,
        cliente,
    ):
        """
        Verifica limpieza si falla el controlador.
        """
        interfaz._cb_clientes.valor = "10 - Ana Pérez"

        interfaz._ids_por_texto = {
            "10 - Ana Pérez": 10,
        }

        interfaz._clientes_por_id = {
            10: cliente,
        }

        interfaz._tree_sesiones.children = [
            "sesion_anterior",
        ]

        interfaz._tree_progreso_mensual.children = [
            "progreso_anterior",
        ]

        control_progreso.calcular_resumen_cliente.side_effect = (
            RuntimeError("No disponible")
        )

        interfaz.cargar_progreso_cliente()

        assert (
            "sesion_anterior"
            in interfaz._tree_sesiones.eliminaciones
        )

        assert (
            "progreso_anterior"
            in interfaz._tree_progreso_mensual.eliminaciones
        )

        for etiqueta in interfaz._labels_resumen.values():
            assert etiqueta.configuraciones[-1][1] == {
                "text": "-",
            }

        assert interfaz._lbl_estado.configuraciones[-1][1] == {
            "text": (
                "No se pudo cargar el progreso: "
                "No disponible"
            ),
            "foreground": "#b71c1c",
        }

    def test_actualizar_resumen_usa_aliases(
        self,
        interfaz,
    ):
        """
        Verifica fallback a claves alternativas del resumen.
        """
        interfaz._actualizar_resumen(
            {
                "total_sesiones": 4,
                "sesiones_completadas": 3,
                "total_minutos": 120,
                "total_calorias": Decimal("650.5"),
                "veces_planificadas": 8,
                "veces_realizadas": 6,
                "porcentaje_cumplimiento": 75,
            }
        )

        assert interfaz._labels_resumen[
            "planificadas"
        ].configuraciones[-1][1] == {
            "text": "8",
        }

        assert interfaz._labels_resumen[
            "realizadas"
        ].configuraciones[-1][1] == {
            "text": "6",
        }

        assert interfaz._labels_resumen[
            "cumplimiento"
        ].configuraciones[-1][1] == {
            "text": "75.00%",
        }

    def test_cargar_sesiones_sin_sesiones(
        self,
        interfaz,
    ):
        """
        Verifica fila informativa sin historial.
        """
        interfaz._cargar_sesiones([])

        assert interfaz._tree_sesiones.insertados[-1][1][
            "values"
        ] == (
            "Sin sesiones",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )

    def test_cargar_sesiones_pendiente_con_porcentaje_callable(
        self,
        interfaz,
    ):
        """
        Verifica sesión pendiente y porcentaje como método.
        """

        def porcentaje():
            return 50.0

        sesion = SimpleNamespace(
            fecha=date(2026, 9, 20),
            nombre_ejercicio="Bicicleta",
            duracion_real=30,
            intensidad_real="ALTA",
            calorias_quemadas=250,
            veces_planificadas=4,
            veces_realizadas=2,
            porcentaje_cumplimiento=porcentaje,
            completada=False,
            observaciones="Cansancio",
        )

        interfaz._cargar_sesiones([sesion])

        assert interfaz._tree_sesiones.insertados[-1][1][
            "values"
        ] == (
            "2026-09-20",
            "Bicicleta",
            "30 min",
            "ALTA",
            "250.00 kcal",
            "2/4",
            "50.00%",
            "PENDIENTE",
            "Cansancio",
        )

    def test_cargar_sesiones_usa_valores_predeterminados(
        self,
        interfaz,
    ):
        """
        Verifica compatibilidad con sesiones incompletas.
        """
        sesion = SimpleNamespace()

        interfaz._cargar_sesiones([sesion])

        valores = interfaz._tree_sesiones.insertados[-1][1][
            "values"
        ]

        assert valores == (
            "",
            "Sin ejercicio",
            "0 min",
            "",
            "0.00 kcal",
            "0/0",
            "0.00%",
            "PENDIENTE",
            "",
        )

    def test_cargar_progreso_mensual_sin_datos(
        self,
        interfaz,
    ):
        """
        Verifica fila informativa sin progreso mensual.
        """
        interfaz._cargar_progreso_mensual([])

        assert interfaz._tree_progreso_mensual.insertados[-1][1][
            "values"
        ] == (
            "Sin progreso mensual",
            "",
            "",
            "",
            "",
        )

    def test_cargar_progreso_mensual_con_porcentaje_callable(
        self,
        interfaz,
    ):
        """
        Verifica progreso con mes no fecha y porcentaje callable.
        """

        def porcentaje():
            return 66.666

        progreso = SimpleNamespace(
            mes="2026-09",
            peso=70,
            sesiones_completadas=2,
            sesiones_planificadas=3,
            porcentaje_cumplimiento=porcentaje,
        )

        interfaz._cargar_progreso_mensual([progreso])

        assert interfaz._tree_progreso_mensual.insertados[-1][1][
            "values"
        ] == (
            "2026-09",
            "70.00 kg",
            "2",
            "3",
            "66.67%",
        )

    def test_limpiar_datos(
        self,
        interfaz,
    ):
        """
        Verifica limpieza de etiquetas y tablas.
        """
        interfaz._tree_sesiones.children = [
            "sesion_1",
            "sesion_2",
        ]

        interfaz._tree_progreso_mensual.children = [
            "progreso_1",
        ]

        interfaz._limpiar_datos()

        assert interfaz._tree_sesiones.eliminaciones == [
            "sesion_1",
            "sesion_2",
        ]

        assert (
            interfaz._tree_progreso_mensual.eliminaciones
            == ["progreso_1"]
        )

        for etiqueta in interfaz._labels_resumen.values():
            assert etiqueta.configuraciones[-1][1] == {
                "text": "-",
            }

    def test_limpiar_tree(
        self,
    ):
        """
        Verifica eliminación de elementos de Treeview.
        """
        tree = TreeviewFalso()

        tree.children = [
            "uno",
            "dos",
        ]

        InterfazProgresoClientesAdmin._limpiar_tree(tree)

        assert tree.eliminaciones == [
            "uno",
            "dos",
        ]

    def test_obtener_nombre_cliente_usa_metodo(
        self,
        cliente,
    ):
        """
        Verifica uso de obtener_nombre_completo.
        """
        resultado = (
            InterfazProgresoClientesAdmin
            ._obtener_nombre_cliente(cliente)
        )

        assert resultado == "Ana Pérez"

    def test_obtener_nombre_cliente_usa_nombre_y_apellido(
        self,
    ):
        """
        Verifica fallback a atributos nombre y apellido.
        """
        cliente = SimpleNamespace(
            nombre="Carlos",
            apellido="Gómez",
        )

        resultado = (
            InterfazProgresoClientesAdmin
            ._obtener_nombre_cliente(cliente)
        )

        assert resultado == "Carlos Gómez"

    def test_obtener_nombre_cliente_sin_nombre(
        self,
    ):
        """
        Verifica texto para cliente sin datos.
        """
        cliente = SimpleNamespace()

        resultado = (
            InterfazProgresoClientesAdmin
            ._obtener_nombre_cliente(cliente)
        )

        assert resultado == "Cliente sin nombre"

    @pytest.mark.parametrize(
        ("valor", "resultado"),
        [
            (Decimal("10.5"), "10.50"),
            (25, "25.00"),
            ("7.25", "7.25"),
            (None, "0.00"),
            ("invalido", "0.00"),
        ],
    )
    def test_formatear_decimal(
        self,
        valor,
        resultado,
    ):
        """
        Verifica formato decimal y valores inválidos.
        """
        assert (
            InterfazProgresoClientesAdmin
            ._formatear_decimal(valor)
            == resultado
        )

    @pytest.mark.parametrize(
        ("valor", "resultado"),
        [
            (100, "100.00"),
            (66.666, "66.67"),
            ("50", "50.00"),
            (None, "0.00"),
            ("invalido", "0.00"),
        ],
    )
    def test_formatear_porcentaje(
        self,
        valor,
        resultado,
    ):
        """
        Verifica formato porcentual y valores inválidos.
        """
        assert (
            InterfazProgresoClientesAdmin
            ._formatear_porcentaje(valor)
            == resultado
        )

def test_evaluar_meta_muestra_error_si_peso_objetivo_no_configurado():
    vista = InterfazProgreso.__new__(InterfazProgreso)

    vista._cliente = SimpleNamespace(
        objetivo="Bajar de peso",
        peso=82.0,
        peso_objetivo=None,
    )

    vista._lbl_meta = Mock()

    vista._evaluar_meta(
        {
            "total_sesiones": 0,
        }
    )

    vista._lbl_meta.config.assert_called_once_with(
        text="Meta de peso no configurada.",
        foreground="red",
    )