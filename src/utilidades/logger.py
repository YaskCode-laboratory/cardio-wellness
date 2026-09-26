"""
Módulo de logging para registrar actividades del sistema
en logs/LOG_CARDIO.txt.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any


RUTA_LOGS = (
    Path(__file__).resolve().parent.parent.parent / "logs"
)

RUTA_LOGS.mkdir(
    parents=True,
    exist_ok=True,
)

ARCHIVO_LOG = RUTA_LOGS / "LOG_CARDIO.txt"


logger = logging.getLogger("cardio_wellness")
logger.setLevel(logging.INFO)
logger.propagate = False


def _configurar_logger() -> None:
    """
    Configura un único handler para LOG_CARDIO.txt.
    """
    ruta_archivo = str(ARCHIVO_LOG.resolve())

    for handler_existente in logger.handlers:
        if isinstance(
            handler_existente,
            logging.FileHandler,
        ):
            if handler_existente.baseFilename == ruta_archivo:
                return

    handler = logging.FileHandler(
        ARCHIVO_LOG,
        encoding="utf-8",
        mode="a",
    )

    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s, %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


_configurar_logger()


def registrar_actividad(
    usuario: Any,
    accion: Any,
    detalle: Any = "",
) -> None:
    """
    Registra una actividad en LOG_CARDIO.txt.

    Formato:
    YYYY-MM-DD HH:MM:SS, USUARIO, ACCION, DETALLE
    """
    usuario_str = (
        "SISTEMA"
        if usuario is None
        else str(usuario).strip()
    )

    if not usuario_str:
        usuario_str = "SISTEMA"

    accion_str = str(accion).strip()

    if not accion_str:
        accion_str = "ACCION_NO_ESPECIFICADA"

    detalle_str = (
        ""
        if detalle is None
        else str(detalle).strip()
    )

    mensaje = f"{usuario_str}, {accion_str}"

    if detalle_str:
        mensaje += f", {detalle_str}"

    logger.info(mensaje)


def log_consulta_progreso(
    usuario: Any,
) -> None:
    """
    Registra una consulta de progreso.

    Se conserva por compatibilidad con código anterior.
    """
    registrar_actividad(
        usuario,
        "CONSULTA_PROGRESO",
        "Cliente consultó su progreso",
    )


def log_generar_progreso(
    usuario: Any,
) -> None:
    """
    Registra la generación de un reporte de progreso.

    Se conserva por compatibilidad con código anterior.
    """
    registrar_actividad(
        usuario,
        "GENERAR_PROGRESO",
        "Se generó reporte de progreso",
    )


def log_calculo_diferencia_peso(
    usuario: Any,
    diferencia: float,
) -> None:
    """
    Registra el cálculo de la diferencia de peso.
    """
    registrar_actividad(
        usuario,
        "CALCULO_DIFERENCIA_PESO",
        f"DIF: {diferencia:.1f}",
    )


def log_reporte_pdf_generado(
    usuario: Any,
    nombre_archivo: str,
) -> None:
    """
    Registra la generación de un reporte PDF.
    """
    registrar_actividad(
        usuario,
        "REPORTE_PDF_GENERADO",
        nombre_archivo,
    )


def log_registro_cliente(
    email: str,
) -> None:
    """
    Registra el alta de un cliente.
    """
    registrar_actividad(
        email,
        "REGISTRO_CLIENTE",
        "Nuevo cliente registrado",
    )


def log_registro_administrador(
    email: str,
) -> None:
    """
    Registra el alta de un administrador.
    """
    registrar_actividad(
        email,
        "REGISTRO_ADMINISTRADOR",
        "Nuevo administrador registrado",
    )


def log_login_exitoso(
    email: str,
) -> None:
    """
    Registra un inicio de sesión exitoso.
    """
    registrar_actividad(
        email,
        "LOGIN_EXITOSO",
        "Inicio de sesión exitoso",
    )


def log_login_fallido(
    email: str,
) -> None:
    """
    Registra un intento de inicio de sesión fallido.
    """
    registrar_actividad(
        email,
        "LOGIN_FALLIDO",
        "Intento de inicio de sesión fallido",
    )


def log_creacion_rutina(
    usuario: Any,
    id_rutina: int,
) -> None:
    """
    Registra la creación de una rutina.
    """
    registrar_actividad(
        usuario,
        "CREACION_RUTINA",
        f"ID: {id_rutina}",
    )


def log_creacion_ejercicio(
    usuario: Any,
    id_ejercicio: int,
) -> None:
    """
    Registra la creación de un ejercicio.
    """
    registrar_actividad(
        usuario,
        "CREACION_EJERCICIO",
        f"ID: {id_ejercicio}",
    )


def log_sugerencia_rutina(
    usuario: Any,
    tipo: str,
) -> None:
    """
    Registra una sugerencia de rutina.
    """
    registrar_actividad(
        usuario,
        "SUGERENCIA_RUTINA",
        tipo,
    )


def log_consulta_impacto(
    usuario: Any,
) -> None:
    """
    Registra una consulta de impacto calórico.
    """
    registrar_actividad(
        usuario,
        "CONSULTA_IMPACTO",
        "Se consultó impacto de rutina",
    )


if __name__ == "__main__":
    print("Configurando logger...")

    log_consulta_progreso("CLIENTE_PRUEBA")

    log_generar_progreso("CLIENTE_PRUEBA")

    log_calculo_diferencia_peso(
        "CLIENTE_PRUEBA",
        -2.5,
    )

    print(
        "✅ Logger configurado correctamente. "
        "Revisa logs/LOG_CARDIO.txt"
    )