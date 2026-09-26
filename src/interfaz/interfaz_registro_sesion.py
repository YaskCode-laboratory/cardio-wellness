from datetime import date

import tkinter as tk
from tkinter import ttk

from src.controladores.control_sesiones import (
    ControlSesiones,
)
from src.interfaz.interfaz_base import InterfazBase


class InterfazRegistroSesion(InterfazBase):
    """
    Pestaña para registrar sesiones de entrenamiento.

    Cuando el cliente posee una rutina activa, solamente
    puede registrar sesiones para ejercicios pertenecientes
    a su asignación individual.
    """

    def __init__(
        self,
        master: tk.Misc,
        control_sesiones: ControlSesiones,
        id_cliente: int,
        id_rutina: int,
    ) -> None:
        super().__init__(
            master,
            controlador=control_sesiones,
            padding=10,
        )

        self.pack(
            fill="both",
            expand=True,
        )

        self._id_cliente = id_cliente
        self._id_rutina = id_rutina

        self._id_asignacion = None
        self._ejercicios_asignados = []
        self._ejercicio_asignado_actual = None

        self.mostrarFormularioSesion()
        self._cargar_rutina_activa()

    @property
    def id_cliente(self) -> int:
        """
        Devuelve el ID del cliente autenticado.
        """
        return self._id_cliente

    @property
    def id_rutina(self) -> int | None:
        """
        Devuelve el ID de la rutina activa del cliente.
        """
        return getattr(
            self,
            "_id_rutina",
            None,
        )

    def mostrarFormularioSesion(self) -> None:
        """
        Construye el formulario de registro.
        """
        form = ttk.LabelFrame(
            self,
            text="Registrar sesión de entrenamiento",
            padding=15,
        )

        form.pack(
            fill="x",
            pady=10,
        )

        self._lbl_rutina = ttk.Label(
            form,
            text="Rutina asignada: cargando...",
        )

        self._lbl_rutina.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 12),
            padx=5,
        )

        ttk.Label(
            form,
            text="Ejercicio de mi rutina:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._cb_ejercicio = ttk.Combobox(
            form,
            state="readonly",
            width=35,
        )

        self._cb_ejercicio.grid(
            row=1,
            column=1,
            pady=8,
            padx=5,
        )

        self._cb_ejercicio.bind(
            "<<ComboboxSelected>>",
            self._seleccionar_ejercicio,
        )

        ttk.Label(
            form,
            text="Meta total:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._lbl_meta_total = ttk.Label(
            form,
            text="-",
        )

        self._lbl_meta_total.grid(
            row=2,
            column=1,
            sticky="w",
            pady=8,
            padx=5,
        )

        ttk.Label(
            form,
            text="Ya realizadas:",
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._lbl_veces_realizadas = ttk.Label(
            form,
            text="-",
        )

        self._lbl_veces_realizadas.grid(
            row=3,
            column=1,
            sticky="w",
            pady=8,
            padx=5,
        )

        ttk.Label(
            form,
            text="Restantes:",
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._lbl_veces_restantes = ttk.Label(
            form,
            text="-",
        )

        self._lbl_veces_restantes.grid(
            row=4,
            column=1,
            sticky="w",
            pady=8,
            padx=5,
        )

        ttk.Label(
            form,
            text="Cantidad realizada ahora:",
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._ent_veces_realizadas = ttk.Entry(
            form,
            width=25,
        )

        self._ent_veces_realizadas.grid(
            row=5,
            column=1,
            pady=8,
            padx=5,
        )

        ttk.Label(
            form,
            text="Duración real (min):",
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._ent_duracion = ttk.Entry(
            form,
            width=25,
        )

        self._ent_duracion.grid(
            row=6,
            column=1,
            pady=8,
            padx=5,
        )

        ttk.Label(
            form,
            text="Intensidad real:",
        ).grid(
            row=7,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._cb_intensidad = ttk.Combobox(
            form,
            values=(
                "BAJA",
                "MEDIA",
                "ALTA",
            ),
            state="readonly",
            width=22,
        )

        self._cb_intensidad.grid(
            row=7,
            column=1,
            pady=8,
            padx=5,
        )

        self._lbl_calorias_estimadas = ttk.Label(
            form,
            text=(
                "Las calorías se calcularán "
                "automáticamente según tu peso, "
                "duración e intensidad."
            ),
            foreground="#555555",
            wraplength=350,
        )

        self._lbl_calorias_estimadas.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8,
            padx=5,
        )
        ttk.Label(
            form,
            text="Observaciones:",
        ).grid(
            row=9,
            column=0,
            sticky="w",
            pady=8,
            padx=5,
        )

        self._ent_observaciones = ttk.Entry(
            form,
            width=25,
        )

        self._ent_observaciones.grid(
            row=9,
            column=1,
            pady=8,
            padx=5,
        )

        self._lbl_mensaje = ttk.Label(
            form,
            text=(
                "La meta solo puede ser modificada "
                "por un administrador."
            ),
            foreground="#555555",
        )

        self._lbl_mensaje.grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8,
            padx=5,
        )

        frame_botones = ttk.Frame(form)

        frame_botones.grid(
            row=11,
            column=1,
            sticky="e",
            pady=15,
        )

        ttk.Button(
            frame_botones,
            text="Guardar sesión",
            command=self.registrarSesion,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            frame_botones,
            text="Actualizar rutina",
            command=self._cargar_rutina_activa,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            frame_botones,
            text="Limpiar",
            command=self.cancelarRegistro,
        ).pack(
            side="left",
            padx=5,
        )

    def _cargar_rutina_activa(self) -> None:
        """
        Busca la asignación activa del cliente y carga los
        ejercicios activos de su rutina individual.
        """
        try:
            asignacion = (
                self.controlador
                .asignacion_dao
                .buscar_activa(
                    self._id_cliente
                )
            )

            if asignacion is None:
                self._id_asignacion = None
                self._id_rutina = None
                self._ejercicios_asignados = []
                self._ejercicio_asignado_actual = None

                self._cb_ejercicio["values"] = []
                self._cb_ejercicio.set("")

                self._lbl_rutina.config(
                    text=(
                        "Rutina asignada: el cliente no "
                        "tiene una rutina activa."
                    )
                )

                self._limpiar_datos_ejercicio()
                return

            self._id_asignacion = (
                asignacion.id_asignacion
            )

            self._id_rutina = asignacion.id_rutina

            estado = getattr(
                asignacion.estado,
                "value",
                str(asignacion.estado),
            )

            self._lbl_rutina.config(
                text=(
                    f"Rutina asignada: "
                    f"{asignacion.id_rutina} | "
                    f"Asignación: "
                    f"{asignacion.id_asignacion} | "
                    f"Estado: {estado}"
                )
            )

            progreso = (
                self.controlador
                .asignacion_ejercicio_dao
                .obtener_progreso(
                    id_asignacion=(
                        asignacion.id_asignacion
                    ),
                    solo_activos=True,
                )
            )

            self._ejercicios_asignados = list(progreso)

            valores_combo = [
                (
                    f"{fila['id_asignacion_ejercicio']} - "
                    f"{fila['nombre_ejercicio']}"
                )
                for fila in self._ejercicios_asignados
            ]

            self._cb_ejercicio["values"] = valores_combo
            self._cb_ejercicio.set("")

            self._ejercicio_asignado_actual = None
            self._limpiar_datos_ejercicio()

            if not valores_combo:
                self._lbl_mensaje.config(
                    text=(
                        "La rutina activa no tiene "
                        "ejercicios disponibles."
                    ),
                    foreground="#b00020",
                )

            else:
                self._lbl_mensaje.config(
                    text=(
                        "Seleccione un ejercicio de su "
                        "rutina y registre la cantidad "
                        "realizada."
                    ),
                    foreground="#555555",
                )

        except Exception as error:
            self.mostrar_error(
                (
                    "No se pudo cargar la rutina activa: "
                    f"{error}"
                )
            )

    def _seleccionar_ejercicio(
        self,
        _evento=None,
    ) -> None:
        """
        Carga la meta, cantidad acumulada y cantidad
        restante del ejercicio seleccionado.
        """
        valor = self._cb_ejercicio.get().strip()

        if not valor:
            self._ejercicio_asignado_actual = None
            self._limpiar_datos_ejercicio()
            return

        try:
            id_asignacion_ejercicio = int(
                valor.split(
                    "-",
                    1,
                )[0].strip()
            )

        except (
            ValueError,
            IndexError,
        ):
            self._ejercicio_asignado_actual = None
            self._limpiar_datos_ejercicio()
            return

        fila_seleccionada = next(
            (
                fila
                for fila in self._ejercicios_asignados
                if int(
                    fila[
                        "id_asignacion_ejercicio"
                    ]
                )
                == id_asignacion_ejercicio
            ),
            None,
        )

        if fila_seleccionada is None:
            self._ejercicio_asignado_actual = None
            self._limpiar_datos_ejercicio()
            return

        meta = int(
            fila_seleccionada[
                "veces_planificadas"
            ]
        )

        realizadas = int(
            fila_seleccionada[
                "veces_realizadas"
            ]
        )

        restantes = max(
            meta - realizadas,
            0,
        )

        self._ejercicio_asignado_actual = (
            fila_seleccionada
        )

        self._lbl_meta_total.config(
            text=str(meta)
        )

        self._lbl_veces_realizadas.config(
            text=str(realizadas)
        )

        self._lbl_veces_restantes.config(
            text=str(restantes)
        )

        self._ent_veces_realizadas.delete(
            0,
            tk.END,
        )

        if restantes == 0:
            self._lbl_mensaje.config(
                text=(
                    "Este ejercicio ya alcanzó su meta. "
                    "Seleccione otro ejercicio."
                ),
                foreground="#1b5e20",
            )

        else:
            self._lbl_mensaje.config(
                text=(
                    "Puede registrar entre 1 y "
                    f"{restantes} repetición(es)."
                ),
                foreground="#555555",
            )

    def registrarSesion(self) -> None:
        """
        Registra una sesión vinculada al ejercicio asignado
        seleccionado por el cliente.
        """
        if self._id_asignacion is None:
            self.mostrar_error(
                "No tiene una rutina activa para registrar."
            )
            return

        if self._ejercicio_asignado_actual is None:
            self.mostrar_error(
                "Seleccione un ejercicio de su rutina."
            )
            return

        duracion_texto = (
            self._ent_duracion.get().strip()
        )

        intensidad = self._cb_intensidad.get().strip()

        realizadas_texto = (
            self._ent_veces_realizadas.get().strip()
        )

        observaciones = (
            self._ent_observaciones.get().strip()
        )

        if (
            not duracion_texto
            or not intensidad
            or not realizadas_texto
        ):
            self.mostrar_error(
                (
                    "Complete duración, intensidad "
                    "y cantidad realizada."
                )
            )
            return

        try:
            duracion = int(duracion_texto)

            veces_realizadas = int(
                realizadas_texto
            )

            if duracion <= 0:
                raise ValueError(
                    "La duración debe ser mayor que cero."
                )

            if veces_realizadas <= 0:
                raise ValueError(
                    "La cantidad realizada debe ser "
                    "mayor que cero."
                )

            meta = int(
                self._ejercicio_asignado_actual[
                    "veces_planificadas"
                ]
            )

            acumuladas = int(
                self._ejercicio_asignado_actual[
                    "veces_realizadas"
                ]
            )

            restantes = meta - acumuladas

            if veces_realizadas > restantes:
                raise ValueError(
                    (
                        "No puede registrar más de "
                        f"{restantes} vez/veces, porque "
                        "esa es la cantidad restante "
                        "para completar el ejercicio."
                    )
                )

            nombre_ejercicio = (
                self._ejercicio_asignado_actual[
                    "nombre_ejercicio"
                ]
            )

            id_asignacion_ejercicio = int(
                self._ejercicio_asignado_actual[
                    "id_asignacion_ejercicio"
                ]
            )

            sesion = self.controlador.registrar_sesion(
                cliente=self._id_cliente,
                rutina=self._id_rutina,
                fecha=date.today(),
                nombre_ejercicio=nombre_ejercicio,
                duracion_real=duracion,
                intensidad_real=intensidad,
                observaciones=observaciones,
                veces_planificadas=restantes,
                veces_realizadas=veces_realizadas,
                id_asignacion_ejercicio=(
                    id_asignacion_ejercicio
                ),
            )

            estado = (
                "completada"
                if sesion.completada
                else "pendiente"
            )

            self.mostrar_mensaje(
                "Sesión registrada correctamente.\n"
                f"Ejercicio: {nombre_ejercicio}\n"
                f"Estado de la sesión: {estado}\n"
                f"Calorías estimadas: "
                f"{sesion.calorias_quemadas:.2f} kcal\n"
                f"Registrado ahora: "
                f"{sesion.veces_realizadas}\n"
                f"Restaban antes del registro: "
                f"{restantes}"
            )

            self.cancelarRegistro()
            self._cargar_rutina_activa()

        except ValueError as error:
            self.mostrar_error(str(error))

        except Exception as error:
            self.mostrar_error(
                f"Error inesperado: {error}"
            )

    def _limpiar_datos_ejercicio(self) -> None:
        """
        Limpia las etiquetas relacionadas con el ejercicio
        seleccionado.
        """
        self._lbl_meta_total.config(
            text="-"
        )

        self._lbl_veces_realizadas.config(
            text="-"
        )

        self._lbl_veces_restantes.config(
            text="-"
        )

    def cancelarRegistro(self) -> None:
        """
        Limpia los campos editables del formulario.
        """
        for atributo in (
            "_ent_duracion",
            "_ent_veces_realizadas",
            "_ent_observaciones",
        ):
            widget = getattr(
                self,
                atributo,
                None,
            )

            if widget is not None:
                widget.delete(
                    0,
                    tk.END,
                )

        intensidad = getattr(
            self,
            "_cb_intensidad",
            None,
        )

        if intensidad is not None:
            intensidad.set("")