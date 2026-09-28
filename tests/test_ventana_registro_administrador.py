from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from src.interfaz.ventana_registro_administrador import (
    VentanaRegistroAdministrador,
)


class WidgetFalso:
    """
    Simula widgets ttk y entradas Tkinter sin abrir ventanas.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.valor = ""
        self.eliminaciones = []
        self.insertados = []
        self.configuraciones = []
        self.encabezados = []
        self.columnas = []
        self.children = []
        self.focus_recibido = False

    def pack(self, *args, **kwargs):
        self.pack_args = args
        self.pack_kwargs = kwargs

    def grid(self, *args, **kwargs):
        self.grid_args = args
        self.grid_kwargs = kwargs

    def get(self):
        return self.valor

    def delete(self, *args, **kwargs):
        self.eliminaciones.append((args, kwargs))
        self.valor = ""

    def insert(self, *args, **kwargs):
        self.insertados.append((args, kwargs))

        if len(args) >= 2 and args[0] == 0:
            self.valor = str(args[1])

    def set(self, valor):
        self.valor = valor

    def focus_set(self):
        self.focus_recibido = True

    def get_children(self):
        return list(self.children)

    def heading(self, *args, **kwargs):
        self.encabezados.append((args, kwargs))

    def column(self, *args, **kwargs):
        self.columnas.append((args, kwargs))

    def configure(self, *args, **kwargs):
        self.configuraciones.append((args, kwargs))

    def yview(self, *args, **kwargs):
        pass

    def rowconfigure(self, *args, **kwargs):
        pass

    def columnconfigure(self, *args, **kwargs):
        pass


class EntryFalso(WidgetFalso):
    pass


class TreeviewFalso(WidgetFalso):
    pass


@pytest.fixture
def control_autenticacion():
    control = MagicMock()
    control.listar_administradores.return_value = []
    return control


@pytest.fixture
def ventana(control_autenticacion):
    instancia = object.__new__(
        VentanaRegistroAdministrador
    )

    instancia._root = MagicMock()
    instancia._control_autenticacion = (
        control_autenticacion
    )

    instancia._ent_nombre = EntryFalso()
    instancia._ent_apellido = EntryFalso()
    instancia._ent_correo = EntryFalso()
    instancia._ent_edad = EntryFalso()
    instancia._ent_contrasenia = EntryFalso()
    instancia._ent_confirmacion = EntryFalso()

    instancia._ent_correo_cambio = EntryFalso()
    instancia._ent_nueva_clave = EntryFalso()
    instancia._ent_confirmar_nueva_clave = EntryFalso()

    instancia._tree_administradores = TreeviewFalso()

    return instancia


def cargar_datos_registro_validos(ventana):
    ventana._ent_nombre.valor = "  Ana  "
    ventana._ent_apellido.valor = "  Pérez  "
    ventana._ent_correo.valor = "ana@correo.com"
    ventana._ent_edad.valor = "30"
    ventana._ent_contrasenia.valor = "ClaveSegura1!"
    ventana._ent_confirmacion.valor = "ClaveSegura1!"


def cargar_datos_cambio_clave_validos(ventana):
    ventana._ent_correo_cambio.valor = "ana@correo.com"
    ventana._ent_nueva_clave.valor = "ClaveNueva1!"
    ventana._ent_confirmar_nueva_clave.valor = (
        "ClaveNueva1!"
    )


def test_constructor_configura_ventana_y_crea_formulario(
    control_autenticacion,
):
    root = MagicMock()
    tree = TreeviewFalso()

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.LabelFrame",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Label",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Entry",
        side_effect=EntryFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Frame",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Button",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Separator",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Scrollbar",
        side_effect=WidgetFalso,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "ttk.Treeview",
        return_value=tree,
    ):
        ventana = VentanaRegistroAdministrador(
            root,
            control_autenticacion,
        )

    root.title.assert_called_once_with(
        "Cardio Wellness - Crear administrador"
    )

    root.geometry.assert_called_once_with("850x780")

    root.resizable.assert_called_once_with(
        False,
        False,
    )

    assert isinstance(ventana._ent_nombre, EntryFalso)
    assert isinstance(ventana._ent_apellido, EntryFalso)
    assert isinstance(ventana._ent_correo, EntryFalso)
    assert isinstance(ventana._ent_edad, EntryFalso)
    assert isinstance(
        ventana._ent_contrasenia,
        EntryFalso,
    )
    assert isinstance(
        ventana._ent_confirmacion,
        EntryFalso,
    )
    assert isinstance(
        ventana._ent_correo_cambio,
        EntryFalso,
    )
    assert isinstance(
        ventana._ent_nueva_clave,
        EntryFalso,
    )
    assert isinstance(
        ventana._ent_confirmar_nueva_clave,
        EntryFalso,
    )

    control_autenticacion.listar_administradores.assert_called_once_with()

    assert ventana._ent_nombre.focus_recibido is True


def test_cargar_administradores_limpia_e_inserta_datos(
    ventana,
    control_autenticacion,
):
    ventana._tree_administradores.children = [
        "fila-anterior",
    ]

    control_autenticacion.listar_administradores.return_value = [
        {
            "id_usuario": 1,
            "nombre": "Ana",
            "apellido": "Pérez",
            "correo_electronico": "ana@correo.com",
            "edad": 30,
            "fecha_registro": "2026-01-15",
        },
        {
            "id_usuario": 2,
            "nombre": "Luis",
            "apellido": "Gómez",
            "correo_electronico": "luis@correo.com",
            "edad": 40,
        },
    ]

    ventana._cargar_administradores()

    assert ventana._tree_administradores.eliminaciones == [
        (
            ("fila-anterior",),
            {},
        ),
    ]

    assert len(
        ventana._tree_administradores.insertados
    ) == 2

    assert (
        ventana._tree_administradores
        .insertados[0][1]["values"]
    ) == (
        1,
        "Ana Pérez",
        "ana@correo.com",
        30,
        "2026-01-15",
    )

    assert (
        ventana._tree_administradores
        .insertados[1][1]["values"]
    ) == (
        2,
        "Luis Gómez",
        "luis@correo.com",
        40,
        "",
    )


def test_cargar_administradores_muestra_error(
    ventana,
    control_autenticacion,
):
    control_autenticacion.listar_administradores.side_effect = (
        RuntimeError("Base de datos no disponible")
    )

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._cargar_administradores()

    mock_error.assert_called_once_with(
        "Error al cargar administradores",
        (
            "No se pudieron mostrar las cuentas "
            "de administrador:\n"
            "Base de datos no disponible"
        ),
        parent=ventana._root,
    )


def test_registrar_administrador_correctamente(
    ventana,
    control_autenticacion,
):
    cargar_datos_registro_validos(ventana)

    administrador = SimpleNamespace(
        correo_electronico="ana@correo.com",
    )

    control_autenticacion.registrar_administrador.return_value = (
        administrador
    )

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showinfo"
    ) as mock_info, patch.object(
        ventana,
        "_limpiar_formulario",
    ) as mock_limpiar, patch.object(
        ventana,
        "_cargar_administradores",
    ) as mock_cargar:
        ventana._registrar_administrador()

    (
        control_autenticacion
        .registrar_administrador
        .assert_called_once_with(
            nombre="Ana",
            apellido="Pérez",
            correo_electronico="ana@correo.com",
            contrasenia_plana="ClaveSegura1!",
            edad=30,
        )
    )

    mock_info.assert_called_once_with(
        "Administrador creado",
        (
            "La cuenta administrativa fue creada "
            "correctamente.\n\n"
            "Correo: ana@correo.com"
        ),
        parent=ventana._root,
    )

    mock_limpiar.assert_called_once_with()
    mock_cargar.assert_called_once_with()


@pytest.mark.parametrize(
    "campo, valor, mensaje",
    [
        (
            "nombre",
            "",
            "Ingrese el nombre.",
        ),
        (
            "apellido",
            "",
            "Ingrese el apellido.",
        ),
        (
            "correo",
            "",
            "Ingrese el correo electrónico.",
        ),
        (
            "edad",
            "",
            "Ingrese la edad.",
        ),
        (
            "edad",
            "texto",
            "La edad debe ser un número entero.",
        ),
        (
            "edad",
            "0",
            "La edad debe ser mayor que cero.",
        ),
        (
            "edad",
            "-10",
            "La edad debe ser mayor que cero.",
        ),
        (
            "contrasenia",
            "",
            "Ingrese una contraseña.",
        ),
    ],
)
def test_registrar_administrador_valida_campos(
    ventana,
    control_autenticacion,
    campo,
    valor,
    mensaje,
):
    cargar_datos_registro_validos(ventana)

    campos = {
        "nombre": ventana._ent_nombre,
        "apellido": ventana._ent_apellido,
        "correo": ventana._ent_correo,
        "edad": ventana._ent_edad,
        "contrasenia": ventana._ent_contrasenia,
    }

    campos[campo].valor = valor

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._registrar_administrador()

    control_autenticacion.registrar_administrador.assert_not_called()

    mock_error.assert_called_once_with(
        "No se pudo crear la cuenta",
        mensaje,
        parent=ventana._root,
    )


def test_registrar_administrador_rechaza_contrasenias_distintas(
    ventana,
    control_autenticacion,
):
    cargar_datos_registro_validos(ventana)

    ventana._ent_confirmacion.valor = "OtraClave1!"

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._registrar_administrador()

    control_autenticacion.registrar_administrador.assert_not_called()

    mock_error.assert_called_once_with(
        "No se pudo crear la cuenta",
        "Las contraseñas no coinciden.",
        parent=ventana._root,
    )


def test_registrar_administrador_rechaza_contrasena_debil(
    ventana,
    control_autenticacion,
):
    cargar_datos_registro_validos(ventana)

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=False,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._registrar_administrador()

    control_autenticacion.registrar_administrador.assert_not_called()

    mock_error.assert_called_once()

    argumentos = mock_error.call_args.args

    assert argumentos[0] == "No se pudo crear la cuenta"
    assert "La contraseña debe tener al menos" in argumentos[1]


def test_registrar_administrador_maneja_error_inesperado(
    ventana,
    control_autenticacion,
):
    cargar_datos_registro_validos(ventana)

    control_autenticacion.registrar_administrador.side_effect = (
        RuntimeError("Correo duplicado")
    )

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._registrar_administrador()

    mock_error.assert_called_once_with(
        "Error inesperado",
        (
            "No se pudo crear la cuenta de "
            "administrador:\nCorreo duplicado"
        ),
        parent=ventana._root,
    )


def test_cambiar_clave_administrador_correctamente(
    ventana,
    control_autenticacion,
):
    cargar_datos_cambio_clave_validos(ventana)

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.askyesno",
        return_value=True,
    ) as mock_confirmar, patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showinfo"
    ) as mock_info:
        ventana._cambiar_clave_administrador()

    mock_confirmar.assert_called_once()

    (
        control_autenticacion
        .restablecer_contrasenia_administrador
        .assert_called_once_with(
            "ana@correo.com",
            "ClaveNueva1!",
        )
    )

    mock_info.assert_called_once_with(
        "Contraseña actualizada",
        (
            "La contraseña del administrador fue "
            "actualizada correctamente."
        ),
        parent=ventana._root,
    )

    assert ventana._ent_correo_cambio.valor == ""
    assert ventana._ent_nueva_clave.valor == ""
    assert (
        ventana._ent_confirmar_nueva_clave.valor
        == ""
    )


@pytest.mark.parametrize(
    "campo, valor, mensaje",
    [
        (
            "correo",
            "",
            "Ingrese el correo del administrador.",
        ),
        (
            "clave",
            "",
            "Ingrese la nueva contraseña.",
        ),
    ],
)
def test_cambiar_clave_valida_campos_obligatorios(
    ventana,
    control_autenticacion,
    campo,
    valor,
    mensaje,
):
    cargar_datos_cambio_clave_validos(ventana)

    campos = {
        "correo": ventana._ent_correo_cambio,
        "clave": ventana._ent_nueva_clave,
    }

    campos[campo].valor = valor

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._cambiar_clave_administrador()

    (
        control_autenticacion
        .restablecer_contrasenia_administrador
        .assert_not_called()
    )

    mock_error.assert_called_once_with(
        "No se pudo cambiar la contraseña",
        mensaje,
        parent=ventana._root,
    )


def test_cambiar_clave_rechaza_confirmacion_distinta(
    ventana,
    control_autenticacion,
):
    cargar_datos_cambio_clave_validos(ventana)

    ventana._ent_confirmar_nueva_clave.valor = (
        "ClaveDiferente1!"
    )

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._cambiar_clave_administrador()

    (
        control_autenticacion
        .restablecer_contrasenia_administrador
        .assert_not_called()
    )

    mock_error.assert_called_once_with(
        "No se pudo cambiar la contraseña",
        "Las contraseñas no coinciden.",
        parent=ventana._root,
    )


def test_cambiar_clave_rechaza_clave_debil(
    ventana,
    control_autenticacion,
):
    cargar_datos_cambio_clave_validos(ventana)

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=False,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._cambiar_clave_administrador()

    (
        control_autenticacion
        .restablecer_contrasenia_administrador
        .assert_not_called()
    )

    mock_error.assert_called_once()

    argumentos = mock_error.call_args.args

    assert argumentos[0] == "No se pudo cambiar la contraseña"
    assert "La contraseña debe tener al menos" in argumentos[1]


def test_cambiar_clave_se_cancela_si_usuario_no_confirma(
    ventana,
    control_autenticacion,
):
    cargar_datos_cambio_clave_validos(ventana)

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.askyesno",
        return_value=False,
    ):
        ventana._cambiar_clave_administrador()

    (
        control_autenticacion
        .restablecer_contrasenia_administrador
        .assert_not_called()
    )


def test_cambiar_clave_maneja_error_inesperado(
    ventana,
    control_autenticacion,
):
    cargar_datos_cambio_clave_validos(ventana)

    (
        control_autenticacion
        .restablecer_contrasenia_administrador
        .side_effect
    ) = RuntimeError("Administrador no encontrado")

    with patch(
        "src.interfaz.ventana_registro_administrador."
        "GestorSeguridad.validar_fortaleza_contrasena",
        return_value=True,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.askyesno",
        return_value=True,
    ), patch(
        "src.interfaz.ventana_registro_administrador."
        "messagebox.showerror"
    ) as mock_error:
        ventana._cambiar_clave_administrador()

    mock_error.assert_called_once_with(
        "Error inesperado",
        (
            "No se pudo restablecer la contraseña "
            "del administrador:\n"
            "Administrador no encontrado"
        ),
        parent=ventana._root,
    )


def test_limpiar_formulario_borra_campos_y_devuelve_foco(
    ventana,
):
    ventana._ent_nombre.valor = "Ana"
    ventana._ent_apellido.valor = "Pérez"
    ventana._ent_correo.valor = "ana@correo.com"
    ventana._ent_edad.valor = "30"
    ventana._ent_contrasenia.valor = "ClaveSegura1!"
    ventana._ent_confirmacion.valor = "ClaveSegura1!"

    ventana._limpiar_formulario()

    assert ventana._ent_nombre.valor == ""
    assert ventana._ent_apellido.valor == ""
    assert ventana._ent_correo.valor == ""
    assert ventana._ent_edad.valor == ""
    assert ventana._ent_contrasenia.valor == ""
    assert ventana._ent_confirmacion.valor == ""

    assert ventana._ent_nombre.focus_recibido is True