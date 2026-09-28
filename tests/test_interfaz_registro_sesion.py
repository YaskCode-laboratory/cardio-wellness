from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


import pytest


from src.interfaz.interfaz_registro_sesion import (
    InterfazRegistroSesion,
)


class WidgetFalso:
    def __init__(self, valor="", *args, **kwargs):
        self.valor = valor
        self.args = args
        self.kwargs = kwargs
        self.configuracion = {}
        self.eliminaciones = []
        self.valores = []

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def bind(self, *args, **kwargs):
        pass

    def get(self):
        return self.valor

    def set(self, valor):
        self.valor = valor

    def delete(self, *args, **kwargs):
        self.eliminaciones.append((args, kwargs))
        self.valor = ""

    def config(self, **kwargs):
        self.configuracion.update(kwargs)

    def __setitem__(self, clave, valor):
        if clave == "values":
            self.valores = list(valor)
        else:
            self.configuracion[clave] = valor

    def __getitem__(self, clave):
        if clave == "values":
            return self.valores

        return self.configuracion.get(clave)


class FrameFalso(WidgetFalso):
    pass


class LabelFalso(WidgetFalso):
    pass


class LabelFrameFalso(WidgetFalso):
    pass


class EntryFalso(WidgetFalso):
    pass


class ComboboxFalso(WidgetFalso):
    pass


class ButtonFalso(WidgetFalso):
    pass


class TestInterfazRegistroSesion:
    @pytest.fixture
    def control_sesiones(self):
        control = MagicMock()

        control.asignacion_dao = MagicMock()
        control.asignacion_ejercicio_dao = MagicMock()

        return control

    @pytest.fixture
    def interfaz(
        self,
        control_sesiones,
    ):
        interfaz = object.__new__(
            InterfazRegistroSesion
        )

        interfaz._controlador = control_sesiones
        interfaz._id_cliente = 10
        interfaz._id_rutina = 25
        interfaz._id_asignacion = 100
        interfaz._ejercicios_asignados = []
        interfaz._ejercicio_asignado_actual = None

        interfaz._cb_ejercicio = ComboboxFalso()
        interfaz._ent_veces_realizadas = EntryFalso()
        interfaz._ent_duracion = EntryFalso()
        interfaz._cb_intensidad = ComboboxFalso()
        interfaz._ent_observaciones = EntryFalso()

        interfaz._lbl_rutina = LabelFalso()
        interfaz._lbl_meta_total = LabelFalso()
        interfaz._lbl_veces_realizadas = LabelFalso()
        interfaz._lbl_veces_restantes = LabelFalso()
        interfaz._lbl_mensaje = LabelFalso()

        return interfaz

    @staticmethod
    def crear_ejercicio_asignado(
        id_asignacion_ejercicio=501,
        nombre="Caminata",
        planificadas=5,
        realizadas=1,
    ):
        return {
            "id_asignacion_ejercicio": (
                id_asignacion_ejercicio
            ),
            "nombre_ejercicio": nombre,
            "veces_planificadas": planificadas,
            "veces_realizadas": realizadas,
        }

    def configurar_formulario_valido(
        self,
        interfaz,
        duracion="45",
        intensidad="MEDIA",
        realizadas="2",
        observaciones="Entrenamiento normal",
    ):
        ejercicio = self.crear_ejercicio_asignado()

        interfaz._ejercicio_asignado_actual = ejercicio
        interfaz._ent_duracion.set(duracion)
        interfaz._cb_intensidad.set(intensidad)
        interfaz._ent_veces_realizadas.set(realizadas)
        interfaz._ent_observaciones.set(observaciones)

        return ejercicio

    def test_propiedad_id_cliente(
        self,
        interfaz,
    ):
        assert interfaz.id_cliente == 10

    def test_propiedad_id_rutina(
        self,
        interfaz,
    ):
        assert interfaz.id_rutina == 25

    def test_propiedad_id_rutina_devuelve_none_si_no_existe(
        self,
        interfaz,
    ):
        del interfaz._id_rutina

        assert interfaz.id_rutina is None

    def test_mostrar_formulario_sesion_crea_widgets(
        self,
        interfaz,
    ):
        with patch(
            "src.interfaz.interfaz_registro_sesion.ttk.LabelFrame",
            side_effect=LabelFrameFalso,
        ), patch(
            "src.interfaz.interfaz_registro_sesion.ttk.Frame",
            side_effect=FrameFalso,
        ), patch(
            "src.interfaz.interfaz_registro_sesion.ttk.Label",
            side_effect=LabelFalso,
        ), patch(
            "src.interfaz.interfaz_registro_sesion.ttk.Entry",
            side_effect=EntryFalso,
        ), patch(
            "src.interfaz.interfaz_registro_sesion.ttk.Combobox",
            side_effect=ComboboxFalso,
        ), patch(
            "src.interfaz.interfaz_registro_sesion.ttk.Button",
            side_effect=ButtonFalso,
        ):
            interfaz.mostrarFormularioSesion()

        assert isinstance(
            interfaz._cb_ejercicio,
            ComboboxFalso,
        )

        assert isinstance(
            interfaz._ent_veces_realizadas,
            EntryFalso,
        )

        assert isinstance(
            interfaz._ent_duracion,
            EntryFalso,
        )

        assert isinstance(
            interfaz._cb_intensidad,
            ComboboxFalso,
        )

        assert isinstance(
            interfaz._ent_observaciones,
            EntryFalso,
        )

    def test_cargar_rutina_activa_sin_asignacion(
        self,
        interfaz,
        control_sesiones,
    ):
        control_sesiones.asignacion_dao.buscar_activa.return_value = (
            None
        )

        interfaz._cargar_rutina_activa()

        assert interfaz._id_asignacion is None
        assert interfaz._id_rutina is None
        assert interfaz._ejercicios_asignados == []
        assert interfaz._ejercicio_asignado_actual is None
        assert interfaz._cb_ejercicio["values"] == []
        assert interfaz._cb_ejercicio.get() == ""

    def test_cargar_rutina_activa_con_ejercicios(
        self,
        interfaz,
        control_sesiones,
    ):
        asignacion = SimpleNamespace(
            id_asignacion=100,
            id_rutina=25,
            estado="ACTIVA",
        )

        ejercicio = self.crear_ejercicio_asignado()

        control_sesiones.asignacion_dao.buscar_activa.return_value = (
            asignacion
        )

        control_sesiones.asignacion_ejercicio_dao.obtener_progreso.return_value = [
            ejercicio
        ]

        interfaz._cargar_rutina_activa()

        assert interfaz._id_asignacion == 100
        assert interfaz._id_rutina == 25

        assert interfaz._cb_ejercicio["values"] == [
            "501 - Caminata"
        ]

        control_sesiones.asignacion_ejercicio_dao.obtener_progreso.assert_called_once_with(
            id_asignacion=100,
            solo_activos=True,
        )

    def test_seleccionar_ejercicio_actualiza_datos(
        self,
        interfaz,
    ):
        ejercicio = self.crear_ejercicio_asignado(
            planificadas=5,
            realizadas=2,
        )

        interfaz._ejercicios_asignados = [ejercicio]

        interfaz._cb_ejercicio.set(
            "501 - Caminata"
        )

        interfaz._seleccionar_ejercicio()

        assert (
            interfaz._ejercicio_asignado_actual
            is ejercicio
        )

        assert (
            interfaz._lbl_meta_total.configuracion["text"]
            == "5"
        )

        assert (
            interfaz._lbl_veces_realizadas.configuracion["text"]
            == "2"
        )

        assert (
            interfaz._lbl_veces_restantes.configuracion["text"]
            == "3"
        )

    def test_registrar_sesion_sin_rutina_activa(
        self,
        interfaz,
        control_sesiones,
    ):
        interfaz._id_asignacion = None

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        control_sesiones.registrar_sesion.assert_not_called()

        mock_error.assert_called_once_with(
            "No tiene una rutina activa para registrar."
        )

    def test_registrar_sesion_sin_ejercicio_seleccionado(
        self,
        interfaz,
        control_sesiones,
    ):
        interfaz._ejercicio_asignado_actual = None

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        control_sesiones.registrar_sesion.assert_not_called()

        mock_error.assert_called_once_with(
            "Seleccione un ejercicio de su rutina."
        )

    @pytest.mark.parametrize(
        "duracion, intensidad, realizadas",
        [
            ("", "MEDIA", "1"),
            ("30", "", "1"),
            ("30", "MEDIA", ""),
        ],
    )
    def test_registrar_sesion_requiere_campos(
        self,
        interfaz,
        control_sesiones,
        duracion,
        intensidad,
        realizadas,
    ):
        self.configurar_formulario_valido(
            interfaz,
            duracion=duracion,
            intensidad=intensidad,
            realizadas=realizadas,
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        control_sesiones.registrar_sesion.assert_not_called()

        mock_error.assert_called_once_with(
            (
                "Complete duración, intensidad "
                "y cantidad realizada."
            )
        )

    @pytest.mark.parametrize(
        "duracion, realizadas, mensaje",
        [
            (
                "0",
                "1",
                "La duración debe ser mayor que cero.",
            ),
            (
                "texto",
                "1",
                "invalid literal for int()",
            ),
            (
                "30",
                "0",
                (
                    "La cantidad realizada debe ser "
                    "mayor que cero."
                ),
            ),
            (
                "30",
                "texto",
                "invalid literal for int()",
            ),
        ],
    )
    def test_registrar_sesion_valida_numeros(
        self,
        interfaz,
        control_sesiones,
        duracion,
        realizadas,
        mensaje,
    ):
        self.configurar_formulario_valido(
            interfaz,
            duracion=duracion,
            realizadas=realizadas,
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        control_sesiones.registrar_sesion.assert_not_called()

        assert mensaje in mock_error.call_args.args[0]

    def test_registrar_sesion_rechaza_superar_restantes(
        self,
        interfaz,
        control_sesiones,
    ):
        ejercicio = self.configurar_formulario_valido(
            interfaz,
            realizadas="5",
        )

        ejercicio["veces_planificadas"] = 5
        ejercicio["veces_realizadas"] = 2

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        control_sesiones.registrar_sesion.assert_not_called()

        assert (
            "No puede registrar más de 3 vez/veces"
            in mock_error.call_args.args[0]
        )

    def test_registrar_sesion_correctamente(
        self,
        interfaz,
        control_sesiones,
    ):
        ejercicio = self.configurar_formulario_valido(
            interfaz,
            duracion="45",
            intensidad="ALTA",
            realizadas="2",
            observaciones="Entrenamiento completado",
        )

        fecha_prueba = date(2026, 9, 19)

        sesion = SimpleNamespace(
            completada=False,
            calorias_quemadas=321.5,
            veces_realizadas=2,
        )

        control_sesiones.registrar_sesion.return_value = sesion

        with patch(
            "src.interfaz.interfaz_registro_sesion.date",
        ) as mock_date, patch.object(
            interfaz,
            "mostrar_mensaje",
        ) as mock_mensaje, patch.object(
            interfaz,
            "cancelarRegistro",
        ) as mock_cancelar, patch.object(
            interfaz,
            "_cargar_rutina_activa",
        ) as mock_cargar:

            mock_date.today.return_value = fecha_prueba

            interfaz.registrarSesion()

        control_sesiones.registrar_sesion.assert_called_once_with(
            cliente=10,
            rutina=25,
            fecha=fecha_prueba,
            nombre_ejercicio="Caminata",
            duracion_real=45,
            intensidad_real="ALTA",
            observaciones="Entrenamiento completado",
            veces_planificadas=4,
            veces_realizadas=2,
            id_asignacion_ejercicio=(
                ejercicio["id_asignacion_ejercicio"]
            ),
        )

        assert (
            "Sesión registrada correctamente."
            in mock_mensaje.call_args.args[0]
        )

        assert "Estado de la sesión: pendiente" in (
            mock_mensaje.call_args.args[0]
        )

        mock_cancelar.assert_called_once_with()
        mock_cargar.assert_called_once_with()

    def test_registrar_sesion_maneja_value_error(
        self,
        interfaz,
        control_sesiones,
    ):
        self.configurar_formulario_valido(
            interfaz
        )

        control_sesiones.registrar_sesion.side_effect = (
            ValueError("La intensidad no es válida")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        mock_error.assert_called_once_with(
            "La intensidad no es válida"
        )

    def test_registrar_sesion_maneja_error_inesperado(
        self,
        interfaz,
        control_sesiones,
    ):
        self.configurar_formulario_valido(
            interfaz
        )

        control_sesiones.registrar_sesion.side_effect = (
            RuntimeError("Error de base de datos")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.registrarSesion()

        mock_error.assert_called_once_with(
            "Error inesperado: Error de base de datos"
        )

    def test_cancelar_registro_limpia_formulario(
        self,
        interfaz,
    ):
        interfaz._ent_duracion.set("45")
        interfaz._ent_veces_realizadas.set("2")
        interfaz._cb_intensidad.set("ALTA")
        interfaz._ent_observaciones.set(
            "Buen entrenamiento"
        )

        interfaz.cancelarRegistro()

        assert interfaz._ent_duracion.get() == ""
        assert (
            interfaz._ent_veces_realizadas.get()
            == ""
        )
        assert interfaz._cb_intensidad.get() == ""
        assert interfaz._ent_observaciones.get() == ""

    def test_constructor_inicializa_atributos_y_carga_rutina(
        self,
        control_sesiones,
    ):
        master = MagicMock()

        with patch(
            "src.interfaz.interfaz_registro_sesion."
            "InterfazBase.__init__",
            return_value=None,
        ) as mock_base_init, patch.object(
            InterfazRegistroSesion,
            "pack",
        ) as mock_pack, patch.object(
            InterfazRegistroSesion,
            "mostrarFormularioSesion",
        ) as mock_formulario, patch.object(
            InterfazRegistroSesion,
            "_cargar_rutina_activa",
        ) as mock_cargar_rutina:
            interfaz = InterfazRegistroSesion(
                master=master,
                control_sesiones=control_sesiones,
                id_cliente=10,
                id_rutina=25,
            )

        mock_base_init.assert_called_once_with(
            master,
            controlador=control_sesiones,
            padding=10,
        )

        mock_pack.assert_called_once_with(
            fill="both",
            expand=True,
        )

        mock_formulario.assert_called_once_with()
        mock_cargar_rutina.assert_called_once_with()

        assert interfaz._id_cliente == 10
        assert interfaz._id_rutina == 25
        assert interfaz._id_asignacion is None
        assert interfaz._ejercicios_asignados == []
        assert interfaz._ejercicio_asignado_actual is None

    def test_seleccionar_ejercicio_sin_valor_limpia_datos(
        self,
        interfaz,
    ):
        interfaz._ejercicio_asignado_actual = (
            self.crear_ejercicio_asignado()
        )

        with patch.object(
            interfaz,
            "_limpiar_datos_ejercicio",
        ) as mock_limpiar:
            interfaz._seleccionar_ejercicio()

        assert interfaz._ejercicio_asignado_actual is None
        mock_limpiar.assert_called_once_with()

    @pytest.mark.parametrize(
        "valor",
        [
            "sin identificador",
            "- Caminata",
            "abc - Caminata",
        ],
    )
    def test_seleccionar_ejercicio_con_valor_invalido_limpia_datos(
        self,
        interfaz,
        valor,
    ):
        interfaz._cb_ejercicio.set(valor)
        interfaz._ejercicio_asignado_actual = (
            self.crear_ejercicio_asignado()
        )

        with patch.object(
            interfaz,
            "_limpiar_datos_ejercicio",
        ) as mock_limpiar:
            interfaz._seleccionar_ejercicio()

        assert interfaz._ejercicio_asignado_actual is None
        mock_limpiar.assert_called_once_with()

    def test_seleccionar_ejercicio_no_encontrado_limpia_datos(
        self,
        interfaz,
    ):
        interfaz._ejercicios_asignados = [
            self.crear_ejercicio_asignado(
                id_asignacion_ejercicio=501,
            ),
        ]

        interfaz._cb_ejercicio.set("999 - Ejercicio inexistente")

        with patch.object(
            interfaz,
            "_limpiar_datos_ejercicio",
        ) as mock_limpiar:
            interfaz._seleccionar_ejercicio()

        assert interfaz._ejercicio_asignado_actual is None
        mock_limpiar.assert_called_once_with()

    def test_seleccionar_ejercicio_con_meta_completada(
        self,
        interfaz,
    ):
        ejercicio = self.crear_ejercicio_asignado(
            id_asignacion_ejercicio=501,
            nombre="Caminata",
            planificadas=5,
            realizadas=5,
        )

        interfaz._ejercicios_asignados = [ejercicio]
        interfaz._cb_ejercicio.set("501 - Caminata")

        interfaz._seleccionar_ejercicio()

        assert (
            interfaz._ejercicio_asignado_actual
            is ejercicio
        )

        assert (
            interfaz._lbl_meta_total.configuracion["text"]
            == "5"
        )

        assert (
            interfaz._lbl_veces_realizadas.configuracion["text"]
            == "5"
        )

        assert (
            interfaz._lbl_veces_restantes.configuracion["text"]
            == "0"
        )

        assert interfaz._ent_veces_realizadas.get() == ""

        assert interfaz._lbl_mensaje.configuracion == {
            "text": (
                "Este ejercicio ya alcanzó su meta. "
                "Seleccione otro ejercicio."
            ),
            "foreground": "#1b5e20",
        }

    def test_registrar_sesion_muestra_estado_completada(
        self,
        interfaz,
        control_sesiones,
    ):
        ejercicio = self.configurar_formulario_valido(
            interfaz,
            duracion="30",
            intensidad="MEDIA",
            realizadas="4",
        )

        ejercicio["veces_planificadas"] = 5
        ejercicio["veces_realizadas"] = 1

        control_sesiones.registrar_sesion.return_value = (
            SimpleNamespace(
                completada=True,
                calorias_quemadas=250.0,
                veces_realizadas=4,
            )
        )

        with patch(
            "src.interfaz.interfaz_registro_sesion.date"
        ) as mock_date, patch.object(
            interfaz,
            "mostrar_mensaje",
        ) as mock_mensaje, patch.object(
            interfaz,
            "cancelarRegistro",
        ), patch.object(
            interfaz,
            "_cargar_rutina_activa",
        ):
            mock_date.today.return_value = date(
                2026,
                9,
                27,
            )

            interfaz.registrarSesion()

        mensaje = mock_mensaje.call_args.args[0]

        assert "Estado de la sesión: completada" in mensaje
        assert "Restaban antes del registro: 4" in mensaje

    def test_cargar_rutina_activa_sin_ejercicios_muestra_mensaje(
        self,
        interfaz,
        control_sesiones,
    ):
        asignacion = SimpleNamespace(
            id_asignacion=100,
            id_rutina=25,
            estado="ACTIVA",
        )

        control_sesiones.asignacion_dao.buscar_activa.return_value = (
            asignacion
        )

        control_sesiones.asignacion_ejercicio_dao.obtener_progreso.return_value = []

        interfaz._cargar_rutina_activa()

        assert interfaz._id_asignacion == 100
        assert interfaz._id_rutina == 25
        assert interfaz._ejercicios_asignados == []
        assert interfaz._cb_ejercicio["values"] == []

        assert interfaz._lbl_mensaje.configuracion == {
            "text": (
                "La rutina activa no tiene ejercicios "
                "disponibles."
            ),
            "foreground": "#b00020",
        }

    def test_cargar_rutina_activa_muestra_error_si_falla_consulta(
        self,
        interfaz,
        control_sesiones,
    ):
        control_sesiones.asignacion_dao.buscar_activa.side_effect = (
            RuntimeError("Fallo de conexión")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz._cargar_rutina_activa()

        mock_error.assert_called_once_with(
            "No se pudo cargar la rutina activa: "
            "Fallo de conexión"
        )