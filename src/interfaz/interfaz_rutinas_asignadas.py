"""
Interfaz para consultar y administrar rutinas asignadas
individualmente a clientes.
"""

from typing import Optional

import tkinter as tk
from tkinter import simpledialog, ttk

from src.controladores.control_ejercicios import (
    ControlEjercicios,
)
from src.controladores.control_rutinas import (
    ControlRutinas,
)
from src.controladores.control_sesiones import (
    ControlSesiones,
)
from src.interfaz.interfaz_base import InterfazBase


class InterfazRutinasAsignadas(InterfazBase):
    """
    Pestaña para administrar las rutinas individualizadas
    de clientes.

    Esta interfaz trabaja con asignaciones individuales y
    no modifica la plantilla global de una rutina.
    """

    def __init__(
        self,
        master: tk.Misc,
        control_rutinas: ControlRutinas,
        control_sesiones: Optional[
            ControlSesiones
        ] = None,
        control_autenticacion=None,
        control_ejercicios: Optional[
            ControlEjercicios
        ] = None,
    ) -> None:
        super().__init__(
            master,
            controlador=control_rutinas,
            padding=10,
        )

        self.pack(
            fill="both",
            expand=True,
        )

        self._control_rutinas = control_rutinas
        self._control_sesiones = control_sesiones
        self._control_autenticacion = (
            control_autenticacion
        )
        self._control_ejercicios = (
            control_ejercicios
        )

        self._id_cliente_actual: Optional[int] = None
        self._id_asignacion_actual: Optional[int] = None

        self._id_ejercicio_asignado_seleccionado: (
            Optional[int]
        ) = None

        self._ejercicios_disponibles = []

        self._construir_formulario_busqueda()
        self._construir_datos_asignacion()
        self._construir_botones()
        self._construir_tabla_ejercicios()

        self._cargar_ejercicios_disponibles()

        try:
            self.winfo_toplevel().bind(
                "<<EjerciciosActualizados>>",
                self._actualizar_ejercicios_disponibles,
                add="+",
            )
        except (
            AttributeError,
            KeyError,
            tk.TclError,
        ):
            pass


    def _construir_formulario_busqueda(self) -> None:
        """
        Construye los controles de búsqueda de una rutina
        activa por cliente.
        """
        frame = ttk.LabelFrame(
            self,
            text="Buscar rutina asignada",
            padding=10,
        )

        frame.pack(
            fill="x",
            pady=5,
        )

        ttk.Label(
            frame,
            text="ID del cliente:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._ent_id_cliente = ttk.Entry(
            frame,
            width=20,
        )

        self._ent_id_cliente.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=5,
        )

        ttk.Button(
            frame,
            text="Buscar rutina activa",
            command=self.buscar_rutina_cliente,
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
        )

        ttk.Button(
            frame,
            text="Limpiar",
            command=self.limpiar_vista,
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

    def _construir_datos_asignacion(self) -> None:
        """
        Construye el panel de información de la asignación.
        """
        frame = ttk.LabelFrame(
            self,
            text="Información de la asignación",
            padding=10,
        )

        frame.pack(
            fill="x",
            pady=5,
        )

        self._lbl_cliente = ttk.Label(
            frame,
            text="Cliente: -",
        )

        self._lbl_cliente.grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=3,
        )

        self._lbl_asignacion = ttk.Label(
            frame,
            text="Asignación: -",
        )

        self._lbl_asignacion.grid(
            row=0,
            column=1,
            sticky="w",
            padx=25,
            pady=3,
        )

        self._lbl_rutina = ttk.Label(
            frame,
            text="Rutina: -",
        )

        self._lbl_rutina.grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=3,
        )

        self._lbl_estado = ttk.Label(
            frame,
            text="Estado: -",
        )

        self._lbl_estado.grid(
            row=1,
            column=1,
            sticky="w",
            padx=25,
            pady=3,
        )

        ttk.Label(
            frame,
            text=(
                "Los cambios de esta pantalla afectan "
                "solo a la rutina individual del cliente."
            ),
            foreground="#555555",
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=5,
        )

    def _construir_tabla_ejercicios(self) -> None:
        """
        Construye la tabla de ejercicios activos y progreso.
        """
        frame = ttk.LabelFrame(
            self,
            text="Ejercicios activos del cliente",
            padding=10,
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=5,
        )

        columnas = (
            "ID",
            "Orden",
            "Ejercicio",
            "Meta",
            "Realizadas",
            "Estado",
        )

        self._tree_ejercicios = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=8,
        )

        self._tree_ejercicios.heading(
            "ID",
            text="ID asignado",
        )

        self._tree_ejercicios.heading(
            "Orden",
            text="Orden",
        )

        self._tree_ejercicios.heading(
            "Ejercicio",
            text="Ejercicio",
        )

        self._tree_ejercicios.heading(
            "Meta",
            text="Meta",
        )

        self._tree_ejercicios.heading(
            "Realizadas",
            text="Realizadas",
        )

        self._tree_ejercicios.heading(
            "Estado",
            text="Estado",
        )

        self._tree_ejercicios.column(
            "ID",
            width=100,
            anchor="center",
        )

        self._tree_ejercicios.column(
            "Orden",
            width=70,
            anchor="center",
        )

        self._tree_ejercicios.column(
            "Ejercicio",
            width=280,
            anchor="w",
        )

        self._tree_ejercicios.column(
            "Meta",
            width=100,
            anchor="center",
        )

        self._tree_ejercicios.column(
            "Realizadas",
            width=110,
            anchor="center",
        )

        self._tree_ejercicios.column(
            "Estado",
            width=150,
            anchor="center",
        )

        self._tree_ejercicios.pack(
            fill="both",
            expand=True,
        )

        self._tree_ejercicios.bind(
            "<<TreeviewSelect>>",
            self._seleccionar_ejercicio,
        )

    def _construir_botones(self) -> None:
        """
        Construye las acciones de administración.

        Se utilizan dos filas para que los botones de
        sesiones no queden ocultos por el ancho de ventana.
        """
        frame_principal = ttk.LabelFrame(
            self,
            text="Acciones de la rutina activa",
            padding=8,
        )

        frame_principal.pack(
            fill="x",
            pady=10,
        )

        frame_ejercicios = ttk.Frame(
            frame_principal,
        )

        frame_ejercicios.pack(
            fill="x",
            pady=(0, 6),
        )

        ttk.Label(
            frame_ejercicios,
            text="Ejercicios:",
            foreground="#555555",
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            frame_ejercicios,
            text="Actualizar vista",
            command=self.actualizar_vista,
        ).pack(
            side="left",
            padx=3,
        )

        ttk.Button(
            frame_ejercicios,
            text="Agregar ejercicio",
            command=self.agregar_ejercicio_cliente,
        ).pack(
            side="left",
            padx=3,
        )

        ttk.Button(
            frame_ejercicios,
            text="Cambiar meta",
            command=self.cambiar_meta_ejercicio,
        ).pack(
            side="left",
            padx=3,
        )

        ttk.Button(
            frame_ejercicios,
            text="Eliminar de rutina",
            command=self.desactivar_ejercicio_cliente,
        ).pack(
            side="left",
            padx=3,
        )

        frame_sesiones = ttk.Frame(
            frame_principal,
        )

        frame_sesiones.pack(
            fill="x",
        )

        ttk.Label(
            frame_sesiones,
            text="Sesiones y rutina:",
            foreground="#555555",
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            frame_sesiones,
            text="Registrar sesión",
            command=self.registrar_sesion_administrador,
        ).pack(
            side="left",
            padx=3,
        )


        ttk.Button(
            frame_sesiones,
            text="Cambiar rutina",
            command=self.cambiar_rutina_cliente,
        ).pack(
            side="left",
            padx=3,
        )

    def buscar_rutina_cliente(self) -> None:
        """
        Busca y muestra la asignación activa del cliente.
        """
        texto_id_cliente = (
            self._ent_id_cliente.get().strip()
        )

        if not texto_id_cliente:
            self.mostrar_error(
                "Ingrese el ID del cliente."
            )
            return

        try:
            id_cliente = int(texto_id_cliente)

            if id_cliente <= 0:
                raise ValueError(
                    "El ID del cliente debe ser mayor que cero."
                )

            asignacion = (
                self._control_rutinas
                .asignacion_dao
                .obtener_activa_por_cliente(
                    id_cliente
                )
            )

            if asignacion is None:
                raise ValueError(
                    "El cliente no tiene una rutina activa."
                )

            self._id_cliente_actual = id_cliente
            self._id_asignacion_actual = (
                asignacion.id_asignacion
            )

            rutina = self._control_rutinas.buscar_por_id(
                asignacion.id_rutina
            )

            nombre_rutina = (
                rutina.nombre
                if rutina is not None
                else f"Rutina #{asignacion.id_rutina}"
            )

            estado = getattr(
                asignacion.estado,
                "value",
                str(asignacion.estado),
            )

            self._lbl_cliente.config(
                text=f"Cliente: {id_cliente}"
            )

            self._lbl_asignacion.config(
                text=(
                    "Asignación: "
                    f"{asignacion.id_asignacion}"
                )
            )

            self._lbl_rutina.config(
                text=f"Rutina: {nombre_rutina}"
            )

            self._lbl_estado.config(
                text=f"Estado: {estado}"
            )

            self._cargar_progreso()

        except ValueError as error:
            self.mostrar_error(str(error))

        except Exception as error:
            self.mostrar_error(
                (
                    "No se pudo buscar la rutina del "
                    f"cliente: {error}"
                )
            )

    def actualizar_vista(self) -> None:
        """
        Recarga el progreso de la asignación actual.
        """
        if self._id_asignacion_actual is None:
            self.mostrar_error(
                "Busque primero la rutina activa de un cliente."
            )
            return

        self._cargar_progreso()

    def _cargar_progreso(self) -> None:
        """
        Carga los ejercicios activos y su progreso.
        """
        if self._id_asignacion_actual is None:
            return

        try:
            for item in (
                self._tree_ejercicios.get_children()
            ):
                self._tree_ejercicios.delete(item)

            progreso = (
                self._control_rutinas
                .obtener_progreso_asignacion(
                    self._id_asignacion_actual
                )
            )

            for fila in progreso:
                estado = (
                    "COMPLETADO"
                    if bool(fila["completado"])
                    else "PENDIENTE"
                )

                self._tree_ejercicios.insert(
                    "",
                    "end",
                    values=(
                        fila[
                            "id_asignacion_ejercicio"
                        ],
                        fila["orden_ejercicio"],
                        fila["nombre_ejercicio"],
                        fila["veces_planificadas"],
                        fila["veces_realizadas"],
                        estado,
                    ),
                )

            self._id_ejercicio_asignado_seleccionado = (
                None
            )

        except Exception as error:
            self.mostrar_error(
                (
                    "No se pudo cargar el progreso de la "
                    f"asignación: {error}"
                )
            )

    def _seleccionar_ejercicio(
        self,
        _evento=None,
    ) -> None:
        """
        Guarda el ID del ejercicio asignado seleccionado.
        """
        seleccion = self._tree_ejercicios.selection()

        if not seleccion:
            self._id_ejercicio_asignado_seleccionado = (
                None
            )
            return

        valores = self._tree_ejercicios.item(
            seleccion[0],
            "values",
        )

        try:
            self._id_ejercicio_asignado_seleccionado = int(
                valores[0]
            )

        except (
            IndexError,
            TypeError,
            ValueError,
        ):
            self._id_ejercicio_asignado_seleccionado = (
                None
            )

    def _actualizar_ejercicios_disponibles(
        self,
        _evento=None,
    ) -> None:
        """
        Recarga los ejercicios globales disponibles para
        agregarlos a la rutina individual del cliente.
        """
        if self._control_ejercicios is None:
            return

        self._cargar_ejercicios_disponibles()

    def _cargar_ejercicios_disponibles(self) -> None:
        """
        Carga ejercicios globales que pueden agregarse a una
        asignación individual.
        """
        if self._control_ejercicios is None:
            return

        try:
            self._ejercicios_disponibles = list(
                self._control_ejercicios.listar()
            )

        except Exception as error:
            self.mostrar_error(
                (
                    "No se pudieron cargar los ejercicios "
                    f"disponibles: {error}"
                )
            )

    def agregar_ejercicio_cliente(self) -> None:
        """
        Agrega un ejercicio al plan individual del cliente.
        """
        if self._id_asignacion_actual is None:
            self.mostrar_error(
                "Busque primero la rutina activa de un cliente."
            )
            return

        if self._control_ejercicios is None:
            self.mostrar_error(
                "No se configuró ControlEjercicios."
            )
            return

        opciones = "\n".join(
            (
                f"{ejercicio.id_ejercicio} - "
                f"{ejercicio.nombre}"
            )
            for ejercicio in self._ejercicios_disponibles
        )

        id_ejercicio = simpledialog.askinteger(
            "Agregar ejercicio",
            (
                "Ingrese el ID del ejercicio.\n\n"
                "Ejercicios disponibles:\n"
                f"{opciones}"
            ),
            parent=self,
            minvalue=1,
        )

        if id_ejercicio is None:
            return

        veces_planificadas = simpledialog.askinteger(
            "Meta del ejercicio",
            (
                "Ingrese cuántas veces debe realizar "
                "el cliente este ejercicio:"
            ),
            parent=self,
            minvalue=1,
        )

        if veces_planificadas is None:
            return

        try:
            administrador_id = (
                self._obtener_id_administrador()
            )

            self._control_rutinas \
                .agregar_ejercicio_a_asignacion(
                    id_asignacion=(
                        self._id_asignacion_actual
                    ),
                    id_ejercicio=id_ejercicio,
                    veces_planificadas=(
                        veces_planificadas
                    ),
                    usuario_accion=administrador_id,
                )

            self.mostrar_mensaje(
                "Ejercicio agregado al plan del cliente."
            )

            self._cargar_progreso()

        except Exception as error:
            self.mostrar_error(
                (
                    "No se pudo agregar el ejercicio: "
                    f"{error}"
                )
            )

    def cambiar_meta_ejercicio(self) -> None:
        """
        Modifica la meta individual de un ejercicio activo.
        """
        if self._id_asignacion_actual is None:
            self.mostrar_error(
                "Busque primero la rutina activa de un cliente."
            )
            return

        if (
            self._id_ejercicio_asignado_seleccionado
            is None
        ):
            self.mostrar_error(
                (
                    "Seleccione un ejercicio de la tabla "
                    "antes de cambiar su meta."
                )
            )
            return

        nueva_meta = simpledialog.askinteger(
            "Cambiar meta",
            "Ingrese la nueva meta del ejercicio:",
            parent=self,
            minvalue=1,
        )

        if nueva_meta is None:
            return

        try:
            administrador_id = (
                self._obtener_id_administrador()
            )

            actualizado = (
                self._control_rutinas
                .actualizar_meta_ejercicio_asignado(
                    id_asignacion_ejercicio=(
                        self
                        ._id_ejercicio_asignado_seleccionado
                    ),
                    veces_planificadas=nueva_meta,
                    usuario_accion=administrador_id,
                )
            )

            if not actualizado:
                raise ValueError(
                    "No se pudo actualizar la meta."
                )

            self.mostrar_mensaje(
                "Meta actualizada correctamente."
            )

            self._cargar_progreso()

        except Exception as error:
            self.mostrar_error(
                f"No se pudo cambiar la meta: {error}"
            )

    def desactivar_ejercicio_cliente(self) -> None:
        """
        Desactiva un ejercicio sin borrar su historial.
        """
        if self._id_asignacion_actual is None:
            self.mostrar_error(
                "Busque primero la rutina activa de un cliente."
            )
            return

        if (
            self._id_ejercicio_asignado_seleccionado
            is None
        ):
            self.mostrar_error(
                (
                    "Seleccione un ejercicio de la tabla "
                    "antes de desactivarlo."
                )
            )
            return

        if not self.confirmar_accion(
            (
                "¿Desea desactivar el ejercicio "
                "seleccionado? Su historial de sesiones "
                "se conservará."
            )
        ):
            return

        try:
            administrador_id = (
                self._obtener_id_administrador()
            )

            desactivado = (
                self._control_rutinas
                .desactivar_ejercicio_de_asignacion(
                    id_asignacion_ejercicio=(
                        self
                        ._id_ejercicio_asignado_seleccionado
                    ),
                    usuario_accion=administrador_id,
                )
            )

            if not desactivado:
                raise ValueError(
                    "El ejercicio ya estaba desactivado."
                )

            self.mostrar_mensaje(
                "Ejercicio desactivado correctamente."
            )

            self._cargar_progreso()

        except Exception as error:
            self.mostrar_error(
                (
                    "No se pudo desactivar el ejercicio: "
                    f"{error}"
                )
            )

    def _obtener_valores_ejercicio_seleccionado(
        self,
    ) -> Optional[tuple]:
        """
        Obtiene los valores de la fila seleccionada.
        """
        seleccion = self._tree_ejercicios.selection()

        if not seleccion:
            return None

        valores = self._tree_ejercicios.item(
            seleccion[0],
            "values",
        )

        if not valores:
            return None

        return tuple(valores)

    def _obtener_rutina_actual(self) -> int:
        """
        Obtiene el ID de rutina de la asignación cargada.
        """
        if self._id_asignacion_actual is None:
            raise ValueError(
                "No existe una asignación activa cargada."
            )

        asignacion = (
            self._control_rutinas
            .asignacion_dao
            .buscar_por_id(
                self._id_asignacion_actual
            )
        )

        if asignacion is None:
            raise ValueError(
                "No se encontró la asignación actual."
            )

        return int(asignacion.id_rutina)

    def registrar_sesion_administrador(self) -> None:
        """
        Registra una sesión para el ejercicio seleccionado.

        Las calorías se calculan automáticamente en
        ControlSesiones usando peso, duración, tipo e
        intensidad del ejercicio.
        """
        if self._control_sesiones is None:
            self.mostrar_error(
                "No se configuró ControlSesiones."
            )
            return

        if self._id_cliente_actual is None:
            self.mostrar_error(
                "Busque primero la rutina activa de un cliente."
            )
            return

        valores = (
            self._obtener_valores_ejercicio_seleccionado()
        )

        if valores is None:
            self.mostrar_error(
                (
                    "Seleccione un ejercicio antes de "
                    "registrar una sesión."
                )
            )
            return

        try:
            id_asignacion_ejercicio = int(valores[0])
            nombre_ejercicio = str(valores[2])
            meta = int(valores[3])
            acumuladas = int(valores[4])

            restantes = meta - acumuladas

            if restantes <= 0:
                raise ValueError(
                    (
                        "El ejercicio ya alcanzó su meta. "
                        "No puede registrar más actividad."
                    )
                )

            cantidad = simpledialog.askinteger(
                "Registrar sesión",
                (
                    f"Ejercicio: {nombre_ejercicio}\n"
                    f"Meta: {meta}\n"
                    f"Realizadas: {acumuladas}\n"
                    f"Restantes: {restantes}\n\n"
                    "Cantidad realizada ahora:"
                ),
                parent=self,
                minvalue=1,
                maxvalue=restantes,
            )

            if cantidad is None:
                return

            duracion = simpledialog.askinteger(
                "Duración",
                "Ingrese la duración en minutos:",
                parent=self,
                minvalue=1,
            )

            if duracion is None:
                return

            intensidad = simpledialog.askstring(
                "Intensidad",
                "Ingrese BAJA, MEDIA o ALTA:",
                parent=self,
            )

            if intensidad is None:
                return

            intensidad = intensidad.strip().upper()

            if intensidad not in {
                "BAJA",
                "MEDIA",
                "ALTA",
            }:
                raise ValueError(
                    "La intensidad debe ser BAJA, "
                    "MEDIA o ALTA."
                )

            observaciones = simpledialog.askstring(
                "Observaciones",
                "Observaciones opcionales:",
                parent=self,
            )

            id_rutina = self._obtener_rutina_actual()

            sesion = (
                self._control_sesiones
                .registrar_sesion(
                    cliente=self._id_cliente_actual,
                    rutina=id_rutina,
                    duracion_real=duracion,
                    intensidad_real=intensidad,
                    observaciones=observaciones or "",
                    nombre_ejercicio=nombre_ejercicio,
                    veces_planificadas=restantes,
                    veces_realizadas=cantidad,
                    id_asignacion_ejercicio=(
                        id_asignacion_ejercicio
                    ),
                )
            )

            self.mostrar_mensaje(
                (
                    "Sesión registrada correctamente.\n"
                    f"ID de sesión: {sesion.id_sesion}\n"
                    f"Ejercicio: {nombre_ejercicio}\n"
                    f"Cantidad agregada: {cantidad}\n"
                    f"Calorías estimadas: "
                    f"{sesion.calorias_quemadas} kcal"
                )
            )

            asignacion_activa = (
                self._control_rutinas
                .asignacion_dao
                .obtener_activa_por_cliente(
                    self._id_cliente_actual
                )
            )

            if asignacion_activa is None:
                self.mostrar_mensaje(
                    (
                        "La rutina alcanzó todas sus metas "
                        "y fue finalizada automáticamente."
                    )
                )

                self.limpiar_vista()
                return

            self._cargar_progreso()

        except ValueError as error:
            self.mostrar_error(str(error))

        except Exception as error:
            self.mostrar_error(
                f"No se pudo registrar la sesión: {error}"
            )

    def cambiar_rutina_cliente(self) -> None:
        """
        Cancela la rutina activa y asigna una nueva rutina.
        """
        if self._id_cliente_actual is None:
            self.mostrar_error(
                "Busque primero la rutina activa de un cliente."
            )
            return

        if self._id_asignacion_actual is None:
            self.mostrar_error(
                "No existe una asignación activa cargada."
            )
            return

        try:
            rutinas = list(
                self._control_rutinas.listar()
            )

            if not rutinas:
                raise ValueError(
                    "No hay rutinas disponibles."
                )

            opciones = "\n".join(
                (
                    f"{rutina.id_rutina} - "
                    f"{rutina.nombre}"
                )
                for rutina in rutinas
            )

            id_nueva_rutina = simpledialog.askinteger(
                "Cambiar rutina",
                (
                    "Ingrese el ID de la nueva rutina.\n\n"
                    "Rutinas disponibles:\n"
                    f"{opciones}"
                ),
                parent=self,
                minvalue=1,
            )

            if id_nueva_rutina is None:
                return

            if not self.confirmar_accion(
                (
                    "¿Desea cambiar la rutina activa "
                    f"del cliente {self._id_cliente_actual}?\n\n"
                    "La rutina actual pasará a CANCELADA "
                    "y se conservará su historial de "
                    "ejercicios y sesiones."
                )
            ):
                return

            administrador_id = (
                self._obtener_id_administrador()
            )

            resultado = (
                self._control_rutinas
                .cambiar_rutina_asignada(
                    id_cliente=self._id_cliente_actual,
                    id_nueva_rutina=id_nueva_rutina,
                    usuario_accion=administrador_id,
                    observaciones=(
                        "Rutina reemplazada por "
                        "un administrador."
                    ),
                )
            )

            self._id_asignacion_actual = (
                resultado["id_asignacion"]
            )

            self.mostrar_mensaje(
                (
                    "Rutina cambiada correctamente.\n"
                    f"Nueva asignación: "
                    f"{resultado['id_asignacion']}"
                )
            )

            self.buscar_rutina_cliente()

        except Exception as error:
            self.mostrar_error(
                f"No se pudo cambiar la rutina: {error}"
            )

    def limpiar_vista(self) -> None:
        """
        Limpia la búsqueda, etiquetas y tabla actual.
        """
        self._id_cliente_actual = None
        self._id_asignacion_actual = None

        self._id_ejercicio_asignado_seleccionado = None

        self._ent_id_cliente.delete(
            0,
            tk.END,
        )

        self._lbl_cliente.config(
            text="Cliente: -"
        )

        self._lbl_asignacion.config(
            text="Asignación: -"
        )

        self._lbl_rutina.config(
            text="Rutina: -"
        )

        self._lbl_estado.config(
            text="Estado: -"
        )

        for item in self._tree_ejercicios.get_children():
            self._tree_ejercicios.delete(item)

    def _obtener_id_administrador(self) -> int:
        """
        Obtiene el ID del administrador autenticado.
        """
        control_autenticacion = getattr(
            self,
            "_control_autenticacion",
            None,
        )

        if control_autenticacion is not None:
            usuario_actual = getattr(
                control_autenticacion,
                "usuario_actual",
                None,
            )

            if usuario_actual is not None:
                id_usuario = getattr(
                    usuario_actual,
                    "id_usuario",
                    None,
                )

                if id_usuario is not None:
                    return int(id_usuario)

        ventana = self

        while (
            hasattr(ventana, "master")
            and ventana.master is not None
        ):
            ventana = ventana.master

        administrador_actual = getattr(
            ventana,
            "_administrador_actual",
            None,
        )

        if administrador_actual is not None:
            id_usuario = getattr(
                administrador_actual,
                "id_usuario",
                None,
            )

            if id_usuario is not None:
                return int(id_usuario)

        raise ValueError(
            (
                "No se pudo obtener el ID del "
                "administrador autenticado."
            )
        )