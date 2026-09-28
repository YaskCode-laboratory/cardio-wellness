from unittest.mock import MagicMock, patch

import pytest

from src.interfaz.interfaz_gestion_ejercicios import (
    InterfazGestionEjercicios,
)


class WidgetFalso:
    """
    Widget falso genérico para pruebas de widgets ttk.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.valor = ""
        self.eliminaciones = []
        self.insertados = []
        self.seleccion_actual = []
        self.items = {}
        self.configuraciones = []

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        self.eliminaciones.append((args, kwargs))
        self.valor = ""

    def get(self):
        return self.valor

    def insert(self, *args, **kwargs):
        self.insertados.append((args, kwargs))

        if len(args) >= 2 and args[0] == 0:
            self.valor = str(args[1])

    def selection(self):
        return self.seleccion_actual

    def item(self, item_id):
        return self.items.get(
            item_id,
            {"values": []},
        )

    def heading(self, *args, **kwargs):
        pass

    def column(self, *args, **kwargs):
        pass

    def config(self, *args, **kwargs):
        self.configuraciones.append((args, kwargs))

    def bind(self, *args, **kwargs):
        self.bind_args = args
        self.bind_kwargs = kwargs

    def set(self, valor):
        self.valor = valor

    def get_children(self):
        return list(self.items.keys())


class EntryFalso(WidgetFalso):
    pass


class ComboboxFalso(WidgetFalso):
    pass


class TreeviewFalso(WidgetFalso):
    pass


class TestInterfazGestionEjercicios:

    @pytest.fixture
    def control_ejercicios(self):
        controlador = MagicMock()
        controlador.listar.return_value = []
        return controlador

    @pytest.fixture
    def ejercicio(self):
        ejercicio = MagicMock()

        ejercicio.id_ejercicio = 1
        ejercicio.nombre = "Caminata"
        ejercicio.tipo = "LISS"
        ejercicio.descripcion = "Actividad suave"
        ejercicio.duracion_minutos = 30
        ejercicio.intensidad.value = "MEDIA"

        return ejercicio

    @pytest.fixture
    def interfaz(self, control_ejercicios):
        interfaz = object.__new__(
            InterfazGestionEjercicios
        )

        interfaz._controlador = control_ejercicios
        interfaz._control_ejercicios = control_ejercicios
        interfaz._descripciones_ejercicios = {}
        interfaz._ejercicios_por_id = {}

        return interfaz

    @pytest.fixture
    def widgets_formulario(self):
        return {
            "nombre": EntryFalso(),
            "tipo": ComboboxFalso(),
            "descripcion": EntryFalso(),
            "duracion": EntryFalso(),
            "intensidad": ComboboxFalso(),
            "buscar": EntryFalso(),
        }

    def asignar_widgets_formulario(
        self,
        interfaz,
        widgets,
    ):
        interfaz._ent_nombre = widgets["nombre"]
        interfaz._cb_tipo = widgets["tipo"]
        interfaz._ent_descripcion = widgets[
            "descripcion"
        ]
        interfaz._ent_duracion = widgets["duracion"]
        interfaz._cb_intensidad = widgets[
            "intensidad"
        ]
        interfaz._ent_buscar = widgets["buscar"]

    def test_control_ejercicios_devuelve_el_controlador(
        self,
        interfaz,
        control_ejercicios,
    ):
        assert (
            interfaz.control_ejercicios
            is control_ejercicios
        )

    def test_mostrar_ejercicios_elimina_datos_anteriores(
        self,
        interfaz,
        control_ejercicios,
        ejercicio,
    ):
        interfaz._tree = TreeviewFalso()

        interfaz._tree.items = {
            "item1": {
                "values": (
                    1,
                    "Ejercicio anterior",
                ),
            },
        }

        control_ejercicios.listar.return_value = [
            ejercicio,
        ]

        interfaz.mostrarEjercicios()

        assert len(
            interfaz._tree.eliminaciones
        ) == 1

        assert interfaz._tree.eliminaciones[0][0] == (
            "item1",
        )

    def test_mostrar_ejercicios_maneja_error(
        self,
        interfaz,
        control_ejercicios,
    ):
        interfaz._tree = TreeviewFalso()

        control_ejercicios.listar.side_effect = (
            RuntimeError("Error de base de datos")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.mostrarEjercicios()

        mock_error.assert_called_once_with(
            "Error al cargar ejercicios: "
            "Error de base de datos"
        )

    def test_crear_ejercicio_maneja_value_error(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        widgets_formulario["nombre"].valor = "Caminata"
        widgets_formulario["tipo"].valor = "LISS"
        widgets_formulario["descripcion"].valor = (
            "Actividad suave"
        )
        widgets_formulario["duracion"].valor = (
            "duración inválida"
        )
        widgets_formulario["intensidad"].valor = "MEDIA"

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.crearEjercicio()

        control_ejercicios.crear_ejercicio.assert_not_called()
        mock_error.assert_called_once()

    def test_crear_ejercicio_maneja_error_del_controlador(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        widgets_formulario["nombre"].valor = "Caminata"
        widgets_formulario["tipo"].valor = "LISS"
        widgets_formulario["descripcion"].valor = (
            "Actividad suave"
        )
        widgets_formulario["duracion"].valor = "30"
        widgets_formulario["intensidad"].valor = "MEDIA"

        control_ejercicios.crear_ejercicio.side_effect = (
            RuntimeError("Error inesperado")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.crearEjercicio()

        mock_error.assert_called_once_with(
            "Error inesperado: Error inesperado"
        )

    def test_editar_ejercicio_sin_seleccion(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.editarEjercicio()

        mock_error.assert_called_once_with(
            "Seleccione un ejercicio para editar."
        )

    def test_eliminar_ejercicio_sin_seleccion(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.eliminarEjercicio()

        mock_error.assert_called_once_with(
            "Seleccione un ejercicio para eliminar."
        )

    def test_eliminar_ejercicio_usuario_cancela(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    5,
                    "Caminata",
                ),
            },
        }

        with patch.object(
            interfaz,
            "confirmar_accion",
            return_value=False,
        ) as mock_confirmar:
            interfaz.eliminarEjercicio()

        mock_confirmar.assert_called_once_with(
            "Eliminar el ejercicio con ID 5?"
        )

    def test_eliminar_ejercicio_correctamente(
        self,
        interfaz,
        control_ejercicios,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    5,
                    "Caminata",
                ),
            },
        }

        with patch.object(
            interfaz,
            "confirmar_accion",
            return_value=True,
        ), patch.object(
            interfaz,
            "mostrar_mensaje",
        ) as mock_mensaje, patch.object(
            interfaz,
            "mostrarEjercicios",
        ) as mock_mostrar_ejercicios:
            interfaz.eliminarEjercicio()

        control_ejercicios.eliminar_ejercicio.assert_called_once_with(
            5
        )

        mock_mensaje.assert_called_once_with(
            "Ejercicio eliminado correctamente."
        )

        mock_mostrar_ejercicios.assert_called_once_with()

    def test_eliminar_ejercicio_maneja_error(
        self,
        interfaz,
        control_ejercicios,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    5,
                    "Caminata",
                ),
            },
        }

        control_ejercicios.eliminar_ejercicio.side_effect = (
            RuntimeError("No se pudo eliminar")
        )

        with patch.object(
            interfaz,
            "confirmar_accion",
            return_value=True,
        ), patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.eliminarEjercicio()

        mock_error.assert_called_once_with(
            "Error al eliminar: No se pudo eliminar"
        )

    def test_buscar_ejercicio_sin_texto(
        self,
        interfaz,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        widgets_formulario["buscar"].valor = "   "

        with patch.object(
            interfaz,
            "mostrarEjercicios",
        ) as mock_mostrar_ejercicios:
            interfaz.buscarEjercicio()

        mock_mostrar_ejercicios.assert_called_once_with()

        control = interfaz.control_ejercicios
        control.listar.assert_not_called()

    def test_buscar_ejercicio_no_encontrado(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
        ejercicio,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        widgets_formulario["buscar"].valor = "natación"

        control_ejercicios.listar.return_value = [
            ejercicio,
        ]

        interfaz.buscarEjercicio()

        assert interfaz._tree.insertados == []

    def test_buscar_ejercicio_maneja_error(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        widgets_formulario["buscar"].valor = "cami"

        control_ejercicios.listar.side_effect = (
            RuntimeError("Error de búsqueda")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.buscarEjercicio()

        mock_error.assert_called_once_with(
            "Error al buscar: Error de búsqueda"
        )

    def test_insertar_ejercicio_inicializa_diccionarios_si_faltan(
        self,
        interfaz,
        ejercicio,
    ):
        interfaz._tree = TreeviewFalso()

        del interfaz._descripciones_ejercicios
        del interfaz._ejercicios_por_id

        interfaz._insertar_ejercicio(ejercicio)

        assert interfaz._descripciones_ejercicios == {
            1: "Actividad suave",
        }

        assert interfaz._ejercicios_por_id == {
            1: ejercicio,
        }

        assert len(interfaz._tree.insertados) == 1

    def test_cargar_ejercicio_sin_seleccion_no_hace_nada(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()

        interfaz._cargar_ejercicio_seleccionado()

        assert not hasattr(
            interfaz,
            "_id_ejercicio_editando",
        )

    def test_cargar_ejercicio_con_item_sin_valores_no_hace_nada(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (),
            },
        }

        interfaz._cargar_ejercicio_seleccionado()

        assert not hasattr(
            interfaz,
            "_id_ejercicio_editando",
        )

    def test_cargar_ejercicio_con_id_invalido_muestra_error(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    "no-es-id",
                ),
            },
        }

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz._cargar_ejercicio_seleccionado()

        mock_error.assert_called_once_with(
            "El ID del ejercicio no es válido."
        )

    def test_cargar_ejercicio_no_encontrado_muestra_error(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    99,
                ),
            },
        }

        interfaz._ejercicios_por_id = {}

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz._cargar_ejercicio_seleccionado()

        mock_error.assert_called_once_with(
            "No se encontró el ejercicio seleccionado."
        )

    def test_editar_ejercicio_item_sin_valores(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (),
            },
        }

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.editarEjercicio()

        mock_error.assert_called_once_with(
            "No se pudo obtener el ejercicio seleccionado."
        )

    def test_editar_ejercicio_con_id_invalido(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    "abc",
                ),
            },
        }

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.editarEjercicio()

        mock_error.assert_called_once_with(
            "El ID del ejercicio no es válido."
        )

    def test_editar_ejercicio_no_encontrado(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]

        interfaz._tree.items = {
            "item1": {
                "values": (
                    55,
                ),
            },
        }

        interfaz._ejercicios_por_id = {}

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.editarEjercicio()

        mock_error.assert_called_once_with(
            "No se encontró el ejercicio seleccionado."
        )

    def test_cancelar_edicion_limpia_formulario(
        self,
        interfaz,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        with patch.object(
            interfaz,
            "_limpiar_formulario",
        ) as mock_limpiar:
            interfaz._cancelar_edicion()

        mock_limpiar.assert_called_once_with()

    def test_limpiar_formulario_reinicia_modo_edicion(
        self,
        interfaz,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._id_ejercicio_editando = 8
        interfaz._lbl_modo = WidgetFalso()

        interfaz._limpiar_formulario()

        assert interfaz._id_ejercicio_editando is None

    def test_buscar_ejercicio_elimina_resultados_anteriores(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()

        interfaz._tree.items = {
            "item_anterior_1": {
                "values": (
                    1,
                    "Ejercicio anterior",
                ),
            },
            "item_anterior_2": {
                "values": (
                    2,
                    "Otro ejercicio",
                ),
            },
        }

        widgets_formulario["buscar"].valor = "cami"

        control_ejercicios.listar.return_value = []

        interfaz.buscarEjercicio()

        assert len(interfaz._tree.eliminaciones) == 2
        assert interfaz._tree.eliminaciones[0][0] == (
            "item_anterior_1",
        )
        assert interfaz._tree.eliminaciones[1][0] == (
            "item_anterior_2",
        )

    def test_insertar_ejercicio_guarda_datos_en_tabla(
        self,
        interfaz,
        ejercicio,
    ):
        interfaz._tree = TreeviewFalso()

        interfaz._insertar_ejercicio(ejercicio)

        assert interfaz._descripciones_ejercicios == {
            1: "Actividad suave",
        }
        assert interfaz._ejercicios_por_id == {
            1: ejercicio,
        }

        assert len(interfaz._tree.insertados) == 1

        argumentos, argumentos_nombrados = (
            interfaz._tree.insertados[0]
        )

        assert argumentos == ("", "end")
        assert argumentos_nombrados["values"] == (
            1,
            "Caminata",
            "LISS",
            "Actividad suave",
            30,
            "MEDIA",
            "Automático",
        )

    def test_insertar_ejercicio_acepta_intensidad_sin_value(
        self,
        interfaz,
        ejercicio,
    ):
        interfaz._tree = TreeviewFalso()
        ejercicio.intensidad = "ALTA"

        interfaz._insertar_ejercicio(ejercicio)

        valores = interfaz._tree.insertados[0][1]["values"]

        assert valores[5] == "ALTA"

    def test_mostrar_ejercicios_inserta_lista_del_controlador(
        self,
        interfaz,
        control_ejercicios,
        ejercicio,
    ):
        interfaz._tree = TreeviewFalso()
        control_ejercicios.listar.return_value = [
            ejercicio,
        ]

        interfaz.mostrarEjercicios()

        control_ejercicios.listar.assert_called_once_with()
        assert len(interfaz._tree.insertados) == 1
        assert interfaz._ejercicios_por_id == {
            1: ejercicio,
        }

    def test_crear_ejercicio_correctamente(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        widgets_formulario["nombre"].valor = "Caminata"
        widgets_formulario["tipo"].valor = "LISS"
        widgets_formulario["descripcion"].valor = (
            "Actividad suave"
        )
        widgets_formulario["duracion"].valor = "30"
        widgets_formulario["intensidad"].valor = "MEDIA"

        toplevel = MagicMock()

        with patch.object(
            interfaz,
            "mostrar_mensaje",
        ) as mock_mensaje, patch.object(
            interfaz,
            "_limpiar_formulario",
        ) as mock_limpiar, patch.object(
            interfaz,
            "mostrarEjercicios",
        ) as mock_mostrar, patch.object(
            interfaz,
            "winfo_toplevel",
            return_value=toplevel,
        ):
            interfaz.crearEjercicio()

        control_ejercicios.crear_ejercicio.assert_called_once_with(
            nombre="Caminata",
            descripcion="Actividad suave",
            tipo="LISS",
            duracion_minutos=30,
            intensidad="MEDIA",
        )
        mock_mensaje.assert_called_once_with(
            "Ejercicio creado exitosamente."
        )
        mock_limpiar.assert_called_once_with()
        mock_mostrar.assert_called_once_with()
        toplevel.event_generate.assert_called_once_with(
            "<<EjerciciosActualizados>>"
        )

    def test_editar_ejercicio_correctamente(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
        ejercicio,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": (
                    1,
                    "Caminata",
                ),
            },
        }
        interfaz._ejercicios_por_id = {
            1: ejercicio,
        }

        widgets_formulario["nombre"].valor = "Bicicleta"
        widgets_formulario["tipo"].valor = "HIIT"
        widgets_formulario["descripcion"].valor = (
            "Intervalos intensos"
        )
        widgets_formulario["duracion"].valor = "45"
        widgets_formulario["intensidad"].valor = "ALTA"

        toplevel = MagicMock()

        with patch.object(
            interfaz,
            "mostrar_mensaje",
        ) as mock_mensaje, patch.object(
            interfaz,
            "_limpiar_formulario",
        ) as mock_limpiar, patch.object(
            interfaz,
            "mostrarEjercicios",
        ) as mock_mostrar, patch.object(
            interfaz,
            "winfo_toplevel",
            return_value=toplevel,
        ):
            interfaz.editarEjercicio()

        assert ejercicio.nombre == "Bicicleta"
        assert ejercicio.tipo == "HIIT"
        assert ejercicio.descripcion == "Intervalos intensos"
        assert ejercicio.duracion_minutos == 45
        assert ejercicio.intensidad == "ALTA"

        control_ejercicios.actualizar_ejercicio.assert_called_once_with(
            ejercicio
        )
        mock_mensaje.assert_called_once_with(
            "Ejercicio actualizado correctamente."
        )
        mock_limpiar.assert_called_once_with()
        mock_mostrar.assert_called_once_with()
        toplevel.event_generate.assert_called_once_with(
            "<<EjerciciosActualizados>>"
        )

    def test_editar_ejercicio_maneja_value_error(
        self,
        interfaz,
        widgets_formulario,
        ejercicio,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": (1,),
            },
        }
        interfaz._ejercicios_por_id = {
            1: ejercicio,
        }

        with patch.object(
            interfaz,
            "_leer_datos_formulario",
            side_effect=ValueError("Datos inválidos"),
        ), patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.editarEjercicio()

        mock_error.assert_called_once_with("Datos inválidos")

    def test_editar_ejercicio_maneja_error_inesperado(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
        ejercicio,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": (1,),
            },
        }
        interfaz._ejercicios_por_id = {
            1: ejercicio,
        }

        widgets_formulario["nombre"].valor = "Caminata"
        widgets_formulario["tipo"].valor = "LISS"
        widgets_formulario["descripcion"].valor = "Suave"
        widgets_formulario["duracion"].valor = "30"
        widgets_formulario["intensidad"].valor = "MEDIA"

        control_ejercicios.actualizar_ejercicio.side_effect = (
            RuntimeError("Fallo al actualizar")
        )

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.editarEjercicio()

        mock_error.assert_called_once_with(
            "Error al editar ejercicio: Fallo al actualizar"
        )

    def test_eliminar_ejercicio_con_valores_vacios_muestra_error(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": (),
            },
        }

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.eliminarEjercicio()

        mock_error.assert_called_once_with(
            "El ID del ejercicio no es válido."
        )

    def test_eliminar_ejercicio_con_id_invalido_muestra_error(
        self,
        interfaz,
    ):
        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": ("abc",),
            },
        }

        with patch.object(
            interfaz,
            "mostrar_error",
        ) as mock_error:
            interfaz.eliminarEjercicio()

        mock_error.assert_called_once_with(
            "El ID del ejercicio no es válido."
        )

    def test_eliminar_ejercicio_limpia_formulario_si_existen_campos(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": (5,),
            },
        }

        toplevel = MagicMock()

        with patch.object(
            interfaz,
            "confirmar_accion",
            return_value=True,
        ), patch.object(
            interfaz,
            "mostrar_mensaje",
        ), patch.object(
            interfaz,
            "mostrarEjercicios",
        ), patch.object(
            interfaz,
            "_limpiar_formulario",
        ) as mock_limpiar, patch.object(
            interfaz,
            "winfo_toplevel",
            return_value=toplevel,
        ):
            interfaz.eliminarEjercicio()

        control_ejercicios.eliminar_ejercicio.assert_called_once_with(
            5
        )
        mock_limpiar.assert_called_once_with()
        toplevel.event_generate.assert_called_once_with(
            "<<EjerciciosActualizados>>"
        )

    def test_buscar_ejercicio_insertar_resultado_coincidente(
        self,
        interfaz,
        control_ejercicios,
        widgets_formulario,
        ejercicio,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        widgets_formulario["buscar"].valor = "CAMI"
        control_ejercicios.listar.return_value = [
            ejercicio,
        ]

        interfaz.buscarEjercicio()

        assert len(interfaz._tree.insertados) == 1
        assert interfaz._ejercicios_por_id == {
            1: ejercicio,
        }

    def test_cargar_ejercicio_seleccionado_correctamente(
        self,
        interfaz,
        widgets_formulario,
        ejercicio,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        interfaz._tree = TreeviewFalso()
        interfaz._tree.seleccion_actual = ["item1"]
        interfaz._tree.items = {
            "item1": {
                "values": (1,),
            },
        }
        interfaz._ejercicios_por_id = {
            1: ejercicio,
        }
        interfaz._lbl_modo = WidgetFalso()

        interfaz._cargar_ejercicio_seleccionado()

        assert interfaz._id_ejercicio_editando == 1
        assert widgets_formulario["nombre"].valor == "Caminata"
        assert widgets_formulario["descripcion"].valor == (
            "Actividad suave"
        )
        assert widgets_formulario["tipo"].valor == "LISS"
        assert widgets_formulario["duracion"].valor == "30"
        assert widgets_formulario["intensidad"].valor == "MEDIA"

        assert interfaz._lbl_modo.configuraciones[-1][1] == {
            "text": "Modo: editando ejercicio #1",
            "foreground": "#174ea6",
        }

    @pytest.mark.parametrize(
        "campo, mensaje",
        [
            ("nombre", "Ingrese el nombre del ejercicio."),
            ("tipo", "Seleccione el tipo."),
            ("descripcion", "Ingrese la descripción."),
            ("duracion", "Ingrese la duración."),
            ("intensidad", "Seleccione la intensidad."),
        ],
    )
    def test_leer_datos_formulario_valida_campos_obligatorios(
        self,
        interfaz,
        widgets_formulario,
        campo,
        mensaje,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        widgets_formulario["nombre"].valor = "Caminata"
        widgets_formulario["tipo"].valor = "LISS"
        widgets_formulario["descripcion"].valor = "Suave"
        widgets_formulario["duracion"].valor = "20"
        widgets_formulario["intensidad"].valor = "MEDIA"

        widgets_formulario[campo].valor = ""

        with pytest.raises(ValueError, match=mensaje):
            interfaz._leer_datos_formulario()

    @pytest.mark.parametrize(
        "duracion, mensaje",
        [
            ("texto", "La duración debe ser un entero."),
            ("0", "La duración debe ser mayor que cero."),
            ("-5", "La duración debe ser mayor que cero."),
        ],
    )
    def test_leer_datos_formulario_valida_duracion(
        self,
        interfaz,
        widgets_formulario,
        duracion,
        mensaje,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        widgets_formulario["nombre"].valor = "Caminata"
        widgets_formulario["tipo"].valor = "LISS"
        widgets_formulario["descripcion"].valor = "Suave"
        widgets_formulario["duracion"].valor = duracion
        widgets_formulario["intensidad"].valor = "MEDIA"

        with pytest.raises(ValueError, match=mensaje):
            interfaz._leer_datos_formulario()

    def test_leer_datos_formulario_retorna_datos_limpios(
        self,
        interfaz,
        widgets_formulario,
    ):
        self.asignar_widgets_formulario(
            interfaz,
            widgets_formulario,
        )

        widgets_formulario["nombre"].valor = "  Caminata  "
        widgets_formulario["tipo"].valor = " LISS "
        widgets_formulario["descripcion"].valor = " Actividad suave "
        widgets_formulario["duracion"].valor = " 30 "
        widgets_formulario["intensidad"].valor = " MEDIA "

        resultado = interfaz._leer_datos_formulario()

        assert resultado == {
            "nombre": "Caminata",
            "tipo": "LISS",
            "descripcion": "Actividad suave",
            "duracion_minutos": 30,
            "intensidad": "MEDIA",
        }

    def test_constructor_crea_formulario_y_carga_ejercicios(
        self,
        control_ejercicios,
    ):
        master = MagicMock()

        with patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "InterfazBase.__init__",
            return_value=None,
        ) as mock_base_init, patch.object(
            InterfazGestionEjercicios,
            "pack",
        ) as mock_pack, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.LabelFrame",
            side_effect=WidgetFalso,
        ) as mock_label_frame, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Frame",
            side_effect=WidgetFalso,
        ) as mock_frame, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Label",
            side_effect=WidgetFalso,
        ) as mock_label, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Entry",
            side_effect=EntryFalso,
        ) as mock_entry, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Combobox",
            side_effect=ComboboxFalso,
        ) as mock_combobox, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Button",
            side_effect=WidgetFalso,
        ) as mock_button, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Treeview",
            side_effect=TreeviewFalso,
        ) as mock_treeview:
            interfaz = InterfazGestionEjercicios(
                master,
                control_ejercicios,
            )

        mock_base_init.assert_called_once_with(
            master,
            controlador=control_ejercicios,
            padding=10,
        )

        mock_pack.assert_called_once_with(
            fill="both",
            expand=True,
        )

        assert interfaz._control_ejercicios is control_ejercicios
        assert interfaz._id_ejercicio_editando is None
        assert interfaz._descripciones_ejercicios == {}
        assert interfaz._ejercicios_por_id == {}

        assert isinstance(interfaz._ent_nombre, EntryFalso)
        assert isinstance(
            interfaz._ent_descripcion,
            EntryFalso,
        )
        assert isinstance(interfaz._ent_duracion, EntryFalso)
        assert isinstance(interfaz._ent_buscar, EntryFalso)

        assert isinstance(interfaz._cb_tipo, ComboboxFalso)
        assert isinstance(
            interfaz._cb_intensidad,
            ComboboxFalso,
        )

        assert isinstance(interfaz._tree, TreeviewFalso)

        assert mock_label_frame.call_count == 1
        assert mock_frame.call_count == 2
        assert mock_label.call_count == 8
        assert mock_entry.call_count == 4
        assert mock_combobox.call_count == 2
        assert mock_button.call_count == 6
        assert mock_treeview.call_count == 1

        control_ejercicios.listar.assert_called_once_with()

    def test_mostrar_formulario_configura_campos_y_botones(
        self,
        interfaz,
    ):
        with patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.LabelFrame",
            side_effect=WidgetFalso,
        ) as mock_label_frame, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Frame",
            side_effect=WidgetFalso,
        ) as mock_frame, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Label",
            side_effect=WidgetFalso,
        ), patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Entry",
            side_effect=EntryFalso,
        ), patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Combobox",
            side_effect=ComboboxFalso,
        ) as mock_combobox, patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Button",
            side_effect=WidgetFalso,
        ) as mock_button:
            interfaz.mostrarFormularioEjercicio()

        assert mock_label_frame.call_args.kwargs == {
            "text": "Registrar Nuevo Ejercicio",
            "padding": 10,
        }

        assert mock_frame.call_count == 2

        assert mock_combobox.call_args_list[0].kwargs == {
            "values": (
                "LISS",
                "HIIT",
                "Cardio funcional",
            ),
            "width": 18,
        }

        assert mock_combobox.call_args_list[1].kwargs == {
            "values": (
                "BAJA",
                "MEDIA",
                "ALTA",
            ),
            "state": "readonly",
            "width": 18,
        }

        textos_botones = [
            llamada.kwargs["text"]
            for llamada in mock_button.call_args_list
        ]

        assert textos_botones == [
            "Crear",
            "Editar",
            "Cancelar",
            "Eliminar",
            "Buscar",
            "Mostrar todos",
        ]

    def test_mostrar_ejercicios_crea_y_configura_treeview(
        self,
        interfaz,
        control_ejercicios,
    ):
        del interfaz._descripciones_ejercicios
        del interfaz._ejercicios_por_id

        with patch(
            "src.interfaz.interfaz_gestion_ejercicios."
            "ttk.Treeview",
            side_effect=TreeviewFalso,
        ) as mock_treeview:
            interfaz.mostrarEjercicios()

        columnas = (
            "ID",
            "Nombre",
            "Tipo",
            "Descripcion",
            "Duracion",
            "Intensidad",
            "Calorias",
        )

        mock_treeview.assert_called_once_with(
            interfaz,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=10,
        )

        assert isinstance(interfaz._tree, TreeviewFalso)

        assert interfaz._tree.bind_args == (
            "<<TreeviewSelect>>",
            interfaz._cargar_ejercicio_seleccionado,
        )

        assert interfaz._descripciones_ejercicios == {}
        assert interfaz._ejercicios_por_id == {}

        control_ejercicios.listar.assert_called_once_with()