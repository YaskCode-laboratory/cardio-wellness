from decimal import Decimal
from typing import Any, Dict, List, Optional

import tkinter as tk
from tkinter import ttk

from src.controladores.control_clientes import (
    ControlClientes,
)
from src.controladores.control_progreso import (
    ControlProgreso,
)


class InterfazProgresoClientesAdmin(ttk.Frame):
    """
    Pestaña administrativa para consultar el progreso
    completo de los clientes.
    """

    def __init__(
        self,
        master: tk.Misc,
        control_clientes: ControlClientes,
        control_progreso: ControlProgreso,
    ) -> None:
        super().__init__(
            master,
            padding=10,
        )

        if control_clientes is None:
            raise ValueError(
                "Se requiere un ControlClientes inicializado."
            )

        if control_progreso is None:
            raise ValueError(
                "Se requiere un ControlProgreso inicializado."
            )

        self._control_clientes = control_clientes
        self._control_progreso = control_progreso

        self._clientes_por_id: Dict[int, Any] = {}
        self._ids_por_texto: Dict[str, int] = {}

        self.pack(
            fill="both",
            expand=True,
        )

        self._crear_selector_cliente()
        self._crear_resumen()
        self._crear_tabla_sesiones()
        self._crear_tabla_progreso_mensual()

        self.cargar_clientes()

    @property
    def control_clientes(self) -> ControlClientes:
        """
        Devuelve el controlador de clientes.
        """
        return self._control_clientes

    @property
    def control_progreso(self) -> ControlProgreso:
        """
        Devuelve el controlador de progreso.
        """
        return self._control_progreso

    def _crear_selector_cliente(self) -> None:
        """
        Construye el selector de cliente y botón de carga.
        """
        frame = ttk.LabelFrame(
            self,
            text="Consultar progreso de cliente",
            padding=10,
        )

        frame.pack(
            fill="x",
            pady=(0, 10),
        )

        ttk.Label(
            frame,
            text="Cliente:",
            font=("Helvetica", 10, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self._cb_clientes = ttk.Combobox(
            frame,
            state="readonly",
            width=55,
        )

        self._cb_clientes.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=5,
        )

        ttk.Button(
            frame,
            text="Cargar progreso",
            command=self.cargar_progreso_cliente,
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
        )

        ttk.Button(
            frame,
            text="Actualizar clientes",
            command=self.cargar_clientes,
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

        self._lbl_estado = ttk.Label(
            frame,
            text="Seleccione un cliente para consultar su progreso.",
            foreground="#555555",
        )

        self._lbl_estado.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="w",
            padx=5,
            pady=(5, 0),
        )

    def _crear_resumen(self) -> None:
        """
        Construye la sección de métricas acumuladas.
        """
        frame = ttk.LabelFrame(
            self,
            text="Resumen de actividad",
            padding=10,
        )

        frame.pack(
            fill="x",
            pady=(0, 10),
        )

        self._labels_resumen = {}

        datos = (
            ("sesiones", "Sesiones registradas:"),
            ("completadas", "Sesiones completadas:"),
            ("minutos", "Minutos entrenados:"),
            ("calorias", "Calorías quemadas:"),
            ("planificadas", "Veces planificadas:"),
            ("realizadas", "Veces realizadas:"),
            ("cumplimiento", "Cumplimiento total:"),
        )

        for indice, (clave, texto) in enumerate(datos):
            fila = indice // 2
            columna = (indice % 2) * 2

            ttk.Label(
                frame,
                text=texto,
                font=("Helvetica", 9, "bold"),
            ).grid(
                row=fila,
                column=columna,
                sticky="w",
                padx=(5, 2),
                pady=4,
            )

            etiqueta_valor = ttk.Label(
                frame,
                text="-",
            )

            etiqueta_valor.grid(
                row=fila,
                column=columna + 1,
                sticky="w",
                padx=(2, 18),
                pady=4,
            )

            self._labels_resumen[clave] = etiqueta_valor

    def _crear_tabla_sesiones(self) -> None:
        """
        Construye la tabla de historial de sesiones.
        """
        frame = ttk.LabelFrame(
            self,
            text="Historial de sesiones y ejercicios",
            padding=10,
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=(0, 10),
        )

        columnas = (
            "Fecha",
            "Ejercicio",
            "Duración",
            "Intensidad",
            "Calorías",
            "Repeticiones",
            "Cumplimiento",
            "Estado",
            "Observaciones",
        )

        self._tree_sesiones = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=10,
        )

        anchos = {
            "Fecha": 100,
            "Ejercicio": 160,
            "Duración": 90,
            "Intensidad": 100,
            "Calorías": 100,
            "Repeticiones": 115,
            "Cumplimiento": 105,
            "Estado": 105,
            "Observaciones": 260,
        }

        for columna in columnas:
            self._tree_sesiones.heading(
                columna,
                text=columna,
            )

            self._tree_sesiones.column(
                columna,
                width=anchos[columna],
                anchor=(
                    "w"
                    if columna in {
                        "Ejercicio",
                        "Observaciones",
                    }
                    else "center"
                ),
            )

        self._tree_sesiones.pack(
            fill="both",
            expand=True,
        )

    def _crear_tabla_progreso_mensual(self) -> None:
        """
        Construye la tabla de progreso mensual.
        """
        frame = ttk.LabelFrame(
            self,
            text="Historial de progreso mensual",
            padding=10,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        columnas = (
            "Mes",
            "Peso",
            "Sesiones completadas",
            "Sesiones planificadas",
            "Cumplimiento",
        )

        self._tree_progreso_mensual = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=6,
        )

        anchos = {
            "Mes": 180,
            "Peso": 120,
            "Sesiones completadas": 170,
            "Sesiones planificadas": 180,
            "Cumplimiento": 140,
        }

        for columna in columnas:
            self._tree_progreso_mensual.heading(
                columna,
                text=columna,
            )

            self._tree_progreso_mensual.column(
                columna,
                width=anchos[columna],
                anchor="center",
            )

        self._tree_progreso_mensual.pack(
            fill="both",
            expand=True,
        )

    def cargar_clientes(self) -> None:
        """
        Carga clientes disponibles en el selector.
        """
        try:
            clientes = self._control_clientes.listar() or []

            self._clientes_por_id = {}
            self._ids_por_texto = {}

            valores = []

            for cliente in clientes:
                id_cliente = getattr(
                    cliente,
                    "id_usuario",
                    None,
                )

                if not isinstance(id_cliente, int):
                    continue

                nombre = self._obtener_nombre_cliente(
                    cliente
                )

                texto = (
                    f"{id_cliente} - {nombre}"
                )

                valores.append(texto)

                self._clientes_por_id[
                    id_cliente
                ] = cliente

                self._ids_por_texto[
                    texto
                ] = id_cliente

            self._cb_clientes["values"] = valores

            if valores:
                self._cb_clientes.set(valores[0])

                self._lbl_estado.config(
                    text=(
                        f"Se cargaron {len(valores)} "
                        "clientes. Seleccione uno y "
                        "presione 'Cargar progreso'."
                    ),
                    foreground="#555555",
                )

            else:
                self._cb_clientes.set("")

                self._lbl_estado.config(
                    text="No hay clientes registrados.",
                    foreground="#b71c1c",
                )

        except Exception as error:
            self._cb_clientes["values"] = []
            self._cb_clientes.set("")

            self._lbl_estado.config(
                text=(
                    "No se pudieron cargar los clientes: "
                    f"{error}"
                ),
                foreground="#b71c1c",
            )

    def cargar_progreso_cliente(self) -> None:
        """
        Consulta y muestra el progreso del cliente elegido.
        """
        texto_seleccionado = self._cb_clientes.get()

        id_cliente = self._ids_por_texto.get(
            texto_seleccionado
        )

        if id_cliente is None:
            self._lbl_estado.config(
                text="Seleccione un cliente válido.",
                foreground="#b71c1c",
            )
            return

        cliente = self._clientes_por_id.get(id_cliente)

        if cliente is None:
            self._lbl_estado.config(
                text="No se encontró el cliente seleccionado.",
                foreground="#b71c1c",
            )
            return

        try:
            resumen = (
                self._control_progreso
                .calcular_resumen_cliente(cliente)
            )

            progreso_mensual = (
                self._control_progreso
                .consultar_progreso(cliente)
            )

            self._actualizar_resumen(resumen)

            sesiones = resumen.get(
                "sesiones",
                [],
            )

            self._cargar_sesiones(sesiones)

            self._cargar_progreso_mensual(
                progreso_mensual
            )

            nombre = self._obtener_nombre_cliente(
                cliente
            )

            self._lbl_estado.config(
                text=(
                    "Progreso cargado correctamente "
                    f"para {nombre}."
                ),
                foreground="#1b5e20",
            )

        except Exception as error:
            self._limpiar_datos()

            self._lbl_estado.config(
                text=(
                    "No se pudo cargar el progreso: "
                    f"{error}"
                ),
                foreground="#b71c1c",
            )

    def _actualizar_resumen(
        self,
        resumen: Dict[str, Any],
    ) -> None:
        """
        Actualiza las métricas acumuladas.
        """
        total_sesiones = resumen.get(
            "total_sesiones",
            0,
        )

        sesiones_completadas = resumen.get(
            "sesiones_completadas",
            0,
        )

        total_minutos = resumen.get(
            "total_minutos",
            0,
        )

        total_calorias = resumen.get(
            "total_calorias",
            Decimal("0"),
        )

        planificadas = resumen.get(
            "total_veces_planificadas",
            resumen.get(
                "veces_planificadas",
                0,
            ),
        )

        realizadas = resumen.get(
            "total_veces_realizadas",
            resumen.get(
                "veces_realizadas",
                0,
            ),
        )

        cumplimiento = resumen.get(
            "porcentaje_cumplimiento",
            0.0,
        )

        self._labels_resumen["sesiones"].config(
            text=str(total_sesiones)
        )

        self._labels_resumen["completadas"].config(
            text=str(sesiones_completadas)
        )

        self._labels_resumen["minutos"].config(
            text=f"{total_minutos} min"
        )

        self._labels_resumen["calorias"].config(
            text=(
                f"{self._formatear_decimal(total_calorias)} "
                "kcal"
            )
        )

        self._labels_resumen["planificadas"].config(
            text=str(planificadas)
        )

        self._labels_resumen["realizadas"].config(
            text=str(realizadas)
        )

        self._labels_resumen["cumplimiento"].config(
            text=f"{self._formatear_porcentaje(cumplimiento)}%"
        )

    def _cargar_sesiones(
        self,
        sesiones: List[Any],
    ) -> None:
        """
        Inserta sesiones en la tabla de historial.
        """
        self._limpiar_tree(self._tree_sesiones)

        if not sesiones:
            self._tree_sesiones.insert(
                "",
                "end",
                values=(
                    "Sin sesiones",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ),
            )
            return

        for sesion in sesiones:
            fecha = getattr(
                sesion,
                "fecha",
                "",
            )

            nombre_ejercicio = getattr(
                sesion,
                "nombre_ejercicio",
                "",
            ) or "Sin ejercicio"

            duracion = getattr(
                sesion,
                "duracion_real",
                0,
            )

            intensidad = getattr(
                sesion,
                "intensidad_real",
                "",
            )

            intensidad_texto = getattr(
                intensidad,
                "value",
                str(intensidad),
            )

            calorias = getattr(
                sesion,
                "calorias_quemadas",
                0,
            )

            planificadas = getattr(
                sesion,
                "veces_planificadas",
                0,
            )

            realizadas = getattr(
                sesion,
                "veces_realizadas",
                0,
            )

            porcentaje = getattr(
                sesion,
                "porcentaje_cumplimiento",
                0.0,
            )

            if callable(porcentaje):
                porcentaje = porcentaje()

            completada = getattr(
                sesion,
                "completada",
                False,
            )

            estado = (
                "COMPLETADA"
                if completada
                else "PENDIENTE"
            )

            observaciones = getattr(
                sesion,
                "observaciones",
                "",
            )

            self._tree_sesiones.insert(
                "",
                "end",
                values=(
                    str(fecha),
                    str(nombre_ejercicio),
                    f"{duracion} min",
                    str(intensidad_texto),
                    (
                        f"{self._formatear_decimal(calorias)} "
                        "kcal"
                    ),
                    f"{realizadas}/{planificadas}",
                    (
                        f"{self._formatear_porcentaje(porcentaje)}%"
                    ),
                    estado,
                    str(observaciones),
                ),
            )

    def _cargar_progreso_mensual(
        self,
        progresos: List[Any],
    ) -> None:
        """
        Inserta el historial mensual en la tabla.
        """
        self._limpiar_tree(
            self._tree_progreso_mensual
        )

        if not progresos:
            self._tree_progreso_mensual.insert(
                "",
                "end",
                values=(
                    "Sin progreso mensual",
                    "",
                    "",
                    "",
                    "",
                ),
            )
            return

        for progreso in progresos:
            mes = getattr(
                progreso,
                "mes",
                "",
            )

            if hasattr(mes, "strftime"):
                mes_texto = mes.strftime("%B %Y")
            else:
                mes_texto = str(mes)

            peso = getattr(
                progreso,
                "peso",
                0,
            )

            completadas = getattr(
                progreso,
                "sesiones_completadas",
                0,
            )

            planificadas = getattr(
                progreso,
                "sesiones_planificadas",
                0,
            )

            porcentaje = getattr(
                progreso,
                "porcentaje_cumplimiento",
                0.0,
            )

            if callable(porcentaje):
                porcentaje = porcentaje()

            self._tree_progreso_mensual.insert(
                "",
                "end",
                values=(
                    mes_texto,
                    (
                        f"{self._formatear_decimal(peso)} "
                        "kg"
                    ),
                    str(completadas),
                    str(planificadas),
                    (
                        f"{self._formatear_porcentaje(porcentaje)}%"
                    ),
                ),
            )

    def _limpiar_datos(self) -> None:
        """
        Limpia resumen y tablas después de un error.
        """
        for etiqueta in self._labels_resumen.values():
            etiqueta.config(text="-")

        self._limpiar_tree(self._tree_sesiones)

        self._limpiar_tree(
            self._tree_progreso_mensual
        )

    @staticmethod
    def _limpiar_tree(tree: ttk.Treeview) -> None:
        """
        Elimina todos los elementos de una tabla.
        """
        for item in tree.get_children():
            tree.delete(item)

    @staticmethod
    def _obtener_nombre_cliente(
        cliente: Any,
    ) -> str:
        """
        Obtiene un nombre legible de cliente.
        """
        metodo = getattr(
            cliente,
            "obtener_nombre_completo",
            None,
        )

        if callable(metodo):
            return str(metodo())

        nombre = getattr(
            cliente,
            "nombre",
            "",
        )

        apellido = getattr(
            cliente,
            "apellido",
            "",
        )

        nombre_completo = (
            f"{nombre} {apellido}"
        ).strip()

        return nombre_completo or "Cliente sin nombre"

    @staticmethod
    def _formatear_decimal(
        valor: Any,
    ) -> str:
        """
        Formatea un número a dos decimales.
        """
        try:
            return f"{float(valor):.2f}"
        except (
            TypeError,
            ValueError,
        ):
            return "0.00"

    @staticmethod
    def _formatear_porcentaje(
        valor: Any,
    ) -> str:
        """
        Formatea un porcentaje a dos decimales.
        """
        try:
            return f"{float(valor):.2f}"
        except (
            TypeError,
            ValueError,
        ):
            return "0.00"