import tkinter as tk
from tkinter import messagebox, ttk

from src.controladores.control_autenticacion import (
    ControlAutenticacion,
)
from src.servicios.gestor_seguridad import GestorSeguridad


class VentanaRegistroAdministrador:
    """
    Ventana independiente para que el propietario de la
    aplicación registre cuentas de administrador.

    No pertenece a las pestañas normales de la aplicación.
    """

    def __init__(
        self,
        root: tk.Tk,
        control_autenticacion: ControlAutenticacion,
    ) -> None:
        self._root = root
        self._control_autenticacion = control_autenticacion

        self._configurar_ventana()
        self._crear_formulario()

    def _configurar_ventana(self) -> None:
        """
        Configura la ventana independiente.
        """
        self._root.title(
            "Cardio Wellness - Crear administrador"
        )

        self._root.geometry("850x780")

        self._root.resizable(
            False,
            False,
        )

    def _crear_formulario(self) -> None:
        """
        Construye el formulario de registro.
        """
        contenedor = ttk.LabelFrame(
            self._root,
            text="Crear cuenta de administrador",
            padding=20,
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        ttk.Label(
            contenedor,
            text=(
                "Uso exclusivo del propietario "
                "de la aplicación."
            ),
            foreground="#8b0000",
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=(0, 15),
        )

        ttk.Label(
            contenedor,
            text="Nombre:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_nombre = ttk.Entry(
            contenedor,
            width=32,
        )

        self._ent_nombre.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            contenedor,
            text="Apellido:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_apellido = ttk.Entry(
            contenedor,
            width=32,
        )

        self._ent_apellido.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            contenedor,
            text="Correo electrónico:",
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_correo = ttk.Entry(
            contenedor,
            width=32,
        )

        self._ent_correo.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            contenedor,
            text="Edad:",
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_edad = ttk.Entry(
            contenedor,
            width=32,
        )

        self._ent_edad.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            contenedor,
            text="Contraseña:",
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_contrasenia = ttk.Entry(
            contenedor,
            width=32,
            show="*",
        )

        self._ent_contrasenia.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            contenedor,
            text="Confirmar contraseña:",
        ).grid(
            row=6,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_confirmacion = ttk.Entry(
            contenedor,
            width=32,
            show="*",
        )

        self._ent_confirmacion.grid(
            row=6,
            column=1,
            padx=5,
            pady=5,
        )

        texto_reglas = (
            "La contraseña debe tener al menos 8 "
            "caracteres, una mayúscula, un número "
            "y un carácter especial."
        )

        ttk.Label(
            contenedor,
            text=texto_reglas,
            foreground="#555555",
            wraplength=400,
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=(10, 5),
        )

        botones = ttk.Frame(contenedor)

        botones.grid(
            row=8,
            column=0,
            columnspan=2,
            pady=15,
        )

        ttk.Button(
            botones,
            text="Crear administrador",
            command=self._registrar_administrador,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            botones,
            text="Limpiar",
            command=self._limpiar_formulario,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            botones,
            text="Cerrar",
            command=self._root.destroy,
        ).pack(
            side="left",
            padx=5,
        )

        separador = ttk.Separator(
            self._root,
            orient="horizontal",
        )

        separador.pack(
            fill="x",
            padx=20,
            pady=(0, 10),
        )

        frame_clave = ttk.LabelFrame(
            self._root,
            text="Cambiar clave de administrador",
            padding=15,
        )

        frame_clave.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        ttk.Label(
            frame_clave,
            text="Correo del administrador:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_correo_cambio = ttk.Entry(
            frame_clave,
            width=32,
        )

        self._ent_correo_cambio.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            frame_clave,
            text="Nueva contraseña:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_nueva_clave = ttk.Entry(
            frame_clave,
            width=32,
            show="*",
        )

        self._ent_nueva_clave.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            frame_clave,
            text="Confirmar nueva contraseña:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_confirmar_nueva_clave = ttk.Entry(
            frame_clave,
            width=32,
            show="*",
        )

        self._ent_confirmar_nueva_clave.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Button(
            frame_clave,
            text="Cambiar clave",
            command=self._cambiar_clave_administrador,
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10,
        )

        frame_lista = ttk.LabelFrame(
            self._root,
            text="Administradores registrados",
            padding=10,
        )

        frame_lista.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20),
        )

        columnas = (
            "ID",
            "Nombre",
            "Correo",
            "Edad",
            "Fecha de registro",
        )

        self._tree_administradores = ttk.Treeview(
            frame_lista,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=8,
        )

        configuracion = {
            "ID": (70, "center"),
            "Nombre": (200, "w"),
            "Correo": (260, "w"),
            "Edad": (70, "center"),
            "Fecha de registro": (170, "center"),
        }

        for columna in columnas:
            ancho, ancla = configuracion[columna]

            self._tree_administradores.heading(
                columna,
                text=columna,
            )

            self._tree_administradores.column(
                columna,
                width=ancho,
                minwidth=70,
                anchor=ancla,
            )

        barra_vertical = ttk.Scrollbar(
            frame_lista,
            orient="vertical",
            command=self._tree_administradores.yview,
        )

        self._tree_administradores.configure(
            yscrollcommand=barra_vertical.set,
        )

        self._tree_administradores.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        ttk.Button(
            frame_lista,
            text="Actualizar lista",
            command=self._cargar_administradores,
        ).grid(
            row=1,
            column=0,
            pady=(10, 0),
        )

        frame_lista.rowconfigure(
            0,
            weight=1,
        )

        frame_lista.columnconfigure(
            0,
            weight=1,
        )

        self._cargar_administradores()

        self._ent_nombre.focus_set()

    def _cargar_administradores(self) -> None:
        """
        Carga los administradores registrados en la tabla.

        No muestra hashes ni contraseñas.
        """
        try:
            for item in (
                self._tree_administradores.get_children()
            ):
                self._tree_administradores.delete(item)

            administradores = (
                self._control_autenticacion
                .listar_administradores()
            )

            for administrador in administradores:
                nombre_completo = (
                    f"{administrador['nombre']} "
                    f"{administrador['apellido']}"
                )

                fecha = administrador.get(
                    "fecha_registro",
                    "",
                )

                if fecha:
                    fecha = str(fecha)

                self._tree_administradores.insert(
                    "",
                    "end",
                    values=(
                        administrador["id_usuario"],
                        nombre_completo,
                        administrador[
                            "correo_electronico"
                        ],
                        administrador["edad"],
                        fecha,
                    ),
                )

        except Exception as error:
            messagebox.showerror(
                "Error al cargar administradores",
                (
                    "No se pudieron mostrar las cuentas "
                    f"de administrador:\n{error}"
                ),
                parent=self._root,
            )

    def _registrar_administrador(self) -> None:
        """
        Valida los campos y registra un administrador.
        """
        try:
            nombre = self._ent_nombre.get().strip()
            apellido = self._ent_apellido.get().strip()
            correo = self._ent_correo.get().strip()
            edad_texto = self._ent_edad.get().strip()
            contrasenia = self._ent_contrasenia.get()
            confirmacion = self._ent_confirmacion.get()

            if not nombre:
                raise ValueError(
                    "Ingrese el nombre."
                )

            if not apellido:
                raise ValueError(
                    "Ingrese el apellido."
                )

            if not correo:
                raise ValueError(
                    "Ingrese el correo electrónico."
                )

            if not edad_texto:
                raise ValueError(
                    "Ingrese la edad."
                )

            try:
                edad = int(edad_texto)

            except ValueError as error:
                raise ValueError(
                    "La edad debe ser un número entero."
                ) from error

            if edad <= 0:
                raise ValueError(
                    "La edad debe ser mayor que cero."
                )

            if not contrasenia:
                raise ValueError(
                    "Ingrese una contraseña."
                )

            if contrasenia != confirmacion:
                raise ValueError(
                    "Las contraseñas no coinciden."
                )

            if not GestorSeguridad.validar_fortaleza_contrasena(
                contrasenia
            ):
                raise ValueError(
                    (
                        "La contraseña debe tener al menos "
                        "8 caracteres, una mayúscula, un "
                        "número y un carácter especial."
                    )
                )

            administrador = (
                self._control_autenticacion
                .registrar_administrador(
                    nombre=nombre,
                    apellido=apellido,
                    correo_electronico=correo,
                    contrasenia_plana=contrasenia,
                    edad=edad,
                )
            )

            messagebox.showinfo(
                "Administrador creado",
                (
                    "La cuenta administrativa fue creada "
                    "correctamente.\n\n"
                    f"Correo: "
                    f"{administrador.correo_electronico}"
                ),
                parent=self._root,
            )

            self._limpiar_formulario()
            self._cargar_administradores()

        except ValueError as error:
            messagebox.showerror(
                "No se pudo crear la cuenta",
                str(error),
                parent=self._root,
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                (
                    "No se pudo crear la cuenta de "
                    f"administrador:\n{error}"
                ),
                parent=self._root,
            )

    def _cambiar_clave_administrador(self) -> None:
        """
        Restablece la clave de un administrador mediante
        el correo electrónico.
        """
        try:
            correo = self._ent_correo_cambio.get().strip()

            nueva_contrasenia = (
                self._ent_nueva_clave.get()
            )

            confirmacion = (
                self._ent_confirmar_nueva_clave.get()
            )

            if not correo:
                raise ValueError(
                    (
                        "Ingrese el correo del "
                        "administrador."
                    )
                )

            if not nueva_contrasenia:
                raise ValueError(
                    "Ingrese la nueva contraseña."
                )

            if nueva_contrasenia != confirmacion:
                raise ValueError(
                    "Las contraseñas no coinciden."
                )

            if not GestorSeguridad.validar_fortaleza_contrasena(
                nueva_contrasenia
            ):
                raise ValueError(
                    (
                        "La contraseña debe tener al menos "
                        "8 caracteres, una mayúscula, un "
                        "número y un carácter especial."
                    )
                )

            confirmar = messagebox.askyesno(
                "Confirmar cambio de clave",
                (
                    "¿Desea cambiar la contraseña del "
                    "administrador con correo:\n\n"
                    f"{correo}?"
                ),
                parent=self._root,
            )

            if not confirmar:
                return

            self._control_autenticacion.restablecer_contrasenia_administrador(
                correo,
                nueva_contrasenia,
            )

            messagebox.showinfo(
                "Contraseña actualizada",
                (
                    "La contraseña del administrador fue "
                    "actualizada correctamente."
                ),
                parent=self._root,
            )

            self._ent_correo_cambio.delete(
                0,
                tk.END,
            )

            self._ent_nueva_clave.delete(
                0,
                tk.END,
            )

            self._ent_confirmar_nueva_clave.delete(
                0,
                tk.END,
            )

        except ValueError as error:
            messagebox.showerror(
                "No se pudo cambiar la contraseña",
                str(error),
                parent=self._root,
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                (
                    "No se pudo restablecer la contraseña "
                    f"del administrador:\n{error}"
                ),
                parent=self._root,
            )

    def _limpiar_formulario(self) -> None:
        """
        Limpia todos los campos.
        """
        for campo in (
            self._ent_nombre,
            self._ent_apellido,
            self._ent_correo,
            self._ent_edad,
            self._ent_contrasenia,
            self._ent_confirmacion,
        ):
            campo.delete(
                0,
                tk.END,
            )

        self._ent_nombre.focus_set()